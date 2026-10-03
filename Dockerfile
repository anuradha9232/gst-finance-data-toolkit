FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Validate a JSONL invoice file:
#   docker run --rm -v "$PWD":/data gst-validator /data/invoices.jsonl /data/report.jsonl
ENTRYPOINT ["python3", "solve.py"]
