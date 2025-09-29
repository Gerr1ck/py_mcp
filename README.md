# py_mcp

A small demo showing a minimal Model Context Protocol (MCP) server and a client that connects to it over stdio.

This repository contains a toy calculator server exposing a few tools (add, subtract, multiply, divide) and a small client that demonstrates how to list resources/tools, read a resource, and call a tool.

## Repository layout

- `client/`
	- `calc_client.py` — example async client that runs a server process and communicates over stdio.
- `server/`
	- `calc_server.py` — example MCP server that registers calculator tools and a greeting resource.
- `README.md` — this file.

## Requirements

- Python 3.8+ (the environment where you run the client and server should have a compatible Python version). The code was exercised with Python 3.13 but any modern 3.x should work.
- The `mcp` package (the MCP framework used by the examples) must be importable in the Python environment. That means either:
	- you have `mcp` installed into the active virtualenv, or
	- your PYTHONPATH includes the location of an `mcp` package/source tree.

If you don't have `mcp` available, install it through your normal package source or make the package importable via PYTHONPATH.

## Quickstart (Windows PowerShell)

Open PowerShell and change into this repository's `py_mcp` directory:

```powershell
cd C:\path\to\py_mcp
```

Option A — run with an environment that already has `mcp` installed:

```powershell
# Run the server in one terminal
python .\server\calc_server.py

# In another terminal (same virtualenv/interpreter) run the client
python .\client\calc_client.py
```

Option B — if `mcp` is a local package sibling (or you want to run without installing), add the current directory to PYTHONPATH so `mcp` can be imported:

```powershell
$env:PYTHONPATH = $PWD
python .\server\calc_server.py
# In another terminal (same $env:PYTHONPATH value):
$env:PYTHONPATH = $PWD
python .\client\calc_client.py
```

## Inspector (optional)

If you'd like an interactive visual inspector to explore the running MCP server, you can use the Model Context Protocol Inspector. It launches a local UI that connects to a server process and displays registered tools, resources, and messages exchanged over the protocol.

Run this command from the `server` directory (it uses `npx` to run the inspector without installing globally):

```powershell
npx @modelcontextprotocol/inspector python calc_server.py
```

Notes about the inspector:
- The inspector will spawn the server script using the Python interpreter you provide (here `python calc_server.py`). Make sure the same interpreter has access to the `mcp` package.
- The inspector is a developer tool for inspecting and debugging MCP servers — it shows available tools/resources, request/response messages, and helps you exercise tools interactively.
- If the command fails with errors about `npx` or permissions, ensure Node.js (which provides `npx`) is installed and available in your PATH, or install the inspector package globally or locally and run it directly.

Inspector troubleshooting

Common issues you may see when running the inspector and how to resolve them:

- "'npx' is not recognized as an internal or external command" — Node.js / npm is not installed or not on your PATH. Install Node.js (which includes npm) from https://nodejs.org/ and re-open your terminal.
- "Permission denied" or EACCES when running `npx` — on Windows this is uncommon; try running PowerShell as Administrator, or install the inspector package locally in the project (`npm i @modelcontextprotocol/inspector`) and run it via `npx` or `npx --no-install @modelcontextprotocol/inspector ...`.
- `ModuleNotFoundError: No module named 'mcp'` — the inspector spawns your server using the Python interpreter you provided. Ensure that interpreter has access to the `mcp` package (install it into the venv, or set `PYTHONPATH` to include the package location). You can reproduce by running the server script directly:

```powershell
python .\calc_server.py
```

and fixing any import errors there first.
- Inspector fails to connect / shows transport errors — verify the server script is being launched by the inspector and that it speaks MCP over stdio. The inspector expects a server process that adheres to the Model Context Protocol over stdio when launched this way.



Notes:
- The example client uses `sys.executable` to launch the server, so use the same Python interpreter / virtualenv for both server and client to avoid import issues.
- If you see ModuleNotFoundError: No module named 'mcp', verify that `mcp` is installed or that PYTHONPATH points to a folder containing an `mcp` package.

## What the demo does

- `server/calc_server.py` registers four tools: `add`, `subtract`, `multiply`, and `divide`. It also exposes a dynamic resource with the template `greeting://{name}` that returns a greeting string for the name provided.
- `client/calc_client.py` launches the server as a subprocess (stdio transport), initializes an MCP `ClientSession`, lists resources and tools, reads the `greeting://hello` resource, and calls the `add` tool with `a=1, b=7`.

Example (trimmed) output you should see when running the client:

```
Using server script at: C:\...\py_mcp\server\calc_server.py
LISTING RESOURCES
Resource:  greeting://{name}
LISTING RESOURCE TEMPLATES
Template: greeting://{name}
LISTING TOOLS
Tool: add
Tool: subtract
Tool: multiply
Tool: divide
READING RESOURCE
Content: Hello, hello!, MIME Type: text/plain
CALL TOOL
1 + 7 = 8    # or similar output depending on how the client prints the tool result
```

## Contract (quick)

- Inputs: client requests contain resource identifiers (string templates) or tool names with JSON-like argument dictionaries.
- Outputs: resource reads return (content, mime_type); tool calls return a result object (the demo prints the tool result).
- Error modes: server returns exceptions for invalid tool calls; division by zero in `divide` returns `inf` in the example server implementation.

## Edge cases and notes

- Division by zero: `divide(a, 0)` returns `float('inf')` in the server implementation — adjust if you prefer an exception or custom error object.
- Keep server and client running with the same Python interpreter to avoid import / path mismatches.
- If your environment blocks subprocess stdio connections (uncommon), run server and client in separate terminals and adapt the client to connect over a different transport.

## Troubleshooting

- ModuleNotFoundError: No module named 'mcp' — ensure `mcp` is installed or reachable via PYTHONPATH.
- Permission / PATH issues launching Python — use the full path to the python executable you want to use (or run from the desired venv's prompt).

## Next steps

- Add a `requirements.txt` or pyproject configuration if this project should declare dependencies.
- Add unit tests that exercise the client-server interaction (using a fake stdio transport or subprocess with captured I/O).
- Extend the server with more tools and resource types to explore the MCP features.

## License

No license specified. Add a LICENSE file if you want to make the project's license explicit.