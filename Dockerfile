# Python 3.11.9 minimal package
FROM python:3.11.9-alpine3.19

USER root

# Setup directory
RUN mkdir -p /home/app/

WORKDIR /home/app/

# Get dependency list
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Directories and Files
COPY src/ ./src
COPY tests/ ./tests
COPY .env .
COPY ./docker/start.sh /usr/local/bin/start.sh

# Make start script executable
RUN chmod +x /usr/local/bin/start.sh

# Make Default Entry Point
CMD ["start.sh"]