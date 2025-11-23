# Interactive Dictionary Web Application

A Flask-based web application that converts markdown content into an interactive dictionary with clickable words. Each word provides AI-generated example sentences using Mistral AI API.

## Features

- 📖 Markdown to interactive HTML conversion
- 🖱️ Clickable words with AI-generated examples
- 🔗 Automatic phrase merging for adjacent selected words
- 📦 Batch processing for multiple words/phrases
- 💾 Caching system for API responses (reduces API calls)
- 📱 Responsive and touch-friendly interface
- 🔒 Security improvements (XSS prevention, input validation)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd 22
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Mistral AI API key:
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

Or create a `.env` file (see `.env.example` for template):
```bash
cp .env.example .env
# Then edit .env and add your API key
```

**Note**: You can get a free API key from [Mistral AI Console](https://console.mistral.ai/)

## Usage

1. Create a `content.md` file in the project root (or edit the existing one)

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:8080`

## Configuration

Environment variables:

- `MISTRAL_API_KEY` (required): Your Mistral AI API key. Get one at https://console.mistral.ai/
- `PORT` (optional): Server port (default: 8080)
- `FLASK_DEBUG` (optional): Enable debug mode (default: False)

Create a `.env` file in the project root to set environment variables:
```
MISTRAL_API_KEY=your_api_key_here
PORT=8080
FLASK_DEBUG=False
```

## Project Structure

```
.
├── app.py                 # Flask backend
├── ai_translator.py      # AI service (Mistral AI API)
├── content.md            # Source markdown content
├── requirements.txt      # Python dependencies
├── templates/
│   └── template.html     # Frontend template
└── data/
    └── translations.json # Cached API responses
```

## Key Improvements

This implementation addresses the critical issues identified in the analysis:

✅ **Security Fixes**:
- API key configuration (supports environment variable with fallback)
- Added XSS prevention (HTML escaping)
- Input validation and length limits
- Proper error handling

✅ **Code Quality**:
- Proper file handling with context managers
- Better variable naming
- Type hints and docstrings
- Comprehensive error handling and logging

✅ **Functionality**:
- Implemented `getDefinedWords()` function
- Cache checking before API calls
- Proper batch processing
- Loading states and error messages

✅ **Performance**:
- Efficient DOM queries
- Client-side HTML escaping
- Caching reduces API calls

## API Endpoints

- `GET /` - Main page with processed content
- `GET /t/<word>` - Get translation/examples for a word
- `POST /batch` - Batch process multiple words

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Limitations and Future Improvements

- Consider using a database instead of JSON file for better concurrency
- Add rate limiting to prevent API abuse
- Implement retry logic for failed API calls
- Add word filtering for punctuation and special characters
- Support for additional AI providers
- User-defined word lists and custom translations

## Troubleshooting

**API Key Error**: Make sure you've set the `MISTRAL_API_KEY` environment variable or added it to your `.env` file.

**Port Already in Use**: Change the port by setting the `PORT` environment variable or modifying `app.py`.

**Module Not Found**: Make sure you've installed all dependencies with `pip install -r requirements.txt`.

## Security Notes

- Always keep your API key secret
- For production, use environment variables for API keys
- Run in production behind a reverse proxy (nginx)
- Enable HTTPS in production
- Consider adding authentication if multi-user support is needed

## License

MIT License

# my-readlang
