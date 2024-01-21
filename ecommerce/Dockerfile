# Use the official Python image as a parent image
FROM python:3.11

# Set environment variables to ensure Python outputs are sent straight to the terminal (makes logs more readable)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your Django project (ecommerce) into the container at /app
COPY . /app/

# Expose port 8000 to allow communication to/from the server
EXPOSE 8001

# Define the default command to run when starting the container
CMD ["bash", "./entrypoint.sh"]
