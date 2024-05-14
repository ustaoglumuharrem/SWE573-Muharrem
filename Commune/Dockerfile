# Use the official Python image as a base
FROM python:3.10

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /code/

# Expose the port that Django runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Commune.wsgi:application"]
