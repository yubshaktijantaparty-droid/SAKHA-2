    def _get_demo_response(self, message: str) -> str:
        """Return a demo response when API keys are not configured"""
        # Simple echo with AI-like response
        responses = {
            "hi": "Hello! I'm SakhaAI, your premium AI assistant. How can I help you today?",
            "hello": "Hi there! Welcome to SakhaAI. What would you like to chat about?",
            "how are you": "I'm doing great! Thanks for asking. I'm here and ready to help with whatever you need.",
            "thanks": "You're welcome! Feel free to ask me anything.",
            "bye": "Goodbye! Thanks for using SakhaAI. See you next time!",
        }
        
        # Check for exact matches (case-insensitive)
        lower_msg = message.lower().strip()
        if lower_msg in responses:
            return responses[lower_msg]
        
        # Default response
        return f"Thanks for your message: '{message}'. I'm currently running in demo mode. To enable full AI capabilities, please configure API keys for OpenAI, Google Gemini, DeepSeek, or other providers. How else can I assist you?"
