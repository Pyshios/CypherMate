# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV SLACK_APP_TOKEN="xapp-1-A06RWBWMR61-6885791286852-3690e5bdea5a3872c2de849a40ea5223e5b11560e411f6e4d5803b63d5ab4213" \
    SLACK_BOT_TOKEN="xoxb-291309891525-6883358677458-odX8zeHNfeOl9tQk7j4uzDwe+" \
    ENCRYPTION_KEY="MLhcQLrN3vEEREfLnX7vZSV1cWMJvdHIvIx4Q5eLmvc="

# Expose the port (if needed)
# EXPOSE 5000

# Run the application
CMD ["python", "cypher_mate.py"]