# Use Microsoft's official Playwright image which comes with browsers pre-installed
FROM mcr.microsoft.com/playwright/javascript:v1.43.0-jammy

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available)
COPY package.json ./
# If you have a package-lock.json, uncomment the next line
# COPY package-lock.json ./

# Install dependencies
# This will also ensure browser binaries are correctly placed by the base image
RUN npm install

# Copy the rest of your application's code
COPY . .

# Command to run the application (runs the test call in browser.js)
CMD ["node", "browser.js"]
