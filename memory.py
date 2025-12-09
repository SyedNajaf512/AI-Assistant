"""
Anna AI Assistant - Memory Management
Handles conversation history, context, and learned information
"""

from datetime import datetime
from config import config
import json


class Memory:
    """Manages Anna's memory and context"""
    
    def __init__(self):
        self.session_context = {}
        self.current_conversation = []
    
    def add_exchange(self, user_input, anna_response, action_taken=None):
        """Add a conversation exchange to memory"""
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "anna": anna_response,
            "action": action_taken
        }
        self.current_conversation.append(exchange)
        
        # Also save to persistent storage
        config.add_to_history(user_input, anna_response)
    
    def get_recent_context(self, count=5):
        """Get recent conversation for context"""
        return self.current_conversation[-count:] if self.current_conversation else []
    
    def get_persistent_history(self, count=10):
        """Get persistent conversation history"""
        return config.get_history(count)
    
    def remember(self, key, value):
        """Remember a piece of information"""
        self.session_context[key] = value
        config.update_context(key, value)
    
    def recall(self, key, default=None):
        """Recall a piece of information"""
        # Check session first, then persistent
        if key in self.session_context:
            return self.session_context[key]
        return config.get_context(key, default)
    
    def forget_session(self):
        """Clear session context (keeps persistent memory)"""
        self.session_context = {}
        self.current_conversation = []
    
    def add_document(self, doc_data):
        """Add a document to memory"""
        try:
            filename = doc_data.get("filename")
            config.save_document(filename, doc_data)
            return True
        except Exception as e:
            return False
    
    def get_document(self, filename):
        """Get a document by filename"""
        return config.get_document(filename)
    
    def list_documents(self):
        """List all stored documents"""
        return config.list_all_documents()
    
    def search_documents(self, query):
        """Search for documents containing query"""
        results = []
        all_docs = config.list_all_documents()
        
        for doc_name in all_docs:
            doc = config.get_document(doc_name)
            if doc:
                content = doc.get("content", "")
                summary = doc.get("summary", "")
                
                # Simple search in content and summary
                if query.lower() in content.lower() or query.lower() in summary.lower():
                    results.append({
                        "filename": doc_name,
                        "summary": summary
                    })
        
        return results
    
    def build_context_string(self):
        """Build context string for AI prompt"""
        context_parts = []
        
        # Recent conversation
        recent = self.get_recent_context(3)
        if recent:
            context_parts.append("Recent conversation:")
            for exchange in recent:
                context_parts.append(f"User: {exchange['user']}")
                context_parts.append(f"Anna: {exchange['anna']}")
        
        # Session context
        if self.session_context:
            context_parts.append("\nCurrent session context:")
            for key, value in self.session_context.items():
                context_parts.append(f"{key}: {value}")
        
        # Document knowledge
        docs = self.list_documents()
        if docs:
            context_parts.append(f"\nKnown documents ({len(docs)}):")
            for doc_name in docs[:5]:  # Show max 5
                doc = self.get_document(doc_name)
                if doc:
                    context_parts.append(f"- {doc_name}: {doc.get('summary', 'No summary')[:100]}")
        
        return "\n".join(context_parts) if context_parts else ""


# Global memory instance
memory = Memory()
