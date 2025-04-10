# Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies separately to leverage caching
COPY package.json package-lock.json* ./  
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Run dev server
CMD ["npm", "run", "dev"]
