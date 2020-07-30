FROM python:3.7-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the worker:
COPY worker.py .
COPY wait-for-it.sh .
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "-u", "worker.py"]