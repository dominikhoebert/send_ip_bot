
FROM python:3.11-alpine
LABEL authors="Dominik"

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY send_ip.py .

ENTRYPOINT ["python3"]
CMD ["send_ip.py"]
