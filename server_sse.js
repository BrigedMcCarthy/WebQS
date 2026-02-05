const express = require('express');
const app = express();

// Serve static files from the repository root so the client can fetch index.html and simple.txt
app.use(express.static('.'));

/*
  SSE endpoint: /events
  - Sets the required SSE headers and flushes them so the connection stays open.
  - Periodically writes `data: ...\n\n` frames to the response which the browser's
    `EventSource` will receive as `message` events.
  - Uses JSON-encoded payloads but writes them as plain text in the SSE `data:` field.
  - When the client closes the connection (`req.on('close')`), we clear the interval.
*/
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  // flushHeaders ensures headers are sent immediately; some frameworks buffer otherwise.
  res.flushHeaders();

  let i = 0;
  const iv = setInterval(() => {
    const payload = { msg: `update ${++i}`, time: new Date().toISOString() };
    // SSE frames must end with a blank line. Each `data:` line is part of one event.
    res.write(`data: ${JSON.stringify(payload)}\n\n`);
  }, 2000);

  // If the client disconnects, cleanup the interval to avoid leaks.
  req.on('close', () => {
    clearInterval(iv);
  });
});

// Start the server on the configured port.
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`SSE server running at http://localhost:${port}`));
