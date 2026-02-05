const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// Middleware to parse JSON and text bodies
app.use(express.json());
app.use(express.text());

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

/*
  POST endpoint: /save-message
  - Accepts a JSON payload with { user: '1' or '2', message: 'text' }
  - Writes the message to the corresponding user file (user1.txt or user2.txt)
*/
app.post('/save-message', (req, res) => {
  try {
    const { user, message } = req.body;
    
    if (!user || !['1', '2'].includes(user)) {
      return res.status(400).json({ error: 'Invalid user. Must be "1" or "2"' });
    }
    
    if (message === undefined) {
      return res.status(400).json({ error: 'Message field is required' });
    }
    
    const filename = `user${user}.txt`;
    const filepath = path.join(__dirname, filename);
    
    // Write the message to the file
    fs.writeFileSync(filepath, String(message), 'utf8');
    
    res.json({ success: true, file: filename });
  } catch (err) {
    console.error('Error saving message:', err);
    res.status(500).json({ error: 'Failed to save message: ' + err.message });
  }
});

// Start the server on the configured port.
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`SSE server running at http://localhost:${port}`));
