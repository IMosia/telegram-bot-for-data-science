# Dockerfile
FROM apache/airflow:2.7.0

# Set the working directory
WORKDIR /opt/airflow

# Copy the requirements.txt file
COPY requirements.txt .

# Install the Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt