FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "Introduction.py", "--server.port=8501", "--server.address=0.0.0.0"]
