# LLM Code Automation Hub 🤖✨

![GitHub Actions Workflow Status](https://github.com/Tech-Case-Team2/workflows/LLM%20Automation%20and%20Reporting/badge.svg)

## 🌟 Project Overview

This project leverages the power of Large Language Models (LLMs) to automate common software development tasks, reduce repetitive work, and increase developer productivity. Using a combination of GitHub Actions, Flask, and OpenAI's API, we've built a comprehensive system that can analyze code changes, suggest improvements, generate tests, and create meaningful reports.

## 🧩 Key Components

### 1. Automated Code Analysis Pipeline 🔍

Our system automatically analyzes code changes in the repository:

- **Code Review** - LLM reviews code and provides constructive feedback
- **Bug Detection** - Identifies common programming issues and suggests fixes
- **Linting Automation** - Finds and resolves style and best practice violations
- **Test Generation** - Automatically creates test cases for code functions

### 2. Report Generation System 📊

Every analysis creates markdown reports that are published to GitHub Pages:

- Individual file reports with detailed findings
- Change history tracking
- Beautiful web interface to browse all code changes

### 3. Pull Request Automation 🔄

Streamlines the PR process:

- Automatically identifies changed files
- Generates meaningful PR descriptions based on code changes
- Creates pull requests with proper metadata

### 4. Content Upload System 📤

A Flask-based server that allows:

- Drag-and-drop file uploads
- Markdown file processing
- Integration with the reporting system

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key
- GitHub repository with Actions enabled

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/Tech-Case-Team2.git
   cd Tech-Case-Team2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create a .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

4. Run the server:
   ```bash
   python src/upload_server.py
   ```

## 🔄 Workflow

The system follows this process:

1. 📝 When code is pushed to the repository, GitHub Actions workflow is triggered
2. 🔍 The workflow identifies changed files in the codebase
3. 🧠 LLM analyzes the code changes for issues and improvement opportunities
4. ✅ Tests are generated for new or modified functions
5. 📊 Report files are created in the `_llm_changes` directory
6. 🌐 GitHub Pages is updated with the latest analysis
7. 🔄 A pull request may be automatically created with LLM-generated description

## 💻 Usage Examples

### Viewing Code Change Reports

Visit the GitHub Pages site at: [https://yourteam.github.io/Tech-Case-Team2/](https://yourteam.github.io/Tech-Case-Team2/)

### Uploading Your Own Files

Access the upload page at: [https://yourteam.github.io/Tech-Case-Team2/drag-drop](https://yourteam.github.io/Tech-Case-Team2/drag-drop)

## 🏗️ Architecture

```
├── .github/workflows     # GitHub Actions configuration
├── _layouts              # Jekyll templates for GitHub Pages
├── _llm_changes          # Generated LLM analysis reports
├── src                   # Core Python source code
│   ├── combined_flow.py  # Main analysis pipeline
│   ├── upload_server.py  # Flask server for uploads
│   └── automate_pull_requests.py  # PR automation
├── tests                 # Generated and manual tests
└── assets                # Web assets for the UI
```

## 🔧 Customization

You can customize the analysis pipeline by modifying:

- The LLM prompt templates in `combined_flow.py`
- The GitHub Actions workflow in `.github/workflows/main.yml`
- The web interface templates in `_layouts/`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Team 2 - AAU Case Competition
