import os
import ast
import re
import openai
from dotenv import load_dotenv
import subprocess
from datetime import datetime

# Define the path for the file list
FILES_TO_PROCESS_PATH = "files_to_process.txt"
# Define the LLM changes directory consistent with other scripts
LLM_CHANGES_DIR = "_llm_changes"

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

def check_for_common_bugs(file_path):
    """Check for common bugs in a Python file using AST parsing"""
    bugs = []
    content = ""
    
    # Add check for file existence
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found. Cannot check for bugs.")
        return bugs, content
        
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            
        # Parse the Python file
        tree = ast.parse(content)
        
        # Find potential division by zero bugs
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                if isinstance(node.right, ast.Num) and node.right.n == 0:
                    bugs.append({
                        'type': 'Division by zero',
                        'line': node.lineno,
                        'suggestion': 'Check for zero before division'
                    })
                    
        # Check for unused imports
        imported_names = set()
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imported_names.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    if name.asname:
                        imported_names.add(name.asname)
                    else:
                        imported_names.add(name.name)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
                
        unused_imports = imported_names - used_names
        if unused_imports:
            bugs.append({
                'type': 'Unused imports',
                'imports': list(unused_imports),
                'suggestion': 'Remove unused imports'
            })
            
        # Check for bare except statements
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type is None:
                        bugs.append({
                            'type': 'Bare except',
                            'line': handler.lineno,
                            'suggestion': 'Specify the exception type to catch'
                        })
                        
        return bugs, content
        
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return [], "" # Return empty content on error

def get_ai_suggestions(file_content, bugs):
    """Get AI-generated suggestions for fixing bugs"""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            return "Could not generate AI suggestions due to missing API key."
        
        # Create a comprehensive prompt
        prompt = f"""
        Analyze the following Python code and suggest fixes for the identified bugs:
        
        ```python
        {file_content}
        ```
        
        Identified potential issues:
        {bugs}
        
        Please provide specific code fixes that can be applied to resolve these issues.
        """
        
        # Using OpenAI to generate suggestions
        response = openai.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes Python code and suggests bug fixes."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=1024
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI suggestions: {e}")
        return "Could not generate AI suggestions."

def save_bug_report(file_path, bugs, suggestions):
    """Save bug detection and fix suggestions to a markdown file in the _llm_changes directory"""
    try:
        # Create the directory if it doesn't exist
        os.makedirs(LLM_CHANGES_DIR, exist_ok=True)
        
        # Skip saving if no bugs found or no suggestions generated
        if not bugs:
            return False
            
        # Create a filename based on the original file path
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_key = file_path.replace('/', '_').replace('.', '_')
        report_file = os.path.join(LLM_CHANGES_DIR, f"{timestamp}_{file_key}_bugs.md")
        
        # Format the report with Jekyll front matter
        title = f"Bug Fix Suggestions for {file_name}"
        front_matter = f"""---
layout: llm_change
title: "{title}"
date: {datetime.now().isoformat()}
file: "{file_path}"
change_type: "Bug Fix Suggestions"
consolidated: true
---
"""
        
        # Format the bugs info
        bugs_md = "## Detected Issues\n\n"
        for i, bug in enumerate(bugs, 1):
            bugs_md += f"### Issue {i}: {bug['type']}\n"
            if 'line' in bug:
                bugs_md += f"- Line: {bug['line']}\n"
            if 'suggestion' in bug:
                bugs_md += f"- Suggestion: {bug['suggestion']}\n"
            if 'imports' in bug:
                bugs_md += f"- Unused imports: {', '.join(bug['imports'])}\n"
            bugs_md += "\n"
            
        # Format the AI suggestions
        ai_md = f"""
## AI-Generated Fix Suggestions

```
{suggestions}
```
"""
        
        # Combine all content
        formatted_report = f"{front_matter}\n{bugs_md}\n{ai_md}"
        
        # Write the report to the file
        with open(report_file, 'w') as f:
            f.write(formatted_report)
            
        print(f"Saved bug report to {report_file}")
        return True
    except Exception as e:
        print(f"Error saving bug report for {file_path}: {e}")
        return False

def suggest_bug_fixes():
    """Analyze code changes and suggest bug fixes for files in files_to_process.txt"""
    print('Analyzing code changes and suggesting bug fixes...')
    
    # Get files to analyze from the list file
    files_to_analyze = get_files_to_process()
    
    if not files_to_analyze:
        print("No files specified for bug analysis.")
        return
    
    for file_path in files_to_analyze:
        print(f"\nAnalyzing {file_path}...")
        # check_for_common_bugs now handles non-existent file check
        bugs, content = check_for_common_bugs(file_path)
        
        if bugs:
            print(f"Found {len(bugs)} potential issues:")
            for bug in bugs:
                print(f"- {bug['type']}: {bug.get('suggestion', '')}")
            
            # Get AI suggestions for fixing the bugs
            # Only get suggestions if we actually read content
            if content:
                suggestions = get_ai_suggestions(content, bugs)
                print("\nAI-suggested fixes:")
                print(suggestions)
                
                # Save the bug report to a file
                save_bug_report(file_path, bugs, suggestions)
            else:
                print("Could not get AI suggestions because file content could not be read.")
        elif content: # Only print "No bugs" if we actually analyzed the file
            print("No common bugs found.")
        # If content is empty and no bugs, it means the file couldn't be read or parsed earlier

if __name__ == '__main__':
    suggest_bug_fixes()