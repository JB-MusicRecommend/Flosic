FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    git \
    libmariadb-dev-compat \
    libmariadb-dev  \
    openjdk-17-jdk \
    g++
    
RUN mkdir -p /webapp
WORKDIR /webapp

COPY requirements.txt .
RUN pip3 install --upgrade pip3
RUN pip3 install -r requirements.txt
RUN pip3 install konlpy tensorflow keras gensim




COPY . .

EXPOSE 5000 3306

CMD ["python", "./app/main.py"]