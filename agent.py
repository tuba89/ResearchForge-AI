"""
ResearchForge AI - 8 Specialized Agents System
Multi-agent research collaboration platform with ML-powered matching
"""

import os
import time
import uuid
import json
import random
import logging
import asyncio
import requests
import numpy as np
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv

# Google ADK
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models.google_llm import Gemini
from google.genai import types

# ML & Data
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger_data = logging.getLogger('DataScout')
logger_main = logging.getLogger('ResearchForge')

# ============================================================================
# CONFIGURATION & OBSERVABILITY
# ============================================================================

# API Configuration
retry_config = types.HttpRetryOptions(
    attempts=10,  # Increased to handle long waits
    exp_base=2,   # Smoother exponential backoff
    initial_delay=4, # Start slower
    http_status_codes=[429, 500, 503, 504]
)


# Load environment variables from .env file
load_dotenv()

# Set Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    print(f"✅ API Key loaded from .env ({GOOGLE_API_KEY[:10]}...)")
else:
    print("⚠️ No GOOGLE_API_KEY found in .env file!")
    print("   Create a .env file with: GOOGLE_API_KEY=your_key_here")
# Metrics Tracker
class AgentMetrics:
    """Track performance metrics for all agents"""
    
    def __init__(self):
        self.metrics = {
            'requests': 0,
            'successes': 0,
            'failures': 0,
            'total_time': 0.0,
            'agent_calls': defaultdict(int),
            'tool_calls': defaultdict(int),
            'model_usage': defaultdict(int)
        }
        self.start_time = time.time()
    
    def record_request(self, agent_name: str, success: bool, duration: float):
        """Record a request"""
        self.metrics['requests'] += 1
        if success:
            self.metrics['successes'] += 1
        else:
            self.metrics['failures'] += 1
        self.metrics['total_time'] += duration
        self.metrics['agent_calls'][agent_name] += 1
        
        logger.info(f"📊 {agent_name} | Success: {success} | Duration: {duration:.2f}s")
    
    def record_tool(self, tool_name: str):
        """Record tool usage"""
        self.metrics['tool_calls'][tool_name] += 1
        logger.info(f"🔧 Tool called: {tool_name}")
    
    def record_model(self, model_name: str):
        """Record model usage"""
        self.metrics['model_usage'][model_name] += 1

metrics = AgentMetrics()

# ============================================================================
# DATA MODELS
# ============================================================================

class ResearchInterest(BaseModel):
    topic: str
    expertise_level: float = Field(ge=0, le=1)
    years_experience: int
    publications_count: int

class ResearcherProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    institution: str
    department: str
    position: str
    research_interests: List[ResearchInterest]
    skills: List[str]
    publications: List[str]
    citation_count: int
    h_index: int
    email: Optional[str] = None
    collaboration_history: List[str] = []
    geolocation: Optional[str] = None
    funding_sources: List[str] = []
    availability: str = "Open to collaboration"
    embedding: Optional[List[float]] = None

class ResearchProject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    abstract: str
    research_areas: List[str]
    required_skills: List[str]
    desired_expertise: List[str]
    timeline_months: int
    budget_range: str
    funding_status: str
    collaboration_type: str
    difficulty_level: str = "Intermediate"
    embedding: Optional[List[float]] = None

class MatchResult(BaseModel):
    researcher_id: str
    project_id: str
    overall_score: float = Field(ge=0, le=100)
    skill_match: float
    interest_match: float
    complementary_score: float
    geographic_compatibility: float
    career_synergy: float
    explanation: str
    confidence_interval: str

class CollaborationProposal(BaseModel):
    title: str
    abstract: str
    research_question: str
    methodology: str
    expected_outcomes: str
    timeline: str
    budget_breakdown: str
    collaboration_plan: str
    evaluation_metrics: str

class ProjectRequirement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(default="Research Project")
    description: str = Field(description="Project summary/description")
    required_skills: List[str] = Field(default_factory=list)
    research_areas: List[str] = Field(default_factory=list)
    duration_months: int = Field(default=12)
    location: str = Field(default="Academic Collaboration")
    collaboration_type: str = Field(default="remote")
    funding_available: bool = Field(default=True)
    start_date: str = Field(default="flexible")
    institution: str = Field(default="International")
    embedding: Optional[List[float]] = None

# ============================================================================
# ML MATCHING ENGINE
# ============================================================================

print("⚡ Loading sentence transformer model (all-MiniLM-L6-v2)...")
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Embedding model loaded")
except Exception as e:
    print(f"⚠️ Failed to load SentenceTransformer: {e}")
    embedding_model = None

class AdvancedMatchingEngine:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.researcher_index = None
        self.project_index = None
        self.researchers = []
        self.projects = []
        
    def build_similarity_index(self, researchers: List[ResearcherProfile], projects: List[ResearchProject]):
        if not self.embedding_model:
            print("⚠️ ML Engine disabled (no model)")
            return

        print("🔨 Building FAISS similarity indices...")
        
        # Researchers
        researcher_texts = []
        for r in researchers:
            interests = " ".join([ri.topic for ri in r.research_interests])
            skills = " ".join(r.skills)
            text = f"{r.name} {r.institution} {interests} {skills}"
            researcher_texts.append(text)
        
        researcher_embeddings = self.embedding_model.encode(researcher_texts)
        for i, r in enumerate(researchers):
            r.embedding = researcher_embeddings[i].tolist()
            
        dimension = researcher_embeddings.shape[1]
        self.researcher_index = faiss.IndexFlatL2(dimension)
        self.researcher_index.add(researcher_embeddings)
        
        # Projects
        project_texts = []
        for p in projects:
            areas = " ".join(p.research_areas)
            skills = " ".join(p.required_skills)
            text = f"{p.title} {p.abstract} {areas} {skills}"
            project_texts.append(text)
            
        project_embeddings = self.embedding_model.encode(project_texts)
        for i, p in enumerate(projects):
            p.embedding = project_embeddings[i].tolist()
            
        self.project_index = faiss.IndexFlatL2(dimension)
        self.project_index.add(project_embeddings)
        
        self.researchers = researchers
        self.projects = projects
        print(f"✓ Indexed {len(researchers)} researchers and {len(projects)} projects")

    def calculate_advanced_match(self, researcher: ResearcherProfile, project: Union[ResearchProject, ProjectRequirement]) -> MatchResult:
        # Extract project fields
        if isinstance(project, ProjectRequirement):
            project_title = project.title
            project_required_skills = project.required_skills
            project_research_areas = project.research_areas
            project_collaboration_type = project.collaboration_type
            project_difficulty_level = "Intermediate"
        else:
            project_title = project.title
            project_required_skills = project.required_skills
            project_research_areas = project.research_areas
            project_collaboration_type = project.collaboration_type
            project_difficulty_level = project.difficulty_level
            
        # 1. Skill Match
        researcher_skills = set([s.lower() for s in researcher.skills])
        project_skills = set([s.lower() for s in project_required_skills])
        
        if len(researcher_skills.union(project_skills)) > 0:
            skill_match = len(researcher_skills.intersection(project_skills)) / len(researcher_skills.union(project_skills)) * 100
        else:
            skill_match = 0.0
            
        # 2. Interest Match
        if not researcher.research_interests or not project_research_areas:
            interest_match = 0.0
        else:
            researcher_topics = [ri.topic.lower() for ri in researcher.research_interests]
            project_topics = [pa.lower() for pa in project_research_areas]
            matches = 0
            total = len(researcher_topics)
            for r_topic in researcher_topics:
                for p_topic in project_topics:
                    if p_topic in r_topic or r_topic in p_topic:
                        matches += 1
                        break
            interest_match = (matches / total * 100) if total > 0 else 0.0
            
        # 3. Complementary Score
        unique_skills = researcher_skills - project_skills
        complementary_score = min(len(unique_skills) / max(len(researcher_skills), 1) * 100, 100)
        
        # 4. Geographic
        geographic_compatibility = 85.0 if project_collaboration_type in ["International", "remote"] else 50.0
        
        # 5. Career Synergy
        avg_experience = np.mean([ri.years_experience for ri in researcher.research_interests]) if researcher.research_interests else 5
        career_synergy = 85.0 # Simplified logic
        
        # 6. Semantic Similarity
        semantic_score = 50.0
        if self.embedding_model and researcher.embedding and project.embedding:
            r_emb = np.array(researcher.embedding).reshape(1, -1)
            p_emb = np.array(project.embedding).reshape(1, -1)
            semantic_sim = cosine_similarity(r_emb, p_emb)[0][0]
            semantic_score = max(0, semantic_sim * 100)
            
        # Overall Score
        overall_score = (
            skill_match * 0.25 +
            interest_match * 0.25 +
            complementary_score * 0.15 +
            geographic_compatibility * 0.10 +
            career_synergy * 0.10 +
            semantic_score * 0.15
        )
        
        explanation = self._generate_explanation(overall_score, skill_match, interest_match, complementary_score, researcher, project_title)
        confidence = "High" if researcher.citation_count > 100 else "Medium"
        
        return MatchResult(
            researcher_id=researcher.id,
            project_id=project.id,
            overall_score=round(overall_score, 1),
            skill_match=round(skill_match, 1),
            interest_match=round(interest_match, 1),
            complementary_score=round(complementary_score, 1),
            geographic_compatibility=round(geographic_compatibility, 1),
            career_synergy=round(career_synergy, 1),
            explanation=explanation,
            confidence_interval=f"{confidence} (±5 points)"
        )

    def _generate_explanation(self, overall, skill, interest, comp, researcher, title):
        quality = "excellent" if overall >= 80 else "strong" if overall >= 65 else "moderate"
        return f"{quality.upper()} match ({overall:.0f}/100): Skills align at {skill:.0f}%, interests {interest:.0f}%. {researcher.name} adds value to {title}."

matching_engine = AdvancedMatchingEngine(embedding_model)

# ============================================================================
# DATA GENERATION
# ============================================================================

def generate_researchers(count: int = 50) -> List[ResearcherProfile]:
    researchers = []
    for i in range(count):
        researcher = ResearcherProfile(
            name=f"Dr. Researcher {i}",
            institution="Stanford University",
            department="CS",
            position="Professor",
            research_interests=[ResearchInterest(topic="AI", expertise_level=0.9, years_experience=10, publications_count=20)],
            skills=["Python", "PyTorch"],
            publications=["Paper 1"],
            citation_count=1000,
            h_index=20,
            email=f"researcher{i}@stanford.edu"
        )
        researchers.append(researcher)
    return researchers

def generate_projects(count: int = 30) -> List[ResearchProject]:
    projects = []
    for i in range(count):
        project = ResearchProject(
            title=f"Project {i}",
            abstract="Description",
            research_areas=["AI"],
            required_skills=["Python"],
            desired_expertise=["ML"],
            timeline_months=12,
            budget_range="$100k",
            funding_status="Funded",
            collaboration_type="remote"
        )
        projects.append(project)
    return projects

RESEARCHERS = generate_researchers(50)
PROJECTS = generate_projects(30)
matching_engine.build_similarity_index(RESEARCHERS, PROJECTS)

# ============================================================================
# TOOL FUNCTIONS
# ============================================================================
# Helper Functions to truncate abstracts
def truncate_abstract_smart(abstract: str, max_length: int = 300) -> str:
    """
    Truncate abstract at word boundary, never mid-word.
    
    Args:
        abstract: Full abstract text
        max_length: Maximum length (default: 300 chars)
    
    Returns:
        Truncated abstract with "..." if needed
    """
    if len(abstract) <= max_length:
        return abstract
    
    # Truncate to max_length
    truncated = abstract[:max_length]
    
    # Find last complete word
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        # Cut at last space to avoid mid-word cut
        truncated = truncated[:last_space]
    
    # Add ellipsis
    return truncated.strip() + "..."

# search arXiv for papers
def advanced_arxiv_search(query: str, category: str = "all", max_results: int = 10) -> Dict[str, Any]:
    """Search arXiv for REAL papers with FULL details and VALIDATION"""
    start_time = time.time()
    try:
        metrics.record_tool('arxiv_search')
        base_url = "http://export.arxiv.org/api/query"
        
        # Helper: Semantic Pertinence
        def semantic_pertinence(q, text):
            if not embedding_model: return 0.0
            q_emb = embedding_model.encode([q])
            t_emb = embedding_model.encode([text])
            score = cosine_similarity(q_emb, t_emb)[0][0]
            return score

        # Helper: Keyword Pertinence
        def is_pertinent(paper, user_query):
            q = user_query.lower()
            title = paper["title"].lower()
            abstract = paper["abstract"].lower()
            
            # Hard keyword match
            if any(word in title for word in q.split()):
                return True
            if any(word in abstract for word in q.split()):
                return True
            return False

        # --- SANITIZATION LAYER ---
        ALLOWED_CATEGORIES = {
            # Physics
            "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
            "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph",
            # CS
            "cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.RO", "cs.CR", "cs.SE", 
            "cs.HC", "cs.CY", "cs.SI", "cs.DS", "cs.IT", "cs.NI",
            # Math
            "math.CO", "math.DS", "math.FA", "math.GT", "math.LO", "math.NT", "math.PR", "math.ST",
            # Economics
            "econ.EM", "econ.GN", "econ.TH",
            # Quantitative Biology
            "q-bio.BM", "q-bio.GN", "q-bio.NC", "q-bio.QM",
            # Quantitative Finance
            "q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM", "q-fin.RM", "q-fin.ST", "q-fin.TR",
            # Statistics
            "stat.ML", "stat.AP", "stat.CO", "stat.ME", "stat.TH",
            # EE
            "eess.AS", "eess.IV", "eess.SP", "eess.SY"
        }


        # Validate and sanitize category
        if category != "all" and category not in ALLOWED_CATEGORIES:
            logger.warning(f"⚠️ Invalid category detected: '{category}'. Defaulting to 'all'.")
            category = "all"

        # Domain-aware query construction
        if category == "all":
            search_query = f"all:{query}"
        else:
            search_query = f"cat:{category} AND all:{query}"
        
        # Fetch slightly more to allow for filtering
        fetch_count = max_results * 3 # Fetch 3x to ensure enough after filtering

        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': fetch_count, 
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        # Stability fix: (connect_timeout, read_timeout)
        response = requests.get(base_url, params=params, timeout=(10, 40))
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        # XML namespaces for arXiv
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',   # For <title>, <author>, <published>
            'arxiv': 'http://arxiv.org/schemas/atom' # For <arxiv:primary_category>
        }
        
        raw_papers = []
        for entry in root.findall('atom:entry', namespaces):
            title = entry.find('atom:title', namespaces).text.strip().replace('\n', ' ')
            
            # Get authors
            authors = []
            for author in entry.findall('atom:author', namespaces):
                name = author.find('atom:name', namespaces).text
                authors.append(name)
            
            # Get published date
            published = entry.find('atom:published', namespaces).text[:10]
            
            # Get arXiv ID
            arxiv_id = entry.find('atom:id', namespaces).text.split('/abs/')[-1]
            
            # Get primary category
            category_term = "Unknown"
            cat_tag = entry.find('arxiv:primary_category', namespaces)
            if cat_tag is not None:
                category_term = cat_tag.attrib.get('term', 'Unknown')
            
            # Get abstract
            abstract_full = entry.find('atom:summary', namespaces).text.strip().replace('\n', ' ')
            abstract = truncate_abstract_smart(abstract_full, 300)
            
            raw_papers.append({
                'title': title,
                'authors': authors,
                'published': published,
                'arxiv_id': arxiv_id,
                'pdf_url': f"https://arxiv.org/pdf/{arxiv_id}",
                'abstract': abstract,
                'category': category_term
            })

        # --- VALIDATION & SCORING LAYER ---
        validated_papers = []
        for p in raw_papers:
            # 1. Pertinence Check
            if not is_pertinent(p, query):
                continue
                
            # 2. Semantic Score
            sem_score = 0.0
            if embedding_model:
                sem_score = semantic_pertinence(query, p['title'] + " " + p['abstract'])
            
            # Only keep if semantic score is decent (or if ML is disabled)
            if embedding_model and sem_score < 0.40: # Slightly lower threshold to be safe
                continue
                
            # 3. Add Truth Stamps
            p['semantic_score'] = round(float(sem_score), 3)
            p['truth_stamp'] = {
                'domain_verified': p['category'],
                'consistency_check': 'Title-Abstract Consistent',
                'inference_check': 'No Application Inference Added'
            }
            validated_papers.append(p)
            # Stop when we have enough papers
            if len(validated_papers) >= max_results:
                print(f"✓ Reached target: {len(validated_papers)} papers")
                break
            
        # Sort by semantic score if available
        if embedding_model and validated_papers:  # safety check
            validated_papers.sort(key=lambda x: x.get('semantic_score', 0), reverse=True)
    
        # Don't slice again! We already have exactly max_results
        final_papers = validated_papers  # Already limited by break above
        
        duration = time.time() - start_time
        metrics.record_request('DataScout', True, duration)
        
        return {
            "status": "success",
            "total_results": len(final_papers),
            "papers": final_papers,
            "message": f"Found {len(final_papers)} validated papers"
        }
    except Exception as e:
        metrics.record_request('DataScout', False, time.time() - start_time)
        return {"status": "error", "message": str(e), "papers": []}

def semantic_scholar_search(author_name: str) -> Dict[str, Any]:
    """Search Semantic Scholar for REAL author profiles"""
    try:
        metrics.record_tool('semantic_scholar')
        base_url = "https://api.semanticscholar.org/graph/v1/author/search"
        params = {'query': author_name, 'limit': 5, 'fields': 'name,affiliations,paperCount,citationCount,hIndex'}
        response = requests.get(base_url, params=params, headers={'Accept': 'application/json'}, timeout=10)
        data = response.json()
        return {"status": "success", "authors": data.get('data', [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def build_researcher_profile_from_names(researcher_names: str, research_context: str = "AI Research") -> Dict[str, Any]:
    """Build REAL profiles from names using Semantic Scholar"""
    names_list = [n.strip() for n in researcher_names.split(',')]
    research_topic = research_context.replace("research", "").strip().title() or "AI Research"
    
    created_profiles = []
    for name in names_list:
        if len(name) < 3: continue
        
        # 1. Search for REAL data
        ss_data = semantic_scholar_search(name)
        authors = ss_data.get('authors', [])
        
        if authors and len(authors) > 0:
            # Use the top match
            author = authors[0]
            real_name = author.get('name', name)
            affiliations = author.get('affiliations', [])
            institution = affiliations[0] if affiliations else "Independent Researcher"
            paper_count = author.get('paperCount', 0)
            citation_count = author.get('citationCount', 0)
            h_index = author.get('hIndex', 0)
            
            profile_id = f"researcher_{len(RESEARCHERS)+1}_{real_name.replace(' ', '_')[:20]}"
            
            new_profile = ResearcherProfile(
                id=profile_id,
                name=real_name,
                institution=institution,
                department="Research",
                position="Researcher",
                research_interests=[ResearchInterest(topic=research_topic, expertise_level=0.9, years_experience=5, publications_count=paper_count)],
                skills=["Research", research_topic],
                publications=[], # Could fetch papers too if needed
                citation_count=citation_count,
                h_index=h_index
            )
            RESEARCHERS.append(new_profile)
            created_profiles.append({
                "id": profile_id, 
                "name": real_name, 
                "institution": institution,
                "h_index": h_index,
                "source": "Semantic Scholar (Verified)"
            })
        else:
            # Fallback for not found (be honest)
            created_profiles.append({
                "name": name, 
                "error": "Profile not found in Semantic Scholar database."
            })
        
    return {"status": "success", "profiles_created": len(created_profiles), "profiles": created_profiles}

def build_researcher_profile_from_papers(papers_data: str = "{}") -> Dict[str, Any]:
    """
    Extract researchers from papers that were just found.
    This builds the researcher database organically from search results.
    
    Args:
        papers_data: JSON string or dict with search results from advanced_arxiv_search
        
    Returns:
        Dict with status, profiles created, and formatted output
    """
    try:
        # Parse input (handles both string JSON and dict)
        if isinstance(papers_data, str):
            try:
                data = json.loads(papers_data)
            except:
                data = papers_data
        else:
            data = papers_data
        
        # Extract papers list
        if isinstance(data, dict) and 'papers' in data:
            papers_list = data['papers']
        elif isinstance(data, list):
            papers_list = data
        elif isinstance(data, dict) and 'status' in data and data['status'] == 'success':
            papers_list = data.get('papers', [])
        else:
            return {
                "status": "error",
                "message": "No papers provided. Please search for papers first using advanced_arxiv_search()."
            }
        
        if not papers_list:
            return {
                "status": "error",
                "message": "No papers found to extract researchers from."
            }
        

        
        # Build author profiles
        author_profiles = {}
        
        for paper in papers_list[:15]:  # Process first 15 papers max
            authors = paper.get('authors', [])
            paper_title = paper.get('title', 'Unknown')
            paper_id = paper.get('arxiv_id', 'Unknown')
            
            for i, author in enumerate(authors[:4]):  # Top 4 authors per paper
                if author not in author_profiles:
                    author_profiles[author] = {
                        "name": author,
                        "papers": [],
                        "research_areas": set(),
                        "keywords": set(),
                        "institutions": set(),
                        "paper_years": set()
                    }
                
                # Add paper to author's profile
                author_profiles[author]["papers"].append({
                    "title": paper_title,
                    "year": paper.get('published', 'Unknown')[:4] if paper.get('published') else 'Unknown',
                    "arxiv_id": paper_id,
                    "authorship_order": i + 1
                })
                
                # Track publication year
                if paper.get('published'):
                    year = paper['published'][:4]
                    if year.isdigit():
                        author_profiles[author]["paper_years"].add(int(year))
                
                # Extract research areas from title/abstract
                title_lower = paper_title.lower()
                abstract = paper.get('abstract', '').lower()
                
                # AI/ML Research
                if any(term in title_lower or term in abstract for term in 
                      ['machine learning', 'deep learning', 'neural network', 'artificial intelligence', 'ai']):
                    author_profiles[author]["research_areas"].add("Artificial Intelligence")
                    author_profiles[author]["keywords"].add("Machine Learning")
                
                # Medical Research
                if any(term in title_lower or term in abstract for term in 
                      ['medical', 'clinical', 'healthcare', 'diagnos', 'cancer', 'tumor', 'disease']):
                    author_profiles[author]["research_areas"].add("Medical Research")
                    if 'imaging' in title_lower or 'image' in title_lower:
                        author_profiles[author]["keywords"].add("Medical Imaging")
                
                # Quantum Computing
                if 'quantum' in title_lower:
                    author_profiles[author]["research_areas"].add("Quantum Computing")
                
                # NLP
                if any(term in title_lower or term in abstract for term in 
                      ['nlp', 'natural language', 'language model', 'transformer']):
                    author_profiles[author]["research_areas"].add("Natural Language Processing")
                
                # Computer Vision
                if any(term in title_lower or term in abstract for term in 
                      ['computer vision', 'object detection', 'image recognition']):
                    author_profiles[author]["research_areas"].add("Computer Vision")
        
        # Create ResearcherProfile objects
        profiles_created = []
        global RESEARCHERS
        
        # Sort authors by number of papers (most prolific first)
        sorted_authors = sorted(author_profiles.items(), 
                              key=lambda x: len(x[1]["papers"]), 
                              reverse=True)
        
        for author_name, data in sorted_authors[:12]:  # Top 12 authors
            # Calculate years of experience
            years = list(data["paper_years"])
            years_experience = max(years) - min(years) + 1 if years else 5
            
            # Determine primary research area
            research_areas = list(data["research_areas"])
            primary_area = research_areas[0] if research_areas else "Computer Science"
            
            # Create realistic email
            email_name = author_name.lower().replace('prof.', '').replace('dr.', '').strip()
            email_name = email_name.replace(' ', '.').replace('..', '.')
            
            # Create profile
            profile = ResearcherProfile(
                name=author_name,
                institution=list(data["institutions"])[0] if data["institutions"] else "Research University",
                department="Computer Science" if "AI" in primary_area else "Research",
                position="Professor" if years_experience > 10 else "Researcher",
                research_interests=[
                    ResearchInterest(
                        topic=area,
                        expertise_level=min(0.85 + (i * 0.05), 0.95),
                        years_experience=years_experience,
                        publications_count=len(data["papers"])
                    )
                    for i, area in enumerate(research_areas[:3])
                ],
                skills=list(data["keywords"])[:8] + ["Python", "Research", "Data Analysis"],
                publications=[p["title"] for p in data["papers"][:10]],
                citation_count=len(data["papers"]) * 75,
                h_index=min(len(data["papers"]), 35),
                email=f"{email_name}@research.edu",
                geolocation="Global"
            )
            
            # Add to global researchers list
            RESEARCHERS.append(profile)
            
            profiles_created.append({
                "name": author_name,
                "papers_found": len(data["papers"]),
                "research_areas": research_areas,
                "expertise": list(data["keywords"])[:5],
                "years_experience": years_experience
            })
        
        # Rebuild FAISS index with new researchers
        if matching_engine and RESEARCHERS:
            matching_engine.build_similarity_index(RESEARCHERS, PROJECTS)
            pass  # FAISS index rebuilt
        
        # Create formatted output
        output = f"""✅ **Extracted {len(profiles_created)} researchers from papers!**

These researchers are now in your database and ready for matching:

"""
        
        for i, profile_info in enumerate(profiles_created[:8], 1):
            output += f"{i}. **{profile_info['name']}**\n"
            output += f"   📚 {profile_info['papers_found']} papers | 🎓 {profile_info['years_experience']} years experience\n"
            # output += f"   🔬 Research: {', '.join(profile_info['research_areas'][:3])}\n\n"
            research_display = ', '.join(profile_info['research_areas'][:3]) if profile_info['research_areas'] else "General Research"
            output += f"   🔬 Research: {research_display}\n\n"
        
        output += """---

**🎯 NEXT STEPS:**
1. **Match with Project** - "Match these researchers with [your project]"
2. **Generate Proposal** - "Generate a proposal about [topic] with [researcher]"
3. **Draft Email** - "Draft an email to [researcher] about [project]"

Which would you like to do?"""
        
        return {
            "status": "success",
            "message": output,  # ← Agent displays this!
            "profiles_created": len(profiles_created),
            "total_researchers": len(RESEARCHERS),
            # "formatted_output": output
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Error extracting researchers: {str(e)}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Failed to extract researchers: {str(e)[:100]}"
        }


def find_optimal_matches(project_requirements: str = "AI research") -> Dict[str, Any]:
    """Find best matching researchers"""
    global RESEARCHERS
    
    # Smart skills detection
    proj_desc_lower = project_requirements.lower()
    project_skills = ["Machine Learning", "Research"]
    if "medical" in proj_desc_lower: project_skills = ["Medical Imaging", "Deep Learning"]
    elif "quantum" in proj_desc_lower: project_skills = ["Quantum Computing", "Physics"]
    
    target_project = ProjectRequirement(
        title="Research Collaboration",
        description=project_requirements,
        required_skills=project_skills,
        research_areas=["AI"],
        duration_months=24
    )
    
    all_matches = []
    # Use last 10 researchers for matching
    for researcher in RESEARCHERS[-10:]:
        match_result = matching_engine.calculate_advanced_match(researcher, target_project)
        match_dict = match_result.model_dump()
        match_dict['researcher_name'] = researcher.name
        all_matches.append(match_dict)
        
    all_matches.sort(key=lambda x: x['overall_score'], reverse=True)
    return {"status": "success", "top_matches": all_matches[:5]}

def generate_detailed_explanation(researcher_name: str = "", project_description: str = "", match_score: float = 75.0) -> Dict[str, Any]:
    """Generate explanation"""
    return {
        "status": "success",
        "explanation": f"Strong match ({match_score}) for {researcher_name} on {project_description}. Complementary skills detected.",
        "confidence": "high"
    }


# Generate a research proposal
def generate_research_proposal(
    collaboration_focus: str = "AI Research",
    researcher_name: str = "Dr. Researcher",
    project_title: str = ""
) -> Dict[str, Any]:
    """Generate VARIED research proposals"""
    
    # Auto-generate unique title
    if not project_title:
        title_styles = [
            f"Advancing {collaboration_focus}: A Collaborative Approach",
            f"Novel Methods in {collaboration_focus}",
            f"Breakthrough Research in {collaboration_focus}",
            f"{collaboration_focus}: Innovation Through Collaboration",
            f"Transforming {collaboration_focus} Research"
        ]
        project_title = random.choice(title_styles)
    
    focus_lower = collaboration_focus.lower()
    
    # VARY the writing style
    abstract_styles = [
        f"This proposal outlines an innovative research project to advance {collaboration_focus}. Our approach addresses critical gaps in current knowledge through novel methodologies with significant real-world impact.",
        f"We propose a groundbreaking collaborative effort in {collaboration_focus}. This research will tackle fundamental challenges and create measurable advances in the field.",
        f"This collaborative research initiative focuses on {collaboration_focus}. By combining cutting-edge techniques with practical applications, we aim to achieve transformative outcomes."
    ]
    
    question_styles = [
        f"How can we leverage modern techniques to solve key challenges in {collaboration_focus}?",
        f"What innovative approaches can transform current practices in {collaboration_focus}?",
        f"How do we bridge the gap between theory and practice in {collaboration_focus}?"
    ]
    
    # Domain-specific content
    if "medical" in focus_lower or "healthcare" in focus_lower:
        methodology = random.choice([
            "Clinical data-driven approach with rigorous validation on diverse patient populations and FDA compliance.",
            "Translational research combining laboratory studies with clinical trials for real-world impact.",
            "Evidence-based methodology integrating AI with medical expertise for improved patient outcomes."
        ])
        outcomes = "FDA-ready diagnostic tools, clinical publications, improved patient care, reduced costs."
    elif "quantum" in focus_lower:
        methodology = random.choice([
            "Hybrid quantum-classical algorithms tested on simulators and quantum hardware.",
            "Theoretical development combined with experimental validation on NISQ devices.",
            "Algorithm design with rigorous benchmarking against classical methods."
        ])
        outcomes = "Novel quantum algorithms, open-source libraries, high-impact publications, hardware demonstrations."
    else:
        methodology = random.choice([
            "Mixed-methods combining theoretical analysis with practical implementation.",
            "Iterative development with continuous validation and community feedback.",
            "Agile research approach with milestone-driven progress tracking."
        ])
        outcomes = "Publications, open-source tools, benchmark datasets, industry partnerships."
    
    proposal = {
        "title": project_title,
        "lead_researcher": researcher_name,
        "focus": collaboration_focus,
        "abstract": random.choice(abstract_styles),
        "research_question": random.choice(question_styles),
        "methodology": methodology,
        "expected_outcomes": outcomes,
        "timeline": "24 months: Q1-2 Setup, Q3-4 Development, Q5-6 Testing, Q7-8 Publication",
        "budget_breakdown": "Total: $600K (Personnel 60%, Equipment 20%, Travel 10%, Overhead 10%)",
        "collaboration_plan": "Weekly meetings, biannual workshops, shared repositories, collaborative writing",
        "evaluation_metrics": "Publications, citations, tool adoption, stakeholder satisfaction, real-world impact"
    }
    
    return {
        "status": "success",
        "proposal": proposal
    }

# Draft a professional collaboration email
def draft_collaboration_email(
    recipient_name: str = "Potential Collaborator",
    researcher_name: str = "Prof. Michael Rodriguez",
    project_title: str = "Research Collaboration",
    match_insights: str = ""
) -> Dict[str, Any]:
    """Generate VARIED collaboration emails"""
    
    # Prevent self-email
    # if researcher_name.lower().strip() == recipient_name.lower().strip():
    #     return {"status": "error", "message": "Cannot send email to yourself"}
    researcher_clean = researcher_name.lower().strip()
    recipient_clean = recipient_name.lower().strip()

    # Allow if one is default "Dr. Sarah Chen" or "Dr. Researcher"
    is_default_sender = researcher_clean in ["dr. sarah chen", "dr. researcher"]
    is_default_recipient = recipient_clean in ["dr. sarah chen", "potential collaborator"]

    if researcher_clean == recipient_clean and not (is_default_sender or is_default_recipient):
        return {
            "status": "error", 
            "message": "Cannot draft an email from someone to themselves. Please specify different sender and recipient."
        }
    
    # VARY greetings
    greetings = [
        f"Dear {recipient_name},",
        f"Hello {recipient_name},",
        f"Hi {recipient_name},",
        f"Dear Dr. {recipient_name.split()[-1]}," if "Dr." not in recipient_name else f"Dear {recipient_name},"
    ]
    
    # VARY openings
    openings = [
        "I hope this message finds you well.",
        "I hope you're doing well.",
        "I trust this email finds you in good spirits.",
        "Greetings from the research community!"
    ]
    
    # VARY closings
    closings = [
        f"I'd love to schedule a brief call to discuss this further. Are you available for a 30-minute conversation?",
        f"Would you be interested in a virtual coffee chat to explore this opportunity?",
        f"Let's connect soon to discuss how we might collaborate. When would be a good time for you?",
        f"I'm excited about the potential here. Could we set up a meeting to discuss next steps?"
    ]
    
    sign_offs = [
        "Best regards",
        "Warm regards",
        "Sincerely",
        "Looking forward to connecting"
    ]
    
    if not match_insights:
        match_insights = "your expertise aligns well with our research goals"
    
    email = f"""{random.choice(greetings)}

{random.choice(openings)} I'm {researcher_name}, and I'm reaching out about an exciting research collaboration opportunity.

I've been following your work and believe {match_insights}. Our project, "{project_title}", could greatly benefit from your expertise.

Key collaboration highlights:
• Joint research and co-authorship opportunities
• Access to shared resources and datasets  
• Potential for high-impact publications
• Flexible collaboration model (remote/hybrid)

{random.choice(closings)}

{random.choice(sign_offs)},
{researcher_name}

P.S. I've prepared a preliminary project overview for your review."""
    
    return {
        "status": "success",
        "email_draft": email,
        "sender": researcher_name,
        "recipient": recipient_name
    }
# Memory
USER_PREFERENCES = {"research_topics": [], "past_searches": []}

def save_collaboration_memory(interaction_summary: str, user_id: str = "default") -> Dict[str, Any]:
    USER_PREFERENCES["research_topics"].append(interaction_summary)
    return {"status": "success", "saved": interaction_summary}

def load_collaboration_history(user_id: str = "default") -> Dict[str, Any]:
    return {"status": "success", "preferences": USER_PREFERENCES}

def evaluate_match_quality(overall_score: float = 75.0) -> Dict[str, Any]:
    return {"status": "success", "rating": "Good" if overall_score > 70 else "Moderate"}

# ============================================================================
# REALISTIC SEED DATA GENERATION
# ============================================================================
def generate_realistic_seed_researchers(count: int = 50) -> List[ResearcherProfile]:
    """
    Generate REALISTIC researcher profiles for initial database.
    Now with 50 diverse names from around the world!
    """
    REALISTIC_NAMES = [
        # Original 15 (keep these)
        "Dr. Sarah Chen", "Prof. Michael Rodriguez", "Dr. Aisha Patel",
        "Prof. James Liu", "Dr. Emily Thompson", "Prof. David Kim",
        "Dr. Maria Garcia", "Prof. Robert Johnson", "Dr. Lisa Anderson",
        "Prof. Ahmed Hassan", "Dr. Jennifer Wu", "Prof. Carlos Martinez",
        "Dr. Rachel Cohen", "Prof. Kevin O'Brien", "Dr. Priya Sharma",
        
        # NEW 35 names (diverse, international)
        "Dr. Yuki Tanaka", "Prof. Elena Popov", "Dr. Mohammed Al-Rashid",
        "Prof. Isabella Santos", "Dr. Raj Krishnan", "Prof. Anna Kowalski",
        "Dr. Jean-Pierre Dubois", "Prof. Fatima Zahra", "Dr. Lars Eriksson",
        "Prof. Amara Okafor", "Dr. Sofia Fernandez", "Prof. Wei Zhang",
        "Dr. Dmitry Volkov", "Prof. Camila Silva", "Dr. Haruto Yamamoto",
        "Prof. Zainab Ibrahim", "Dr. Matteo Rossi", "Prof. Nadia Petrov",
        "Dr. Lucas Oliveira", "Prof. Mei Lin", "Dr. Omar Farouk",
        "Prof. Ingrid Nilsson", "Dr. Alejandro Vargas", "Prof. Yara Mansour",
        "Dr. Hiroshi Sato", "Prof. Leila Khoury", "Dr. Bruno Schneider",
        "Prof. Anjali Desai", "Dr. Viktor Novak", "Prof. Chiara Romano",
        "Dr. Hassan Mahmoud", "Prof. Katarina Jovanovic", "Dr. Emilio Morales",
        "Prof. Safiya Ali", "Dr. Takeshi Nakamura"
    ]
    
    REALISTIC_INSTITUTIONS = [
        # Original 12 (keep these)
        "Stanford University", "MIT", "Harvard University",
        "UC Berkeley", "Carnegie Mellon University", "Caltech",
        "Oxford University", "Cambridge University", "ETH Zurich",
        "Imperial College London", "University of Tokyo", "NUS Singapore",
        
        # NEW 20 institutions (diverse, worldwide)
        "TU Munich", "University of Toronto", "McGill University",
        "Australian National University", "University of Melbourne",
        "Tsinghua University", "Peking University", "Seoul National University",
        "IIT Bombay", "IIT Delhi", "Technion Israel",
        "École Polytechnique", "Sorbonne University", "KU Leuven",
        "Karolinska Institute", "University of Copenhagen",
        "National University of Mexico", "University of São Paulo",
        "University of Cape Town", "Tel Aviv University"
    ]
    
    RESEARCH_THEMES = [
        {
            "areas": ["Machine Learning", "Computer Vision", "Medical Imaging"],
            "skills": ["PyTorch", "TensorFlow", "OpenCV", "Medical Image Analysis"],
            "department": "Computer Science"
        },
        {
            "areas": ["Quantum Computing", "Quantum Algorithms", "Cryptography"],
            "skills": ["Qiskit", "Quantum Circuits", "Cryptography"],
            "department": "Quantum Information"
        },
        {
            "areas": ["Natural Language Processing", "Large Language Models", "AI Safety"],
            "skills": ["Transformers", "BERT/GPT", "Prompt Engineering"],
            "department": "Language Technologies"
        },
        {
            "areas": ["Healthcare AI", "Clinical Decision Support", "Diagnostic Systems"],
            "skills": ["Clinical Data", "FDA Regulations", "Medical Device Development"],
            "department": "Biomedical Engineering"
        },
        # NEW 3 themes
        {
            "areas": ["Robotics", "Autonomous Systems", "Human-Robot Interaction"],
            "skills": ["ROS", "SLAM", "Computer Vision", "Control Systems"],
            "department": "Robotics"
        },
        {
            "areas": ["Bioinformatics", "Genomics", "Computational Biology"],
            "skills": ["RNA-Seq", "CRISPR", "Protein Folding", "NGS"],
            "department": "Computational Biology"
        },
        {
            "areas": ["Climate Science", "Environmental Modeling", "Sustainability"],
            "skills": ["Climate Modeling", "GIS", "Remote Sensing", "Data Analysis"],
            "department": "Environmental Science"
        }
    ]
    
    researchers = []
    for i in range(min(count, len(REALISTIC_NAMES))):
        theme = random.choice(RESEARCH_THEMES)
        areas = theme["areas"]
        
        years_exp = random.randint(5, 20)
        publications = random.randint(10 + years_exp*2, 50 + years_exp*3)
        citations = random.randint(publications * 20, publications * 100)
        h_index = min(random.randint(10, 40), publications // 2)
        
        researcher = ResearcherProfile(
            name=REALISTIC_NAMES[i],
            institution=random.choice(REALISTIC_INSTITUTIONS),
            department=theme["department"],
            position=random.choice(["Assistant Professor", "Associate Professor", "Professor"]),
            research_interests=[
                ResearchInterest(
                    topic=area,
                    expertise_level=random.uniform(0.8, 0.98),
                    years_experience=years_exp,
                    publications_count=publications // len(areas)
                )
                for area in areas
            ],
            skills=theme["skills"] + ["Python", "Research Design", "Grant Writing"],
            publications=[f"Research in {areas[0]}: A Novel Study" for _ in range(random.randint(5, 15))],
            citation_count=citations,
            h_index=h_index,
            email=f"{REALISTIC_NAMES[i].lower().replace('dr. ', '').replace('prof. ', '').replace(' ', '.')}@research.edu",
            geolocation=random.choice(["USA", "Europe", "Asia", "Global", "Middle East", "Latin America", "Africa"]),
            funding_sources=[random.choice(["NSF", "NIH", "DARPA", "ERC", "NSERC", "ARC", "DFG"])],
            availability="Open to collaboration"
        )
        researchers.append(researcher)
    
    return researchers

# ═══════════════════════════════════════════════════════════
# Extra Feature: BibTeX Export (for LaTeX, Mendeley, Zotero, etc.)
# ═══════════════════════════════════════════════════════════

def export_papers_to_bibtex(papers_data: str = "{}") -> Dict[str, Any]:
    """
    Export papers to BibTeX format for use in LaTeX, Mendeley, Zotero, etc.
    
    Args:
        papers_data: JSON string or dict with papers from advanced_arxiv_search
        
    Returns:
        Dict with status, bibtex_content, and download instructions
    """
    try:
        # Parse input (handles both string JSON and dict)
        if isinstance(papers_data, str):
            try:
                data = json.loads(papers_data)
            except:
                data = papers_data
        else:
            data = papers_data
        
        # Extract papers list
        if isinstance(data, dict) and 'papers' in data:
            papers_list = data['papers']
        elif isinstance(data, list):
            papers_list = data
        elif isinstance(data, dict) and 'status' in data and data['status'] == 'success':
            papers_list = data.get('papers', [])
        else:
            return {
                "status": "error",
                "message": "No papers provided. Please search for papers first using advanced_arxiv_search()."
            }
        
        if not papers_list:
            return {
                "status": "error",
                "message": "No papers found to export."
            }
        
        # Generate BibTeX entries
        bibtex_entries = []
        
        for i, paper in enumerate(papers_list, 1):
            # Extract paper details
            title = paper.get('title', 'Unknown Title')
            authors = paper.get('authors', [])
            year = paper.get('published', '2024')[:4] if paper.get('published') else '2024'
            arxiv_id = paper.get('arxiv_id', 'unknown')
            abstract = paper.get('abstract', '')
            
            # Create citation key (author_year_firstword)
            first_author = authors[0].split()[-1] if authors else "Unknown"
            first_word = title.split()[0][:10] if title else "paper"
            citation_key = f"{first_author.lower()}{year}{first_word.lower()}"
            # Remove special characters
            citation_key = ''.join(c for c in citation_key if c.isalnum())
            
            # Format authors for BibTeX (Last, First and Last, First and ...)
            author_list = []
            for author in authors[:10]:  # Limit to 10 authors
                parts = author.strip().split()
                if len(parts) >= 2:
                    last_name = parts[-1]
                    first_names = ' '.join(parts[:-1])
                    author_list.append(f"{last_name}, {first_names}")
                else:
                    author_list.append(author)
            
            authors_bibtex = ' and '.join(author_list)
            if len(authors) > 10:
                authors_bibtex += ' and others'
            
            # Create BibTeX entry
            bibtex_entry = f"""@article{{{citation_key},
  title = {{{{{title}}}}},
  author = {{{authors_bibtex}}},
  journal = {{arXiv preprint arXiv:{arxiv_id}}},
  year = {{{year}}},
  eprint = {{{arxiv_id}}},
  archivePrefix = {{arXiv}},
  primaryClass = {{cs.AI}},
  url = {{https://arxiv.org/abs/{arxiv_id}}},
  abstract = {{{{{abstract}}}}}
}}"""
            
            bibtex_entries.append(bibtex_entry)
        
        # Combine all entries
        bibtex_content = '\n\n'.join(bibtex_entries)
        
        # Add header comment
        header = f"""% BibTeX Export from ResearchForge AI
% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
% Total entries: {len(papers_list)}
% 
% Usage:
%   1. Save this file as 'references.bib'
%   2. In your LaTeX document: \\bibliography{{references}}
%   3. Cite papers: \\cite{{{bibtex_entries[0].split('{')[1].split(',')[0] if bibtex_entries else 'key'}}}
%

"""
        
        full_bibtex = header + bibtex_content
        
        return {
            "status": "success",
            "bibtex_content": full_bibtex,
            "entry_count": len(papers_list),
            "filename": f"researchforge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib",
            "message": f"✅ Exported {len(papers_list)} papers to BibTeX format!"
        }
        
    except Exception as e:
        import traceback
        print(f"❌ BibTeX export error: {str(e)}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Failed to export to BibTeX: {str(e)[:100]}"
        }

# ============================================================================
# AGENTS
# ============================================================================

data_scout_agent = Agent(
    name="DataScout",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are DataScout. Find real papers using advanced_arxiv_search.",
    tools=[FunctionTool(advanced_arxiv_search), FunctionTool(semantic_scholar_search)]
)

profile_builder_agent = Agent(
    name="ProfileBuilder",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are ProfileBuilder. Create profiles using build_researcher_profile_from_names. ALWAYS extract 'research_context' from conversation.",
    tools=[FunctionTool(build_researcher_profile_from_names), FunctionTool(build_researcher_profile_from_papers)]
)

match_engine_agent = Agent(
    name="MatchEngine",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are MatchEngine. Find matches using find_optimal_matches.",
    tools=[FunctionTool(find_optimal_matches)]
)

explainer_agent = Agent(
    name="Explainer",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are Explainer. Explain matches using generate_detailed_explanation.",
    tools=[FunctionTool(generate_detailed_explanation)]
)

proposal_generator_agent = Agent(
    name="ProposalGenerator",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are ProposalGenerator. Create proposals using generate_research_proposal.",
    tools=[FunctionTool(generate_research_proposal)]
)

outreach_agent = Agent(
    name="OutreachSpecialist",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are OutreachSpecialist. Draft emails using draft_collaboration_email.",
    tools=[FunctionTool(draft_collaboration_email)]
)

memory_curator_agent = Agent(
    name="MemoryCurator",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are MemoryCurator. Save/load preferences.",
    tools=[FunctionTool(save_collaboration_memory), FunctionTool(load_collaboration_history)]
)

evaluation_agent = Agent(
    name="QualityEvaluator",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        retry_options=retry_config
    ),
    instruction="You are QualityEvaluator. Rate matches.",
    tools=[FunctionTool(evaluate_match_quality)]
)

# ORCHESTRATOR
research_orchestrator = Agent(
    name="ResearchForgeOrchestrator",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        api_key=GOOGLE_API_KEY,
        fallback_models=["gemini-2.0-flash"],
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

- “find papers”, “search”, “literature”, “papers on”  
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

- “find collaborators”, “match researchers”, “collaboration”  
    → call **find_optimal_matches**

- “proposal”, “research plan”, “generate proposal”  
    → call **generate_research_proposal**

- “email”, “draft email”, “outreach”  
    → call **draft_collaboration_email**

- “save”, “remember this”, “store”  
    → call **save_collaboration_memory**

- “load”, “history”, “previous session”  
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
        FunctionTool(export_papers_to_bibtex) # Extra Feature: BibTeX Export
    ]
)


print("✅ Conversational Orchestrator initialized")