# Contributing to Interactive Dictionary

Thank you for your interest in contributing to this project!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/interactive-dictionary.git
   cd interactive-dictionary
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions and classes

## Testing

Please test your changes before submitting:
- Test with different markdown content
- Test word selection and merging
- Test batch processing
- Verify error handling

## Reporting Issues

When reporting issues, please include:
- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)

## Questions?

Feel free to open an issue for questions or discussions.

