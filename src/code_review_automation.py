import os
import re
import openai
from dotenv import load_dotenv
from github import Github
import subprocess

def get_modified_python_files():
    """Get a list of modified Python files using git"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'], 
            capture_output=True, 
            text=True
        )
        files = result.stdout.strip().split('\n')
        # Normalize paths and ensure they exist
        normalized_files = []
        for f in files:
            if f.endswith('.py'):
                # Normalize the path to handle different separators
                normalized_path = os.path.normpath(f)
                if os.path.exists(normalized_path):
                    normalized_files.append(normalized_path)
                else:
                    print(f"Warning: File {normalized_path} does not exist, skipping")
        return normalized_files
    except Exception as e:
        print(f"Error getting modified files: {e}")
        return []
    

def get_locally_modified_files():
    """Get locally modified files for demonstration purposes"""
    try:
        # Get the list of modified files
        files_result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'], 
            capture_output=True, 
            text=True
        )
        modified_files = files_result.stdout.strip().split('\n')
        
        files_with_diff = []
        for file_path in modified_files:
            # Normalize the path
            normalized_path = os.path.normpath(file_path)
            
            # Skip non-existent or non-code files
            if not os.path.exists(normalized_path) or not is_code_file(normalized_path):
                print(f"Warning: Skipping {normalized_path} - file does not exist or is not a code file")
                continue
                
            # Get the diff for each file
            diff_result = subprocess.run(
                ['git', 'diff', 'HEAD', '--', normalized_path],
                capture_output=True,
                text=True
            )
            files_with_diff.append((normalized_path, diff_result.stdout))
            
        # If no modified files found, use example_code.py for demonstration
        if not files_with_diff:
            example_file = os.path.normpath('src/example_code.py')
            if os.path.exists(example_file):
                with open(example_file, 'r') as f:
                    content = f.read()
                files_with_diff.append((example_file, content))
                
        return files_with_diff
        
    except Exception as e:
        print(f"Error getting local changes: {e}")
        return []

def is_code_file(file_path):
    """Check if a file is a code file based on its extension"""
    code_extensions = ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php']
    return any(file_path.endswith(ext) for ext in code_extensions)

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
    """Automate code review process"""
    print('Automating code review process...')
    
    # Get files to review
    files = get_modified_python_files()
    
    if not files:
        print("No files to review.")
        return
    
    for file_path in files:
        print(f"\nReviewing {file_path}...")
        
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
                    posted = post_review_comments(repo_name, pr_number, file_path, review_comments)
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