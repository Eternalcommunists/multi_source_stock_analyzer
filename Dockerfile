# Multi-stage Dockerfile for the multi-source stock analyzer

# Stage 1: Build the frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./frontend/
COPY . .

# Install frontend dependencies
RUN cd frontend && npm ci --only=production

# Build the frontend
RUN cd frontend && npm run build


# Stage 2: Final image
FROM node:18-alpine

WORKDIR /app

# Install Python and other dependencies for akshare
RUN apk add --no-cache python3 py3-pip gcc g++ make python3-dev

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy backend from builder stage
COPY backend ./backend

# Copy data-sources from builder stage
COPY data-sources ./data-sources

# Copy frontend build from builder stage
COPY --from=frontend-builder /app/frontend/build ./backend/public

# Create non-root user
RUN addgroup -g 1001 -S nodejs &&\
    adduser -S nextjs -u 1001

# Change ownership of app directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python backend/healthcheck.py &

# Start the application
CMD ["python", "backend/main.py"]