FROM continuumio/miniconda3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --retries 3 --timeout 300 -r requirements.txt

CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--reload"]