FROM python:3.12

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY iss_tracker.py /app/iss_tracker.py

ENTRYPOINT ["python"]
CMD ["iss_tracker.py"]
