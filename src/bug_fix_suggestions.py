import os
import ast
import re
import openai
from dotenv import load_dotenv
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
        return [f for f in files if f.endswith('.py')]
    except Exception as e:
        print(f"Error getting modified files: {e}")
        return []

def check_for_common_bugs(file_path):
    """Check for common bugs in a Python file using AST parsing"""
    bugs = []
    
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
        return [], ""

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
            max_completion_tokens=1024,
            temperature=0.2,
            top_p=0.95,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI suggestions: {e}")
        return "Could not generate AI suggestions."

def suggest_bug_fixes():
    """Analyze code changes and suggest bug fixes"""
    print('Analyzing code changes and suggesting bug fixes...')
    
    # Get modified Python files
    files = get_modified_python_files()
    if not files:
        # If no modified files found, check evaluate directory
        try:
            evaluate_files = subprocess.run(
                ['find', 'evaluate', '-name', '*.py'],
                capture_output=True, text=True, check=True
            )
            files = evaluate_files.stdout.strip().split('\n')
        except Exception as e:
            print(f"Error finding files in evaluate/: {e}")
            return
    
    for file_path in files:
        print(f"\nAnalyzing {file_path}...")
        bugs, content = check_for_common_bugs(file_path)
        
        if bugs:
            print(f"Found {len(bugs)} potential issues:")
            for bug in bugs:
                print(f"- {bug['type']}: {bug.get('suggestion', '')}")
            
            # Get AI suggestions for fixing the bugs
            suggestions = get_ai_suggestions(content, bugs)
            print("\nAI-suggested fixes:")
            print(suggestions)
        else:
            print("No common bugs found.")

if __name__ == '__main__':
    suggest_bug_fixes()