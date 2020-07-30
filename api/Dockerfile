FROM python:3.7-slim-buster

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Install dependencies:
COPY requirements.txt .
COPY wait-for-it.sh .
RUN pip install -r requirements.txt

VOLUME [ "/app" ]

EXPOSE 8000

CMD ["./wait-for-it.sh", "db:5432", "--", "python", "-u", "run.py"]