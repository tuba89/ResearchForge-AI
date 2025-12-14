# ResearchForge AI ⚛️
<div align="center">
  <img src="static/images/System_Infographics.png" width="85%" alt="System Infographics">
</div>

<a id="top"></a>
<div align="center">

![ResearchForge AI](https://img.shields.io/badge/AI-Powered-blue)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Ready-green)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Multi-agent research collaboration platform built with Google Gemini & Agent Development Kit**

| [Features](#-features) | [Installation](#-installation) | [Competition Track](#-competition-track) |

⚛️ [ Try Live Demo](https://researchforge-112206130932.us-central1.run.app/) • 
📖 [ Read Blog](https://medium.com/@iiiassia.beniii/building-researchforge-ai-how-we-created-a-multi-agent-system-to-revolutionize-research-b1ab0f21af4f) • 
💻 [ Kaggle Notebook](https://www.kaggle.com/code/assiaben/researchforge-ai)

</div>

---

## 🌟 Overview

**ResearchForge AI** is an intelligent multi-agent system that automates the entire research collaboration lifecycle. We transform a process that typically takes researchers **months** of manual effort into a seamless, **minute-long conversation**. By coordinating eight specialized AI agents, ResearchForge finds relevant papers, identifies ideal collaborators using ML-powered matching, and generates professional proposals and outreach emails—all through a natural language interface.

Built for the **5-Day AI Agents Intensive** [capstone project](https://www.kaggle.com/competitions/agents-intensive-capstone-project), it demonstrates advanced Agent-to-Agent (A2A) communication, real-world API integration, and production-ready deployment.

### 🎯 The Problem

Researchers waste countless hours on the logistics of collaboration instead of doing the research itself. Manually sifting through academic databases, assessing potential partners, and drafting proposals is slow, inefficient, and limits the scale and diversity of potential collaborations.

### 💡 Our Solution

A sophisticated multi-agent system where each agent has a specialized role:

- **DataScout**: Finds real papers via live arXiv API
- **ProfileBuilder**: Constructs structured researcher profiles
- **MatchEngine**: Uses FAISS + Sentence Transformers for ML-powered matching
- **Explainer**: Provides clear reasoning behind recommendations
- **ProposalGenerator**: Creates funding-ready research proposals
- **OutreachSpecialist**: Drafts personalized collaboration emails
- **MemoryCurator**: Learns user preferences over time
- **QualityEvaluator**: Assesses match quality and system performance

An **Orchestrator** agent intelligently routes requests to the right specialist, enabling complex workflows like: *"Search for papers on medical imaging, find me the top 3 collaborators, and draft a proposal."*

## 🧠 How A2A Works (Simple Visual Trace)

<img src="https://i.ibb.co/b5Thdgvr/How-It-Works.png" width="100%" alt="Agents Diagram">

---

## 🆚 ResearchForge AI vs ChatGPT

While ChatGPT is a powerful language model, ResearchForge AI extends its capabilities through real data pipelines, agent-to-agent communication, and ML-powered analysis.  
The comparison below highlights the functional differences:

| Capability | ChatGPT Alone | ResearchForge AI |
|-----------|----------------|-------------------|
| Paper search | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> cannot access real APIs |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> live arXiv + researcher data |
| Verifiable citations | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> may generate fabricated references | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> real paper IDs + metadata |
| Persistent memory | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> limited across turns |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> session-level memory curator |
| Matching collaborators | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> no embeddings or FAISS |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> ML similarity + scoring |
| Agent collaboration | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> single-model reasoning only |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> eight autonomous agents using A2A |
| Proposal generation |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> generic text generation |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> proposals built from real retrieved sources |
| End-to-end workflow | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> requires manual steps |  <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> fully automated research pipeline |

**ResearchForge AI operates as a full platform, not just a model prompt.  
ChatGPT serves as one component inside a broader, intelligent system.**

## ✨ Features

### 🔍 **Smart Paper Discovery**
- Search millions of research papers from arXiv in real-time
- Advanced filtering by category (AI, ML, CV, NLP, Robotics, etc.)
- Instant results with complete metadata (authors, dates, abstracts)
- Direct PDF downloads and arXiv page links

### 🤖 **AI Research Assistant**
- Intelligent chat interface powered by Google Gemini
- Multi-model fallback system for reliability (gemini-2.0-flash-exp, gemini-2.5-flash-lite, etc.)
- Context-aware conversations with session management
- Markdown-formatted responses with beautiful styling

### 📝 **Automated Content Generation**
- Generate comprehensive research proposals in seconds
- Draft professional collaboration emails
- Customizable templates with smart defaults
- Professional formatting and structure

### 🎨 **Modern User Experience**
- Beautiful gradient UI with glassmorphism effects
- Responsive design (mobile, tablet, desktop)
- Real-time typing indicators
- Smooth animations and transitions
- Dark mode code blocks with syntax highlighting

## 📸 Screenshots

### Hero Section

<img src="static/images/screenshots/hero_section.png" width="60%" style="max-width: 600px;" alt="Hero Section">
_Modern landing page with gradient design and intelligent agent orchestration_


### AI Chat Interface

<img src="static/images/screenshots/chat_interface.png" width="60%" style="max-width: 600px;" alt="Chat Interface">
_Real-time research assistant powered by 8 specialized AI agents_


### Search & Export Features
<img src="static/images/screenshots/search_export.png" width="60%" style="max-width: 600px;" alt="Search and Export">
_Advanced paper search with BibTeX export and automatic search history_

---

## 🏆 Competition: Agents for Good

**Track:** Education & Research  
**Competition:** [5-Day AI Agents Intensive Capstone](https://www.kaggle.com/competitions/agents-intensive-capstone-project)  
**Course:** [Google Kaggle AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents)

### Why "Agents for Good"?

ResearchForge **democratizes research collaboration**:

<img width="16" height="16" alt="image" src="https://github.com/user-attachments/assets/78c16424-a06e-422c-b2d7-fae9a2973d27" /> Helps researchers at **underserved institutions** access elite collaboration opportunities  
<img width="16" height="16" alt="image" src="https://github.com/user-attachments/assets/78c16424-a06e-422c-b2d7-fae9a2973d27" /> **Reduces barriers** to international collaboration  
<img width="16" height="16" alt="image" src="https://github.com/user-attachments/assets/78c16424-a06e-422c-b2d7-fae9a2973d27" /> **Automates tedious logistics** so researchers focus on discovery  
<img width="16" height="16" alt="image" src="https://github.com/user-attachments/assets/78c16424-a06e-422c-b2d7-fae9a2973d27" /> **Accelerates scientific progress** through better matching

### Key Concepts Demonstrated

- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **Multi-Agent Systems**: 8 specialized agents + orchestrator
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **A2A Protocol**: Agent-to-agent communication via Google ADK
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **Real-World Integration**: Live arXiv API, not synthetic data
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **ML-Powered Tools**: FAISS vector search + semantic embeddings
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **Context Engineering**: Proactive agent behaviors and memory
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **Production Deployment**: Google Cloud with 100+ concurrent users
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/4ece1f2f-f9a7-4b0d-b7ec-033f7a492b90" /> **Observability**: Comprehensive logging and performance metrics

---

## 📓 Kaggle Notebook

**[View Complete Implementation on Kaggle →](https://www.kaggle.com/code/assiaben/researchforge-ai)**

The notebook includes:

- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/33914868-f3b6-4dd1-9aa4-67ec00e9586f" /> Full agent system code (V1 and V2 implementations)
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/33914868-f3b6-4dd1-9aa4-67ec00e9586f" /> Interactive demos with real arXiv data
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/33914868-f3b6-4dd1-9aa4-67ec00e9586f" /> Step-by-step explanations of each agent
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/33914868-f3b6-4dd1-9aa4-67ec00e9586f" /> Architecture diagrams and visualizations
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/33914868-f3b6-4dd1-9aa4-67ec00e9586f" /> Performance metrics and validation tests
- <img width="15" height="15" alt="image" src="https://github.com/user-attachments/assets/33914868-f3b6-4dd1-9aa4-67ec00e9586f" /> Context extraction and memory demonstrations

**⭐ Please upvote if you find it helpful!**


---


## 🏗️ System Architecture



 <img src="static/images/ResearchForge_Diagram_dark.png" width="50%" style="max-width: 500px;" alt="Architecture Diagram">


### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **AI Models** | Google Gemini 2.0 Flash, Gemini 2.5 Flash Lite |
| **Backend** | Flask, Google ADK, Python 3.12 |
| **Frontend** | HTML5, TailwindCSS, Vanilla JavaScript |
| **ML/AI Tools** | FAISS, SentenceTransformers, arXiv API |
| **Deployment** | Google Cloud App Engine (optional) |
| **Observability** | Python logging, structured metrics |

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- Google API key for Gemini ([Get one here](https://aistudio.google.com/apikey))
- (Optional) Google Cloud account for deployment

### Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ResearchForge-AI.git
cd ResearchForge-AI
```

2. **Create virtual environment**

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
# Copy template
cp .env.template .env

# Edit .env and add your credentials:
# GOOGLE_API_KEY=your_api_key_here
```

5. **Run the application**

```bash
python app.py
```

6. **Open in browser**

```
http://localhost:8080
```

---

## 🚀 Deployment

### Option 1: Local/VPS Deployment

```bash
# Production mode
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### Option 2: Google Cloud App Engine

1. **Install Google Cloud SDK**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Initialize project**
   ```bash
   gcloud init
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Update app.yaml**
   ```yaml
   runtime: python312
   env_variables:
     GOOGLE_API_KEY: "your-api-key"
   ```

4. **Deploy**
   ```bash
   gcloud app deploy
   ```

5. **View your app**
   ```bash
   gcloud app browse
   ```

For detailed deployment instructions, see [DEPLOY.md](DEPLOY.md)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
SECRET_KEY=your_secret_key_for_flask_sessions
PORT=8080
```

### API Endpoints

| Endpoint              | Method | Description             |
| --------------------- | ------ | ----------------------- |
| `/`                   | GET    | Main application UI     |
| `/api/search`         | POST   | Search arXiv papers     |
| `/api/chat`           | POST   | Chat with AI agents     |
| `/api/export-bibtex`  | POST   | Export papers to BibTeX |
| `/api/search-history` | GET    | Get search history      |
| `/api/search-history` | POST   | Save search             |
| `/api/search-history` | DELETE | Clear history           |
| `/api/health`         | GET    | Health check            |
| `/api/agent-status`   | GET    | Agent status            |
---

## 📚 Usage Examples

### Web Interface

1. **Search Papers**: Enter keywords like "quantum computing" or "deep learning"
2. **Chat with AI**: Ask questions like:
   - "Find papers about medical imaging AI"
   - "Generate a research proposal for climate change"
   - "Draft a collaboration email for my project"

### API Usage

**Search Papers:**
```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "transformer models",
    "category": "cs.CL",
    "max_results": 5
  }'
```

**Chat with Agent:**
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find recent papers on reinforcement learning",
    "session_id": "user-123"
  }'
```

**Example: Export to BibTeX**
```bash
curl -X POST http://localhost:8080/api/export-bibtex \\
-H "Content-Type: application/json" \\
-d '{
"papers": [
{
"title": "Attention Is All You Need",
"authors": ["Vaswani et al."],
"arxiv_id": "1706.03762",
"published": "2017-06-12",
"abstract": "The dominant sequence transduction models..."
}
]
}'
```

---

## 🎯 Project Structure

```

ResearchForge-AI/
├── main.py                               # Flask app with search history API
├── agent.py                              # 8 agents + BibTeX export
├── chat_interface.py                     # Session management
├── requirements.txt                      # Python dependencies
├── .env.template                         # Environment template
├── .gitignore                            # Git ignore rules
│
├── templates/
│ └── index.html                          # UI with export & history
│
├── static/
│ ├── images/
│ │ ├── screenshots/                      #  App screenshots
│ │ │ ├── hero_section.png
│ │ │ ├── chat_interface.png
│ │ │ └── search_export.png
│ │ ├── System_Infographics.png
│ │ └── ResearchForge_Diagram_dark.png
│ ├── css/
│ │ └── agent-dashboard.css                # Gradient animations
│ └── js/
│ └── app.js                               # Export & history logic
│
├── docs/
│ ├── DEPLOY.md
│ └── CONTRIBUTING.md
│
└── README.md

```

---

## 🧪 Testing

### Run Local Tests

```bash
# Test agent functionality
python test_agent.py

# Test API endpoints
python -m pytest tests/
```

### Test Queries

Try these in the chat interface:
1. "Find papers about transformer models in NLP"
2. "Generate a proposal for AI in education"
3. "Draft an email for my healthcare AI project"

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🐛 Known Issues & Limitations

- **API Rate Limits**: Free Gemini API has rate limits; multi-model fallback helps
- **arXiv Scope**: Only searches arXiv (not all academic databases)
- **Session Persistence**: In-memory sessions (lost on restart)

See [Issues](https://github.com/tuba89/ResearchForge-AI/issues) for planned improvements.

---

## 📊 Performance

- **Paper Search**: < 2 seconds (arXiv API)
- **AI Response**: 2-5 seconds (Gemini API)
- **Proposal Generation**: < 3 seconds
- **Concurrent Users**: 100+ (with gunicorn)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google AI** for the 5-Day Agents Intensive course
- **Google Gemini** team for the incredible AI capabilities
- **arXiv.org** for providing open access to research papers
- **Semantic Scholar** for researcher data APIs

---

## 📧 Contact

## 📧 Contact
**Built by Assia, Ariamehr and Chukwuebuka** for the Agents Intensive Capstone Project
- **Track**: Agents for Good
- **Course**: [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents) (November 2025)
- **GitHub**: [@tuba89](https://github.com/tuba89) | [@Ariamehr-Maleki](https://github.com/Ariamehr-Maleki) | [@ExploHealth](https://github.com/ExploHealth)

---

## 👥 Team

**Assia Benkedia** - 
- LinkedIn: [Assia Benkedia](https://www.linkedin.com/in/assia-benkedia-20708195/)

**Chukwuebuka Okeke** - 
- LinkedIn: [Chukwuebuka Okeke](https://www.linkedin.com/in/chukwuebuka-okeke-3937b571/)

**Ariamehr Maleki** -
- LinkedIn: [Ariamehr Maleki](https://www.linkedin.com/in/ariamehr-maleki/)


---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

**Made with ❤️ and ⚛️ using Google Gemini & Agent Development Kit**


[⬆ Back to Top](#top)

</div>
