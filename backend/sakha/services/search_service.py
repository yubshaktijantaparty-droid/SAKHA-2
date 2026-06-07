"""Search Service for SAKHA AI Premium"""

import aiohttp
import json
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """Service for web search integration"""
    
    def __init__(self, tavily_api_key: Optional[str] = None, perplexity_api_key: Optional[str] = None):
        self.tavily_api_key = tavily_api_key
        self.perplexity_api_key = perplexity_api_key
    
    async def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Perform web search"""
        try:
            if self.tavily_api_key:
                return await self._tavily_search(query, num_results)
            elif self.perplexity_api_key:
                return await self._perplexity_search(query)
            else:
                return []
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def _tavily_search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search using Tavily API"""
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            data = {
                "api_key": self.tavily_api_key,
                "query": query,
                "max_results": num_results,
                "include_answer": True
            }
            
            async with session.post(
                "https://api.tavily.com/search",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("results", [])
                return []
    
    async def _perplexity_search(self, query: str) -> List[Dict]:
        """Search using Perplexity API"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "sonar-online",
                "messages": [{"role": "user", "content": query}]
            }
            
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return [{
                        "title": "Search Result",
                        "content": result["choices"][0]["message"]["content"]
                    }]
                return []
