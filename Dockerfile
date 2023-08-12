# Use an official Python runtime as a parent image
FROM python:3.9 as base

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Run tests
FROM base as test
# Add the current directory contents into the container at /app
COPY . /app

RUN pip install pytest && pytest

# Final stage to run the application
FROM base as app

# Add our shell script
# Add the current directory contents into the container at /app
COPY . /app
COPY start.sh /usr/local/bin/

# Make sure our script is executable
RUN chmod +x /usr/local/bin/start.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENTRYPOINT ["start.sh"]
