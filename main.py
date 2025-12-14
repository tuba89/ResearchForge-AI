import os
import uuid
import time
import logging
import agent
import json
import datetime # 
from collections import defaultdict # 
from flask import Flask, request, jsonify, render_template
from google.genai import types
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import google.generativeai as genai  # For direct API key testing
# from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from agent import (
    research_orchestrator, 
    advanced_arxiv_search,
    semantic_scholar_search,
    build_researcher_profile_from_names,
    build_researcher_profile_from_papers,
    find_optimal_matches,
    generate_detailed_explanation,
    generate_research_proposal,
    draft_collaboration_email,
    save_collaboration_memory,
    load_collaboration_history,
    retry_config,
    export_papers_to_bibtex,
    generate_realistic_seed_researchers  # For database initialization
)
# Added from Step 4
from chat_interface import ResearchForgeChatV2
import asyncio
import nest_asyncio
import os
from dotenv import load_dotenv


# Apply nest_asyncio for async compatibility
nest_asyncio.apply()

# Initialize Flask app
app = Flask(__name__)

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️ WARNING: GOOGLE_API_KEY not found in environment!")
    print("   Make sure you have a .env file with GOOGLE_API_KEY=your_key")
# Global status
agent_status = {
    "Orchestrator": "ready",
    "DataScout": "ready",
    "ProfileBuilder": "ready",
    "MatchEngine": "ready",
    "Explainer": "ready",
    "ProposalGenerator": "ready",
    "OutreachAgent": "ready",
    "MemoryCurator": "ready",
    "QualityEvaluator": "ready"
}

# Rate limiting from your notebook
last_request_time = 0
REQUEST_DELAY = 5.0  # 5 seconds between API calls

# Store user API keys (Session ID -> API Key)
user_api_keys = {}

# Usage statistics
usage_stats = defaultdict(list)

def rate_limit():
    """Enforce minimum delay between API calls"""
    global last_request_time
    now = time.time()
    elapsed = now - last_request_time
    if elapsed < REQUEST_DELAY:
        sleep_time = REQUEST_DELAY - elapsed
        time.sleep(sleep_time)
        print(f"⏳ Rate limiting: waited {sleep_time:.1f}s")
    last_request_time = time.time()

# Initialize services
try:
    # Use the SAME initialization as your notebook
    # from agent import research_orchestrator # Imported at top
    
    # Create chat interface
    chat_interface = ResearchForgeChatV2(research_orchestrator)
    
    # Initialize asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_interface.start())
    
    # ============================================================================
    # DATABASE INITIALIZATION WITH SEED DATA
    # ============================================================================
    print("🌱 Initializing researcher database with seed data...")
    try:
        
        seed_researchers = generate_realistic_seed_researchers(50)
        agent.RESEARCHERS = seed_researchers
        if hasattr(agent, 'generate_projects'):
            agent.PROJECTS = agent.generate_projects(20)
        if hasattr(agent, 'matching_engine') and agent.matching_engine:
            agent.matching_engine.build_similarity_index(agent.RESEARCHERS, agent.PROJECTS)
            print(f"✅ Database initialized with {len(agent.RESEARCHERS)} researchers")
        
        # Also update global PROJECTS variable
        if hasattr(agent, 'PROJECTS'):
            from agent import PROJECTS as GLOBAL_PROJECTS
            GLOBAL_PROJECTS = agent.PROJECTS

        else:
            print(f"✅ Database initialized with {len(agent.RESEARCHERS)} researchers")
    except Exception as init_error:
        print(f"⚠️ Database initialization warning: {init_error}")
    
    AGENTS_LOADED = True
    print("✅ Agents loaded successfully with notebook configuration")
except Exception as e:
    print(f"⚠️ Failed to initialize agents: {e}")
    AGENTS_LOADED = False
    chat_interface = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_papers():
    """
    API endpoint for searching research papers directly.
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
        
        # Call DataScout's advanced search
        # categories = [category] if category != 'all' else ['all']
        result = advanced_arxiv_search(query, category, max_results)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# FEATURE : BibTeX Export - Frontend Endpoint
@app.route('/api/export-bibtex', methods=['POST'])
def export_bibtex():
    """
    Export papers to BibTeX format.
    Accepts papers data and returns downloadable .bib file content.
    """
    try:
        data = request.get_json()
        papers_data = data.get('papers', [])
        
        if not papers_data:
            return jsonify({
                "status": "error",
                "message": "No papers provided for export"
            }), 400
        
        # Call the export function
        from agent import export_papers_to_bibtex
        result = export_papers_to_bibtex(json.dumps({"papers": papers_data}))
        
        if result.get('status') == 'success':
            return jsonify({
                "status": "success",
                "bibtex_content": result.get('bibtex_content'),
                "filename": result.get('filename'),
                "entry_count": result.get('entry_count')
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get('message', 'Export failed')
            }), 500
            
    except Exception as e:
        logger.error(f"BibTeX export error: {str(e)}")
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
        "version": "2.0.0",
        "agents_loaded": AGENTS_LOADED,
        "agents_count": 8 if AGENTS_LOADED else 0
    })

@app.route('/api/agent-status', methods=['GET'])
def get_agent_status():
    """Get current status of all agents."""
    return jsonify({
        "status": "success",
        "agents": agent_status,
        "timestamp": time.time()
    })


@app.route('/api/set-api-key', methods=['POST'])
def set_api_key():
    """Allow users to provide their own Gemini API key"""
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'Please provide an API key'
            }), 400
        
        if not api_key.startswith('AIzaSy'):
            return jsonify({
                'status': 'error',
                'message': 'Invalid API key format (should start with AIzaSy...)'
            }), 400
        
        # Test the key
        from google import genai
        client = genai.Client(api_key=api_key)
        
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-lite',
                contents='test'
            )
            
            # Key works! Store it
            user_api_keys[session_id] = api_key
            
            print(f"✅ User API key validated for session: {session_id[:8]}...")
            
            # Log usage
            ip_address = request.remote_addr
            usage_stats[ip_address].append({
                'timestamp': datetime.datetime.now(),
                'action': 'api_key_set',
                'session_id': session_id
            })
            
            return jsonify({
                'status': 'success',
                'message': 'API key validated and saved! You can now use the app.'
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'API key validation failed: {str(e)}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/usage-stats', methods=['GET'])
def get_usage_stats():
    """View who's using the app"""
    try:
        # Build summary
        stats_summary = {}
        total_requests = 0
        
        for ip, logs in usage_stats.items():
            if logs:
                total_requests += len(logs)
                stats_summary[ip] = {
                    'request_count': len(logs),
                    'first_seen': logs[0]['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                    'last_active': logs[-1]['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                    'using_own_key': any(log.get('using_own_key', False) for log in logs),
                    'recent_messages': [log.get('message', '')[:30] for log in logs[-3:]]  # Last 3 messages
                }
        
        return jsonify({
            'total_visitors': len(usage_stats),
            'total_requests': total_requests,
            'recent_activity': stats_summary,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

# ═════════════════════════════════
# Search History - Backend Endpoint 

# Global variable to store search history (in-memory, per session)
search_history = defaultdict(list)  # session_id -> list of searches

@app.route('/api/search-history', methods=['GET', 'POST', 'DELETE'])
def manage_search_history():
    """
    Manage search history for users.
    GET: Retrieve search history
    POST: Save a search
    DELETE: Clear search history
    """
    try:
        # Get session_id from appropriate source based on method
        if request.method == 'GET' or request.method == 'DELETE':
            session_id = request.args.get('session_id', 'default')
        else:  # POST
            data = request.get_json() or {}
            session_id = data.get('session_id', 'default')
        
        if request.method == 'GET':
            # Retrieve history
            history = search_history.get(session_id, [])
            # Return last 20 searches (most recent first)
            return jsonify({
                "status": "success",
                "history": history[-20:][::-1],  # Reverse to show newest first
                "count": len(history)
            })
        
        elif request.method == 'POST':
            # Save a search
            data = request.get_json()
            search_entry = {
                "query": data.get('query', ''),
                "category": data.get('category', 'all'),
                "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "result_count": data.get('result_count', 0),
                "papers": data.get('papers', [])[:5]  # Store only first 5 papers to save memory
            }
            
            search_history[session_id].append(search_entry)
            
            # Limit to 50 searches per session
            if len(search_history[session_id]) > 50:
                search_history[session_id] = search_history[session_id][-50:]
            
            return jsonify({
                "status": "success",
                "message": "Search saved to history"
            })
        
        elif request.method == 'DELETE':
            # Clear history
            if session_id in search_history:
                del search_history[session_id]
            
            return jsonify({
                "status": "success",
                "message": "Search history cleared"
            })
    
    except Exception as e:
        logger.error(f"Search history error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ============================================================================
# CHAT ENDPOINT
# ============================================================================


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chatting with the 8-agent orchestrator.
    """
    try:
        # 1. GET USER MESSAGE
        data = request.get_json()
        user_message = data.get('message', '')
        user_session_id = data.get('session_id') or str(uuid.uuid4())
        user_provided_key = data.get('api_key', '').strip()  # Get API key from request
        
        if not user_message:
            return jsonify({
                "status": "error",
                "message": "Message parameter is required"
            }), 400
        
        # print(f"📥 Received: '{user_message}'")
        # print(f"🔑 API Key from request: {'Provided' if user_provided_key else 'Not provided'}")
        
        # Check if agents loaded
        if not AGENTS_LOADED or chat_interface is None:
            return jsonify({
                "status": "success",
                "response": f"I received: '{user_message}'. System initializing...",
                "session_id": user_session_id
            })

        # Log usage BEFORE processing
        ip_address = request.remote_addr
        timestamp = datetime.datetime.now()
        using_user_key = bool(user_provided_key and user_provided_key.startswith('AIza'))
        usage_stats[ip_address].append({
            'timestamp': timestamp,
            'message': user_message[:50],
            'session_id': user_session_id,
            'using_own_key': using_user_key
        })
        
        # Save to file (append mode)
        try:
            with open('usage_log.txt', 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} | {ip_address} | {user_session_id[:8]}... | {user_message[:50]} | {'User Key' if using_user_key else 'Default Key'}\n")
        except Exception as log_err:
            print(f"⚠️ Failed to write log: {log_err}")
        
        # Get API key 
        api_key_to_use = None
        default_key = os.getenv('GOOGLE_API_KEY')
        
        # Priority: User provided key > Session stored key > Default key
        if user_provided_key and user_provided_key.startswith('AIza'):
            api_key_to_use = user_provided_key
            # print(f"🔑 Using API key from REQUEST: {user_provided_key[:15]}...")
            # Save it for future requests in this session
            user_api_keys[user_session_id] = user_provided_key
        elif user_session_id in user_api_keys:
            api_key_to_use = user_api_keys[user_session_id]
            # print(f"🔑 Using API key from SESSION: {api_key_to_use[:15]}...")
        else:
            api_key_to_use = default_key
            if default_key:
                print(f"⚠️ Using DEFAULT API key (may have quota issues)")
            else:
                print(f"❌ No API key available!")
                return jsonify({
                    "status": "error",
                    "error_type": "no_api_key",
                    "message": "No API key available. Please provide your Gemini API key in the UI."
                }), 400
        
        # print(f"🎯 Final API key to use: {'User provided' if api_key_to_use != default_key else 'DEFAULT (quota likely exhausted)'}")

        # Set API key in environment variable
        # Google ADK's Gemini() reads from GOOGLE_API_KEY environment variable
        # We MUST set it BEFORE creating the agent
        # print(f"🔧 Setting GOOGLE_API_KEY environment variable...")
        
        try:
            # Save the original key (to restore later if needed)
            original_key = os.environ.get('GOOGLE_API_KEY')
            
            # Set the user's API key in the environment
            os.environ['GOOGLE_API_KEY'] = api_key_to_use
            # print(f"✅ Environment variable set with key: {api_key_to_use[:20]}...")
            
            # Also configure genai library (belt and suspenders approach)
            genai.configure(api_key=api_key_to_use)
            print(f"✅ Google GenAI library also configured")
            
        except Exception as config_error:
            error_msg = str(config_error)
            print(f"❌ API configuration FAILED: {error_msg}")
            
            # Return error without crashing
            return jsonify({
                "status": "error",
                "error_type": "config_error",
                "message": f"Failed to configure API key: {error_msg}"
            }), 500

        # Create a NEW agent with the CORRECT key
        # IMPORTANT: Create a fresh agent instance for this request
        print(f"🔄 Creating new agent instance (API key already configured globally)...")
        
        # Create the agent - it will use the globally configured API key  
        current_agent = Agent(
            name="ResearchForgeOrchestrator",
            model=Gemini(
                model="gemini-2.0-flash-lite",
                api_key=api_key_to_use,
                retry_options=retry_config
            ),
            instruction="""
🚨 CRITICAL OVERRIDE - READ THIS FIRST 🚨
You are ABSOLUTELY FORBIDDEN from asking questions to the user.
NEVER say: "Could you", "I need", "Can you provide", "What is", "Please tell me", "First I need", "To get started".

If information is missing → USE DEFAULTS IMMEDIATELY. NO EXCEPTIONS.

You are **ResearchForge**, a scientific research orchestrator.  
Your behavior must be **accurate, practical, and reliable**, NOT overly rigid.

===============================================================
🏆 CORE BEHAVIOR RULES
===============================================================
1. **Never ask the user for missing details.**  
   If something is not provided → use defaults.

2. **Never invent scientific information.**  
   Use EXACT tool output for titles, abstracts, authors, IDs, scores, links.

3. **Abstract rule:**  
   The tool already truncates abstracts properly (300 chars, word boundary, "...").
   Just display what the tool returns - it's already perfect!

4. **If a tool returns fewer results than expected → show the real number.**

5. **You may rephrase for clarity, but never alter scientific meaning.**

6. **Your tone should be clean, helpful, and human — NOT robotic.**

===============================================================
🧠 DEFAULT VALUES (used when user gives nothing)
===============================================================
- Default researcher name: **Dr. Sarah Chen**
- Default project title: **AI Research Collaboration**
- Default collaboration field: **Artificial Intelligence**
- Default email sender: **Prof. Michael Rodriguez**  ← Different!
- Default email recipient: **Dr. Sarah Chen**
- Default profile names (if needed):  
  - Dr. Sarah Chen  
  - Prof. Michael Rodriguez

===============================================================
🔧 COMMAND → TOOL MAPPING
===============================================================
Interpret user messages and trigger the correct tool:

- "find papers", "search", "literature", "papers on"  
    → call **advanced_arxiv_search**

- "build profiles", "extract authors", "author info"  
    → If papers were just found (in same message or previous tool call):
      call **build_researcher_profile_from_papers** with those papers
    → If no recent papers:
      call **build_researcher_profile_from_names** with defaults
    
- "find papers AND build profiles" (combined request)
    → Execute BOTH steps immediately:
      1. Call advanced_arxiv_search
      2. Call build_researcher_profile_from_papers with results
    → Show both results to user

- "find collaborators", "match researchers", "collaboration"  
    → call **find_optimal_matches**

- "proposal", "research plan", "generate proposal"  
    → call **generate_research_proposal**

- "email", "draft email", "outreach"  
    → call **draft_collaboration_email**
    → If recipient not specified, use "Dr. Sarah Chen"
    → If sender not specified, use "Prof. Michael Rodriguez"
    → This prevents self-emails!

- "save", "remember this", "store"  
    → call **save_collaboration_memory**

- "load", "history", "previous session"  
    → call **load_collaboration_history**

- "export", "bibtex", "download", "save papers"  
    → call **export_papers_to_bibtex**
    → Export papers to BibTeX format for citation managers

===============================================================
🔄 MULTI-STEP WORKFLOW ENGINE
===============================================================
**SPECIAL CASE: Profile Building**
If user says "find papers AND build profiles" or "search papers and extract authors":
→ Execute BOTH steps immediately in ONE response:
   1. Call advanced_arxiv_search
   2. Immediately call build_researcher_profile_from_papers with the results
→ Do NOT break into separate steps for this specific workflow!

**OTHER MULTI-STEP WORKFLOWS:**
For other chains like "Find papers, match researchers, and draft email":
1. Perform ONLY the first step
2. Stop and respond: "Step 1 done. Reply 'continue' to proceed."
3. When user replies "continue" → Execute next step only

This keeps the tool call results in context for profile building.

===============================================================
📚 PAPER RESULT FORMAT (clean + readable)
===============================================================
📚 I found **[N]** papers:

1. **[Exact Title]**  
   👤 Authors: [Authors]  
   📅 Published: [Date]  
   🆔 arXiv: [ID]  
   📄 PDF: https://arxiv.org/pdf/[ID]  
   📝 [First paragraph of abstract]...

===============================================================
👥 PROFILE RESULT FORMAT
===============================================================
When build_researcher_profile_from_papers returns data:
- ALWAYS display the "message" or "formatted_output" field
- Show the complete profile information to the user
- Include researcher names, institutions, and expertise

Example output:
✅ Extracted 8 researchers from papers!

1. **Felix Mohr**
   📚 3 papers | 🎓 5 years experience
   🔬 Research: Machine Learning, Data Science

2. **[Next researcher]**...
===============================================================
🎯 MATCH RESULT FORMAT
===============================================================
1. **[Name]** – [Institution]  
   ⭐ Match Score: [X]/100  
   🔬 Relevant Expertise: [Areas]

===============================================================
😌 FRIENDLY FLEX RULES (important!)
===============================================================
- If tool output lacks some fields, gracefully skip them.  
- If a tool fails, give a soft, human message and continue.  
- Keep responses clean and readable — NOT strict JSON.

===============================================================
Your job:  
Detect intent → choose correct tool → apply defaults → respond clearly  
""",
            tools=[
                FunctionTool(advanced_arxiv_search),
                FunctionTool(semantic_scholar_search),
                FunctionTool(build_researcher_profile_from_names),
                FunctionTool(build_researcher_profile_from_papers),
                FunctionTool(find_optimal_matches),
                FunctionTool(generate_detailed_explanation),
                FunctionTool(generate_research_proposal),
                FunctionTool(draft_collaboration_email),
                FunctionTool(save_collaboration_memory),
                FunctionTool(load_collaboration_history),
                FunctionTool(export_papers_to_bibtex)
            ]
        )
        # Create a NEW chat interface with the user's agent
        # Don't reuse the global one - create a fresh one
        user_chat_interface = ResearchForgeChatV2(current_agent)
        
        # Initialize asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(user_chat_interface.start())
        
        # 6. APPLY RATE LIMITING
        rate_limit()
        
        try:
            # 7. CALL CHAT INTERFACE with user's agent

            
            response = loop.run_until_complete(
                user_chat_interface.send_message(user_message)
            )
            
            loop.close()
            

            
            # 8. Extract text from response
            response_text = ""
            
            if isinstance(response, str):
                response_text = response

            elif hasattr(response, 'text'):
                response_text = response.text

            elif hasattr(response, 'content'):
                response_text = response.content

            elif isinstance(response, dict):
                if 'text' in response:
                    response_text = response['text']
                elif 'response' in response:
                    response_text = response['response']
                elif 'message' in response:
                    response_text = response['message']
                else:
                    response_text = str(response)

            else:
                response_text = str(response)
                print(f"⚠️ Using str() fallback")
            
            # 9. Clean response
            response_text = response_text.strip()
            
            # 10. Check if response is empty
            if not response_text or response_text == "None" or response_text == "":
                print("⚠️ Empty response from agent")
                response_text = "I processed your request but didn't generate a response. Please try:\n\n• 'Find papers about [topic]'\n• 'Generate a proposal for [topic]'\n• 'Match researchers for [project]'"
            
            # print(f"📤 Sending response ({len(response_text)} chars)")
            
            return jsonify({
                "status": "success",
                "response": response_text,
                "session_id": user_session_id,
                "used_user_key": api_key_to_use != default_key  # Tell frontend if user key was used
            })
            
        except Exception as agent_error:
            print(f"❌ Agent error: {str(agent_error)}")
            import traceback
            traceback.print_exc()
            
            error_msg = str(agent_error)
            
            # Better error detection
            if "429" in error_msg and "RESOURCE_EXHAUSTED" in error_msg:
                # Check which key failed
                if api_key_to_use == default_key:
                    error_message = "The default API key has reached its daily limit. Please use your own Gemini API key."
                else:
                    error_message = "Your API key has reached its quota limit. Please check your usage at https://aistudio.google.com/apikey"
                
                return jsonify({
                    "status": "error",
                    "error_type": "quota_exhausted",
                    "message": error_message,
                    "retry_after": "24 hours"
                }), 429
            elif "quota" in error_msg.lower():
                return jsonify({
                    "status": "error",
                    "error_type": "quota_exhausted",
                    "message": "API quota exceeded. Please try again in a few minutes or use a different key.",
                }), 429
            elif "API key not valid" in error_msg or "invalid API key" in error_msg.lower():
                return jsonify({
                    "status": "error",
                    "error_type": "invalid_key",
                    "message": "Invalid API key. Please check your key and try again.",
                }), 400
            else:
                user_msg = "The AI assistant encountered an error. Please try again."
            
            return jsonify({
                "status": "error",
                "message": user_msg,
                "error_details": error_msg if app.debug else None
            }), 500
        
    except Exception as e:
        print(f"❌ Outer error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "status": "error",
            "message": f"Server error. Please refresh the page and try again."
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)