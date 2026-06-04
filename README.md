# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through either a local Ollama server or Anthropic Claude. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Either:
  - Ollama installed and running locally with `qwen2.5:7b`, or
  - An Anthropic account and valid API key for Claude models

## Setup

### Step 1: Choose your model backend

#### Option A: Local Ollama (`qwen2.5:7b`)

1. Install Ollama from https://ollama.com.
2. Pull the `qwen2.5:7b` model:

```bash
ollama pull qwen2.5:7b
```

3. Start the Ollama server:

```bash
ollama serve
```

4. Configure `.env`:

```bash
CLAUDE_MODEL="qwen2.5:7b"
```

> Local Ollama does not require Anthropic credits or an API key.

#### Option B: Anthropic Claude

1. Sign up for Anthropic and obtain an API key.
2. Configure `.env`:

```bash
CLAUDE_MODEL="claude-3.5"
ANTHROPIC_API_KEY="your-anthropic-api-key"
```

> Use an Anthropic Claude model alias such as `claude-3.5` or `claude-3.5-mini`.

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Linting and Typing Check

There are no lint or type checks implemented.
