--project=$PROJECT_ID \
 --region=us-central1 \
 . \
 --agent_engine_config_file=.agent_engine_config.json

```

### 4. Test

After deployment, test via:

- Google Cloud Console
- API endpoint
- ADK CLI

## Regions

Available regions:

- us-central1
- us-east4
- us-west1
- europe-west1
- europe-west4

## Costs

Estimated costs:

- Gemini API: ~$0.001 per request
- Agent Engine: Pay-per-use
- Cloud Run: ~$0.40 per million requests

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues.

```

---

## 📁 **FINAL FOLDER STRUCTURE:**

```

ResearchForge-AI/
├── agent.py # ← Main deployment file
├── requirements.txt # ← Dependencies
├── .agent_engine_config.json # ← Deployment config
├── .env.template # ← Environment template
├── README.md # ← Project description
├── DEPLOY.md # ← Deployment instructions
├── .gitignore # ← Git ignore file
├── notebook.ipynb # ← Your full Kaggle notebook
├── architecture_diagram.png # ← Your diagram
└── LICENSE # ← MIT license
```
