// cluster.js
const cluster = require('cluster');
const os = require('os');
const { WORKER_COUNT } = require('./config');
const logger = require('./logger');

if (cluster.isMaster) {
  const numWorkers = parseInt(WORKER_COUNT, 10);
  logger.info('Master process started. Spawning %d workers.', numWorkers);

  // Fork workers.
  for (let i = 0; i < numWorkers; i++) {
    cluster.fork();
  }

  // Replace any dead workers.
  cluster.on('exit', (worker, code, signal) => {
    logger.error('Worker %d died. Spawning a new worker.', worker.process.pid);
    cluster.fork();
  });
} else {
  // Worker process runs the server.
  require('./server');
}
