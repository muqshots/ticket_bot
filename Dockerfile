FROM python:3.9-slim

COPY requirements.txt .

RUN pip3 install -r requirements.txt

LABEL com.centurylinklabs.watchtower.enable="true"

COPY src/ .
CMD ["python", "bot.py"]