// metrics.js
const client = require('prom-client');

// Collect default metrics (CPU, memory, event loop lag, etc.)
client.collectDefaultMetrics({ timeout: 5000 });

// You can define custom metrics here, for example, a counter for WebSocket messages.
const wsMessageCounter = new client.Counter({
  name: 'relay_ws_messages_total',
  help: 'Total number of WebSocket messages relayed',
});

module.exports = {
  client,
  wsMessageCounter,
};
