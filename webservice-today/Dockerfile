FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1

# Create the app directory
RUN mkdir /app
COPY . /app
WORKDIR /app

# Copy the requirements file and install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port
EXPOSE 8000

# Run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]