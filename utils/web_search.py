# Web search utility module
import requests
import json
from typing import List, Dict, Any
import os
from config.config import TAVILY_API_KEY

class TavilySearch:
    """Tavily API integration for web search functionality."""
    
    def __init__(self, api_key: str = None):
        """Initialize Tavily search with API key."""
        self.api_key = api_key or TAVILY_API_KEY
        if self.api_key == "your_tavily_api_key_here":
            raise ValueError("Please set your Tavily API key in config/config.py")
        self.base_url = "https://api.tavily.com"
    
    def search(self, query: str, max_results: int = 10, include_images: bool = False) -> List[Dict[str, Any]]:
        """
        Perform a web search using Tavily API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            include_images: Whether to include image URLs in results
            
        Returns:
            List of search results with title, url, content, etc.
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "include_images": include_images,
            "max_results": max_results,
            "include_answer": True,
            "include_raw_content": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("results", [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error performing search: {e}")
            return []
    
    def get_trending_skincare_info(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get trending skincare products, routines, and hacks for 2024.
        
        Returns:
            Dictionary with categorized trending information
        """
        trending_data = {
            "products": [],
            "routines": [],
            "hacks": [],
            "ingredients": []
        }
        
        # Search for trending skincare products 2024
        products_query = "trending skincare products 2024 viral social media"
        products_results = self.search(products_query, max_results=8, include_images=False)
        trending_data["products"] = products_results
        
        # Search for trending skincare routines 2024
        routines_query = "trending skincare routines 2024 K-beauty glass skin"
        routines_results = self.search(routines_query, max_results=8, include_images=False)
        trending_data["routines"] = routines_results
        
        # Search for skincare hacks and tips 2024
        hacks_query = "skincare hacks 2024 viral beauty tips TikTok Instagram"
        hacks_results = self.search(hacks_query, max_results=8, include_images=False)
        trending_data["hacks"] = hacks_results
        
        # Search for trending skincare ingredients 2024
        ingredients_query = "trending skincare ingredients 2024 niacinamide retinol vitamin C"
        ingredients_results = self.search(ingredients_query, max_results=6, include_images=False)
        trending_data["ingredients"] = ingredients_results
        
        return trending_data
    
    def format_trending_results(self, trending_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Format trending skincare data into a readable markdown string.
        
        Args:
            trending_data: Dictionary with categorized trending information
            
        Returns:
            Formatted markdown string
        """
        formatted_output = "# 🔥 Trending Skincare 2024\n\n"
        
        # Products section
        formatted_output += "## 📦 Trending Products\n\n"
        for i, product in enumerate(trending_data["products"][:5], 1):
            title = product.get("title", "No title")
            content = product.get("content", "No description available")[:150] + "..."
            url = product.get("url", "")
            image_url = product.get("image", "")
            formatted_output += f"**{i}. {title}**\n{content}\n[Read more]({url})\n\n"
        
        # Routines section
        formatted_output += "## 🧖‍♀️ Viral Skincare Routines\n\n"
        for i, routine in enumerate(trending_data["routines"][:5], 1):
            title = routine.get("title", "No title")
            content = routine.get("content", "No description available")[:150] + "..."
            url = routine.get("url", "")
            image_url = routine.get("image", "")
            formatted_output += f"**{i}. {title}**\n{content}\n[Read more]({url})\n\n"
        
        # Hacks section
        formatted_output += "## 💡 Skincare Hacks & Tips\n\n"
        for i, hack in enumerate(trending_data["hacks"][:5], 1):
            title = hack.get("title", "No title")
            content = hack.get("content", "No description available")[:150] + "..."
            url = hack.get("url", "")
            image_url = hack.get("image", "")
            formatted_output += f"**{i}. {title}**\n{content}\n[Read more]({url})\n\n"
        
        # Ingredients section
        formatted_output += "## 🧪 Trending Ingredients\n\n"
        for i, ingredient in enumerate(trending_data["ingredients"][:4], 1):
            title = ingredient.get("title", "No title")
            content = ingredient.get("content", "No description available")[:120] + "..."
            url = ingredient.get("url", "")
            image_url = ingredient.get("image", "")
            formatted_output += f"**{i}. {title}**\n{content}\n[Read more]({url})\n\n"
        
        return formatted_output

# Convenience functions for direct usage
def get_trending_skincare_markdown() -> str:
    """
    Get formatted markdown of trending skincare information.
    
    Returns:
        Markdown formatted string with trending skincare data
    """
    try:
        tavily = TavilySearch()
        trending_data = tavily.get_trending_skincare_info()
        return tavily.format_trending_results(trending_data)
    except ValueError as e:
        return f"⚠️ {str(e)}\n\nPlease set up your Tavily API key in config/config.py to access trending skincare information."
    except Exception as e:
        return f"❌ Error fetching trending information: {str(e)}"

def search_skincare(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for specific skincare information.
    
    Args:
        query: Search query
        max_results: Maximum results to return
        
    Returns:
        List of search results
    """
    try:
        tavily = TavilySearch()
        return tavily.search(query, max_results)
    except ValueError:
        return []
    except Exception:
        return []