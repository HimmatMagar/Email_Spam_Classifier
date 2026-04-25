FROM python:3.12-slim

WORKDIR /app


COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc \
      g++ \
      build-essential \
      && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000" ]