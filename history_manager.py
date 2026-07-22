"""
History Manager - Handles calculation history persistence
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

class HistoryManager:
    """Manages calculation history with JSON persistence"""
    
    def __init__(self, filename: str = "data/history.json"):
        self.filename = filename
        self.history: List[Dict] = []
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.load_history()
    
    def add_entry(self, operation: str, expression: str, 
                  result: str, category: str = "basic") -> None:
        """Add a new calculation to history"""
        entry = {
            "id": self._generate_id(expression + str(datetime.now())),
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "expression": expression,
            "result": str(result),
            "category": category
        }
        self.history.append(entry)
        
        # Keep only last 500 entries to prevent file bloat
        if len(self.history) > 500:
            self.history = self.history[-500:]
        
        self.save_history()
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve history entries, optionally limited"""
        if limit:
            return self.history[-limit:]
        return self.history
    
    def clear_history(self) -> None:
        """Clear all history"""
        self.history = []
        self.save_history()
    
    def search_history(self, query: str) -> List[Dict]:
        """Search history by query string"""
        query_lower = query.lower()
        return [entry for entry in self.history 
                if query_lower in str(entry).lower()]
    
    def export_history(self, filename: str) -> bool:
        """Export history to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.history, f, indent=2)
            return True
        except Exception:
            return False
    
    def import_history(self, filename: str) -> bool:
        """Import history from a JSON file"""
        try:
            with open(filename, 'r') as f:
                imported = json.load(f)
                self.history.extend(imported)
                self.save_history()
            return True
        except Exception:
            return False
    
    def load_history(self) -> None:
        """Load history from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.history = []
    
    def save_history(self) -> None:
        """Save history to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def _generate_id(self, data: str) -> str:
        """Generate unique ID for history entry"""
        return hashlib.md5(data.encode()).hexdigest()[:8]
