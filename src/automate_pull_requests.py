import os
import re
import openai
import requests
from dotenv import load_dotenv
from github import Github
import subprocess

# Define the path for the file list
FILES_TO_PROCESS_PATH = "files_to_process.txt"

def get_changed_evaluate_files():
    """Get the list of changed/new Python files in the evaluate directory compared to the base branch."""
    try:
        # Determine the base branch: Use GITHUB_BASE_REF if available (from PR event), otherwise default to origin/main
        base_ref = os.getenv('GITHUB_BASE_REF')
        if base_ref:
            base_branch = f'origin/{base_ref}'
            print(f"Using base branch from GITHUB_BASE_REF: {base_branch}")
            # Fetch the specific base branch to ensure it exists locally
            try:
                subprocess.run(['git', 'fetch', 'origin', base_ref], check=True, capture_output=True)
                print(f"Fetched base branch {base_ref} from origin.")
            except subprocess.CalledProcessError as fetch_error:
                print(f"Warning: Failed to fetch specific base branch '{base_ref}': {fetch_error}. Falling back to fetching all.")
                # Fallback to fetching everything if specific fetch fails
                subprocess.run(['git', 'fetch', 'origin'], check=True, capture_output=True)
        else:
            base_branch = 'origin/main'
            print(f"GITHUB_BASE_REF not set. Defaulting base branch to: {base_branch}")
            # Ensure origin/main is up-to-date
            try:
                subprocess.run(['git', 'fetch', 'origin', 'main'], check=True, capture_output=True)
                print("Fetched main branch from origin.")
            except subprocess.CalledProcessError as fetch_error:
                print(f"Warning: Failed to fetch main branch: {fetch_error}. The diff might be inaccurate.")

        # Define the git diff command
        diff_command = ['git', 'diff', '--name-only', '--diff-filter=ARM', base_branch, '--', 'evaluate/**/*.py']
        print(f"Running git diff command: {' '.join(diff_command)}")

        # Get the diff limited to Python files in the evaluate directory and its subdirectories
        result = subprocess.run(
            diff_command, 
            capture_output=True, 
            text=True,
            check=True # Check for errors
        )
        
        print(f"Git diff output:\n{result.stdout.strip()}") # Log the raw output for debugging

        files = result.stdout.strip().split('\n')
        # Filter out empty strings if any
        changed_files = [f for f in files if f and os.path.exists(f)] 
        
        if not changed_files:
            print(f"No changed Python files detected in the evaluate directory compared to {base_branch}.")
        else:
            print(f"Detected changed Python files in evaluate/: {', '.join(changed_files)}")
            
        return changed_files
    except subprocess.CalledProcessError as e:
        print(f"Warning: git diff command failed: {e}. Output: {e.stderr}")
        print(f"Assuming no changed files due to diff error.")
        return []
    except Exception as e:
        print(f"Error getting changed files: {e}")
        return []

def save_files_to_process(file_list):
    """Saves the list of files to the specified path."""
    try:
        # Ensure the directory exists (though not needed if saving in root)
        # os.makedirs(os.path.dirname(FILES_TO_PROCESS_PATH), exist_ok=True) 
        with open(FILES_TO_PROCESS_PATH, 'w') as f:
            for file_path in file_list:
                f.write(f"{file_path}\n")
        print(f"Saved list of files to process in {FILES_TO_PROCESS_PATH}")
    except Exception as e:
        print(f"Error saving file list to {FILES_TO_PROCESS_PATH}: {e}")

def get_diff_for_files(file_list):
    """Get the combined git diff for a specific list of files against the base branch."""
    if not file_list:
        return None
    try:
        # Determine the base branch similarly to get_changed_evaluate_files
        base_ref = os.getenv('GITHUB_BASE_REF')
        base_branch = f'origin/{base_ref}' if base_ref else 'origin/main'
        print(f"Generating specific file diff against base: {base_branch}")

        # Create the command list, including the file paths at the end
        command = ['git', 'diff', base_branch, '--'] + file_list
        print(f"Running git diff command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
         print(f"Warning: git diff failed for specific files: {e}. Output: {e.stderr}. Cannot generate specific diff.")
         return None
    except Exception as e:
        print(f"Error getting git diff for specific files: {e}")
        return None

def generate_pr_description(diff):
    """Generate a PR description based on the code changes using OpenAI"""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            return "Automated Pull Request"
        
        prompt = f"""
        Based on the following git diff, generate a detailed and professional pull request description.
        Include:
        1. A clear title that summarizes the changes
        2. A detailed description of the changes made
        3. Any important technical details or implementation decisions
        4. Testing instructions if applicable

        Git diff:
        {diff[:4000]}  # Limit the diff size to avoid token limits
        """
        
        # Using OpenAI to generate PR description
        response = openai.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes detailed pull request descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=1024
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating PR description: {e}")
        return "Automated Pull Request"

def create_pull_request():
    """Identify changed files, save the list, generate PR description and create Pull Request"""
    print('Identifying changed files and preparing for Pull Request...')
    
    # 1. Identify changed files
    changed_files = get_changed_evaluate_files()
    
    # 2. Save the list for other scripts
    save_files_to_process(changed_files)

    # --- PR Generation Logic (should ideally run *after* other scripts) ---
    # Check if there are any files to actually create a PR for
    if not changed_files:
        print("No changed files found in evaluate/ to create a Pull Request for.")
        return

    print("\nGenerating Pull Request content...")
    try:
        load_dotenv()
        # Get GitHub token from environment variables
        github_token = os.getenv("GITHUB_TOKEN")
        
        # Get the git diff *specifically for the changed files* for the description
        diff = get_diff_for_files(changed_files)
        if not diff:
            print("Could not get diff for changed files. Using generic PR description.")
            pr_description = "Automated Pull Request for changes in evaluate/"
            pr_title = "Automated PR for evaluate/ changes"
        else:
            # Generate PR description based on the specific diff
            pr_description = generate_pr_description(diff)
            # Extract PR title from the description (first line)
            pr_title = pr_description.split('\n')[0]

        # --- Actual PR Creation (Conditional based on token) ---
        if not github_token:
            print("GITHUB_TOKEN environment variable not set.")
            print("\nHere's the PR description that would be generated:")
            print(f"Title: {pr_title}")
            print("\nDescription:")
            print(pr_description)
            print("\nTo create an actual PR, set the GITHUB_TOKEN environment variable.")
            return
            
        # Get repository details
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            print("GITHUB_REPOSITORY environment variable not set.")
            return
        
        # Create GitHub instance
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        # Get the current branch name
        branch_name = os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME")
        
        # Create PR
        # Use the actual base branch name (e.g., 'main' or the value of GITHUB_BASE_REF)
        pr_base_branch_name = os.getenv('GITHUB_BASE_REF', 'main') 
        pr = repo.create_pull(
            title=pr_title,
            body=pr_description,
            head=branch_name,
            base=pr_base_branch_name # Use the correct base branch name
        )
        
        print(f"Pull request created successfully: {pr.html_url}")
        
    except Exception as e:
        print(f"Error creating pull request: {e}")

if __name__ == '__main__':
    # This script now primarily identifies files and saves the list.
    # The PR creation part might be called separately or conditionally later in the workflow.
    # For now, let's keep the execution flow as is, but be aware of the needed changes in main.yml
    create_pull_request()