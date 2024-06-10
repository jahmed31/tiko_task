# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . .

# Set the environment variables for Django
ENV DJANGO_SETTINGS_MODULE=tiko_test.settings
ENV PYTHONUNBUFFERED=1

# Expose port 8000 for the Django app
EXPOSE 8000

# Run migrations, if any, before starting the server
RUN python manage.py makemigrations event_management user_profile && \
    python manage.py migrate

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
