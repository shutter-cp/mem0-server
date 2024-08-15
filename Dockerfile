FROM python:3.11.9
WORKDIR /app
COPY requirements.txt .

RUN PIP_NO_PROGRESS_BAR=off pip install  --no-cache-dir --no-use-pep517 --progress-bar off  --upgrade pip -i  https://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com &&  PIP_NO_PROGRESS_BAR=off pip install  --no-cache-dir --no-use-pep517 -r requirements.txt --progress-bar off  -i  https://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com

COPY Mem0Server.py .

EXPOSE 5000

CMD ["python", "Mem0Server.py"]