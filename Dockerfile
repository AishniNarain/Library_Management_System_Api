# # Use an official Python runtime as a parent image
# FROM python:3.11-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # COPY wait-for-it.sh /usr/local/bin/
# # RUN chmod +x /usr/local/bin/wait-for-it.sh

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Set environment variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Run app.py when the container launches using flask command as below
# # CMD ["wait-for-it.sh", "mysql-db:3306", "--", "wait-for-it.sh", "mongo-db:27017", "--", "flask", "run", "--reload"]
# CMD ["flask", "run", "--reload"]

FROM ubuntu:latest

# Install dependencies and add MongoDB repository
RUN apt-get update && \
    apt-get install -y gnupg wget lsb-release curl && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    CODENAME=$(lsb_release -cs) && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $CODENAME/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    apt-get install -y mysql-server mongodb-org supervisor

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for MySQL and MongoDB
EXPOSE 3306 27017

# Command to run supervisord
CMD ["/usr/bin/supervisord"]




