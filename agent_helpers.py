# ============================================================================
# ENHANCEMENT FEATURES: Caching, Retry, Suggestions, Export
# ============================================================================

import hashlib
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
import json
import pandas as pd
import os
import requests
from typing import Dict, Any, List


class SearchCache:
    """Simple cache for API calls to improve performance"""
    def __init__(self):
        self.cache = {}
    
    def get_key(self, query: str, source: str) -> str:
        """Generate cache key from query and source"""
        return hashlib.md5(f"{query}_{source}".encode()).hexdigest()
    
    def get(self, query: str, source: str, max_age_minutes: int = 60):
        """Get cached result if fresh enough"""
        key = self.get_key(query, source)
        if key in self.cache:
            result, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(minutes=max_age_minutes):
                return result
        return None
    
    def set(self, query: str, source: str, result):
        """Cache a result with timestamp"""
        key = self.get_key(query, source)
        self.cache[key] = (result, datetime.now())


# Initialize global cache
search_cache = SearchCache()


def suggest_better_queries(original_query: str) -> List[str]:
    """
    Suggest improved search queries based on domain detection
    
    Args:
        original_query: User's original search query
        
    Returns:
        List of suggested alternative queries
    """
    suggestions = []
    query_lower = original_query.lower()
    
    # Medical/health domain suggestions
    if any(term in query_lower for term in ['medical', 'health', 'cancer', 'disease', 'clinical']):
        suggestions.append(f"{original_query} deep learning")
        suggestions.append(f"{original_query} machine learning")
        suggestions.append(f"{original_query} AI diagnosis")
    
    # Computer vision suggestions
    if any(term in query_lower for term in ['detection', 'classification', 'segmentation', 'imaging']):
        suggestions.append(f"{original_query} transformer")
        suggestions.append(f"{original_query} CNN")
        suggestions.append(f"{original_query} neural network")
    
    # NLP domain suggestions
    if any(term in query_lower for term in ['language', 'text', 'nlp', 'translation']):
        suggestions.append(f"{original_query} BERT")
        suggestions.append(f"{original_query} GPT")
        suggestions.append(f"{original_query} attention mechanism")
    
    return suggestions[:5]


def download_pdf(arxiv_id: str, save_path: str = None) -> Dict[str, Any]:
    """
    Download PDF for an arXiv paper
    
    Args:
        arxiv_id: arXiv paper ID (e.g., "2301.12345")
        save_path: Optional path to save PDF
        
    Returns:
        Dictionary with download status and file info
    """
    try:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        response = requests.get(pdf_url, stream=True, timeout=30)
        response.raise_for_status()
        
        if save_path is None:
            save_path = f"{arxiv_id}.pdf"
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return {
            "status": "success",
            "arxiv_id": arxiv_id,
            "file_path": save_path,
            "file_size": os.path.getsize(save_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to download PDF: {str(e)}",
            "arxiv_id": arxiv_id
        }


def export_results(results: Dict[str, Any], format: str = "json") -> Dict[str, Any]:
    """
    Export search results in various formats
    
    Args:
        results: Search results dictionary
        format: Export format ('json', 'csv', 'bibtex')
        
    Returns:
        Dictionary with exported content
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == "json":
            return {
                "status": "success",
                "format": "json",
                "content": json.dumps(results, indent=2),
                "filename": f"research_results_{timestamp}.json"
            }
        
        elif format == "csv":
            papers = results.get('papers', [])
            if papers:
                df = pd.DataFrame(papers)
                csv_content = df.to_csv(index=False)
                return {
                    "status": "success",
                    "format": "csv",
                    "content": csv_content,
                    "filename": f"research_results_{timestamp}.csv"
                }
            else:
                return {"status": "error", "message": "No papers to export"}
        
        elif format == "bibtex":
            bibtex = ""
            for paper in results.get('papers', []):
                arxiv_id = paper.get('arxiv_id', 'unknown').replace('v', '_v')
                title = paper.get('title', '')
                authors = ' and '.join(paper.get('authors', []))
                year = paper.get('published', '').split('-')[0] if paper.get('published') else 'N/A'
                
                bibtex += f"""@article{{{arxiv_id},
  title={{{title}}},
  author={{{authors}}},
  year={{{year}}},
  url={{{paper.get('pdf_url', '')}}}
}}

"""
            return {
                "status": "success",
                "format": "bibtex",
                "content": bibtex,
                "filename": f"research_results_{timestamp}.bib"
            }
        
        else:
            return {"status": "error", "message": f"Unsupported format: {format}"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}
