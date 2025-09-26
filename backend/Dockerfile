FROM python:3.10-slim
WORKDIR /app
RUN pip install --default-timeout=100 --upgrade pip
RUN pip install --default-timeout=100 "numpy<2.0"
COPY requirement.txt .
RUN pip install --default-timeout=100 torch==2.2.2+cpu --find-links https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --default-timeout=100 --no-cache-dir -r requirement.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

