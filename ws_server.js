const WebSocket = require('ws');

/*
  Simple WebSocket server:
  - Listens on port 8080 for WebSocket connections.
  - On each connection it sends a welcome message and then periodically sends
    JSON-encoded 'tick' messages. It also logs any messages received from clients.
  - When the connection closes, the server clears the periodic timer to avoid leaks.
*/
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', function connection(ws) {
  // Send a small JSON welcome payload to the client right away.
  ws.send(JSON.stringify({ msg: 'welcome', time: new Date().toISOString() }));

  // Periodically send a 'tick' message every 1s. In real apps, replace with real events.
  let i = 0;
  const iv = setInterval(() => {
    ws.send(JSON.stringify({ msg: 'tick ' + (++i), time: new Date().toISOString() }));
  }, 1000);

  // Log messages received from the client. You can parse JSON here if the client sends structured data.
  ws.on('message', function message(data) {
    console.log('received from client: %s', data);
  });

  // Clean up when the socket closes to avoid keeping timers running.
  ws.on('close', () => clearInterval(iv));
});

console.log('WebSocket server running on ws://localhost:8080');
