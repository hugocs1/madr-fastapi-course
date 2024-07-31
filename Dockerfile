FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR madr/
COPY . .

RUN chmod -R 777 entrypoint.sh

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
