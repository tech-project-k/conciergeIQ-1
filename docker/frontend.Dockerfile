FROM node:20-slim

WORKDIR /app

# Copy package configurations
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source files
COPY frontend/ ./

EXPOSE 5173

# Start Vite dev server exposing host for container mapping
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
