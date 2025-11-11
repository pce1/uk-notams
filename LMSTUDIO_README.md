# LM Studio Chat Application

A simple interactive chat interface for local LLM models via LM Studio.

## Prerequisites

1. **LM Studio** must be installed and running
2. A model must be loaded in LM Studio
3. The local server should be running on `http://127.0.0.1:1234`

## Installation

Install the required Python package:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the chat application:

```bash
python lmstudiochat.py
```

Or if made executable:

```bash
./lmstudiochat.py
```

### Custom Server URL

If your LM Studio is running on a different address:

```bash
python lmstudiochat.py http://localhost:1234
```

## Features

- **Interactive Chat**: Have a conversation with your local LLM
- **Conversation History**: Maintains context throughout the session
- **Built-in Commands**:
  - `/clear` - Clear conversation history
  - `/history` - Show full conversation history
  - `/quit` - Exit the application
  - `/help` - Display help message

## Configuration

The application uses these default settings:
- **Temperature**: 0.7 (controls randomness)
- **Max Tokens**: 2000 (maximum response length)
- **Endpoint**: `/v1/chat/completions`

## LM Studio Setup

1. Open LM Studio
2. Download and load a model (e.g., Mistral, Llama, etc.)
3. Go to the "Local Server" tab
4. Click "Start Server"
5. Ensure it's running on port 1234 (default)

## Example Session

```
============================================================
LM Studio Chat Interface
============================================================
Connecting to: http://127.0.0.1:1234/v1/chat/completions
✓ Connected to LM Studio

Commands:
  /clear  - Clear conversation history
  /history - Show conversation history
  /quit   - Exit the chat
  /help   - Show this help message

Type your message and press Enter to chat.

============================================================

You: Hello! Can you help me understand NOTAMs?