FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy all project files
COPY . .

# Expose dev server port
EXPOSE 5173

# Run Vite dev server correctly
CMD ["npm", "run", "dev"]
