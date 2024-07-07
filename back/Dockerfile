FROM python:3.11-slim

# Set the locale to support Spanish language and UTF-8 encoding
RUN apt-get update && apt-get install -y locales \
    && echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen \
    && echo "de_DE.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen es_ES.UTF-8 \
    && locale-gen de_DE.UTF-8 \
    && locale-gen en_US.UTF-8 \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LANG es_ES.UTF-8
ENV LC_ALL es_ES.UTF-8

# Set the working directory for the application
WORKDIR /app

# Copy the application files
COPY . .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "main.py"]