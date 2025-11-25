# Use Free Local Ollama Models in VS Code (Alongside GitHub Copilot Chat)

This quick tutorial shows how to install lightweight Ollama models locally and use them in VS Code to offload exploratory chats and save hosted‑model requests. You'll keep using GitHub Copilot Chat for its deep editor integration while running additional chats on fast, free local models.

Important note: GitHub Copilot Chat **can** select local Ollama models directly in its settings (via the model picker). Additionally, you can:

- Use a VS Code extension that talks to Ollama (recommended: Continue) for extended workflows and copy suggestions to Copilot Chat.
- Expose local capabilities to Copilot Chat via MCP servers (advanced/optional).

All steps below cite repos and docs hosted on GitHub for reference.

---

## 1) Install Ollama and pull “lite” models

References (GitHub):

- Ollama repo and README: <https://github.com/ollama/ollama>
- Ollama model list and sizes (examples in README):
  - Llama 3.2 1B (~1.3 GB): `ollama run llama3.2:1b`
  - Gemma 3 1B (~815 MB): `ollama run gemma3:1b`
  - Moondream 2 1.4B (~829 MB): `ollama run moondream`
  - Phi 4 Mini 3.8B (~2.5 GB): `ollama run phi4-mini`

Install Ollama (Windows):

- Download installer from the repo README: <https://github.com/ollama/ollama> (Windows section links to `OllamaSetup.exe`).
- Start the Ollama service:

```bash
# If running headless
ollama serve

# Pull a small model (examples)
ollama pull llama3.2:1b
ollama pull gemma3:1b
ollama pull moondream
ollama pull phi4-mini
```

Quick sanity check:

```bash
ollama run llama3.2:1b
> Write a 1‑sentence summary of Django.
```

More from README:

- REST API examples: <https://github.com/ollama/ollama/blob/main/docs/api.md>
- CLI reference (pull, list, ps, stop): <https://github.com/ollama/ollama#cli-reference>

---

## 2a) GitHub Copilot Chat Native Support for Local Models

GitHub Copilot Chat in VS Code can select local Ollama models directly via the model picker—no separate extensions required for basic chat.

**References (official documentation):**

- VS Code language models guide: <https://code.visualstudio.com/docs/copilot/customization/language-models>
  - Sections: "Bring your own language model key", "Add a model from a built in provider"
  - Screenshot showing Ollama model picker: "built-in model providers that you can use to add more models"
  - FAQ confirms: "You can use locally hosted models in chat by using bring your own model key (BYOK)"
- VS Code Copilot overview: <https://code.visualstudio.com/docs/copilot/overview>
  - Section "Language models": Switch between different AI models optimized for specific tasks
- GitHub Copilot AI models: <https://docs.github.com/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat?tool=vscode>

**Setup:**

1. Open GitHub Copilot Chat settings (Ctrl+Alt+I → select model picker gear icon or "Manage Models").
2. In the model picker, select your local Ollama model (if Ollama is running on `http://localhost:11434`, VS Code auto-detects available models).
3. Chat as usual—responses now come from your local model, consuming zero hosted requests.

**Benefits:**

- No separate extension needed; all within Copilot Chat.
- Seamless editor integration (inline chat, Chat view, etc.).
- Zero hosted requests when using local models exclusively.

---

## 2b) Recommended: Use "Continue" extension for extended local workflows

Continue is an open‑source VS Code extension that supports local LLMs via Ollama for extended workflows.

References (GitHub):

- Continue repo: <https://github.com/continuedev/continue>
- VS Code extension link (from repo README): <https://marketplace.visualstudio.com/items?itemName=Continue.continue>

**Why this approach alongside Copilot Chat?**

- Zero API keys needed for Ollama models.
- Great side‑by‑side workflow: keep Copilot Chat (local or hosted) for code transforms/inline actions and project-aware suggestions; use Continue for long brainstorming, RAG‑style chats on local docs, and custom prompts—then **copy the output and paste it into GitHub Copilot Chat** for further editing, context-aware improvements, or inline insertion.

**Setup (high level):**

1. Install the Continue extension from the VS Code Marketplace (linked in the repo README above).
2. With Ollama running on `http://localhost:11434`, open Continue settings and set the provider to "Ollama", choosing a small model like `llama3.2:1b`.
3. Start a chat in Continue's panel. Your prompts now run locally via Ollama.
4. When Continue generates code or suggestions you like, **copy the output and paste it into GitHub Copilot Chat** for further editing, context-aware improvements, or inline insertion.

Tip: Use tiny models (1B–4B) for fast responses on laptops. Examples cited in the Ollama README: `llama3.2:1b`, `gemma3:1b`, `moondream`, `phi4-mini`.

---

## 3) Advanced (optional): Expose local tools to Copilot Chat via MCP

GitHub Copilot Chat supports connecting to MCP (Model Context Protocol) servers. You can publish local "tools" or "resources" that Copilot can call—those tools can internally delegate to Ollama's REST API.

**References (GitHub + official docs):**

- MCP TypeScript SDK (includes VS Code integration snippet): <https://github.com/modelcontextprotocol/typescript-sdk>
  - See the README "Quick Start" and the VS Code add‑MCP example: `code --add-mcp "{...}"`
- MCP server catalog (examples and community servers): <https://github.com/modelcontextprotocol/servers>
- Ollama REST API endpoints (chat/generate): <https://github.com/ollama/ollama/blob/main/docs/api.md>
- VS Code MCP servers guide: <https://code.visualstudio.com/docs/copilot/customization/mcp-servers>
  - Section: "Extend the capabilities of the chat experience with specialized tools from MCP servers"
- VS Code customization overview: <https://code.visualstudio.com/docs/copilot/customization/overview>
  - Section "MCP and tools": Connect external services and specialized tools through Model Context Protocol

Concept:

- Write a tiny MCP server (TypeScript SDK) exposing a tool like `local_ask`.
- Inside the tool handler, call Ollama’s `POST /api/chat` or `POST /api/generate` on `http://localhost:11434`.
- Add your server to VS Code as an MCP server; Copilot Chat can then call your `local_ask` tool when appropriate.

Skeleton steps:

```bash
# 1) Create a Node project and add MCP SDK (see SDK README for details)
npm init -y
npm install @modelcontextprotocol/sdk express zod

# 2) Implement a minimal HTTP MCP server
#    (Use examples in the SDK README; register a tool that POSTs to Ollama REST.)

# 3) Run your MCP server locally (e.g., http://localhost:3000/mcp)

# 4) Register the MCP server with VS Code (from SDK README)
code --add-mcp "{\"name\":\"local-ollama\",\"type\":\"http\",\"url\":\"http://localhost:3000/mcp\"}"
```

Result:

- Copilot Chat remains Copilot, but now has a callable tool backed by your local models for specific tasks.

Note: This does not replace Copilot’s model; it augments Copilot with local capabilities.

---

## 4) Practical workflow to "save requests"

**Three pathways for using local models with VS Code:**

- **Direct local use**: Select a local Ollama model in GitHub Copilot Chat settings (see section 2a) for all interactions—no hosted requests at all.
  - Reference: [VS Code language models guide](https://code.visualstudio.com/docs/copilot/customization/language-models) (BYOK and built-in providers section)
- **Hybrid workflow**: Use Copilot Chat (local or hosted) for editor‑aware refactors, code transforms, PR help, and inline chat. Use Continue (Ollama) for long brainstorming, RAG‑style research on local docs, or frequent "try many variants" prompts, then copy the best suggestions back to Copilot Chat for final integration.
  - Reference: [VS Code Copilot Chat guide](https://code.visualstudio.com/docs/copilot/copilot-chat) (chat workflows and context)
- **Advanced**: Optionally add an MCP tool for lightweight local tasks (summaries, draft text) that Copilot can call without leaving its chat.
  - Reference: [VS Code MCP servers guide](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) (tools and external services)

---

## 5) Troubleshooting

- Ollama not responding: ensure `ollama serve` is running and port `11434` is free.
- Model too slow or OOM: switch to a smaller variant (e.g., `llama3.2:1b`, `gemma3:1b`).
- Continue can’t find Ollama: verify `http://localhost:11434` and that at least one model is pulled (`ollama list`).
- MCP server not visible: re‑check the `code --add-mcp` JSON and your server logs; use the SDK’s examples to validate routing.

---

## Source links (GitHub + official documentation)

**GitHub repositories:**

- Ollama (install, models, API): <https://github.com/ollama/ollama>
- Continue (VS Code extension with Ollama support): <https://github.com/continuedev/continue>
- Model Context Protocol TypeScript SDK (VS Code + MCP): <https://github.com/modelcontextprotocol/typescript-sdk>
- MCP servers directory (examples/community servers): <https://github.com/modelcontextprotocol/servers>
- VS Code (editor project page): <https://github.com/microsoft/vscode>

**Official VS Code documentation:**

- Language models in VS Code: <https://code.visualstudio.com/docs/copilot/customization/language-models>
- GitHub Copilot overview: <https://code.visualstudio.com/docs/copilot/overview>
- Copilot Chat guide: <https://code.visualstudio.com/docs/copilot/copilot-chat>
- Customization overview: <https://code.visualstudio.com/docs/copilot/customization/overview>
- MCP servers guide: <https://code.visualstudio.com/docs/copilot/customization/mcp-servers>

**GitHub Copilot documentation:**

- AI models for Copilot Chat: <https://docs.github.com/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat?tool=vscode>
