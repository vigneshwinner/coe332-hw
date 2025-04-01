FROM python:3.12

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY gene_api.py /app/gene_api.py

ENTRYPOINT ["python"]
CMD ["gene_api.py"]
