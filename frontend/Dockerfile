# Build React App
FROM node:alpine AS build

# Set working directory
WORKDIR /home

# Copy necessary files for dependency installation
COPY ./package.json ./yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code and build the app
COPY . ./
RUN yarn build

# Serve with Nginx
FROM nginx:alpine

# Copy Nginx configuration
COPY --from=nginx nginx.conf /etc/nginx/conf.d/default.conf

# Copy build output from the previous stage
COPY --from=build /home/build /usr/share/nginx/html

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]