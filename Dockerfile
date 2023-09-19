FROM python:3.11.5-slim

WORKDIR /app

# install poetry
ENV POETRY_VERSION=1.2.0
RUN pip install "poetry==$POETRY_VERSION"

# copy application
COPY ["pyproject.toml", "poetry.lock", "README.md", ".env", "./"]
COPY ["src/", "src/"]

# build wheel
RUN poetry build --format wheel

# install package
RUN pip install dist/*.whl


# expose port
EXPOSE 9000


# command to run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--workers", "1"]
