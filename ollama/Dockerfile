FROM ollama/ollama:latest

# Install required tools and fix GPG issues
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        ca-certificates \
        gnupg \
        apt-transport-https \
        software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Create a startup script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command to keep the container running
CMD ["tail", "-f", "/dev/null"]
