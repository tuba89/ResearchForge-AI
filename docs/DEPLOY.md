# Deployment Guide

Complete guide for deploying ResearchForge AI to production environments.

## Quick Deploy Options

### Option 1: Flask (Local/VPS) - Easiest ✅
**Best for:** Quick testing, small scale  
**Time:** 5 minutes  
**Cost:** Free (your own server)

### Option 2: Google Cloud App Engine - Recommended ⭐
**Best for:** Production, auto-scaling  
**Time:** 15 minutes  
**Cost:** ~$20/month (with free tier)

### Option 3: Vertex AI Agent Engine - Advanced
**Best for:** Enterprise, full ADK features  
**Time:** 30 minutes  
**Cost:** Pay-per-use

---

## Option 1: Flask Deployment (Local/VPS)

### Prerequisites
- Python 3.12+
- 512MB RAM minimum
- Domain name (optional)

### Steps

1. **Clone repository**
```bash
git clone https://github.com/yourusername/ResearchForge-AI.git
cd ResearchForge-AI
```

2. **Setup environment**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.template .env
# Edit .env with your API keys
nano .env
```

4. **Run with Gunicorn (production)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

5. **Setup systemd service (optional)**
```bash
sudo nano /etc/systemd/system/researchforge.service
```

Add:
```ini
[Unit]
Description=ResearchForge AI
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/ResearchForge-AI
Environment="PATH=/path/to/ResearchForge-AI/venv/bin"
ExecStart=/path/to/ResearchForge-AI/venv/bin/gunicorn -w 4 -b 0.0.0.0:8080 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable researchforge
sudo systemctl start researchforge
```

---

## Option 2: Google Cloud App Engine (Recommended)

### Prerequisites
- Google Cloud account ([Sign up](https://cloud.google.com))
- Billing enabled
- gcloud CLI installed

### Setup

1. **Install Google Cloud SDK**

**macOS:**
```bash
brew install google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**  
Download from: https://cloud.google.com/sdk/docs/install

2. **Initialize gcloud**
```bash
gcloud init
gcloud auth login
```

3. **Create new project (or use existing)**
```bash
# Create project
gcloud projects create researchforge-ai --name="ResearchForge AI"

# Set as default
gcloud config set project researchforge-ai

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
```

4. **Enable required APIs**
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

5. **Create app.yaml**

Create `app.yaml` in project root:
```yaml
runtime: python312

env_variables:
  GOOGLE_API_KEY: "your-api-key-here"
  SECRET_KEY: "your-secret-key-here"

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

⚠️ **Security Note:** For production, use Secret Manager instead of hardcoding keys:
```yaml
env_variables:
  SECRET_KEY: "random-secret-key"

# Then in app.py, get API key from Secret Manager
```

6. **Deploy**
```bash
# First deployment
gcloud app deploy

# Choose region when prompted (e.g., us-central1)
```

7. **Access your app**
```bash
gcloud app browse
# Your app will be at: https://PROJECT_ID.appspot.com
```

### Custom Domain (Optional)

1. **Map custom domain**
```bash
gcloud app domain-mappings create www.yourdomain.com
```

2. **Update DNS records** as instructed by Google Cloud

### Monitoring

View logs:
```bash
gcloud app logs tail -s default
```

View app in console:
```
https://console.cloud.google.com/appengine
```

---

## Option 3: Vertex AI Agent Engine

### Prerequisites
- Google Cloud project with billing
- ADK CLI installed: `pip install google-genai-adk`

### Setup

1. **Enable APIs**
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
```

2. **Create deployment config**

Create `.agent_engine_config.json`:
```json
{
  "display_name": "ResearchForge AI",
  "description": "Multi-agent research collaboration platform",
  "agent_config": {
    "name": "ResearchForgeAI",
    "model": "gemini-2.5-flash"
  }
}
```

3. **Prepare agent.py** (already exists in repo)

4. **Deploy with ADK CLI**
```bash
export PROJECT_ID=your-project-id

adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=us-central1 \
  . \
  --agent_engine_config_file=.agent_engine_config.json
```

5. **Test deployment**
```bash
# Via Python
from google.cloud import aiplatform

aiplatform.init(project=PROJECT_ID, location="us-central1")
# Test your agent
```

---

## Available Regions

Choose the region closest to your users:

| Region | Location | Latency (US East) |
|--------|----------|-------------------|
| `us-central1` | Iowa, USA | ~30ms |
| `us-east4` | Virginia, USA | ~10ms |
| `us-west1` | Oregon, USA | ~70ms |
| `europe-west1` | Belgium | ~90ms |
| `europe-west4` | Netherlands | ~95ms |

---

## Cost Estimates

### Google Cloud App Engine
- **Free tier:** 28 instance hours/day
- **Paid:** ~$0.05/hour (~$36/month for 1 instance)
- **Scaling:** Auto-scales based on traffic

### Gemini API
- **Free tier:** 15 requests/minute
- **Paid:** ~$0.001 per request
- **Monthly (1000 users):** ~$30-50

### Total Estimated Cost
- **Small scale** (< 100 users/day): $0-20/month
- **Medium scale** (1000 users/day): $50-100/month
- **Large scale** (10k+ users/day): $200+/month

---

## Environment Variables

Required variables for all deployments:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Recommended
SECRET_KEY=random-secret-for-sessions
PORT=8080

# Optional (for Vertex AI)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

---

## Security Best Practices

1. **Never commit API keys to Git**
   ```bash
   # Ensure .env is in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use Secret Manager (production)**
   ```python
   from google.cloud import secretmanager
   
   def get_secret(secret_id):
       client = secretmanager.SecretManagerServiceClient()
       name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
       response = client.access_secret_version(request={"name": name})
       return response.payload.data.decode("UTF-8")
   
   GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")
   ```

3. **Enable HTTPS** (automatic with App Engine)

4. **Set CORS properly** (already configured in app.py)

---

## Troubleshooting

### Issue: Deployment fails with quota error
**Solution:** Enable billing or increase quotas in Cloud Console

### Issue: 502 Bad Gateway
**Solution:** Check app logs: `gcloud app logs tail`

### Issue: API key invalid
**Solution:** Verify key at https://aistudio.google.com/apikey

### Issue: Import errors
**Solution:** Ensure all dependencies in requirements.txt

### Issue: Slow response times
**Solution:** 
- Use Cloud CDN
- Enable caching
- Optimize Gemini prompts

---

## Monitoring & Logs

### View App Engine logs
```bash
gcloud app logs tail -s default
```

### Set up alerts
```bash
# CPU usage alert
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High CPU Usage" \
  --condition-threshold-value=0.8
```

### Check metrics
```
https://console.cloud.google.com/monitoring
```

---

## Updating Deployment

### App Engine
```bash
# Deploy new version
gcloud app deploy

# Route traffic to new version
gcloud app services set-traffic default --splits=NEW_VERSION=1
```

### Rollback if needed
```bash
gcloud app versions list
gcloud app services set-traffic default --splits=OLD_VERSION=1
```

---

## CI/CD (Optional)

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to App Engine

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to App Engine
        uses: google-github-actions/deploy-appengine@v0.2.0
        with:
          credentials: ${{ secrets.GCP_SA_KEY }}
```

---

## Support

- **App Engine Docs:** https://cloud.google.com/appengine/docs
- **Gemini API:** https://ai.google.dev/docs
- **ADK Docs:** https://github.com/google/genai-adk

---

## Quick Reference

| Task | Command |
|------|---------|
| Deploy | `gcloud app deploy` |
| View logs | `gcloud app logs tail` |
| Browse app | `gcloud app browse` |
| Check versions | `gcloud app versions list` |
| Set traffic | `gcloud app services set-traffic` |

---

**Need help?** Open an issue on [GitHub](https://github.com/yourusername/ResearchForge-AI/issues)
