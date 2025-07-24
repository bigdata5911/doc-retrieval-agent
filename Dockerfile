FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install streamlit sseclient

COPY . .

EXPOSE 8000
EXPOSE 8501

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]