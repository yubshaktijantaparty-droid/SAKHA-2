"""Export Service for SAKHA AI Premium"""

from typing import List, Dict, Optional
from datetime import datetime
import json

class ExportService:
    """Service for exporting chats in various formats"""
    
    async def export_as_markdown(self, chat: Dict, include_metadata: bool = True) -> str:
        """Export chat as Markdown"""
        md = ""
        
        if include_metadata:
            md += f"# {chat.get('title', 'Chat')}\n\n"
            md += f"**Date**: {chat.get('created_at', '')}\n"
            md += f"**Model**: {chat.get('model', 'Unknown')}\n\n"
            md += "---\n\n"
        
        for message in chat.get("messages", []):
            role = message.get("role", "").upper()
            content = message.get("content", "")
            md += f"## {role}\n\n{content}\n\n"
        
        return md
    
    async def export_as_txt(self, chat: Dict, include_metadata: bool = True) -> str:
        """Export chat as plain text"""
        txt = ""
        
        if include_metadata:
            txt += f"{'=' * 50}\n"
            txt += f"{chat.get('title', 'Chat')}\n"
            txt += f"{'=' * 50}\n\n"
            txt += f"Date: {chat.get('created_at', '')}\n"
            txt += f"Model: {chat.get('model', 'Unknown')}\n\n"
            txt += f"{'-' * 50}\n\n"
        
        for message in chat.get("messages", []):
            role = message.get("role", "").upper()
            content = message.get("content", "")
            txt += f"[{role}]\n{content}\n\n"
        
        return txt
    
    async def export_as_pdf(self, chat: Dict, include_metadata: bool = True) -> Optional[bytes]:
        """Export chat as PDF"""
        try:
            # Would require reportlab or similar
            # For now, return None
            return None
        except Exception as e:
            return None
    
    async def export_as_json(self, chat: Dict) -> str:
        """Export chat as JSON"""
        return json.dumps(chat, indent=2, default=str)
