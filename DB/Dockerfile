# Use the official MySQL image as the base image
FROM mysql:latest

# Set environment variables for MySQL configuration
COPY setup.sql /docker-entrypoint-initdb.d/setup.sql

# Expose the default MySQL port (adjust as needed)
EXPOSE 3306
