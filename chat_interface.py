# chat_interface.py
import uuid
import time
import logging
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

logger = logging.getLogger(__name__)

class ResearchForgeChatV2:
    """A2A protocol chat interface"""
    
    def __init__(self, orchestrator):
        self.session_service = InMemorySessionService()
        self.orchestrator = orchestrator
        self.runner = Runner(
            agent=self.orchestrator,
            session_service=self.session_service,
            app_name="ResearchForge"
        )
        self.session_id = f"chat_{uuid.uuid4().hex[:8]}"
        self.user_id = "researcher"
        self.model_used = None
        self.agents_called = []
        
        print(f"💬 Chat interface initialized - Session: {self.session_id}")
    
    async def start(self):
        """Initialize session"""
        try:
            # In your notebook, this worked with create_session
            self.session_service.create_session(
                app_name="ResearchForge",
                user_id=self.user_id,
                session_id=self.session_id
            )
            print("✅ Session created successfully")
        except Exception as e:
            print(f"ℹ️ Session already exists: {e}")
            pass
    
    async def send_message(self, user_message: str) -> str:
        """Send message with A2A tracking"""
        self.agents_called = []
        start_time = time.time()
        
        message = types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
        
        response_text = ""
        
        try:
            async for event in self.runner.run_async(
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=message
            ):
                # Track agent calls
                if (hasattr(event, 'content') and event.content and 
                    hasattr(event.content, 'parts') and event.content.parts):
                    
                    for part in event.content.parts:
                        # Track function calls (Agent delegation)
                        if hasattr(part, 'function_call') and part.function_call:
                            if hasattr(part.function_call, 'name'):
                                agent_name = part.function_call.name
                                if agent_name not in self.agents_called:
                                    self.agents_called.append(agent_name)
                                    print(f"🎯 Agent called: {agent_name}")
                        
                        # Collect response text
                        if hasattr(part, 'text') and part.text and part.text != "None":
                            response_text += part.text
                
                # Track model usage
                if hasattr(event, 'model') and event.model:
                    self.model_used = event.model
            
            duration = time.time() - start_time
            print(f"✅ Response generated in {duration:.2f}s")
            print(f"🤖 Agents used: {', '.join(self.agents_called) if self.agents_called else 'None'}")
            
            return response_text
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            raise
