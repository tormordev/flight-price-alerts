# Use a Node.js image for building the React app
FROM node:18 as build-stage

# Set the working directory
WORKDIR /usr/src/app

# Copy dependency files first to leverage Docker's build cache
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Use an Nginx image to serve the build
FROM nginx:alpine

# Copy the React build files to the Nginx HTML directory
COPY --from=build-stage /usr/src/app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
