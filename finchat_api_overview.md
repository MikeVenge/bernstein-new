# Finchat API Overview

Based on studying the **xinobi-ir-api** repository, here's how Finchat works:

## Architecture Overview

The system is a Django REST API that integrates with **Finchat** (a financial chat service) to provide an AI-powered Investor Relations chatbot.

### Key Components

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────┐
│   Client    │ ───> │  Django API  │ ───> │   Finchat   │ ───> │ Consomme │
│  (Frontend) │      │   (Xinobi)   │      │     API     │      │  (Docs)  │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────┘
                            │
                            ↓
                     ┌──────────────┐
                     │  L2M2 (LLM)  │
                     │   OpenAI     │
                     └──────────────┘
```

---

## Core Services

### 1. **Finchat Service** (`utils/finchat.py`)

Primary interface to Finchat API using `adgolibs.finchat.FinchatClient`:

```python
finchat = FinchatClient(
    base_url=settings.FINCHAT_URL,  # https://finchat-api.adgo.dev
    api_token=settings.FINCHAT_API_TOKEN,
    debug=False,
    timeout=300,
)
```

**Key Functions:**

- **`create_finchat_session()`**
  - Creates a new Finchat session for a user
  - Attaches all company documents to the session
  - Waits until the session is ready (documents processed)
  - Returns session data with `remote_id`

- **`send_finchat_message(session_id, message)`**
  - Sends a user message to a Finchat session
  - Waits for the AI response
  - Returns both the chat and response objects

### 2. **Consomme Service** (`utils/consomme.py`)

Document management system that Finchat uses as its knowledge base:

```python
client = ConsommeClient(
    base_url=settings.CONSOMME_API_URL,
    auth_token=settings.CONSOMME_API_TOKEN,
    app_name="xinobi_ir",
    timeout=300,
)
```

- **Purpose**: Uploads and stores documents (PDFs, reports, etc.)
- **Returns**: `remote_id` for each uploaded document
- Finchat queries these documents when answering questions

### 3. **L2M2 / OpenAI Service** (`utils/prompt_manager.py`)

Post-processing LLM layer using OpenAI-compatible API:

```python
client = OpenAI(
    base_url=settings.L2M2_API_URL,
    api_key=settings.L2M2_API_KEY,
)
```

**PromptManager Features:**
- Model: `gemini-2.5-pro` (default)
- Temperature: 0.2
- Max tokens: 1,048,576
- Automatic message trimming to stay within token limits
- Retry logic with exponential backoff

---

## Three-Stage Response Pipeline

When a user asks a question, the system processes it through **3 stages**:

### Stage 1: Data Retrieval (Finchat)
```python
# Send query to Finchat
_, finchat_response = send_finchat_message(
    finchat_session_id=session.remote_id,
    message=user_message
)
```

**Purpose**: Extract **raw, factual information** from documents
- Uses `DATA_RETRIEVAL_PROMPT` system prompt
- Returns plain factual data without interpretation
- Only uses information from uploaded documents

### Stage 2: Personality (L2M2)
```python
# Apply company personality/tone
pm = PromptManager(...)
pm.add_message(role="system", content=PERSONALITY_PROMPT)
pm.add_message(role="user", content=finchat_response["content"])
response = pm.generate()
```

**Purpose**: Transform data into **Nexie's voice**
- Rewrites facts in the company's brand voice
- Professional, warm, visionary tone
- Speaks as "we" (representing XinobiAI)

### Stage 3: Guardrails (L2M2)
```python
# Apply compliance and legal checks
pm = PromptManager(...)
pm.add_message(role="system", content=GUARDRAILS_PROMPT)
pm.add_message(role="user", content=response)
final_response = pm.generate()
```

**Purpose**: Ensure **compliance and safety**
- Validates only public information is shared
- Blocks investment advice, speculation, MNPI
- Adds required disclaimers
- Enforces IR standards for Japanese companies

---

## API Endpoints

### Authentication
All endpoints require authentication via Token:
```
Authorization: token <API_TOKEN>
```

### Main Endpoints

#### 1. **Create Chat Session**
```http
POST /api/v1/chat-sessions/
```

**What happens:**
1. Creates Finchat session with supplemental system prompt
2. Uploads all documents from database to the session
3. Waits for documents to be indexed
4. Creates welcome message from Nexie
5. Returns session UID

**Response:**
```json
{
  "id": "uuid",
  "created_on": "2024-01-01T00:00:00Z",
  "remote_id": "finchat_session_id"
}
```

#### 2. **Send Message**
```http
POST /api/v1/messages/
Content-Type: application/json

{
  "chat_session": "session_uuid",
  "content": "What was the revenue in Q2 2024?"
}
```

**What happens:**
1. Validates user owns the session
2. Sends message to Finchat (Stage 1)
3. Applies personality layer (Stage 2)
4. Applies guardrails (Stage 3)
5. Saves both user message and AI response
6. Returns the user message (response appears via list endpoint)

**Response:**
```json
{
  "id": "message_uuid",
  "chat_session": "session_uuid",
  "role": "user",
  "content": "What was the revenue in Q2 2024?",
  "created_on": "2024-01-01T00:00:00Z"
}
```

#### 3. **List Messages**
```http
GET /api/v1/messages/?chat_session=<session_uuid>
```

Returns all messages (both user and assistant) in chronological order.

#### 4. **Upload Document**
```http
POST /api/v1/documents/
Content-Type: multipart/form-data

{
  "title": "Q2 2024 Earnings Report",
  "file": <file_upload>,
  "document_type": "earnings_report"
}
```

**What happens:**
1. Uploads file to Consomme
2. Stores document metadata with `remote_id`
3. Document becomes available to all future chat sessions

---

## Data Models

### ChatSession
```python
class ChatSession(BaseModel):
    remote_id = CharField()  # Finchat session ID
    actor = ForeignKey(User)  # Session owner
```

### Message
```python
class Message(BaseModel):
    chat_session = ForeignKey(ChatSession)
    role = CharField()  # "user" or "assistant"
    content = TextField()
    remote_id = CharField()  # Finchat chat ID
    actor = ForeignKey(User)
```

### Document
```python
class Document(BaseModel):
    title = CharField()
    remote_id = CharField()  # Consomme document ID
    file = FileField()
    document_type = CharField()  # e.g., "earnings_report"
```

---

## Key Features

### 1. **Multi-Tenant Security**
- Each user can only access their own chat sessions
- Admin users can see all sessions
- Session validation prevents cross-user access

### 2. **Document Management**
- Documents uploaded once, available to all sessions
- Organized into Document Groups
- Stored in Consomme, referenced by Finchat

### 3. **Configurable Prompts**
- All system prompts stored in `AppSetting` model
- Can be updated via admin panel without code changes
- Three configurable prompts:
  - `DATA_RETRIEVAL_PROMPT`
  - `PERSONALITY_PROMPT`
  - `GUARDRAILS_PROMPT`

### 4. **Error Handling**
- Automatic retries with exponential backoff
- Graceful fallbacks for Finchat failures
- Transaction management for message creation

---

## Environment Configuration

Required environment variables:

```bash
# Finchat API
FINCHAT_URL=https://finchat-api.adgo.dev
FINCHAT_API_TOKEN=<your_token>

# Consomme (Document Storage)
CONSOMME_API_URL=<url>
CONSOMME_API_TOKEN=<token>

# L2M2 (LLM Processing)
L2M2_API_URL=<url>
L2M2_API_KEY=<key>
```

---

## Usage Flow Example

```python
# 1. User creates a session
session = create_chat_session(
    client_id="xinobi_user123",
    supplemental_prompt="You are an IR assistant..."
)

# 2. Documents are automatically attached
# (All documents in DB are sent to Finchat)

# 3. User sends a message
chat, response = send_finchat_message(
    finchat_session_id=session["id"],
    message="What was Q2 revenue?"
)

# 4. Response is processed through 3 stages:
#    - Finchat extracts data from documents
#    - Personality layer adds company voice
#    - Guardrails ensure compliance

# 5. Final response is returned to user
```

---

## Key Integrations

### adgolibs
External library providing:
- `FinchatClient` - Main Finchat API client
- `ConsommeClient` - Document management client
- Custom exceptions and utilities

### OpenAI SDK
Used for L2M2 integration:
- Compatible with OpenAI API format
- Uses `responses.create()` endpoint
- Supports custom context and caching

---

## Testing

The codebase includes comprehensive tests:
- Authentication and permissions
- Message CRUD operations
- Session creation and management
- Document uploads
- Error handling scenarios

Run tests with:
```bash
python manage.py test
```

---

## Summary

**Finchat** is a financial document Q&A service that:

1. **Indexes documents** via Consomme
2. **Answers questions** by querying indexed documents
3. **Returns factual data** that can be post-processed
4. **Maintains sessions** for conversation context
5. **Supports metadata** for custom behavior

The Xinobi IR API wraps Finchat with:
- User authentication and multi-tenancy
- Post-processing pipeline (personality + guardrails)
- Document management
- RESTful API interface

This architecture separates concerns:
- **Finchat**: Document retrieval & factual answers
- **L2M2**: Tone, personality, compliance
- **Django API**: User management, orchestration, persistence

