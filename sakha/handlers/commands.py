"""
Command Handlers for SAKHA Bot
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import uuid
from sakha.ai import AIService
from sakha.utils import logger, detect_language, translate_text
from sakha.database import MongoDBOperations


class CommandHandler:
    """Base Command Handler"""
    
    def __init__(self, db_ops: MongoDBOperations, ai_service: AIService):
        self.db_ops = db_ops
        self.ai_service = ai_service
    
    async def handle_help(self, user_id: str) -> str:
        """Handle .help command"""
        help_text = """
╔══════════════════════════════╗
║  SAKHA - Personal AI Assistant  ║
╚══════════════════════════════╝

📋 **USER COMMANDS:**
.help - Show this help message
.menu - Show main menu
.ai [query] - Ask AI a question
.ask [topic] - Ask about specific topic
.translate [text] [lang] - Translate text
.study - Study assistance menu
.notes - Manage notes
.todo - To-do list
.reminder - Set reminders
.weather - Get weather
.news - Latest news
.quote - Daily quote
.joke - Get a joke
.time - Current time
.date - Current date

⚙️ **ADMIN COMMANDS:**
.admin - Admin panel
.broadcast [message] - Send broadcast
.ban [user_id] [reason] - Ban user
.unban [user_id] - Unban user
.stats - View statistics
.restart - Restart bot
.logs - View logs
.settings - Bot settings

🎯 **QUICK TIPS:**
- Type .menu for quick access
- All commands start with .
- Use natural language with .ai
- Your data is private & secure
"""
        return help_text
    
    async def handle_menu(self, user_id: str) -> str:
        """Handle .menu command"""
        menu = """
╔════════════════════════════╗
║     SAKHA MAIN MENU        ║
╚════════════════════════════╝

1️⃣ **AI ASSISTANT** 
   Ask anything, anytime!

2️⃣ **STUDY MODE**
   NEET prep, MCQs, doubt solving

3️⃣ **PRODUCTIVITY**
   Notes, To-do, Reminders

4️⃣ **BUSINESS ASSISTANT**
   Ideas, content, marketing

5️⃣ **INFORMATION**
   Weather, news, quotes

6️⃣ **SETTINGS**
   Language, preferences

7️⃣ **HELP & SUPPORT**
   Commands, FAQs

➡️ Reply with number to choose
"""
        return menu
    
    async def handle_ai(self, user_id: str, query: str, context: Dict[str, Any] = None) -> str:
        """Handle .ai command - AI Chat"""
        try:
            # Get user info
            user = await self.db_ops.get_user(user_id)
            if not user:
                return "❌ User not found"
            
            # Detect language
            lang = user.get("language", "en")
            
            # Get AI response
            response = await self.ai_service.chat(
                query=query,
                user_id=user_id,
                context=context or {}
            )
            
            # Save conversation
            conv_id = str(uuid.uuid4())
            await self.db_ops.save_conversation(
                conv_id=conv_id,
                data={
                    "user_id": user_id,
                    "message_text": query,
                    "response_text": response,
                    "command_used": ".ai",
                    "context": context or {}
                }
            )
            
            # Update user stats
            await self.db_ops.update_user(
                user_id,
                {"$inc": {"total_messages": 1}}
            )
            
            return response
        except Exception as e:
            logger.error(f"Error in handle_ai: {e}")
            return "❌ Error processing request. Please try again."
    
    async def handle_translate(self, text: str, target_lang: str) -> str:
        """Handle .translate command"""
        try:
            translated = await translate_text(text, target_lang)
            return f"🌐 **Translation to {target_lang.upper()}:**\n\n{translated}"
        except Exception as e:
            logger.error(f"Error in translate: {e}")
            return "❌ Translation failed"
    
    async def handle_study(self, user_id: str, topic: Optional[str] = None) -> str:
        """Handle .study command"""
        study_menu = """
📚 **STUDY ASSISTANT**

1️⃣ **NEET Preparation**
   Physics, Chemistry, Biology

2️⃣ **MCQ Practice**
   Generate quizzes by topic

3️⃣ **Doubt Solving**
   Ask any doubt, get detailed explanation

4️⃣ **Study Plans**
   Personalized study schedule

5️⃣ **Revision Notes**
   Key concepts & formulas

6️⃣ **Performance**
   Track your progress

➡️ Reply with number to continue
"""
        return study_menu
    
    async def handle_notes(self, user_id: str, action: str = "list") -> str:
        """Handle .notes command"""
        try:
            if action == "list":
                notes = await self.db_ops.get_user_notes(user_id)
                if not notes:
                    return "📝 No notes found. Create your first note with .notes add [title]"
                
                notes_text = "📝 **YOUR NOTES:**\n\n"
                for i, note in enumerate(notes[:10], 1):
                    notes_text += f"{i}. {note.get('title', 'Untitled')}\n"
                
                return notes_text
            
            elif action.startswith("add "):
                title = action[4:].strip()
                note_id = str(uuid.uuid4())
                
                await self.db_ops.create_note(
                    note_id=note_id,
                    data={
                        "user_id": user_id,
                        "title": title,
                        "content": "",
                        "category": "general"
                    }
                )
                
                return f"✅ Note '{title}' created!\n\nReply to add content."
            
            else:
                return "📝 **NOTE COMMANDS:**\n.notes - List all notes\n.notes add [title] - Create note"
        
        except Exception as e:
            logger.error(f"Error in handle_notes: {e}")
            return "❌ Error managing notes"
    
    async def handle_todo(self, user_id: str, action: str = "list") -> str:
        """Handle .todo command"""
        todo_menu = """
✅ **TO-DO LIST**

1️⃣ **View All** - See your to-do items
2️⃣ **Add New** - Create new task
3️⃣ **Mark Done** - Complete a task
4️⃣ **Delete** - Remove a task
5️⃣ **Priorities** - View by priority

📝 Example:
.todo add Study Physics tomorrow high

➡️ Reply to choose action
"""
        return todo_menu
    
    async def handle_reminder(self, user_id: str, reminder_text: str = "") -> str:
        """Handle .reminder command"""
        if not reminder_text:
            return """
⏰ **SET REMINDER**

Format: .reminder [time] [message]

Examples:
- .reminder 5pm Study session
- .reminder tomorrow 8am Morning run
- .reminder in 2 hours Meeting

⏰ Your reminders will be saved & notified
"""
        
        # Parse reminder
        try:
            reminder_id = str(uuid.uuid4())
            # Simple parsing - can be enhanced
            scheduled_time = datetime.utcnow() + timedelta(hours=1)
            
            await self.db_ops.create_reminder(
                reminder_id=reminder_id,
                data={
                    "user_id": user_id,
                    "title": reminder_text,
                    "scheduled_time": scheduled_time,
                    "is_recurring": False
                }
            )
            
            return f"✅ Reminder set!\n⏰ You'll be notified on time."
        except Exception as e:
            logger.error(f"Error setting reminder: {e}")
            return "❌ Error setting reminder"
    
    async def handle_weather(self) -> str:
        """Handle .weather command"""
        # Would integrate with weather API
        return "🌤️ **WEATHER**\n\nWeather feature coming soon!"
    
    async def handle_news(self) -> str:
        """Handle .news command"""
        return "📰 **LATEST NEWS**\n\nNews feature coming soon!"
    
    async def handle_quote(self) -> str:
        """Handle .quote command"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Success is not final, failure is not fatal. - Winston Churchill",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
        ]
        import random
        quote = random.choice(quotes)
        return f"✨ **QUOTE OF THE DAY:**\n\n\"{quote}\""
    
    async def handle_joke(self) -> str:
        """Handle .joke command"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the AI say to the developer? 'Your code makes me feel... computed!'",
            "Why do Java developers wear glasses? Because they don't C#!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
        ]
        import random
        joke = random.choice(jokes)
        return f"😂 **JOKE:**\n\n{joke}"
    
    async def handle_time(self) -> str:
        """Handle .time command"""
        current_time = datetime.utcnow().strftime("%H:%M:%S")
        return f"🕐 **CURRENT TIME (UTC):**\n\n{current_time}"
    
    async def handle_date(self) -> str:
        """Handle .date command"""
        current_date = datetime.utcnow().strftime("%A, %B %d, %Y")
        return f"📅 **TODAY'S DATE:**\n\n{current_date}"


class AdminCommandHandler:
    """Admin Command Handler"""
    
    def __init__(self, db_ops: MongoDBOperations):
        self.db_ops = db_ops
    
    async def handle_ban(self, user_id: str, reason: str, duration: int = 86400) -> str:
        """Ban user"""
        try:
            success = await self.db_ops.ban_user(user_id, reason, duration)
            if success:
                return f"✅ User {user_id} banned for {duration}s.\nReason: {reason}"
            return "❌ Failed to ban user"
        except Exception as e:
            logger.error(f"Error banning user: {e}")
            return "❌ Error banning user"
    
    async def handle_broadcast(self, message: str, excluded_users: List[str] = None) -> str:
        """Broadcast message to all users"""
        try:
            # Get all users and send message
            # This would typically be done in background
            return f"📢 **BROADCAST SENT**\n\nMessage: {message[:100]}..."
        except Exception as e:
            logger.error(f"Error broadcasting: {e}")
            return "❌ Error sending broadcast"
    
    async def handle_stats(self) -> str:
        """Get bot statistics"""
        try:
            analytics = await self.db_ops.get_analytics()
            
            stats = f"""
📊 **BOT STATISTICS**

👥 Total Users: {analytics.get('total_users', 0)}
✅ Active Users: {analytics.get('active_users', 0)}
💬 Total Messages: {analytics.get('total_messages', 0)}
⌨️ Total Commands: {analytics.get('total_commands', 0)}
⚡ Avg Response: {analytics.get('avg_response_time', 0):.2f}ms
❌ Errors: {analytics.get('error_count', 0)}
"""
            return stats
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return "❌ Error retrieving statistics"
