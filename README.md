# WebQS — Dynamic Update Template

This workspace provides a small template demonstrating three client-side techniques for dynamic updates:

- Polling (fetch) — works with static servers
- Server‑Sent Events (SSE) — server -> browser push over HTTP
- WebSocket — bidirectional low-latency channel

Files added:

- `index.html` — client UI to choose mode and start/stop updates
- `server_sse.js` — Express-based SSE example (serves static files)
- `ws_server.js` — WebSocket server example using `ws`
- `package.json` — convenience scripts

Quick start

1. Install Node deps (for SSE and WS servers):

```bash
npm install
```

2. Run the SSE server (serves `index.html` and `/events`):

```bash
npm run start-sse
# open http://localhost:3000/
```

3. Run the WebSocket server (serve `index.html` separately):

```bash
npm run start-ws
# in another terminal (serve static files):
npm run start-static
# open http://localhost:8000/
```

4. Or just run a static server and use polling:

```bash
npm run start-static
# open http://localhost:8000/
```

Notes

- For production, secure WebSocket and SSE endpoints (TLS) and handle reconnection/backoff.
- The template app uses `simple.txt` for polling; replace with your API or endpoint.

**Credits**

- Template created and documented by the project owner with assistance from GitHub Copilot.

If you'd prefer a different credit line or additional author information, let me know and I can update this.
