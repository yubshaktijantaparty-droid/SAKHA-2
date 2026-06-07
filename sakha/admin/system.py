"""
Admin System for SAKHA Bot
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from sakha.config import settings
from sakha.utils import logger


class AdminRole(str, Enum):
    """Admin Roles"""
    OWNER = "owner"
    MODERATOR = "moderator"
    SUPPORT = "support"


class AdminPermission(str, Enum):
    """Admin Permissions"""
    # User management
    BAN_USER = "ban_user"
    UNBAN_USER = "unban_user"
    KICK_USER = "kick_user"
    MUTE_USER = "mute_user"
    
    # Content moderation
    DELETE_MESSAGE = "delete_message"
    EDIT_MESSAGE = "edit_message"
    CLEAR_CHAT = "clear_chat"
    
    # Bot management
    BROADCAST = "broadcast"
    RESTART_BOT = "restart_bot"
    CHANGE_SETTINGS = "change_settings"
    VIEW_ANALYTICS = "view_analytics"
    VIEW_LOGS = "view_logs"
    
    # Group management
    CREATE_GROUP = "create_group"
    DELETE_GROUP = "delete_group"
    MANAGE_GROUP = "manage_group"


class AdminSystem:
    """Admin System Manager"""
    
    # Role-based permissions
    ROLE_PERMISSIONS = {
        AdminRole.OWNER: [perm.value for perm in AdminPermission],
        AdminRole.MODERATOR: [
            AdminPermission.BAN_USER.value,
            AdminPermission.UNBAN_USER.value,
            AdminPermission.DELETE_MESSAGE.value,
            AdminPermission.EDIT_MESSAGE.value,
            AdminPermission.CLEAR_CHAT.value,
            AdminPermission.VIEW_ANALYTICS.value,
        ],
        AdminRole.SUPPORT: [
            AdminPermission.VIEW_ANALYTICS.value,
            AdminPermission.VIEW_LOGS.value,
        ]
    }
    
    def __init__(self):
        self.owner_id = settings.bot_owner_id
        self.admins: Dict[str, AdminRole] = {self.owner_id: AdminRole.OWNER}
    
    def is_owner(self, user_id: str) -> bool:
        """Check if user is bot owner"""
        return user_id == self.owner_id
    
    def is_admin(self, user_id: str) -> bool:
        """Check if user is admin"""
        return user_id in self.admins
    
    def get_admin_role(self, user_id: str) -> Optional[AdminRole]:
        """Get admin role"""
        return self.admins.get(user_id)
    
    def has_permission(self, user_id: str, permission: AdminPermission) -> bool:
        """Check if user has permission"""
        if not self.is_admin(user_id):
            return False
        
        role = self.admins[user_id]
        return permission.value in self.ROLE_PERMISSIONS.get(role, [])
    
    async def add_admin(self, user_id: str, role: AdminRole, added_by: str) -> bool:
        """Add admin"""
        if not self.has_permission(added_by, AdminPermission.CHANGE_SETTINGS):
            logger.warning(f"{added_by} attempted to add admin without permission")
            return False
        
        self.admins[user_id] = role
        logger.info(f"Added {user_id} as {role}")
        return True
    
    async def remove_admin(self, user_id: str, removed_by: str) -> bool:
        """Remove admin"""
        if not self.has_permission(removed_by, AdminPermission.CHANGE_SETTINGS):
            return False
        
        if user_id == self.owner_id:
            logger.warning("Cannot remove owner")
            return False
        
        if user_id in self.admins:
            del self.admins[user_id]
            logger.info(f"Removed {user_id} from admins")
            return True
        
        return False
    
    async def ban_user(self, user_id: str, banned_by: str, reason: str = "") -> bool:
        """Ban user"""
        if not self.has_permission(banned_by, AdminPermission.BAN_USER):
            return False
        
        logger.info(f"Banned {user_id} by {banned_by}. Reason: {reason}")
        return True
    
    async def unban_user(self, user_id: str, unbanned_by: str) -> bool:
        """Unban user"""
        if not self.has_permission(unbanned_by, AdminPermission.UNBAN_USER):
            return False
        
        logger.info(f"Unbanned {user_id} by {unbanned_by}")
        return True
    
    async def send_broadcast(self, message: str, sent_by: str) -> bool:
        """Send broadcast message"""
        if not self.has_permission(sent_by, AdminPermission.BROADCAST):
            return False
        
        logger.info(f"Broadcast sent by {sent_by}: {message[:100]}...")
        return True
    
    async def view_analytics(self, requested_by: str) -> Optional[Dict[str, Any]]:
        """View analytics"""
        if not self.has_permission(requested_by, AdminPermission.VIEW_ANALYTICS):
            return None
        
        analytics = {
            "total_users": 0,
            "active_users": 0,
            "total_messages": 0,
            "total_commands": 0,
            "avg_response_time": 0,
            "error_count": 0
        }
        
        logger.info(f"Analytics requested by {requested_by}")
        return analytics
    
    async def view_logs(self, requested_by: str, limit: int = 100) -> List[str]:
        """View logs"""
        if not self.has_permission(requested_by, AdminPermission.VIEW_LOGS):
            return []
        
        # Would fetch actual logs in production
        logger.info(f"Logs requested by {requested_by}")
        return []
    
    async def restart_bot(self, requested_by: str) -> bool:
        """Restart bot"""
        if not self.has_permission(requested_by, AdminPermission.RESTART_BOT):
            return False
        
        logger.info(f"Restart requested by {requested_by}")
        return True
    
    async def change_setting(self, setting: str, value: Any, changed_by: str) -> bool:
        """Change bot setting"""
        if not self.has_permission(changed_by, AdminPermission.CHANGE_SETTINGS):
            return False
        
        logger.info(f"Setting '{setting}' changed by {changed_by}: {value}")
        return True


class AdminCommandHandler:
    """Admin Command Handler"""
    
    def __init__(self, admin_system: AdminSystem):
        self.admin_system = admin_system
    
    async def handle_admin_command(self, user_id: str, command: str, args: str) -> str:
        """Handle admin command"""
        
        if command == "admin":
            return self.show_admin_menu(user_id)
        
        elif command == "broadcast":
            success = await self.admin_system.send_broadcast(args, user_id)
            return "📢 Broadcast sent!" if success else "❌ Broadcast failed"
        
        elif command == "ban":
            # Parse: .ban [user_id] [reason]
            parts = args.split(maxsplit=1)
            if len(parts) < 1:
                return "Usage: .ban [user_id] [reason]"
            
            target_user = parts[0]
            reason = parts[1] if len(parts) > 1 else ""
            
            success = await self.admin_system.ban_user(target_user, user_id, reason)
            return f"✅ User {target_user} banned" if success else "❌ Failed to ban user"
        
        elif command == "unban":
            target_user = args.strip()
            success = await self.admin_system.unban_user(target_user, user_id)
            return f"✅ User {target_user} unbanned" if success else "❌ Failed to unban user"
        
        elif command == "stats":
            analytics = await self.admin_system.view_analytics(user_id)
            if not analytics:
                return "❌ Permission denied"
            
            return f"""
📊 **BOT STATISTICS**

👥 Total Users: {analytics['total_users']}
✅ Active Users: {analytics['active_users']}
💬 Total Messages: {analytics['total_messages']}
⌨️ Total Commands: {analytics['total_commands']}
⚡ Avg Response: {analytics['avg_response_time']}ms
❌ Errors: {analytics['error_count']}
"""
        
        elif command == "restart":
            success = await self.admin_system.restart_bot(user_id)
            return "✅ Bot restart initiated" if success else "❌ Permission denied"
        
        elif command == "logs":
            logs = await self.admin_system.view_logs(user_id, 50)
            if logs is None:
                return "❌ Permission denied"
            return "📋 Last 50 logs:\n" + "\n".join(logs[:10])
        
        elif command == "settings":
            return self.show_settings_menu(user_id)
        
        else:
            return "❌ Unknown admin command"
    
    def show_admin_menu(self, user_id: str) -> str:
        """Show admin menu"""
        role = self.admin_system.get_admin_role(user_id)
        
        if not role:
            return "❌ Not authorized"
        
        menu = f"""
⚙️ **ADMIN PANEL** ({role.value.upper()})

1️⃣ .broadcast [message] - Send broadcast
2️⃣ .ban [user_id] [reason] - Ban user
3️⃣ .unban [user_id] - Unban user
4️⃣ .stats - View statistics
5️⃣ .logs - View logs
6️⃣ .restart - Restart bot
7️⃣ .settings - Bot settings
"""
        return menu
    
    def show_settings_menu(self, user_id: str) -> str:
        """Show settings menu"""
        if not self.admin_system.is_admin(user_id):
            return "❌ Not authorized"
        
        return """
⚙️ **BOT SETTINGS**

Current Settings:
• Debug Mode: OFF
• Auto Moderation: ON
• Anti-Spam: ON
• Max Messages/min: 10
• Response Timeout: 30s

Format: .settings [setting] [value]
Example: .settings max_messages 20
"""


# Global admin system
admin_system = AdminSystem()
admin_command_handler = AdminCommandHandler(admin_system)
