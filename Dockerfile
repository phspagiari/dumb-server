FROM python:3.7.5

RUN pip install flask redis
ADD ./app.py /app.py

EXPOSE 5000
CMD ["python", "/app.py"]
