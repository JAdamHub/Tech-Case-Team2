import os
import sys
import re
import ast
import openai
import subprocess
import difflib
import json
from dotenv import load_dotenv
from datetime import datetime
import importlib.util

# Define constants
FILES_TO_PROCESS_PATH = "files_to_process.txt"
LLM_CHANGES_DIR = "_llm_changes"

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

# ===== Code Review Functions =====

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
              Please review the following code, add comments and provide constructive feedback.
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

# ===== Bug Fix Functions =====

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

# ===== Admin Tasks Functions =====

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

# ===== Workflow Bottlenecks Functions =====

def extract_test_requirements(file_path):
    """Extract test requirements (function definitions) from a file"""
    # Add check for file existence
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found. Cannot extract requirements.")
        return []
        
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Look for function definitions (improved regex to handle async def)
        functions = re.findall(r'^(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\):' , content, re.MULTILINE)
        
        test_requirements = []
        for func_name, args_str in functions:
            # Skip test functions and private/magic methods
            if func_name.startswith('test_') or func_name.startswith('_'):
                continue
                
            # Extract docstring if available (improved regex)
            docstring_pattern = re.compile(r'def\s+' + func_name + r'\s*\([^)]*\):\s*"""(.*?)"""', re.DOTALL)
            docstring_match = docstring_pattern.search(content)
            docstring = docstring_match.group(1).strip().replace('"' , '\"') if docstring_match else "No docstring found."
            
            # Basic argument parsing (can be complex)
            args = [arg.split('=')[0].split(':')[0].strip() for arg in args_str.split(',') if arg.strip()]
            
            test_requirements.append({
                'function': func_name,
                'arguments': args,
                'docstring': docstring
            })
            
        return test_requirements
    except FileNotFoundError:
         # Should be caught above, but keep for robustness
         print(f"Error: File not found at {file_path}")
         return []
    except Exception as e:
        print(f"Error extracting test requirements from {file_path}: {e}")
        return []

def generate_test_file_with_ai(file_path, test_requirements):
    """Generate a test file using AI"""
    try:
        if not test_requirements:
            return None
            
        original_content = None
        # Add check for file existence before reading
        if not os.path.exists(file_path):
            print(f"Error: Source file {file_path} not found. Cannot generate tests.")
            return None
            
        with open(file_path, 'r') as f:
            original_content = f.read()
            
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             print("Error: OPENAI_API_KEY environment variable not set.")
             return None
        
        # Determine the test file name relative to the project root
        relative_path = os.path.relpath(file_path, start=os.getcwd())
        test_file_name = f"test_{os.path.basename(file_path)}"
        # Place tests in a parallel 'tests' directory
        test_dir_rel = os.path.join('tests', os.path.dirname(relative_path).replace('src/', '', 1))
        test_file_rel_path = os.path.join(test_dir_rel, test_file_name)

        # Prepare requirements string for the prompt
        req_str = "\n".join([f"- {req['function']}({', '.join(req['arguments'])})" for req in test_requirements])
        
        prompt = f"""
        You are tasked with generating a complete Python test file using the pytest framework for the following source code file: `{relative_path}`.

        Source Code (`{relative_path}`):
        ```python
        {original_content}
        ```

        Functions to generate tests for:
        {req_str}

        Requirements for the test file (`{test_file_rel_path}`):
        1.  Import necessary modules from the source file (`{relative_path}`). Ensure the import path is correct assuming the tests are run from the project root (e.g., `from {relative_path.replace('/', '.').replace('.py', '')} import ...`).
        2.  Import `pytest`.
        3.  Create test functions named `test_<function_name>` for each function listed above.
        4.  Include meaningful test cases covering:
            *   Typical inputs and expected outputs.
            *   Edge cases (e.g., empty inputs, zero values, boundaries).
            *   Error conditions (using `pytest.raises` for expected exceptions).
        5.  Use pytest fixtures if setup/teardown is needed (e.g., for temporary files or database connections), though likely not needed for simple functions.
        6.  Add clear assertions (`assert`) to check the results.
        7.  Do NOT include tests for private functions (starting with `_`) or test functions (starting with `test_`).

        Generate the complete Python code for the test file `{test_file_rel_path}`. Respond ONLY with the Python code enclosed in ```python ... ``` blocks.
        """
        
        # Using OpenAI to generate test file
        response = openai.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates Python test code."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2048
        )
        
        # Updated response handling
        test_file_content_raw = response.choices[0].message.content
        
        # Clean up the response
        match = re.search(r"```python\n(.*?)\n```", test_file_content_raw, re.DOTALL)
        if match:
            test_file_content = match.group(1).strip()
        elif test_file_content_raw.startswith("```") and test_file_content_raw.endswith("```"):
            test_file_content = test_file_content_raw[3:-3].strip()
            if test_file_content.startswith("python"):
                test_file_content = test_file_content[len("python"):].strip()
        else:
            print("Warning: AI response for test generation did not contain the expected ```python ... ``` block. Using raw response.")
            test_file_content = test_file_content_raw.strip()
        
        return {
            'test_file_path': test_file_rel_path,
            'content': test_file_content
        }
        
    except Exception as e:
        print(f"Error interacting with OpenAI for test generation: {e}")
        return None

def save_test_file(test_file_info):
    """Save the generated test file, creating directories if needed."""
    test_file_path = test_file_info['test_file_path']
    test_dir = os.path.dirname(test_file_path)
    try:
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            print(f"Created test directory: {test_dir}")
            # Add .gitkeep to new test subdirectories if needed
            if test_dir != 'tests':
                 gitkeep_path = os.path.join(test_dir, '.gitkeep')
                 if not os.path.exists(gitkeep_path):
                      with open(gitkeep_path, 'w') as gk: gk.write("# Keep this directory")
            
        with open(test_file_path, 'w') as f:
            f.write(test_file_info['content'])
            
        print(f"Saved generated test file: {test_file_path}")
        return test_file_path
    except Exception as e:
        print(f"Error saving test file {test_file_path}: {e}")
        return None

def run_tests(test_path):
    """Run pytest tests for a specific file or directory"""
    if not os.path.exists(test_path):
        print(f"Test path not found: {test_path}. Skipping tests.")
        return False
    try:
        print(f"\n--- Running tests for: {test_path} ---")
        # Ensure pytest runs from the project root so imports work
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', test_path, '-v'],
            capture_output=True,
            text=True,
            cwd=os.getcwd() # Explicitly set cwd
        )
        
        print("Test Results:")
        print(result.stdout)
        if result.stderr:
            print("Test Errors:")
            print(result.stderr)
        
        if result.returncode != 0 and result.returncode != 5: # 5 means no tests collected
            print(f"❌ Some tests failed for {test_path}. Review output and report.")
            return False
        elif result.returncode == 5:
             print(f"⚠️ No tests were collected for {test_path}. The generated file might be empty or invalid.")
             return False # Treat no tests collected as a failure in generation
        else:
            print(f"✅ All tests passed for {test_path}!")
            return True
            
    except FileNotFoundError:
        print("Error: 'pytest' command not found. Make sure pytest is installed (`pip install pytest`).")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while running tests for {test_path}: {e}")
        return False

# ===== Combined Report Generation =====

def generate_individual_report(file_result):
    """Generate an individual report for a single file in Markdown format"""
    timestamp = datetime.now()
    file_path = file_result['file_path']
    file_name = os.path.basename(file_path)
    report_filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{file_name}_report.md"
    report_path = os.path.join(LLM_CHANGES_DIR, report_filename)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(LLM_CHANGES_DIR):
        os.makedirs(LLM_CHANGES_DIR)
        print(f"Created directory: {LLM_CHANGES_DIR}")
    
    # Extract title from filename
    report_title = f"Analysis Report for {file_name}"
    
    # Jekyll Front Matter
    front_matter = f"""---
layout: llm_change
title: "{report_title}"
date: {timestamp.isoformat()}
change_type: "Individual Analysis"
consolidated: false
file_name: "{file_name}"
---
"""
    
    # Report header
    report_content = f"""# {report_title}
Generated on: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

This report contains code review, bug fix suggestions, linting fixes, and test generation for {file_path}.

"""
    
    # Add detailed results for the file
    report_content += f"\n## File: {file_path}\n\n"
    
    # Code Review section
    if file_result.get('code_review'):
        report_content += "### Code Review\n\n"
        report_content += "```python\n"
        report_content += file_result['code_review']
        report_content += "\n```\n\n"
    
    # Bug Fixes section
    if file_result.get('bugs'):
        report_content += "### Bug Fix Suggestions\n\n"
        for i, bug in enumerate(file_result['bugs'], 1):
            report_content += f"#### Issue {i}: {bug['type']}\n"
            if 'line' in bug:
                report_content += f"- Line: {bug['line']}\n"
            if 'suggestion' in bug:
                report_content += f"- Suggestion: {bug['suggestion']}\n"
            if 'imports' in bug:
                report_content += f"- Unused imports: {', '.join(bug['imports'])}\n"
            report_content += "\n"
        
        if file_result.get('bug_suggestions'):
            report_content += "#### AI-Generated Fix Suggestions\n\n"
            report_content += "```\n"
            report_content += file_result['bug_suggestions']
            report_content += "\n```\n\n"
    
    # Linting Issues section
    if file_result.get('linting_issues'):
        report_content += "### Linting Issues\n\n"
        for issue in file_result['linting_issues']:
            report_content += f"- Line {issue['line']}: {issue['message']} ({issue['symbol']})\n"
        report_content += "\n"
        
        if file_result.get('linting_diff'):
            report_content += "#### Linting Fixes\n\n"
            report_content += "```diff\n"
            report_content += file_result['linting_diff']
            report_content += "\n```\n\n"
    
    # Test Generation section
    if file_result.get('test_file'):
        report_content += "### Generated Tests\n\n"
        report_content += f"Test file created: `{file_result['test_file']}`\n\n"
        
        if file_result.get('test_content'):
            report_content += "```python\n"
            report_content += file_result['test_content']
            report_content += "\n```\n\n"
        
        if file_result.get('test_results'):
            report_content += "#### Test Results\n\n"
            report_content += "```\n"
            report_content += file_result['test_results']
            report_content += "\n```\n\n"

    # Write the report to file
    try:
        with open(report_path, 'w') as f:
            f.write(front_matter + report_content)
        print(f"Individual report saved to: {report_path}")
        return report_path
    except Exception as e:
        print(f"Error saving individual report: {e}")
        return None

def generate_combined_report(file_results):
    """Generate a combined report in Markdown format"""
    timestamp = datetime.now()
    report_filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_combined_report.md"
    report_path = os.path.join(LLM_CHANGES_DIR, report_filename)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(LLM_CHANGES_DIR):
        os.makedirs(LLM_CHANGES_DIR)
        print(f"Created directory: {LLM_CHANGES_DIR}")
    
    # Extract title from filename (e.g., "20240101_120000_combined_report")
    report_title = os.path.splitext(os.path.basename(report_filename))[0]
    
    # Jekyll Front Matter
    front_matter = f"""---
layout: llm_change
title: "{report_title}"
date: {timestamp.isoformat()}
change_type: "Combined Analysis"
consolidated: true
---
"""
    
    # Report header
    report_content = f"""# {report_title}
Generated on: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

This report combines code review, bug fix suggestions, linting fixes, and test generation for the analyzed files.

## Summary

- **Files Analyzed**: {len(file_results)}
- **Code Reviews**: {sum(1 for f in file_results if f.get('code_review'))}
- **Bug Fixes**: {sum(1 for f in file_results if f.get('bugs'))}
- **Linting Issues**: {sum(1 for f in file_results if f.get('linting_issues'))}
- **Tests Generated**: {sum(1 for f in file_results if f.get('test_file'))}

"""
    
    # Add detailed results for each file
    for file_result in file_results:
        file_path = file_result['file_path']
        report_content += f"\n## File: {file_path}\n\n"
        
        # Code Review section
        if file_result.get('code_review'):
            report_content += "### Code Review\n\n"
            report_content += "```python\n"
            report_content += file_result['code_review']
            report_content += "\n```\n\n"
        
        # Bug Fixes section
        if file_result.get('bugs'):
            report_content += "### Bug Fix Suggestions\n\n"
            for i, bug in enumerate(file_result['bugs'], 1):
                report_content += f"#### Issue {i}: {bug['type']}\n"
                if 'line' in bug:
                    report_content += f"- Line: {bug['line']}\n"
                if 'suggestion' in bug:
                    report_content += f"- Suggestion: {bug['suggestion']}\n"
                if 'imports' in bug:
                    report_content += f"- Unused imports: {', '.join(bug['imports'])}\n"
                report_content += "\n"
            
            if file_result.get('bug_suggestions'):
                report_content += "#### AI-Generated Fix Suggestions\n\n"
                report_content += "```\n"
                report_content += file_result['bug_suggestions']
                report_content += "\n```\n\n"
        
        # Linting Issues section
        if file_result.get('linting_issues'):
            report_content += "### Linting Issues\n\n"
            for issue in file_result['linting_issues']:
                report_content += f"- Line {issue['line']}: {issue['message']} ({issue['symbol']})\n"
            report_content += "\n"
            
            if file_result.get('linting_diff'):
                report_content += "#### Linting Fixes\n\n"
                report_content += "```diff\n"
                report_content += file_result['linting_diff']
                report_content += "\n```\n\n"
        
        # Test Generation section
        if file_result.get('test_file'):
            report_content += "### Generated Tests\n\n"
            report_content += f"Test file created: `{file_result['test_file']}`\n\n"
            
            if file_result.get('test_content'):
                report_content += "```python\n"
                report_content += file_result['test_content']
                report_content += "\n```\n\n"
            
            if file_result.get('test_results'):
                report_content += "#### Test Results\n\n"
                report_content += "```\n"
                report_content += file_result['test_results']
                report_content += "\n```\n\n"
    
    # Write the report to file
    try:
        with open(report_path, 'w') as f:
            f.write(front_matter + report_content)
        print(f"Combined report saved to: {report_path}")
        return report_path
    except Exception as e:
        print(f"Error saving combined report: {e}")
        return None

# ===== Main Combined Flow =====

def combined_flow():
    """Run the combined flow of code review, bug fixes, admin tasks, and workflow bottlenecks"""
    print("=== Starting Combined Analysis Flow ===")
    
    # Get files to process
    files_to_process = get_files_to_process()
    
    if not files_to_process:
        print("No files specified for processing.")
        return
    
    # Results container for the individual reports
    file_results = []
    report_paths = []
    
    for file_path in files_to_process:
        print(f"\n=== Processing {file_path} ===")
        
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. Skipping.")
            continue
        
        file_result = {'file_path': file_path}
        
        # Read file content
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        # 1. Code Review
        print(f"Generating code review for {file_path}...")
        code_review = review_code_with_ai(file_path, content)
        file_result['code_review'] = code_review
        
        # 2. Bug Fix Suggestions
        print(f"Checking for bugs in {file_path}...")
        bugs, _ = check_for_common_bugs(file_path)
        file_result['bugs'] = bugs
        
        if bugs:
            print(f"Found {len(bugs)} potential issues.")
            bug_suggestions = get_ai_suggestions(content, bugs)
            file_result['bug_suggestions'] = bug_suggestions
        
        # 3. Linting Fixes
        print(f"Running linting checks on {file_path}...")
        pylint_output = run_pylint(file_path)
        linting_issues = parse_pylint_output(pylint_output)
        file_result['linting_issues'] = linting_issues
        
        if linting_issues:
            print(f"Found {len(linting_issues)} linting issues.")
            original_content, fixed_code = fix_linting_issues_with_ai(file_path, linting_issues)
            
            if fixed_code:
                diff = generate_diff(original_content, fixed_code)
                file_result['linting_diff'] = diff
                
                # Optionally apply fixes (commented out for safety)
                # if apply_fixes(file_path, fixed_code):
                #     print(f"Applied linting fixes to {file_path}")
        
        # 4. Test Generation
        if file_path.endswith('.py'):
            print(f"Generating tests for {file_path}...")
            test_requirements = extract_test_requirements(file_path)
            
            if test_requirements:
                print(f"Found {len(test_requirements)} functions to test.")
                test_file_info = generate_test_file_with_ai(file_path, test_requirements)
                
                if test_file_info:
                    file_result['test_file'] = test_file_info['test_file_path']
                    file_result['test_content'] = test_file_info['content']
                    
                    # Optionally save and run tests (commented out for safety)
                    # saved_test_path = save_test_file(test_file_info)
                    # if saved_test_path:
                    #     test_results = run_tests(saved_test_path)
                    #     file_result['test_results'] = test_results
        
        # Generate individual report for this file
        report_path = generate_individual_report(file_result)
        if report_path:
            report_paths.append(report_path)
            
        # Add the file result to the collection (in case we still want to generate a combined report later)
        file_results.append(file_result)
    
    # No longer generating combined report by default
    # report_path = generate_combined_report(file_results)
    
    if report_paths:
        print(f"\n=== Individual Analysis Complete ===")
        print(f"Generated {len(report_paths)} individual reports:")
        for path in report_paths:
            print(f"- {path}")
    else:
        print("\n=== Analysis Failed ===")

if __name__ == '__main__':
    combined_flow()