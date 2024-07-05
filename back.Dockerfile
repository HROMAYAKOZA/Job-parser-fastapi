FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

# RUN apt-get update && apt-get update

COPY src /app/src
COPY main.py /app
# COPY .env /app

EXPOSE 8000 8000

CMD [ "python3", "-u", "main.py" ]