FROM eclipse-temurin:21-jdk-jammy

# Set working directory
WORKDIR /opt/red5

# Copy everything from current folder into the container
COPY . /opt/red5

# Expose default Red5 ports
EXPOSE 1935 5080

# Run Red5 server
CMD ["sh", "/opt/red5/red5.sh", "-n"]