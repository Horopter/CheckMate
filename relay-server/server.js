// server.js
const fs = require('fs');
const http = require('http');
const https = require('https');
const express = require('express');
const WebSocket = require('ws');
const { PORT, USE_TLS, TLS_CERT_PATH, TLS_KEY_PATH } = require('./config');
const logger = require('./logger');
const { wsMessageCounter, client: promClient } = require('./metrics'); // Import metrics

const app = express();

// Health Check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('Relay server is running.');
});

// Metrics endpoint for Prometheus
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', promClient.register.contentType);
    res.end(await promClient.register.metrics());
  } catch (ex) {
    res.status(500).end(ex);
  }
});

// Create HTTP or HTTPS server based on configuration
let server;
if (USE_TLS) {
  const cert = fs.readFileSync(TLS_CERT_PATH);
  const key = fs.readFileSync(TLS_KEY_PATH);
  server = https.createServer({ cert, key }, app);
} else {
  server = http.createServer(app);
}

// Create a WebSocket server attached to the HTTP/HTTPS server
const wss = new WebSocket.Server({ server });

// WebSocket handling
wss.on('connection', (ws, req) => {
  const clientIP = req.socket.remoteAddress;
  logger.info('New WebSocket connection from %s', clientIP);

  // Set up a heartbeat mechanism to detect broken connections.
  ws.isAlive = true;
  ws.on('pong', () => {
    ws.isAlive = true;
  });

  ws.on('message', (message) => {
    logger.debug('Received message from %s: %s', clientIP, message);

    // Increment custom metric for each relayed message.
    wsMessageCounter.inc();

    // For production, forward the message to the intended recipient.
    // For now, simply echo back the message.
    ws.send(message, (err) => {
      if (err) {
        logger.error('Error sending message: %s', err);
      }
    });
  });

  ws.on('close', () => {
    logger.info('Connection from %s closed', clientIP);
  });

  ws.on('error', (error) => {
    logger.error('WebSocket error from %s: %s', clientIP, error);
  });
});

// Heartbeat interval to detect and close dead connections
const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) {
      logger.warn('Terminating dead connection');
      return ws.terminate();
    }
    ws.isAlive = false;
    ws.ping(() => {});
  });
}, 30000);

server.listen(PORT, () => {
  logger.info('Relay server is running on port %d', PORT);
});

// Graceful shutdown
function shutdown() {
  logger.info('Shutting down server...');
  clearInterval(interval);
  wss.close(() => {
    server.close(() => {
      logger.info('Server shutdown complete.');
      process.exit(0);
    });
  });
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);