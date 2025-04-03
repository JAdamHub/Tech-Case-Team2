# Tech case for AAU Case Competition

https://jadamhub.github.io/Tech-Case-Team2/

## Context

In today’s fast-paced software industry, companies like Vestas face increasing pressure to innovate while maintaining efficient development processes. Software engineers are responsible for a wide range of tasks—from fixing bugs and writing new features to reviewing code and ensuring best practices. This leaves limited time for creative problem-solving, as much of their effort is spent on repetitive or administrative tasks.

## Challenge

Your challenge is to explore how large language models (LLMs), like those available through platforms such as Azure OpenAI, can bridge these gaps and address inefficiencies Copilot doesn’t currently handle. Think critically about where bottlenecks occur in your workflow and what manual tasks could be automated to improve overall efficiency.

## Tasks

These tasks are intended to inspire you and provide ideas for your projects. You can choose to work on any of them, or come up with your own unique solutions. The goal is to be creative and think outside the box, focusing on developing tools that reduce daily repetitive and administrative tasks.

1. **Automating Pull Requests**: Implement a solution that uses LLMs to automatically generate pull requests for bug fixes or new features. This includes generating detailed descriptions based on the changes made.
2. **Bug Fix Suggestions**: Develop a system where LLMs analyze code changes and suggest potential bug fixes. This could involve identifying common coding errors and proposing corrections.
3. **Code Review Automation**: Create a tool that uses LLMs to assist in code reviews by automatically adding suggestions and comments to the code where improvements can be made. This includes enforcing consistent quality and style across the codebase.
4. **Automating Administrative Tasks**: Implement automation for detecting linter issues and ensuring they are fixed before the review process. This task involves integrating LLMs to identify and resolve common linter errors.
5. **Addressing Workflow Bottlenecks**: Explore how LLMs can help automate manual testing. This task focuses on identifying and mitigating workflow bottlenecks beyond just coding.

## Getting Started

1. **Fork the Repository**: Begin by forking this repository to your own GitHub account.
2. **Set Up GitHub Actions**: Follow the instructions provided in the `.github/workflows` directory to configure GitHub Actions for automated testing and deployment.
3. **Implement Your Solutions**: Modify the files in the `src/` directory to develop and implement your solutions for the tasks.

### Notes:

- **Flexibility in Coding Languages**: Feel free to use any programming language that you are comfortable with. The files in the `src/` directory are provided as ideas for your projects and can be adapted to suit your needs.
- **Customizing GitHub Actions**: You are welcome to modify the GitHub Actions workflow file to better fit your project requirements. The provided configuration is just a starting point.
- **Example Code**: The `src/example_code.py` file contains sample functions with intentional bugs and linter errors. Use this code as an idea for your projects to test and validate your solutions, ensuring they can effectively identify and address these issues.
