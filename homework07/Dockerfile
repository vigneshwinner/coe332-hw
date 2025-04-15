FROM python:3.12

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src/ /app/src

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["src/api.py"]
