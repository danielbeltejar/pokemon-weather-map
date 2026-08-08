FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends locales \
    && echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen \
    && echo "de_DE.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen es_ES.UTF-8 \
    && locale-gen de_DE.UTF-8 \
    && locale-gen en_US.UTF-8 \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && /usr/sbin/update-locale LANG=en_US.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG es_ES.UTF-8
ENV LC_ALL es_ES.UTF-8

WORKDIR /app

COPY . .

ENV PYTHONPATH="/app"

RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip setuptools wheel \
    && addgroup --gid 10001 --system app \
    && adduser --uid 10001 --gid 10001 --system --home /app app \
    && chown -R app:app /app

USER app

CMD ["python", "src/main.py"]
