FROM python:3.11 AS build

# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
RUN pip install poetry

COPY . /app
WORKDIR /app
ENV PATH=/opt/poetry/bin:$PATH
RUN poetry config virtualenvs.in-project true && poetry install


FROM python:3.11

# Copy poetry from build stage
COPY --from=build /app /app
WORKDIR /app
CMD ["/app/.venv/bin/python", "main.py"]