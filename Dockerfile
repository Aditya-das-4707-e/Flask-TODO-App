# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# We also install gunicorn for a production-ready WSGI server
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Expose port 5000 for the application to be accessible
EXPOSE 5000

# Run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
