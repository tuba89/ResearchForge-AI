"""
Simple test script for ResearchForge AI
Run this to test locally before deploying
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types
import requests
import xml.etree.ElementTree as ET

# Load environment variables
load_dotenv()

# Set API key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')


# ============================================================================
# TOOL FUNCTIONS (Same as agent.py)
# ============================================================================

def advanced_arxiv_search(query: str, max_results: int = 5):
    """Search arXiv for research papers"""
    print(f"🔍 Searching arXiv for: {query}")
    
    try:
        base_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        papers = []
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', namespaces):
            title_elem = entry.find('atom:title', namespaces)
            title = title_elem.text.strip() if title_elem is not None else "No title"
            
            id_elem = entry.find('atom:id', namespaces)
            arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else "unknown"
            
            papers.append({
                'title': title,
                'arxiv_id': arxiv_id,
                'pdf_url': f"https://arxiv.org/pdf/{arxiv_id}"
            })
        
        print(f"✅ Found {len(papers)} papers")
        return {
            "status": "success",
            "papers": papers,
            "total": len(papers)
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"status": "error", "message": str(e)}


def generate_research_proposal(
    researcher_name: str = "Dr. Sarah Chen",
    project_title: str = "AI Research"
):
    """Generate research proposal"""
    print(f"📝 Generating proposal for: {project_title}")
    
    proposal = {
        "title": f"Collaborative Research: {project_title}",
        "lead_researcher": researcher_name,
        "abstract": f"Research proposal for {project_title}",
        "timeline": "24 months",
        "budget": "$600K"
    }
    
    print("✅ Proposal generated")
    return {"status": "success", "proposal": proposal}


# ============================================================================
# CREATE AGENT
# ============================================================================

test_agent = Agent(
    name="ResearchForgeAI",
    model="gemini-2.5-flash",
    description="Research collaboration assistant",
    instruction="""You are ResearchForge AI.

When users ask to:
- "Find papers" → Use advanced_arxiv_search
- "Generate proposal" → Use generate_research_proposal

Be helpful and use the tools immediately.""",
    tools=[
        FunctionTool(advanced_arxiv_search),
        FunctionTool(generate_research_proposal)
    ]
)


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_tool_directly():
    """Test 1: Test tools directly (no agent)"""
    print("\n" + "="*70)
    print("TEST 1: Direct Tool Test")
    print("="*70)
    
    # Test arXiv search
    result = advanced_arxiv_search("artificial intelligence", max_results=3)
    
    if result['status'] == 'success':
        print(f"\n✅ SUCCESS: Found {result['total']} papers")
        for i, paper in enumerate(result['papers'], 1):
            print(f"\n{i}. {paper['title'][:80]}...")
            print(f"   ID: {paper['arxiv_id']}")
    else:
        print(f"\n❌ FAILED: {result.get('message', 'Unknown error')}")


def test_agent_with_query(query: str):
    """Test 2: Test agent with a query"""
    print("\n" + "="*70)
    print(f"TEST 2: Agent Test - Query: '{query}'")
    print("="*70)
    
    try:
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        
        # Initialize session service
        session_service = InMemorySessionService()
        
        # Create session explicitly
        session_service.create_session_sync(
            app_name="ResearchForgeAI_Test",
            user_id="test_user",
            session_id="test_session"
        )
        
        # Create Runner
        runner = Runner(
            agent=test_agent,
            session_service=session_service,
            app_name="ResearchForgeAI_Test"
        )
        
        # Create message
        message = types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
        
        # Send to agent
        print("\n🤖 Agent is processing...")
        response_parts = []
        
        # Use runner.run instead of agent.generate_content
        for event in runner.run(
            user_id="test_user",
            session_id="test_session",
            new_message=message
        ):
            # Inspect event structure
            if hasattr(event, 'content') and event.content:
                 for part in event.content.parts:
                    if part.text:
                        response_parts.append(part.text)
            elif hasattr(event, 'text') and event.text:
                response_parts.append(event.text)

        response_text = ''.join(response_parts)
        
        print("\n" + "-"*70)
        print("AGENT RESPONSE:")
        print("-"*70)
        print(response_text)
        print("\n✅ Agent test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Agent test failed: {str(e)}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 RESEARCHFORGE AI - LOCAL TESTING")
    print("="*70)
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env file")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test 1: Direct tool test
    test_tool_directly()
    
    # Test 2: Agent test
    test_agent_with_query("Find papers about machine learning")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    run_all_tests()