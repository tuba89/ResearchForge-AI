# ResearchForge AI 🔬

<div align="center">

![ResearchForge AI](https://img.shields.io/badge/AI-Powered-blue)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Deployed-green)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8)

**AI-powered research collaboration platform built with Google Gemini & Agent Development Kit**

[Live Demo](#) | [Features](#features) | [Installation](#installation) | [Deployment](#deployment)

</div>

---

## 🌟 Overview

ResearchForge AI is a modern, intelligent research collaboration platform that leverages Google's Gemini AI to help researchers discover papers, generate proposals, and accelerate their research workflow.

Built as a capstone project for the **Agents Intensive** course, it demonstrates advanced multi-agent systems, tool integration, and production deployment on Google Cloud.

## ✨ Features

### 🔍 **Paper Discovery**

- Search millions of research papers from arXiv
- Advanced filtering by category (AI, ML, CV, NLP, etc.)
- Real-time results with paper metadata
- Direct links to PDFs and arXiv pages

### 🤖 **AI Research Assistant**

- Intelligent chat interface powered by Gemini 2.0
- Context-aware conversations with session management
- Automatic tool selection and execution
- Helpful responses with actionable insights

### 📝 **Proposal Generator**

├── agent.py # Core agent definition (deprecated - integrated into app.py)
├── templates/
│ └── index.html # Main HTML interface
├── static/
│ ├── css/ # Custom stylesheets
│ └── js/
│ └── app.js # Frontend JavaScript
├── requirements.txt # Python dependencies
├── app.yaml # Google Cloud App Engine config
└── .env # Environment variables (not in repo)

````

**Technology Stack:**

- **Backend**: Flask, Google ADK, Gemini API
- **Frontend**: HTML5, TailwindCSS, Vanilla JavaScript
- **AI**: Google Gemini 2.0 Flash Exp
- **Deployment**: Google Cloud App Engine
- **Tools**: arXiv API, Python requests

## 📦 Installation

### Prerequisites

- Python 3.12+
- Google Cloud account (for deployment)
- Google API key for Gemini

### Local Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ResearchForge-AI.git
cd ResearchForge-AI
````

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.template .env
# Edit .env and add your GOOGLE_API_KEY
```

5. **Run the application**

```bash
python app.py
```

6. **Open in browser**

```
http://localhost:8080
```

## 🚀 Deployment

### Google Cloud App Engine

1. **Install Google Cloud SDK**

```bash
# Follow: https://cloud.google.com/sdk/docs/install
```

2. **Initialize gcloud**

```bash
gcloud init
gcloud config set project YOUR_PROJECT_ID
```

3. **Update app.yaml**

- Replace `your-api-key-here` with your actual API key
- Or use Secret Manager for production

4. **Deploy**

```bash
gcloud app deploy
```

5. **Access your app**

```bash
gcloud app browse
```

For detailed deployment instructions, see [DEPLOY.md](DEPLOY.md)

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
SECRET_KEY=your_secret_key_for_flask_sessions
PORT=8080
```

### API Endpoints

| Endpoint      | Method | Description            |
| ------------- | ------ | ---------------------- |
| `/`           | GET    | Main application page  |
| `/api/search` | POST   | Search research papers |
| `/api/chat`   | POST   | Chat with AI agent     |
| `/api/health` | GET    | Health check           |

## 📚 Usage Examples

### Search for Papers

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "category": "cs.LG",
    "max_results": 10
  }'
```

### Chat with AI Agent

```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find papers about quantum computing",
    "session_id": "optional-session-id"
  }'
```

## 🎯 Key Concepts from Agents Intensive

This project demonstrates:

1. **Multi-Agent Systems**: Agent with multiple specialized tools
2. **Tool Integration**: arXiv API, proposal generation, email drafting
3. **Session Management**: Persistent conversations with context
4. **Context Engineering**: Optimized prompts for better responses
5. **Observability**: Structured logging throughout
6. **Deployment**: Production-ready Google Cloud setup

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Agents Intensive** course by Google
- **Google Gemini** team for the amazing AI capabilities
- **arXiv** for providing open access to research papers

## 📧 Contact

Built by **Assia** for the Agents Intensive Capstone Project

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ using Google Gemini & Agent Development Kit

</div>
ls
