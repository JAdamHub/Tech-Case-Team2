import os
import re
import openai
from dotenv import load_dotenv
from github import Github
import subprocess
from datetime import datetime

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
        1. Make sure that the respond is a python code.
        2. Code quality and best practices
        3. Potential bugs or edge cases
        4. Performance issues
        5. Security concerns
        6. Style and consistency
        
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


def save_review_to_file(file_path, review_comments, content):
    """Save review comments to a Python file in the changes/reviews directory"""
    try:
        # Create the reviews directory if it doesn't exist
        reviews_dir = os.path.normpath('changes/reviews')
        os.makedirs(reviews_dir, exist_ok=True)
        
        # Create a filename based on the original file path
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        review_file = os.path.join(reviews_dir, f"{timestamp}_{file_name}")
        
        # Format the review as a Python file with proper comments
        formatted_review = f'''"""
Review for: {file_path}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

# Review Comments:
"""
{review_comments}
"""

# Original code with review comments:
"""
{content}
"""
'''
        
        # Write the review to the file
        with open(review_file, 'w') as f:
            f.write(formatted_review)
            
        print(f"Saved review to {review_file}")
        return True
    except Exception as e:
        print(f"Error saving review for {file_path}: {e}")
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
        
        try:
            # Read the file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Use AI to generate review comments
            review_comments = review_code_with_ai(file_path, content)
            
            # Save the review to a file
            save_review_to_file(file_path, review_comments, content)
            
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