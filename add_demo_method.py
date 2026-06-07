#!/usr/bin/env python3
"""Add demo method to AI service"""

demo_code = '''
    def _get_demo_response(self, message: str) -> str:
        """Return a demo response when API keys are not configured"""
        responses = {
            "hi": "Hello! I'm SakhaAI, your premium AI assistant. How can I help you today?",
            "hello": "Hi there! Welcome to SakhaAI. What would you like to chat about?",
            "how are you": "I'm doing great! Thanks for asking. I'm ready to help with whatever you need.",
            "thanks": "You're welcome! Feel free to ask me anything.",
            "bye": "Goodbye! Thanks for using SakhaAI. See you soon!",
        }
        
        lower_msg = message.lower().strip()
        if lower_msg in responses:
            return responses[lower_msg]
        
        return f"Thanks for your message: '{message}'. I'm currently in demo mode. To use real AI, configure API keys (OpenAI, Gemini, DeepSeek, etc)."
'''

with open("backend/sakha/services/ai_service.py", "a") as f:
    f.write(demo_code)

print("✅ Demo method added successfully!")
