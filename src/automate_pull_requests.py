import os
import re
import openai
import requests
from dotenv import load_dotenv
from github import Github

def get_git_diff():
    """Get the git diff of the current branch compared to main"""
    try:
        import subprocess
        # Get the diff
        result = subprocess.run(['git', 'diff', 'origin/main'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error getting git diff: {e}")
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
            max_completion_tokens=1024,
            temperature=0.7,  # Slightly higher temperature for creative PR descriptions
            top_p=0.95,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating PR description: {e}")
        return "Automated Pull Request"

def create_pull_request():
    """Analyze code and create Pull Request"""
    print('Analyzing code and creating Pull Request...')
    
    try:
        load_dotenv()
        # Get GitHub token from environment variables
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("GITHUB_TOKEN environment variable not set.")
            return
        
        # Get repository details
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            print("GITHUB_REPOSITORY environment variable not set.")
            return
        
        # Get the git diff
        diff = get_git_diff()
        if not diff:
            print("No changes detected or error getting diff.")
            return
        
        # Generate PR description
        pr_description = generate_pr_description(diff)
        
        # Extract PR title from the description (first line)
        pr_title = pr_description.split('\n')[0]
        
        # Create GitHub instance
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        # Get the current branch name
        branch_name = os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME")
        
        # Create PR
        pr = repo.create_pull(
            title=pr_title,
            body=pr_description,
            head=branch_name,
            base="main"
        )
        
        print(f"Pull request created successfully: {pr.html_url}")
        
    except Exception as e:
        print(f"Error creating pull request: {e}")

if __name__ == '__main__':
    create_pull_request()