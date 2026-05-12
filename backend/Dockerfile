FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget default-jre && \
    wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz && \
    tar -xzf apache-jmeter-5.6.3.tgz && \
    mv apache-jmeter-5.6.3 /opt/jmeter && \
    ln -s /opt/jmeter/bin/jmeter /usr/local/bin/jmeter && \
    rm apache-jmeter-5.6.3.tgz

RUN pip install flask prometheus_client groq python-dotenv requests

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]