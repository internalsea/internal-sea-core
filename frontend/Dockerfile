# Build stage
FROM node:18-alpine as build

# Set work directory
WORKDIR /app

# Accept build arguments for React environment variables
ARG REACT_APP_API_URL=/api/v1
ARG NODE_ENV=production

# Set environment variables for build
ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV NODE_ENV=$NODE_ENV

# Copy package files
COPY package*.json ./

# Install dependencies (need devDependencies for React build)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 