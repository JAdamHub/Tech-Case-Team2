import os
import sys
import subprocess
import re
import openai
from dotenv import load_dotenv
import tempfile
import difflib
from datetime import datetime
import pylint
import json

LLM_CHANGES_DIR = "_llm_changes"

# Define the path for the file list
FILES_TO_PROCESS_PATH = "files_to_process.txt"

# Dictionary to track the latest report for each file
file_report_map = {}

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

def run_pylint(file_path):
    """Run pylint on a file and return the output"""
    try:
        result = subprocess.run(
            ['pylint', '--output-format=text', file_path],
            capture_output=True,
            text=True
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: 'pylint' command not found. Make sure pylint is installed (`pip install pylint`).")
        return ""
    except Exception as e:
        print(f"Error running pylint on {file_path}: {e}")
        return ""

def parse_pylint_output(output):
    """Parse pylint output to extract issues"""
    issues = []
    lines = output.split('\n')
    
    pattern = re.compile(r'^(.*?):(\d+):(\d+):\s+([A-Z]\d{4}):\s+(.*)\s+\((.*)\)$')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_num, col, code, message, symbol = match.groups()
            issues.append({
                'file': file_path,
                'line': int(line_num),
                'column': int(col),
                'code': code,
                'message': message,
                'symbol': symbol
            })
    
    return issues

def fix_linting_issues_with_ai(file_path, issues):
    """Use AI to fix linting issues in a file. Returns original and fixed content."""
    if not issues:
        return None, None
    
    original_content = None
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found. Cannot fix linting issues.")
        return None, None
        
    try:
        with open(file_path, 'r') as f:
            original_content = f.read()
        
        issues_text = "\n".join([f"- Line {issue['line']}: {issue['message']} ({issue['symbol']})" for issue in issues])
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             print("Error: OPENAI_API_KEY environment variable not set.")
             return original_content, None
        
        prompt = f"""
        Please fix the following linting issues ({len(issues)} issues found) in the Python file '{os.path.basename(file_path)}':

        Linting Issues:
        {issues_text}

        Original code:
        ```python
        {original_content}
        ```

        Please provide the complete fixed Python code only, enclosed in ```python ... ``` blocks, with no other text before or after.
        Ensure all the listed linting issues are resolved in the corrected code.
        """
        
        # Using OpenAI to generate completion
        response = openai.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that fixes Python code linting issues."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2048
        )
        
        # Updated response handling
        fixed_code_raw = response.choices[0].message.content
        
        match = re.search(r"```python\n(.*?)\n```", fixed_code_raw, re.DOTALL)
        if match:
            fixed_code = match.group(1).strip()
            return original_content, fixed_code
        else:
            if fixed_code_raw.startswith("```") and fixed_code_raw.endswith("```"):
                fixed_code = fixed_code_raw[3:-3].strip()
                if fixed_code.startswith("python"):
                    fixed_code = fixed_code[len("python"):].strip()
                return original_content, fixed_code
            else:
                print("Warning: AI response did not contain the expected ```python ... ``` block. Attempting to use the full response.")
                return original_content, fixed_code_raw.strip()
        
    except Exception as e:
        print(f"Error interacting with OPENAI API: {e}")
        return original_content, None
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred in fix_linting_issues_with_ai: {e}")
        return original_content, None

def generate_diff(original_content, fixed_content):
    """Generate a unified diff between two strings"""
    if original_content is None or fixed_content is None:
        return "Error: Cannot generate diff, content missing."
    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        fixed_content.splitlines(keepends=True),
        fromfile='original',
        tofile='fixed'
    )
    return ''.join(diff)

def save_change_report(file_path, diff_content, change_type):
    """Save the diff report as a markdown file for Jekyll, consolidating reports for the same file"""
    if not os.path.exists(LLM_CHANGES_DIR):
        os.makedirs(LLM_CHANGES_DIR)
        print(f"Created directory: {LLM_CHANGES_DIR}")
        
    basename = os.path.basename(file_path)
    file_key = file_path.replace('/', '_').replace('.', '_')
    
    # Check if we already have a report for this file
    existing_reports = []
    if os.path.exists(LLM_CHANGES_DIR):
        for filename in os.listdir(LLM_CHANGES_DIR):
            if filename.endswith('.md') and file_key in filename and not filename.startswith('action_run_marker'):
                existing_reports.append(os.path.join(LLM_CHANGES_DIR, filename))
    
    timestamp = datetime.now()
    report_filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{file_key}.md"
    report_path = os.path.join(LLM_CHANGES_DIR, report_filename)
    
    title = f"{change_type.capitalize()} for {basename}"
    
    front_matter = f"""---
layout: llm_change
title: "{title}"
date: {timestamp.isoformat()}
file: "{file_path}"
change_type: "{change_type}"
consolidated: true
---
"""
    
    try:
        # Ensure the directory exists (in case it was deleted after first check)
        os.makedirs(LLM_CHANGES_DIR, exist_ok=True)
        
        # Delete any existing reports for this file
        for old_report in existing_reports:
            try:
                print(f"Removing older report for {basename}: {old_report}")
                os.remove(old_report)
            except Exception as e:
                print(f"Error removing old report {old_report}: {e}")
        
        # Write the new consolidated report
        with open(report_path, 'w') as f:
            f.write(front_matter)
            f.write(diff_content)
            f.flush()  # Ensure data is written to disk
            
        print(f"Saved consolidated change report: {report_path}")
        
        # Debug: Verify the file was actually created
        if os.path.exists(report_path):
            print(f"DEBUG: Verified report file exists at {report_path}, size: {os.path.getsize(report_path)} bytes")
            # Update index file with category information
            update_index_with_category(title, os.path.basename(report_filename), change_type, timestamp)
            # Store this as the latest report for this file
            file_report_map[file_path] = report_path
        else:
            print(f"DEBUG: PROBLEM! Report file was not created at {report_path}!")
            
    except Exception as e:
        print(f"Error saving change report {report_path}: {e}")
        import traceback
        traceback.print_exc()  # Print detailed stack trace

def update_index_with_category(title, report_filename, change_type, timestamp):
    """Update the index file with categorized change information"""
    try:
        index_path = os.path.join(LLM_CHANGES_DIR, "index.md")
        
        # Create index file if it doesn't exist
        if not os.path.exists(index_path):
            with open(index_path, 'w') as idx:
                idx.write("---\nlayout: page\ntitle: LLM-generated Changes\n---\n\n")
                idx.write("# LLM-generated Changes\n\n")
                idx.write("This is an overview of all changes made by LLM (Large Language Model) in this project.\n\n")
                idx.write("## Latest Changes\n\n")
                idx.write("The following changes have been generated by LLM:\n\n")
                idx.write("<!-- Automatically updated by LLM scripts -->")
        
        # Append the new change entry with date and category information
        with open(index_path, 'a') as idx:
            date_formatted = timestamp.strftime("%Y%m%d_%H%M%S")
            idx.write(f"\n- [{title}](./{report_filename}) <small>[{change_type}] {timestamp.strftime('%d-%m-%Y %H:%M')}</small>")
            
    except Exception as e:
        print(f"Error updating index with category: {e}")

def apply_fixes(file_path, fixed_code):
    """Apply the fixed code to the file"""
    try:
        with open(file_path, 'w') as f:
            f.write(fixed_code)
        print(f"Applied fixes to {file_path}")
        return True
    except Exception as e:
        print(f"Error applying fixes to {file_path}: {e}")
        return False

def verify_fixes(file_path):
    """Verify that the fixes resolved the linting issues"""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found. Cannot verify fixes.")
        return False
        
    import time
    time.sleep(0.1)
    new_output = run_pylint(file_path)
    new_issues = parse_pylint_output(new_output)
    
    return len(new_issues) == 0

def automate_admin_tasks():
    """Automate administrative tasks (linting) for files in files_to_process.txt"""
    print('Automating administrative tasks (Linting Fixes)...')

    # Get Python files from the list file
    files_to_check = get_files_to_process()
    
    if not files_to_check:
        print("No files specified for linting checks.")
        return

    for file_path in files_to_check:
        if not os.path.exists(file_path):
             print(f"Skipping non-existent file specified in list: {file_path}")
             continue

        print(f"\n--- Checking {file_path} for linting issues ---")
        
        pylint_output = run_pylint(file_path)
        
        if not pylint_output or "Your code has been rated at 10.00/10" in pylint_output:
            print(f"No linting issues found or pylint error for {file_path}.")
            continue
        
        issues = parse_pylint_output(pylint_output)
        
        if issues:
            print(f"Found {len(issues)} linting issues:")
            
            print(f"Attempting AI fix for {len(issues)} issues in {file_path}...")
            original_content, fixed_code = fix_linting_issues_with_ai(file_path, issues)
            
            if original_content is None:
                 print(f"Could not read original content for {file_path}. Skipping fix.")
                 continue
                 
            if fixed_code:
                diff = generate_diff(original_content, fixed_code)
                
                if apply_fixes(file_path, fixed_code):
                    save_change_report(file_path, diff, "Linting") 
                    
                    print(f"Verifying fixes in {file_path}...")
                    if verify_fixes(file_path):
                        print(f"✅ All linting issues successfully fixed and verified in {file_path}!")
                    else:
                        print(f"⚠️ Some linting issues might remain after fix in {file_path}. Review the report.")
                else:
                     print(f"❌ Failed to apply fixes to {file_path}.")
            else:
                print(f"❌ AI could not generate fixes for {file_path}. Manual intervention required.")
        else:
            print(f"✅ No actionable linting issues found in {file_path}.")
            
    print("\n--- Linting Fix Automation Complete ---")

if __name__ == '__main__':
    automate_admin_tasks()