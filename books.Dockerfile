FROM python:3.11-slim

WORKDIR /books

COPY books/ books/
COPY pyproject.toml README.md ./

RUN pip install --no-cache-dir .

VOLUME [ "/data" ]

CMD ["books"]