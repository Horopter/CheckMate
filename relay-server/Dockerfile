# Use an official Node.js runtime as a base image (alpine for a lightweight image)
FROM node:18-alpine

# Create and set the working directory
WORKDIR /usr/src/app

# Copy package files and install production dependencies
COPY package*.json ./
RUN npm install --only=production

# Copy the rest of the application code
COPY . .

# Expose the port your server is listening on (adjust if needed)
EXPOSE 8443

# Start the server using the cluster entrypoint
CMD [ "node", "cluster.js" ]