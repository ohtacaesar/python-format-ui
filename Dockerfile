FROM python:3

RUN set -eux \
  && pip install flask


WORKDIR /app

COPY templates/ ./templates/
COPY main.py ./

CMD ["python", "main.py"]

