FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

EXPOSE 8000

COPY ["main.py","/app/"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]