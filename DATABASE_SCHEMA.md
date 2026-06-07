"""
Database Schemas and Examples
"""

# =====================
# MongoDB Collections
# =====================

# USERS Collection
users_schema = {
    "_id": "919999999999",  # WhatsApp phone number
    "name": "John Doe",
    "phone_number": "+919999999999",
    "language": "en",  # en, bn, hi, hinglish
    "is_banned": False,
    "ban_reason": None,
    "ban_until": None,
    "total_messages": 150,
    "total_commands": 25,
    "created_at": "2024-01-01T00:00:00Z",
    "last_seen": "2024-01-10T15:30:00Z",
    "preferences": {
        "study_level": "neet",
        "subjects": ["physics", "chemistry", "biology"],
        "notifications_enabled": True
    }
}

# CONVERSATIONS Collection
conversations_schema = {
    "_id": "conv_12345",
    "user_id": "919999999999",
    "message_text": "How to solve physics problems?",
    "response_text": "Here are 5 steps to solve physics problems...",
    "command_used": ".ai",
    "context": {
        "topic": "physics",
        "difficulty": "intermediate"
    },
    "created_at": "2024-01-10T15:30:00Z",
    "is_pinned": False
}

# NOTES Collection
notes_schema = {
    "_id": "note_12345",
    "user_id": "919999999999",
    "title": "NEET Physics Formulas",
    "content": "F = ma\nE = mc^2\n...",
    "category": "study",  # general, study, work, personal
    "is_archived": False,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-10T15:30:00Z"
}

# REMINDERS Collection
reminders_schema = {
    "_id": "rem_12345",
    "user_id": "919999999999",
    "title": "Physics Study Session",
    "description": "Study chapter 5 - Mechanics",
    "scheduled_time": "2024-01-15T18:00:00Z",
    "is_completed": False,
    "is_recurring": True,
    "recurrence_pattern": "daily",  # daily, weekly, monthly
    "created_at": "2024-01-01T00:00:00Z"
}

# TODOS Collection
todos_schema = {
    "_id": "todo_12345",
    "user_id": "919999999999",
    "title": "Complete Physics Assignment",
    "description": "Chapter 5 - 20 questions",
    "priority": "high",  # low, medium, high
    "is_completed": False,
    "due_date": "2024-01-15T18:00:00Z",
    "category": "study",
    "created_at": "2024-01-01T00:00:00Z"
}

# ADMIN_LOGS Collection
admin_logs_schema = {
    "_id": "log_12345",
    "admin_id": "919999999999",
    "action": "ban_user",  # ban_user, unban_user, broadcast, etc.
    "target_user_id": "918888888888",
    "details": {
        "reason": "Spam",
        "duration": 86400
    },
    "timestamp": "2024-01-10T15:30:00Z"
}

# ANALYTICS Collection
analytics_schema = {
    "_id": "analytics_2024_01_10",
    "date": "2024-01-10T00:00:00Z",
    "total_users": 150,
    "active_users": 45,
    "total_messages": 2500,
    "total_commands": 500,
    "avg_response_time": 1.2,  # seconds
    "error_count": 5,
    "command_stats": {
        "ai": 200,
        "study": 100,
        "notes": 80,
        "todo": 60,
        "reminder": 40,
        "other": 20
    }
}

# =====================
# PostgreSQL Tables
# =====================

# users table
"""
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    phone_number VARCHAR(20) UNIQUE,
    language VARCHAR(10) DEFAULT 'en',
    is_banned BOOLEAN DEFAULT FALSE,
    ban_reason VARCHAR(500),
    ban_until TIMESTAMP,
    total_messages INTEGER DEFAULT 0,
    total_commands INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preferences JSONB DEFAULT '{}'
);
"""

# conversations table
"""
CREATE TABLE conversations (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    message_text TEXT,
    response_text TEXT,
    command_used VARCHAR(100),
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_pinned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# notes table
"""
CREATE TABLE notes (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    content TEXT,
    category VARCHAR(50) DEFAULT 'general',
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# reminders table
"""
CREATE TABLE reminders (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    description TEXT,
    scheduled_time TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# todos table
"""
CREATE TABLE todos (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    is_completed BOOLEAN DEFAULT FALSE,
    due_date TIMESTAMP,
    category VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# admin_logs table
"""
CREATE TABLE admin_logs (
    id VARCHAR(50) PRIMARY KEY,
    admin_id VARCHAR(50),
    action VARCHAR(100),
    target_user_id VARCHAR(50),
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# analytics table
"""
CREATE TABLE analytics (
    id VARCHAR(50) PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_users INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    total_messages INTEGER DEFAULT 0,
    total_commands INTEGER DEFAULT 0,
    avg_response_time FLOAT DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    command_stats JSONB DEFAULT '{}'
);
"""
