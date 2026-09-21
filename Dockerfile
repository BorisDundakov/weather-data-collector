FROM python:3.10-slim
WORKDIR /application
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
RUN useradd -m weather-app-user
COPY application/ .
USER weather-app-user
CMD ["python", "main.py"]