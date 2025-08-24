# 🔥 Web Search Integration Guide

## Overview
This guide explains how to use the new Tavily API integration for discovering trending skincare products, routines, and hacks.

## 🚀 Quick Setup

### 1. Get Your Tavily API Key
1. Visit [tavily.com](https://tavily.com)
2. Sign up for a free account
3. Copy your API key from the dashboard

### 2. Configure Your API Key
Update `config/config.py`:
```python
TAVILY_API_KEY = "your_actual_api_key_here"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 📱 Usage Examples

### Using the Streamlit Interface
1. Run the application: `streamlit run app.py`
2. Navigate to the "Trending Skincare" page
3. Click "Refresh Trending Data" to see latest trends
4. Use "Custom Search" for specific queries

### Using the API Directly

```python
from utils.web_search import TavilySearch, get_trending_skincare_markdown

# Get trending information
trending_markdown = get_trending_skincare_markdown()
print(trending_markdown)

# Custom search
search_results = TavilySearch().search("best vitamin C serums", max_results=5)
for result in search_results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content'][:100]}...")
    print("-" * 50)
```

## 🎯 Features Available

### Trending Categories
- **Products**: Viral skincare products from social media
- **Routines**: Popular K-beauty and glass skin routines
- **Hacks**: TikTok and Instagram viral tips
- **Ingredients**: Trending skincare ingredients

### Search Parameters
- `query`: Your search string
- `max_results`: 1-10 results (default: 5)
- `include_images`: Include image URLs (default: False)

## 🔍 Sample Queries

### Trending Searches
- "trending skincare products 2024"
- "viral skincare hacks TikTok"
- "K-beauty glass skin routine"
- "best niacinamide serums"

### Custom Searches
- "retinol for beginners guide"
- "sunscreen for oily skin"
- "skincare routine for acne"
- "vitamin C vs niacinamide"

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `TAVILY_API_KEY` is set in `config/config.py`
   - Verify the key is active on tavily.com

2. **No Results**
   - Try different search terms
   - Check internet connection
   - Verify API key permissions

3. **Rate Limits**
   - Tavily free tier has 1000 requests/month
   - Consider upgrading if needed

### Error Handling
The API includes comprehensive error handling:
- Invalid API key detection
- Network timeout protection
- Graceful fallback for missing data

## 📊 Data Sources
The integration searches across:
- Beauty blogs and magazines
- Social media platforms (TikTok, Instagram)
- Skincare expert websites
- Product review sites
- Dermatologist recommendations

## 🔄 Updates
- Data is fetched in real-time from web sources
- No local caching (fresh results every time)
- Updates reflect current social media trends

## 📞 Support
For issues with the Tavily API, visit:
- [Tavily Documentation](https://docs.tavily.com)
- [Tavily Discord](https://discord.gg/tavily)
- [GitHub Issues](https://github.com/tavily-ai/tavily-python)