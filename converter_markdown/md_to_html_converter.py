import os
import glob
import openai
from dotenv import load_dotenv


def get_script_directory():
    """Get the directory where the script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def setup_openai():
    """Setup OpenAI API key from environment variables."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    print("OpenAI API key loaded successfully")
    return True

def convert_markdown_to_html(markdown_text):
    """Convert markdown text to HTML using OpenAI."""
    # Create a prompt for the model
    prompt = f"""Convert the following Markdown to HTML:
1.Make sure that you will use the original language of the text.
2.The new HTML file should have the same format as the original markdown file.
3.Make sure to manteing all the funcionalities and content of the original markdown file.
```markdown
{markdown_text}
```

HTML output:
```html
"""
    
    try:
        # Using OpenAI to generate HTML
        response = openai.chat.completions.create(
            model="o3-mini",  # Using a more reliable model
            messages=[
                {"role": "system", "content": "You are a helpful developer that converts markdown to html."},
                {"role": "user", "content": prompt}
            ]
        )
        
        html_output = response.choices[0].message.content
        
        # Extract the HTML part from the response
        try:
            html_output = html_output.split("```html")[1].split("```")[0].strip()
        except IndexError:
            # If the model didn't format the output as expected, return the raw response
            html_output = html_output.replace(prompt, "").strip()
        
        return html_output
    except openai.AuthenticationError as e:
        print("Authentication error: Please check your OpenAI API key")
        raise
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise

def read_markdown_file(file_path):
    """Read markdown content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Input file not found: {file_path}")
        raise
    except Exception as e:
        print(f"Error reading file: {e}")
        raise

def write_html_file(file_path, html_content):
    """Write HTML content to a file."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except Exception as e:
        print(f"Error writing file: {e}")
        raise

def process_markdown_files(input_folder, output_folder):
    """Process all markdown files in the input folder."""
    # Get all markdown files in the input folder
    markdown_files = glob.glob(os.path.join(input_folder, '*.md'))
    
    if not markdown_files:
        print(f"No markdown files found in {input_folder}")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process")
    
    for input_file in markdown_files:
        try:
            # Get the base filename without extension
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_folder, f"{base_name}.html")
            
            print(f"\nProcessing: {input_file}")
            print(f"Output will be saved to: {output_file}")
            
            # Read the markdown file
            markdown_text = read_markdown_file(input_file)
            
            # Convert markdown to HTML
            print("Converting markdown to HTML...")
            html_content = convert_markdown_to_html(markdown_text)
            
            # Write the HTML file
            write_html_file(output_file, html_content)
            print("Conversion completed successfully!")
            
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")
            continue

def main():
    # Get the script's directory
    script_dir = get_script_directory()
    
    # Define input and output folders relative to the script's location
    input_folder = os.path.join(script_dir, 'input_folder_markdown')
    output_folder = os.path.join(script_dir, 'output_folder_markdown')
    
    # Create folders if they don't exist
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    
    try:
        # Setup OpenAI API
        setup_openai()
        
        process_markdown_files(input_folder, output_folder)
        print("\nAll files processed successfully!")
    except Exception as e:
        print(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()