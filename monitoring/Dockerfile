# Dockerfile for System Monitoring Dashboard
# Uses Python 3 slim image for minimal footprint

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (though we use stdlib only, good practice)
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 5050
EXPOSE 5050

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5050/api/metrics || exit 1

# Run the application
CMD ["python3", "server.py"]