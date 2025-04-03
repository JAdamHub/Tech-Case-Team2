import os
import sys
import subprocess
import openai
import json
import re
import pytest
from dotenv import load_dotenv
import tempfile
import difflib # Though not used for diff here, keep for consistency if needed later
from datetime import datetime # Added for timestamping
import ast
import inspect
import importlib.util

LLM_CHANGES_DIR = "_llm_changes" # Consistent directory name

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
            # Ensure we only process Python files from the list
            files = [line.strip() for line in f if line.strip() and line.strip().endswith('.py')]
        if not files:
            print(f"File list '{FILES_TO_PROCESS_PATH}' is empty or contains no Python files. No files to process.")
        return files
    except Exception as e:
        print(f"Error reading file list from {FILES_TO_PROCESS_PATH}: {e}")
        return []

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
    except FileNotFoundError:
         # Should be caught above, but keep for robustness
         print(f"Error: Source file not found at {file_path}")
         return None
    except Exception as e:
        print(f"An unexpected error occurred in generate_test_file_with_ai: {e}")
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

def save_creation_report(original_file_path, test_file_path, test_content):
    """Save a report about the created test file for Jekyll, consolidating reports for the same file"""
    if not os.path.exists(LLM_CHANGES_DIR):
        os.makedirs(LLM_CHANGES_DIR)
        print(f"Created directory: {LLM_CHANGES_DIR}")
    
    # Use the original file as the key for consolidation
    basename = os.path.basename(original_file_path)
    original_file_key = original_file_path.replace('/', '_').replace('.', '_')
    
    # Check if we already have a report for this file
    existing_reports = []
    if os.path.exists(LLM_CHANGES_DIR):
        for filename in os.listdir(LLM_CHANGES_DIR):
            # Look for test reports for this original file
            if (filename.endswith('.md') and 
                original_file_key in filename and 
                'test' in filename.lower() and 
                not filename.startswith('action_run_marker')):
                existing_reports.append(os.path.join(LLM_CHANGES_DIR, filename))
    
    timestamp = datetime.now()
    # Use the test file path for the report name, but key off the original file
    report_filename_base = test_file_path.replace('/', '_').replace('.', '_')
    report_filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{report_filename_base}.md"
    report_path = os.path.join(LLM_CHANGES_DIR, report_filename)
    
    title = f"Generated Tests for {basename}"
    
    # Jekyll Front Matter
    front_matter = f"""---
layout: llm_change
title: "{title}"
date: {timestamp.isoformat()}
file: "{test_file_path}"
change_type: "Test Generation"
source_file: "{original_file_path}"
consolidated: true
---
"""
    
    # Content is the generated test code itself
    report_content = f"```python\n{test_content}\n```"
    
    try:
        # Ensure the directory exists (in case it was deleted after first check)
        os.makedirs(LLM_CHANGES_DIR, exist_ok=True)
        
        # Delete any existing reports for this file
        for old_report in existing_reports:
            try:
                print(f"Removing older test report for {basename}: {old_report}")
                os.remove(old_report)
            except Exception as e:
                print(f"Error removing old report {old_report}: {e}")
        
        # Write the new consolidated report
        with open(report_path, 'w') as f:
            f.write(front_matter)
            f.write(report_content)
            f.flush()  # Ensure data is written to disk
        
        print(f"Saved consolidated test creation report: {report_path}")
        
        # Debug: Verify the file was actually created
        if os.path.exists(report_path):
            print(f"DEBUG: Verified report file exists at {report_path}, size: {os.path.getsize(report_path)} bytes")
            # Update index file with category information
            update_index_with_category(title, os.path.basename(report_filename), "Test Generation", timestamp)
            # Store this as the latest report for this file
            file_report_map[original_file_path] = report_path
        else:
            print(f"DEBUG: PROBLEM! Report file was not created at {report_path}!")
            
    except Exception as e:
        print(f"Error saving test creation report {report_path}: {e}")
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

def analyze_workflow_bottlenecks():
    """Analyze workflow bottlenecks using AI (Placeholder/Optional)"""
    # This function is less about direct code changes and more about analysis.
    # Keeping it simple for now, focusing on test generation as the actionable part.
    print("\n--- Analyzing Workflow Bottlenecks (Conceptual) ---")
    print("Common bottlenecks include manual testing, code reviews, documentation.")
    print("AI can assist via automated test generation (demonstrated below), review suggestions, documentation drafting.")
    # In a real scenario, this could call the LLM as before to get a detailed text analysis.
    return "Analysis placeholder."

def address_workflow_bottlenecks():
    """Address workflow bottlenecks, focusing on automated test generation for files in files_to_process.txt"""
    print('--- Addressing Workflow Bottlenecks (Automated Test Generation) ---')
    
    # Get Python files from the list file
    source_files_to_process = get_files_to_process()
    
    if not source_files_to_process:
        print("No Python source files specified in list to generate tests for.")
        return

    generated_tests_count = 0
    passed_tests_count = 0
    failed_generation_count = 0
    
    # Process each source file from the list to generate tests
    for file_path in source_files_to_process:
        print(f"\n>>> Processing source file: {file_path}")
        
        # Add check for file existence early (though also checked in extract_test_requirements)
        if not os.path.exists(file_path):
            print(f"Skipping non-existent source file specified in list: {file_path}")
            continue
            
        # Extract test requirements (functions)
        test_requirements = extract_test_requirements(file_path)
        
        if test_requirements:
            print(f"Found {len(test_requirements)} potential functions to test.")
            
            # Generate test file content using AI
            print(f"Generating tests with AI for {file_path}...")
            test_file_info = generate_test_file_with_ai(file_path, test_requirements)
            
            if test_file_info:
                # Save the generated test file
                saved_test_path = save_test_file(test_file_info)
                
                if saved_test_path:
                    generated_tests_count += 1
                    # Save the creation report for Jekyll
                    save_creation_report(file_path, saved_test_path, test_file_info['content'])
                    
                    # Run the newly generated tests
                    if run_tests(saved_test_path):
                         passed_tests_count += 1
            else:
                print(f"AI failed to generate tests for {file_path}.")
                failed_generation_count += 1
        else:
            print("No testable functions found or error extracting requirements.")
            
    print("\n--- Test Generation Summary ---")
    print(f"Processed {len(source_files_to_process)} source files from the list.") # Updated count source
    print(f"Generated {generated_tests_count} test files.")
    print(f"Generated tests passed for {passed_tests_count} files.")
    if failed_generation_count > 0:
        print(f"AI failed to generate tests for {failed_generation_count} files.")
    print("Reports saved in: _llm_changes/")
    print("--- Automated Test Generation Complete ---")

if __name__ == '__main__':
    address_workflow_bottlenecks()