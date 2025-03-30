// logger.js
const { createLogger, format, transports } = require('winston');
const { LOG_LEVEL } = require('./config');

const logger = createLogger({
  level: LOG_LEVEL,
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.splat(),
    format.json()
  ),
  defaultMeta: { service: 'relay-server' },
  transports: [
    new transports.Console(),
    // In production, you might add file or remote transports here.
  ],
});

module.exports = logger;
