# 💰 Financial Advisor AI Chatbot

A sophisticated AI-powered financial advisor chatbot built with FastAPI and Groq's Llama 3.1 model. This application provides educational financial guidance while maintaining conversation context across sessions.

## ✨ Features

- 🤖 **AI Financial Advisor**: Specialized in personal finance, investing, retirement planning, and more
- 💾 **Persistent Memory**: Remembers conversations across server restarts
- 🎨 **Modern UI**: Clean, responsive web interface with financial theme
- 🔄 **Session Management**: Multiple conversation sessions with clear/new options
- ⚠️ **Safety First**: Built-in disclaimers and educational focus
- 🚀 **Fast API**: Built with FastAPI for high performance

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Model**: Groq Llama 3.1-8b-instant
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Storage**: JSON file-based conversation persistence
- **Dependencies**: See `requirements.txt`

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/financial-advisor-chatbot.git
cd financial-advisor-chatbot
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
```bash
# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables**
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

6. **Run the application**
```bash
uvicorn server:app --reload
```

7. **Open your browser**
Navigate to `http://127.0.0.1:8000`

## 📁 Project Structure

```
financial-advisor-chatbot/
├── server.py              # FastAPI backend
├── chatbot.py             # CLI version
├── requirements.txt       # Python dependencies
├── conversation_history.json # Persistent chat storage
├── static/
│   ├── index.html         # Web interface
│   └── app.js            # Frontend JavaScript
└── README.md             # This file
```

## 🎯 Usage

### Web Interface
- Open `http://127.0.0.1:8000` in your browser
- Start chatting about financial topics
- Use "🗑️ Clear Chat" to clear current session
- Use "🆕 New Session" to start fresh

### CLI Version
```bash
python chatbot.py
```

## 💡 Example Questions

- "How do I create a budget?"
- "What should I know about 401(k) plans?"
- "How can I start investing?"
- "What's the difference between stocks and bonds?"
- "How much should I save for retirement?"

## ⚠️ Important Disclaimers

- **Educational Purpose Only**: This chatbot provides financial education, not personalized advice
- **Not Financial Advice**: Always consult licensed professionals for investment decisions
- **No Recommendations**: The AI does not make specific investment recommendations
- **General Guidance**: Focus on financial principles and educational content

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)

### Customization
- Modify `FINANCIAL_ADVISOR_PROMPT` in `server.py` to change the AI's personality
- Update CSS in `static/index.html` for different styling
- Adjust conversation persistence settings in `server.py`

## 📝 API Endpoints

- `POST /chat` - Send a message to the chatbot
- `DELETE /chat/{session_id}` - Clear a specific conversation
- `GET /sessions` - List all conversation sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for the AI model API
- [FastAPI](https://fastapi.tiangolo.com) for the web framework
- [Llama 3.1](https://llama.meta.com) for the language model

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/financial-advisor-chatbot/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Remember**: This is for educational purposes only. Always consult qualified financial professionals for personalized advice! 💼
