# Use the official Playwright image
FROM mcr.microsoft.com/playwright:v1.40.0-focal

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Command to run the app
CMD ["npm", "start"]

