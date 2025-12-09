"""
Anna AI Assistant - Web Handler
Handles web searches, URL opening, and browser control
"""

import webbrowser
from urllib.parse import quote
from logger import logger


class WebHandler:
    """Manages web-related operations"""
    
    def __init__(self):
        self.search_engines = {
            "google": "https://www.google.com/search?q=",
            "youtube": "https://www.youtube.com/results?search_query=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
        }
    
    def open_url(self, url):
        """Open URL in default browser"""
        try:
            # Add https:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            logger.log_action("open_url", url, True)
            return {"success": True, "message": f"Opening {url}"}
            
        except Exception as e:
            logger.log_error("OPEN_URL", str(e), url)
            return {"success": False, "message": f"Error opening URL: {str(e)}"}
    
    def web_search(self, query, engine="google"):
        """Perform web search"""
        try:
            engine = engine.lower()
            if engine not in self.search_engines:
                engine = "google"
            
            search_url = self.search_engines[engine] + quote(query)
            webbrowser.open(search_url)
            
            logger.log_action("web_search", f"{engine}: {query}", True)
            return {"success": True, "message": f"Searching {engine} for '{query}'"}
            
        except Exception as e:
            logger.log_error("WEB_SEARCH", str(e), query)
            return {"success": False, "message": f"Error searching: {str(e)}"}
    
    def google_search(self, query):
        """Google search shortcut"""
        return self.web_search(query, "google")
    
    def youtube_search(self, query):
        """YouTube search shortcut"""
        return self.web_search(query, "youtube")
    
    def open_youtube(self, video_query=None):
        """Open YouTube, optionally with search"""
        if video_query:
            return self.youtube_search(video_query)
        else:
            return self.open_url("https://www.youtube.com")
    
    def open_gmail(self):
        """Open Gmail"""
        return self.open_url("https://mail.google.com")
    
    def open_github(self):
        """Open GitHub"""
        return self.open_url("https://github.com")


# Global web handler instance
web_handler = WebHandler()
