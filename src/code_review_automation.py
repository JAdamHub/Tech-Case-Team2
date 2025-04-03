import os
import re
import openai
from dotenv import load_dotenv
from github import Github
import subprocess

# Define the path for the file list
FILES_TO_PROCESS_PATH = "files_to_process.txt"

def get_files_to_process():
    """Reads the list of files to process from the specified file."""
    if not os.path.exists(FILES_TO_PROCESS_PATH):
        print(f"Warning: File list '{FILES_TO_PROCESS_PATH}' not found. No files to process.")
        return []
    try:
        with open(FILES_TO_PROCESS_PATH, 'r') as f:
            files = [line.strip() for line in f if line.strip()]
        if not files:
            print(f"File list '{FILES_TO_PROCESS_PATH}' is empty. No files to process.")
        return files
    except Exception as e:
        print(f"Error reading file list from {FILES_TO_PROCESS_PATH}: {e}")
        return []

def review_code_with_ai(file_path, content):
    """Generate code review comments using AI"""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            return "Could not generate review comments due to missing API key."
        
        # Normalize the file path
        normalized_path = os.path.normpath(file_path)
        
        # Determine file type
        file_ext = os.path.splitext(normalized_path)[1]
        
        # Create a prompt based on file type
        prompt = f"""
        Please review the following code and provide constructive feedback.
        Focus on:
        1. Code quality and best practices
        2. Potential bugs or edge cases
        3. Performance issues
        4. Security concerns
        5. Style and consistency
        
        Make sure that in the review add comments on each line of code. 
        For example:
        
            input:
            x+1=x
        
            output:
            # x is not defined
            x+1=x
        
        For each issue, provide:
        - The line number or code section
        - What the issue is
        - How to fix it
        
        Here's the code from {normalized_path}:
        ```{file_ext}
        {content[:4000]}  # Limit content size
        ```
        """
        
        # Using OpenAI to generate review comments
        response = openai.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that reviews code and provides constructive feedback."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error reviewing code: {e}")
        return "Could not generate review comments."

def post_review_comments(repo_name, pr_number, file_path, review_comments):
    """Post review comments to GitHub PR"""
    try:
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("GITHUB_TOKEN environment variable not set.")
            return False
        
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))
        
        # Extract line-specific comments from the AI review
        # This is a simplified approach - in a real implementation, you would want
        # to parse the AI output more carefully to get precise line numbers
        line_pattern = re.compile(r'line (\d+)', re.IGNORECASE)
        lines_mentioned = line_pattern.findall(review_comments)
        
        if lines_mentioned:
            # Post individual line comments
            for line in lines_mentioned:
                line_num = int(line)
                # Get the relevant section of the review for this line
                line_context = review_comments.split(f"line {line}")[1].split("line")[0] if len(lines_mentioned) > 1 else review_comments
                pr.create_review_comment(body=f"AI review for line {line}: {line_context}", commit_id=pr.get_commits().reversed[0].sha, path=file_path, position=line_num)
        else:
            # Post a general comment if no specific lines are mentioned
            pr.create_issue_comment(f"AI Code Review for {file_path}:\n\n{review_comments}")
        
        return True
    except Exception as e:
        print(f"Error posting review comments: {e}")
        return False

def automate_code_review():
    """Automate code review process for files specified in files_to_process.txt"""
    print('Automating code review process...')
    
    # Get files to review from the list file
    files_to_review = get_files_to_process()
    
    if not files_to_review:
        print("No files specified for review.")
        return
    
    for file_path in files_to_review:
        print(f"\nReviewing {file_path}...")
        
        # Check if the file exists before trying to open it
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} specified in list does not exist. Skipping.")
            continue
            
        try:
            # Read the file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Use AI to generate review comments
            review_comments = review_code_with_ai(file_path, content)
            
            # In GitHub Actions context, post comments to PR
            if os.getenv("GITHUB_ACTIONS") == "true":
                repo_name = os.getenv("GITHUB_REPOSITORY")
                pr_number = os.getenv("PR_NUMBER")
                if repo_name and pr_number:
                    # Make sure file_path is relative for GitHub API
                    relative_file_path = os.path.relpath(file_path, os.getcwd())
                    posted = post_review_comments(repo_name, pr_number, relative_file_path, review_comments)
                    if posted:
                        print(f"Posted review comments for {file_path}.")
                    else:
                        print(f"Failed to post review comments for {file_path}.")
            
            # Print review locally
            print("\nAI Code Review:")
            print(review_comments)
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

if __name__ == '__main__':
    automate_code_review()