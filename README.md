# ResearchForge AI ⚛️

<a id="top"></a>

<div align="center">

![ResearchForge AI](https://img.shields.io/badge/AI-Powered-blue)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Ready-green)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Multi-Agent Research Collaboration Platform Built with Google Gemini & Agent Development Kit**

[Live Demo](https://researchforge-112206130932.us-central1.run.app/) | [Features](#-features) | [Installation](#-installation) | [Competition Track](#-competition-track)

</div>

---

## 🌟 What is ResearchForge AI?

**ResearchForge AI** transforms research collaboration from a **months-long manual process** into a **minutes-long conversation**.

Our intelligent multi-agent system automates the entire research collaboration workflow:

1. 🔍 Search academic papers from arXiv
2. 👥 Build researcher profiles
3. 🤝 Match ideal collaborators using ML
4. 📝 Generate funding proposals
5. ✉️ Draft outreach emails

All through natural language—just tell ResearchForge what you need.

Built for the **5-Day AI Agents Intensive** capstone project, it demonstrates advanced Agent-to-Agent (A2A) communication, real-world API integration, and production-ready deployment.

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

An **Orchestrator** agent intelligently routes requests to the right specialist, enabling complex workflows like: _"Search for papers on medical imaging, find me the top 3 collaborators, and draft a proposal."_

## 🧠 How A2A Works (Simple Visual Trace)

👤 **User Query**  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
⚡ **Orchestrator** → routes request to relevant agents  
&nbsp;&nbsp;&nbsp;&nbsp;↓

1. 🕵️‍♀️ **DataScout** → finds papers
2. 👤 **ProfileBuilder** → creates profiles
3. 💞 **MatchEngine** → ML matching
4. 👩🏫 **Explainer** → match analysis
5. ⭐ **QualityEvaluator** → quality check
6. 👨💻 **ProposalGenerator** → builds proposal
7. 👩💼 **OutreachAgent** → drafts email
8. 🧠 **MemoryCurator** → saves preferences

&nbsp;&nbsp;&nbsp;&nbsp;↓  
📋 **Combined output from all 8 agents → 👤 User**

<img src="https://i.ibb.co/b5Thdgvr/How-It-Works.png" width="100%" alt="Agents Diagram">

---

## 🆚 ResearchForge AI vs ChatGPT

While ChatGPT is a powerful language model, ResearchForge AI extends its capabilities through real data pipelines, agent-to-agent communication, and ML-powered analysis.  
The comparison below highlights the functional differences:

| Capability             | ChatGPT Alone                                                                                                                                                       | ResearchForge AI                                                                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Paper search           | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> cannot access real APIs            | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> live arXiv + researcher data                |
| Verifiable citations   | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> may generate fabricated references | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> real paper IDs + metadata                   |
| Persistent memory      | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> limited across turns               | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> session-level memory curator                |
| Matching collaborators | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> no embeddings or FAISS             | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> ML similarity + scoring                     |
| Agent collaboration    | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> single-model reasoning only        | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> eight autonomous agents using A2A           |
| Proposal generation    | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> generic text generation            | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> proposals built from real retrieved sources |
| End-to-end workflow    | <img width="12" height="12" alt="image" src="https://github.com/user-attachments/assets/c8219bfa-ae2a-4bba-8b31-f79ff7869b62" /> requires manual steps              | <img width="11" height="11" alt="image" src="https://github.com/user-attachments/assets/3dc6bc90-0405-4ef4-bdec-027b5612daa9" /> fully automated research pipeline           |

**ResearchForge AI operates as a full platform, not just a model prompt.  
ChatGPT serves as one component inside a broader, intelligent system.**

## 🆕 Latest Updates (December 2024)

### New Features

- ✅ **BibTeX Export**: Download search results as `.bib` files for citation managers
- ✅ **Search History**: Automatic tracking with timestamps and paper counts
- ✅ **Enhanced UI**: Gradient animations and glassmorphism effects
- ✅ **Bug Fixes**: Resolved search history backend issues

### Coming Soon

- 🔄 Multi-database search (Google Scholar, PubMed)
- 🔄 Persistent database storage
- 🔄 Advanced filtering options
- 🔄 Collaborative workspaces

---

## 🔄 How It Works: Agent Collaboration

```
👤 User: "Find quantum computing papers and match collaborators"
      ↓
🎯 Orchestrator analyzes request → routes to agents
      ↓
┌─────────────────────────────────────────────┐
│  🕵️ DataScout searches arXiv               │
│  👤 ProfileBuilder creates researcher info  │
│  🤝 MatchEngine runs ML matching            │
│  💡 Explainer analyzes why matches work     │
│  ⭐ QualityEvaluator scores confidence      │
│  📝 ProposalGenerator writes proposal       │
│  ✉️ OutreachSpecialist drafts emails        │
└─────────────────────────────────────────────┘
      ↓
📊 Comprehensive result → 👤 User
```

<div align="center">
  <img src="https://i.ibb.co/b5Thdgvr/How-It-Works.png" width="100%" alt="Agent Collaboration Diagram">
</div>

---

## 🎮 Try It Yourself

### Quick Start (3 Steps)

1. **🌐 [Try Live Demo](https://researchforge-112206130932.us-central1.run.app/)** - No installation needed
2. **💻 [View Kaggle Notebook](https://www.kaggle.com/code/assiaben/researchforge-ai)** - Full implementation with explanations
3. **⚡ Run Locally** - Clone repo and run in 5 minutes (see [Installation](#-installation))

### Example Queries

Try these in the chat interface:

**🔍 Paper Search:**

- `"Find papers about medical imaging AI"`
- `"Show me recent quantum computing research"`
- `"Search for climate change modeling papers"`

**👥 Collaboration:**

- `"Build profiles from: Dr. Alice, Dr. Bob"`
- `"Match researchers for my quantum project"`
- `"Explain why Dr. Alice is a good match"`

**📝 Content Generation:**

- `"Generate a research proposal for AI in healthcare"`
- `"Draft an email to Dr. Alice about collaboration"`
- `"Evaluate the overall match quality"`

---

## 📸 Screenshots

### Hero Section

![Hero Section](static/images/screenshots/hero_section.png)
_Modern landing page with gradient design and intelligent agent orchestration_

### AI Chat Interface

![Chat Interface](static/images/screenshots/chat_interface.png)
_Real-time research assistant powered by 8 specialized AI agents_

### Search & Export Features

![Search and Export](static/images/screenshots/search_export.png)
_Advanced paper search with BibTeX export and automatic search history_

## ✨ Key Features

### 🔍 Smart Paper Discovery

- Real-time search of **millions of arXiv papers**
- Smart category detection (medical → cs.CV + q-bio.QM; quantum → quant-ph + physics)
- Complete metadata: titles, authors, dates, abstracts, **PDF links**
- Supports **any research field** (not limited to predefined domains)

### 🤝 ML-Powered Matching

- **FAISS vector search** with 384-dimensional embeddings
- **Multi-factor scoring**: Skills (30%), Interests (35%), Complementary (25%), Collaboration (10%)
- Partial string matching for interests (works even with slight variations)
- Handles cross-domain collaborations (e.g., quantum + biology)

### 📝 Professional Content Generation

- **Domain-specific proposals**: Clinical data-driven for medical, quantum algorithms for physics
- **Realistic outcomes**: FDA-ready tools, peer-reviewed publications, open-source libraries
- **Complete structure**: Abstract, methodology, timeline, budget, evaluation metrics
- **Personalized emails**: References researcher expertise and project details

### 🧠 Context-Aware AI

- **Multi-turn memory**: Remembers entire conversation context
- **Context extraction**: Profiles automatically get research interests from previous queries
- **Conversation coherence**: No need to repeat information across turns

### 🎨 Modern User Interface

- Beautiful gradient UI with glassmorphism effects
- Responsive design (mobile, tablet, desktop)
- Real-time typing indicators
- Smooth animations and transitions
- Dark mode code blocks with syntax highlighting

---

## 🏆 Competition Track

**Agents for Good** - Education & Research

ResearchForge democratizes research collaboration, helping academics in underserved institutions access the same opportunities as those at elite universities. By automating the tedious parts of collaboration, we enable researchers to focus on what matters: advancing human knowledge.

### Key Concepts Demonstrated

1. ✅ **Multi-Agent Systems** - 8 specialized agents coordinated by an orchestrator
2. ✅ **A2A Protocol** - Agent-to-agent communication via Google ADK
3. ✅ **Custom Tools** - Real arXiv API integration, not synthetic data
4. ✅ **Session Management** - Persistent conversations with context
5. ✅ **Observability** - Comprehensive logging and metrics tracking
6. ✅ **Context Engineering** - Optimized prompts for proactive behavior

---

## 📓 Kaggle Notebook

**Full implementation with detailed explanations:**

[View on Kaggle](https://www.kaggle.com/code/assiaben/researchforge-ai-multi-agent-research-platform)

The notebook includes:

- Complete agent system implementation (V1 and V2)
- Interactive demos with real arXiv data
- Step-by-step explanations
- Architecture diagrams
- Performance metrics

**⭐ Please upvote the notebook if you find it helpful!**

---

## 🏗️ System Architecture

 <img src="static/images/ResearchForge_Diagram_dark.png" width="60%" style="max-width: 600px;" alt="Architecture Diagram">

### Technology Stack

| Layer               | Technologies                                     |
| ------------------- | ------------------------------------------------ |
| **AI Models**       | Google Gemini 2.5 Flash, Gemini 2.0 Flash        |
| **Agent Framework** | Google Agent Development Kit (ADK)               |
| **Backend**         | Python 3.11+, Flask 3.0                          |
| **ML/Search**       | FAISS, SentenceTransformers (384-dim embeddings) |
| **External APIs**   | arXiv.org (live academic papers)                 |
| **Frontend**        | HTML5, TailwindCSS 3.0, Vanilla JavaScript       |
| **Deployment**      | Google Cloud Run / App Engine                    |
| **Observability**   | Python logging, structured metrics               |

### Key Technical Features

- **Agent-to-Agent (A2A) Protocol**: Agents communicate directly using Google ADK
- **Multi-Model Fallback**: Automatic failover between Gemini models for reliability
- **Session Management**: Persistent conversations with context preservation
- **Vector Search**: FAISS indexing for semantic similarity matching
- **Real-Time API Integration**: Live arXiv queries, not cached/demo data

---

## 📦 Installation

### Prerequisites

- **Python 3.11+** (3.11 or 3.12 recommended)
- **Google API Key** for Gemini ([Get free key here](https://aistudio.google.com/apikey))
- **(Optional)** Google Cloud account for deployment

### Local Setup (5 minutes)

1. **Clone the repository**

   ```bash
   git clone https://github.com/tuba89/ResearchForge-AI.git
   cd ResearchForge-AI
   ```

2. **Create virtual environment**

   ```bash
   python3 -m venv venv

   # Activate:
   # macOS/Linux:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   ```bash
   # Copy template
   cp .env.template .env

   # Edit .env and add your Gemini API key:
   # GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. **Run locally**

   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:8080
   ```

---

## 🚀 Deployment

### Option 1: Google Cloud Run (Recommended)

```bash
# Install Google Cloud SDK
brew install google-cloud-sdk  # macOS
# Or: https://cloud.google.com/sdk/docs/install

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy researchforge \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key
```

### Option 2: Local/VPS Production

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

For detailed deployment guide, see **[DEPLOY.md](DEPLOY.md)**

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:

```env
# Required
GOOGLE_API_KEY=your_google_gemini_api_key

# Optional
PORT=8080
SECRET_KEY=random_secret_for_flask_sessions
GOOGLE_CLOUD_PROJECT=your_gcp_project_id
```

### API Endpoints

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

**Example: Export to BibTeX**
\`\`\`bash
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
\`\`\`

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

## 🎯 Project Structure

\`\`\`
ResearchForge-AI/
├── main.py # Flask app with search history API
├── agent.py # 8 agents + BibTeX export
├── chat_interface.py # Session management
├── requirements.txt # Python dependencies
├── .env.template # Environment template
├── .gitignore # Git ignore rules
│
├── templates/
│ └── index.html # UI with export & history
│
├── static/
│ ├── images/
│ │ ├── screenshots/ # 🆕 App screenshots
│ │ │ ├── hero_section.png
│ │ │ ├── chat_interface.png
│ │ │ └── search_export.png
│ │ ├── System_Infographics.png
│ │ └── ResearchForge_Diagram_dark.png
│ ├── css/
│ │ └── agent-dashboard.css # Gradient animations
│ └── js/
│ └── app.js # Export & history logic
│
├── docs/
│ ├── DEPLOY.md
│ └── CONTRIBUTING.md
│
└── README.md
\`\`\`

---

## 🧪 Validated System Tests

All 8 agents tested with real arXiv data. See **[Kaggle Notebook](https://www.kaggle.com/code/assiaben/researchforge-ai)** for complete test results.

**Test Workflow: Medical Imaging AI Collaboration**

| Agent              | Query Example                                                | Result                                         |
| ------------------ | ------------------------------------------------------------ | ---------------------------------------------- |
| DataScout          | "Find papers about deep learning in medical imaging"         | ✅ 10 papers with PDF links                    |
| ProfileBuilder     | "Build profiles from: Dr. Sarah Chen, Dr. Michael Rodriguez" | ✅ Context: "Deep Learning In Medical Imaging" |
| MatchEngine        | "Match researchers for AI-powered diagnostic imaging"        | ✅ 68/100 score (75% skills, 100% interests)   |
| Explainer          | "Explain why Dr. Sarah Chen is a good match"                 | ✅ Detailed analysis with actionable steps     |
| QualityEvaluator   | "Evaluate the overall match quality"                         | ✅ Confidence scores provided                  |
| ProposalGenerator  | "Generate a research proposal"                               | ✅ Domain-specific, funding-ready              |
| OutreachSpecialist | "Draft an email to Dr. Sarah Chen"                           | ✅ Personalized, professional                  |
| MemoryCurator      | _(Implicit validation)_                                      | ✅ Context maintained across 7 turns           |

---

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Make your changes and test thoroughly
4. Commit: `git commit -m 'Add AmazingFeature'`
5. Push: `git push origin feature/AmazingFeature`
6. Open a Pull Request

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines.

---

## 🐛 Known Limitations

- **API Rate Limits**: Free Gemini API has limits; system includes multi-model fallback
- **arXiv Only**: Currently only searches arXiv (not Google Scholar, PubMed, etc.)
- **Session Storage**: Uses in-memory sessions (reset on server restart)
- **Demo Researchers**: Some test data included for demonstration

**Planned improvements** tracked in [GitHub Issues](https://github.com/tuba89/ResearchForge-AI/issues)

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Google AI** for the 5-Day AI Agents Intensive course and Gemini API
- **Google Cloud** for deployment infrastructure and credits
- **arXiv.org** for providing open access to research papers
- **Semantic Scholar** for researcher data APIs

---

## 📧 Contact

**Built by Assia** for the Agents Intensive Capstone Project

- **Track**: Agents for Good
- **Course**: 5-Day AI Agents Intensive (November 2025)
- **GitHub**: [@tuba89](https://github.com/tuba89)

---

## 👥 Team

**Assia Benkedia** - Lead Developer

- LinkedIn: [Assia Benkedia](https://www.linkedin.com/in/assia-benkedia-20708195/)

**Chukwuebuka Okeke** - Contributor

- LinkedIn: [Chukwuebuka Okeke](https://www.linkedin.com/in/chukwuebuka-okeke-3937b571/)

**Ariamehr Maleki** - Contributor

- LinkedIn: [Ariamehr Maleki](https://www.linkedin.com/in/ariamehr-maleki/)

---

<div align="center">

### ⭐ If you find this project useful, please star it!

**Made with ❤️ and ⚛️ using Google Gemini & Agent Development Kit**

[⬆ Back to Top](#researchforge-ai-)

</div>
