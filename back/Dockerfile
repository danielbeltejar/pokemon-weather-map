FROM python:3.12-slim

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

WORKDIR /app

COPY . .

ENV PYTHONPATH="/app"

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]