FROM python:3.11-slim
 
# System deps: libzbar0 for pyzbar, libgl1/libglib for opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
# Uploads + DB live here — mount a Railway volume at this path
RUN mkdir -p /app/data/uploads
 
ENV PORT=5000
 
CMD gunicorn -w 1 -b 0.0.0.0:${PORT} --timeout 120 app:app