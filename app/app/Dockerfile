# Use official Python image
FROM python:3.11-slim
 
# Set working directory
WORKDIR /app
 
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the full project
COPY . .
 
# Set env vars if needed (can also be passed via docker run --env-file)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/
 
 
# Run the app with Gunicorn
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn.conf.py", "--timeout", "6000"]