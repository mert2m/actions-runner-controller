# Base image with Python 3
FROM python:3.9

# Create work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install cryptography
RUN pip install pymysql
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Environment variables for database connection
ENV DB_USER=root \
    DB_PASSWORD=secret \
    DB_NAME=TaskDB \
    DB_HOST=mert-mysql

# Connect to MySQL using pymysql
CMD ["python", "main.py"]

# Expose Flask application port
EXPOSE 8080
