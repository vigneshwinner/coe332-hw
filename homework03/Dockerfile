FROM python:3.12

RUN pip3 install pytest==8.3.4

COPY ml_data_analysis.py
COPY gcd_algorithm.py
COPY test_ml_data_analysis.py
COPY test_gcd_algorithm.py

RUN chmod +rx ml_data_analysis.py
RUN chmod +rx gcd_algorithm.py
RUN chmod +rx test_ml_data_analysis.py
RUN chmod +rx test_gcd_algorithm.py  

ENV PATH="/code:$PATH"
