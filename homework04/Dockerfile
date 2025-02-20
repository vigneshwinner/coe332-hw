FROM python:3.12

RUN pip3 install pytest==8.3.4 requests xmltodict

COPY iss_tracker.py /code/iss_tracker.py
COPY test_iss_tracker.py /code/test_iss_tracker.py

RUN chmod +rx /code/iss_tracker.py
RUN chmod +rx /code/test_iss_tracker.py

ENV PATH="/code:$PATH"
