# SAKHA Bot - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints use header authentication. Admin endpoints require admin verification.

---

## Endpoints

### 1. Get Bot Info
```http
GET /
```
**Response:**
```json
{
    "name": "SAKHA",
    "owner": "Pranab Goswami",
    "status": "🟢 Online",
    "version": "1.0.0"
}
```

### 2. Health Check
```http
GET /health
```
**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-10T15:30:00Z",
    "bot_name": "SAKHA"
}
```

### 3. Send Message
```http
POST /api/message
Content-Type: application/json

{
    "user_id": "919999999999",
    "message": ".ai How to solve physics problems?",
    "context": {
        "subject": "physics"
    }
}
```

**Response:**
```json
{
    "status": "success",
    "response": "Here are 5 steps to solve physics problems..."
}
```

### 4. Get User Profile
```http
GET /api/users/{user_id}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "_id": "919999999999",
        "name": "John Doe",
        "phone_number": "+919999999999",
        "language": "en",
        "is_banned": false,
        "total_messages": 150,
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

### 5. Send Broadcast (Admin)
```http
POST /api/broadcast
Content-Type: application/json

{
    "admin_id": "919999999999",
    "message": "🎉 New features available! Check .menu for details"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Broadcast sent"
}
```

### 6. Get Statistics (Admin)
```http
POST /api/stats
Content-Type: application/json

{
    "admin_id": "919999999999"
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "total_users": 150,
        "active_users": 45,
        "total_messages": 2500,
        "total_commands": 500,
        "avg_response_time": 1.2,
        "error_count": 5,
        "command_stats": {
            "ai": 200,
            "study": 100,
            "notes": 80
        }
    }
}
```

### 7. WhatsApp Webhook
```http
POST /webhook/whatsapp
Content-Type: application/json

{
    "from": "919999999999",
    "body": ".ai Hello",
    "type": "text"
}
```

**Response:**
```json
{
    "status": "received"
}
```

---

## Command Examples

### AI Chat
```
User: .ai How does photosynthesis work?
Bot: Photosynthesis is a process... [detailed explanation]
```

### Study Mode
```
User: .study
Bot: 📚 STUDY ASSISTANT

1️⃣ NEET Preparation
2️⃣ MCQ Practice
...
```

### Create Note
```
User: .notes add Physics Formulas
Bot: ✅ Note 'Physics Formulas' created!
```

### Set Reminder
```
User: .reminder 5pm Study session
Bot: ✅ Reminder set!
⏰ You'll be notified on time.
```

### Get Statistics (Admin)
```
Admin: .stats
Bot: 📊 BOT STATISTICS

👥 Total Users: 150
✅ Active Users: 45
💬 Total Messages: 2500
...
```

---

## Error Responses

### Bad Request
```json
{
    "status": "error",
    "detail": "Missing required fields"
}
```

### Unauthorized
```json
{
    "status": "error",
    "detail": "Not authorized"
}
```

### Not Found
```json
{
    "status": "error",
    "detail": "User not found"
}
```

### Internal Server Error
```json
{
    "status": "error",
    "detail": "Internal server error"
}
```

---

## Rate Limiting

- **Default:** 100 requests per 3600 seconds (1 hour) per user
- **Webhook:** 100 requests per second
- Headers returned:
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Reset time (Unix timestamp)

---

## Data Types

### User ID
Format: WhatsApp phone number
Example: `919999999999`

### Message Types
- `text` - Plain text message
- `image` - Image with caption
- `document` - Document file
- `audio` - Audio message
- `video` - Video message

### Languages
- `en` - English
- `bn` - Bengali
- `hi` - Hindi
- `hinglish` - English + Hindi mixed

### Priority Levels
- `low` - Low priority
- `medium` - Medium priority (default)
- `high` - High priority

---

## Pagination

Supported endpoints: `/api/users/{user_id}/conversations`

```
?page=1&limit=20
```

---

## Webhooks

### WhatsApp Incoming Message
Triggered when a message is received:

```json
POST /webhook/whatsapp

{
    "from": "919999999999",
    "body": "Message text",
    "type": "text",
    "timestamp": "2024-01-10T15:30:00Z",
    "media_url": null
}
```

---

## Testing

### Using curl
```bash
# Test health
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -d '{"user_id": "919999999999", "message": ".ai Hello"}'
```

### Using Python
```python
import requests

# Get user profile
response = requests.get('http://localhost:8000/api/users/919999999999')
print(response.json())

# Send message
response = requests.post('http://localhost:8000/api/message', json={
    'user_id': '919999999999',
    'message': '.ai Hello'
})
print(response.json())
```

### Using JavaScript
```javascript
// Send message
fetch('http://localhost:8000/api/message', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        user_id: '919999999999',
        message: '.ai Hello'
    })
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## API Versioning

Current version: `v1` (default)

Future versions will be available at:
```
/api/v2/...
```

---

## Support

For API issues or questions, contact: support@example.com
