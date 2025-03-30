// config.js
require('dotenv').config(); // Load environment variables from .env file, if present

module.exports = {
  PORT: process.env.PORT || 8443,
  USE_TLS: process.env.USE_TLS === 'true', // Enable TLS if set to 'true'
  TLS_CERT_PATH: process.env.TLS_CERT_PATH || './certs/cert.pem',
  TLS_KEY_PATH: process.env.TLS_KEY_PATH || './certs/key.pem',
  // Number of worker processes (default to number of CPU cores)
  WORKER_COUNT: process.env.WORKER_COUNT || require('os').cpus().length,
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
};
