"""
ResearchForge AI - Flask Web Application
A beautiful, modern web interface for AI-powered research collaboration.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
# google-adk imports removed to fix deployment
# from google.adk.agents import Agent
# from google.adk.tools import FunctionTool
# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
from google.genai import types
import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any, List
import uuid

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
CORS(app)

# Set API key
# Set API key - ensure it's loaded
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.warning("GOOGLE_API_KEY not found in environment variables")
else:
    # Ensure it's in os.environ for libraries that might look for it implicitly
    os.environ['GOOGLE_API_KEY'] = api_key

# Session service removed
# session_service = InMemorySessionService()


# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

def advanced_arxiv_search(
    query: str, 
    category: str = "all", 
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search arXiv for research papers using the official API.
    
    Args:
        query: Search query string
        category: arXiv category filter (e.g., 'cs.AI', 'cs.LG')
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary containing search results with status and papers list
    """
    try:
        base_url = "http://export.arxiv.org/api/query"
        
        # Build search query
        if category != "all":
            search_query = f"cat:{category} AND all:{query}"
        else:
            search_query = f"all:{query}"
        
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        logger.info(f"Searching arXiv for: {query} (category: {category})")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        papers = []
        entries = root.findall('atom:entry', namespaces)
        
        for entry in entries:
            # Extract paper details
            title_elem = entry.find('atom:title', namespaces)
            title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "No title"
            
            authors = []
            for author in entry.findall('atom:author', namespaces):
                name_elem = author.find('atom:name', namespaces)
                if name_elem is not None:
                    authors.append(name_elem.text.strip())
            
            id_elem = entry.find('atom:id', namespaces)
            arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else "unknown"
            
            summary_elem = entry.find('atom:summary', namespaces)
            abstract = summary_elem.text.strip().replace('\n', ' ')[:500] if summary_elem is not None else ""
            
            published_elem = entry.find('atom:published', namespaces)
            published = published_elem.text[:10] if published_elem is not None else "Unknown"
            
            pdf_link = f"https://arxiv.org/pdf/{arxiv_id}"
            web_link = f"https://arxiv.org/abs/{arxiv_id}"
            
            papers.append({
                'title': title,
                'authors': authors,
                'arxiv_id': arxiv_id,
                'published': published,
                'abstract': abstract,
                'pdf_url': pdf_link,
                'web_url': web_link
            })
        
        logger.info(f"Found {len(papers)} papers")
        return {
            "status": "success",
            "query": query,
            "total_results": len(papers),
            "papers": papers,
            "message": f"Found {len(papers)} papers"
        }
        
    except Exception as e:
        logger.error(f"arXiv API error: {str(e)}")
        return {
            "status": "error",
            "message": f"Search failed: {str(e)}",
            "papers": [],
            "query": query
        }


def generate_research_proposal(
    researcher_name: str = "Dr. Sarah Chen",
    project_title: str = "AI Research Collaboration",
    collaboration_focus: str = "artificial intelligence and machine learning"
) -> Dict[str, Any]:
    """
    Generate a comprehensive research proposal.
    
    Args:
        researcher_name: Lead researcher's name
        project_title: Project title
        collaboration_focus: Main research focus area
        
    Returns:
        Dictionary with complete proposal details
    """
    logger.info(f"Generating proposal for: {project_title}")
    
    proposal = {
        "title": f"Collaborative Research: {project_title}",
        "lead_researcher": researcher_name,
        "abstract": f"This proposal outlines an innovative collaborative research project led by "
                   f"{researcher_name} to advance {collaboration_focus}. The research addresses "
                   f"critical gaps in current knowledge and proposes novel methodologies.",
        "research_question": f"How can we leverage advanced AI techniques to solve key challenges "
                           f"in {collaboration_focus}?",
        "methodology": "Mixed-methods approach combining quantitative ML analysis with qualitative "
                      "domain expertise. We will use state-of-the-art deep learning models and "
                      "rigorous experimental validation.",
        "timeline": "24 months with quarterly milestones: Q1-2 (Setup), Q3-4 (Development), "
                   "Q5-6 (Validation), Q7-8 (Dissemination)",
        "budget": "$600K over 24 months",
        "expected_outcomes": "High-impact publications, open-source tools, and field advancement"
    }
    
    return {
        "status": "success",
        "proposal": proposal
    }


def draft_collaboration_email(
    researcher_name: str = "Dr. Sarah Chen",
    recipient_name: str = "Dr. Research Colleague",
    project_title: str = "AI Research Collaboration",
    match_insights: str = "strong research synergy and complementary expertise"
) -> Dict[str, Any]:
    """
    Draft a personalized collaboration email.
    
    Args:
        researcher_name: Sender's name
        recipient_name: Recipient's name
        project_title: Project title
        match_insights: Key collaboration insights
        
    Returns:
        Dictionary with email draft and subject
    """
    logger.info(f"Drafting email for: {project_title}")
    
    email = f"""Subject: Research Collaboration Opportunity: {project_title}

Dear {recipient_name},

I hope this message finds you well. I'm reaching out to propose a research collaboration 
opportunity that aligns with your expertise in {match_insights}.

I believe our work shows remarkable synergy with the project "{project_title}". 
Our preliminary assessment indicates strong alignment in research interests and methodologies.

I would be delighted to schedule a brief call to discuss potential collaboration.

Best regards,
{researcher_name}"""
    
    return {
        "status": "success",
        "email_draft": email,
        "subject": f"Research Collaboration: {project_title}"
    }


# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

# Agent initialization removed as it depends on google-adk
# agent = Agent(
#     name="ResearchForgeAI",
#     model="gemini-2.0-flash-exp",
#     description="Multi-agent research collaboration platform for finding papers, researchers, and generating proposals",
#     instruction="""You are ResearchForge AI, an intelligent research collaboration assistant.
# 
# Your capabilities:
# 1. Search arXiv for research papers (use advanced_arxiv_search)
# 2. Generate research proposals (use generate_research_proposal)
# 3. Draft collaboration emails (use draft_collaboration_email)
# 
# When users ask to:
# - "Find papers" or "search papers" → Use advanced_arxiv_search
# - "Generate proposal" → Use generate_research_proposal
# - "Draft email" → Use draft_collaboration_email
# 
# Be proactive, helpful, and use tools immediately with reasonable defaults.
# Always provide clear, organized responses with actionable information.""",
#     tools=[
#         FunctionTool(advanced_arxiv_search),
#         FunctionTool(generate_research_proposal),
#         FunctionTool(draft_collaboration_email)
#     ]
# )


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_papers():
    """
    API endpoint for searching research papers.
    
    Request JSON:
        {
            "query": "machine learning",
            "category": "cs.AI",
            "max_results": 10
        }
    
    Returns:
        JSON response with search results
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        category = data.get('category', 'all')
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({
                "status": "error",
                "message": "Query parameter is required"
            }), 400
        
        result = advanced_arxiv_search(query, category, max_results)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chatting with the AI agent.
    
    Request JSON:
        {
            "message": "Find papers about quantum computing",
            "session_id": "optional-session-id"
        }
    
    Returns:
        JSON response with agent's reply
    """
    try:
        from google.genai.client import Client
        
        data = request.get_json()
        user_message = data.get('message', '')
        user_session_id = data.get('session_id') or str(uuid.uuid4())
        
        if not user_message:
            return jsonify({
                "status": "error",
                "message": "Message parameter is required"
            }), 400
        
        # Use Gemini client directly for simple chat
        client = Client(api_key=os.environ.get('GOOGLE_API_KEY'))
        
        # Create system instruction
        system_instruction = """You are ResearchForge AI, a PROACTIVE research assistant.

CRITICAL: When users ask questions, provide IMMEDIATE, COMPLETE answers. DO NOT ask clarifying questions first.

Your capabilities:
1. Search arXiv for research papers
2. Generate research proposals
3. Draft collaboration emails

BEHAVIOR RULES:

When user asks "Find papers about X":
- Assume they want recent papers (last 2 years)
- Use their exact query terms
- Return 5-10 papers with titles, authors, links
- Format clearly with bullet points

When user asks "Generate a proposal for X":
- Use X as the project focus
- Create COMPLETE proposal immediately
- Include: title, abstract, methodology, timeline, budget
- Use defaults: researcher="Dr. Sarah Chen", timeline="24 months", budget="$600K"

When user asks "Draft an email for X":
- Create COMPLETE email immediately
- Use X as the project topic
- Include: subject line, greeting, body, closing
- Use defaults: sender="Dr. Sarah Chen", recipient="Dr. Colleague"

FORMATTING:
- Use markdown: **bold**, *italic*, ## headers
- Use bullet points for lists
- Keep responses clear and organized
- Always include specific details and numbers

NEVER say:
- "Could you specify..."
- "What area are you interested in..."
- "To make this better..."
- "Please provide more details..."

ALWAYS:
- Provide complete, actionable information immediately
- Use reasonable defaults when details are missing
- Format responses professionally with markdown
- Be specific and detailed in your answers"""
        
        # Fallback models in priority order (based on your available quota)
        models_to_try = [
            'gemini-2.0-flash-exp',          # Primary - 0/50 RPD available
            'gemini-2.5-flash-lite',         # Fast, lightweight - 0/15 RPM available
            'gemini-2.0-flash-lite',         # Very fast - 17/30 RPM available
            'gemini-2.0-flash'               # Standard - 0/15 RPM available
        ]
        
        response_text = None
        last_error = None
        
        # Try each model until one succeeds
        for model_name in models_to_try:
            try:
                logger.info(f"Trying model: {model_name}")
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7
                    )
                )
                
                response_text = response.text if hasattr(response, 'text') else str(response)
                logger.info(f"✅ Success with model: {model_name}")
                break  # Success! Exit the loop
                
            except Exception as model_error:
                last_error = str(model_error)
                logger.warning(f"❌ Model {model_name} failed: {last_error}")
                # Continue to next model
                continue
        
        # If all models failed
        if response_text is None:
            return jsonify({
                "status": "error",
                "message": f"All models failed. Last error: {last_error}. Please try again in a few moments."
            }), 503
        
        return jsonify({
            "status": "success",
            "response": response_text,
            "session_id": user_session_id
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "ResearchForge AI",
        "version": "1.0.0"
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "message": "Resource not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
