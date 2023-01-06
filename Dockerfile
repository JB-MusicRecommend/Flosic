FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    git \
    libmariadb-dev-compat \
    libmariadb-dev 
    
RUN mkdir -p /webapp
WORKDIR /webapp
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000 3306

CMD ["python", "./app/main.py"]