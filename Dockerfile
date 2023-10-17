FROM python:3.9-slim
WORKDIR /app
# 複製專案
COPY . . 

# 提供默認的埠為8000
EXPOSE 8000

# 定義默認命令來運行當使用 “docker run”
CMD ["python3", "app.py"]