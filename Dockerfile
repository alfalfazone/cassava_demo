FROM continuumio/miniconda3

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir --retries 3 --timeout 300 -r requirements.txt

# 複製全部程式碼
COPY . .

# 使用 flask run，Render 會提供 PORT
CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=${PORT}"]
