"""
ResearchForge AI - Deployable Agent
Multi-agent research collaboration platform
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import vertexai
import os
import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any

# Initialize Vertex AI
vertexai.init(
    project=os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id"),
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
)


# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

def advanced_arxiv_search(
    query: str, 
    category: str = "all", 
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search arXiv for REAL research papers using official API
    
    Args:
        query: Search query
        category: arXiv category filter
        max_results: Number of results to return
        
    Returns:
        Dictionary with search results
    """
    try:
        base_url = "http://export.arxiv.org/api/query"
        
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
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        papers = []
        entries = root.findall('atom:entry', namespaces)
        
        for entry in entries:
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
            
            papers.append({
                'title': title,
                'authors': authors,
                'arxiv_id': arxiv_id,
                'published': published,
                'abstract': abstract,
                'pdf_url': pdf_link,
            })
        
        return {
            "status": "success",
            "query": query,
            "total_results": len(papers),
            "papers": papers,
            "message": f"Found {len(papers)} real papers from arXiv"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"arXiv API error: {str(e)}",
            "papers": [],
            "query": query
        }


def generate_research_proposal(
    researcher_name: str = "Dr. Sarah Chen",
    project_title: str = "AI Research Collaboration",
    collaboration_focus: str = "artificial intelligence and machine learning"
) -> Dict[str, Any]:
    """
    Generate comprehensive research proposal
    
    Args:
        researcher_name: Lead researcher's name
        project_title: Project title
        collaboration_focus: Main research focus area
        
    Returns:
        Dictionary with complete proposal
    """
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
    Draft personalized collaboration email
    
    Args:
        researcher_name: Sender's name
        recipient_name: Recipient's name
        project_title: Project title
        match_insights: Key collaboration insights
        
    Returns:
        Dictionary with email draft
    """
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
# MAIN AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name="ResearchForgeAI",
    model="gemini-2.5-flash",
    description="Multi-agent research collaboration platform for finding papers, researchers, and generating proposals",
    instruction="""You are ResearchForge AI, a research collaboration assistant.

Your capabilities:
1. Search arXiv for research papers (use advanced_arxiv_search)
2. Generate research proposals (use generate_research_proposal)
3. Draft collaboration emails (use draft_collaboration_email)

When users ask to:
- "Find papers" or "search papers" → Use advanced_arxiv_search
- "Generate proposal" → Use generate_research_proposal with defaults
- "Draft email" → Use draft_collaboration_email with defaults

Be proactive and use tools immediately with reasonable defaults.""",
    tools=[
        FunctionTool(advanced_arxiv_search),
        FunctionTool(generate_research_proposal),
        FunctionTool(draft_collaboration_email)
    ]
)