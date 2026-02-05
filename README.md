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

## GitHub Pages Deployment

Since GitHub Pages only serves static files, you can use the **polling template** which fetches from a JSON file:

1. Open `github-pages.html` in your browser (or serve it locally for testing).
2. The page polls `data.json` every 2 seconds (adjustable).
3. To trigger updates, either:
   - Manually edit `data.json` and push to your repo.
   - Let the GitHub Actions workflow auto-update it every 5 minutes (see below).

**Setup automatic updates with GitHub Actions:**

- The workflow `.github/workflows/update-data.yml` runs every 5 minutes and bumps `data.json`.
- It will only commit if data actually changed (to avoid noise).
- To modify the schedule, edit the `cron` line in the workflow file.

**To deploy on GitHub Pages:**

```bash
git add github-pages.html data.json .github/workflows/update-data.yml
git commit -m "Add GitHub Pages live update template"
git push origin main
```

Then enable Pages under repo Settings → Pages → deploy from `main` branch.

## Update simple.txt on Demand

Use the **update-simple.yml** workflow to update `simple.txt` from GitHub without pushing code:

1. Go to your repo on GitHub → **Actions** tab
2. Select **"Update simple.txt"** workflow
3. Click **"Run workflow"** (dropdown on the right)
4. Optionally enter a custom message in the input field
5. Click **"Run workflow"** again to confirm
6. The workflow commits and pushes the change automatically

The page polling `simple.txt` (using `index.html` or `github-pages.html`) will fetch the updated content on the next interval.

---

**Credits**

- Template created and documented by the project owner with assistance from GitHub Copilot.

If you'd prefer a different credit line or additional author information, let me know and I can update this.
