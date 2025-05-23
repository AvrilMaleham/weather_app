FROM python:3.11-slim

WORKDIR /app

# Install dependencies first to leverage caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the code
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

