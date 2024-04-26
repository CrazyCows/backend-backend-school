FROM python:3.11.9-slim-bullseye

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc git tree \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HTTP_TIMEOUT=300

# Install Poetry
#RUN pip install poetry==1.2.2 \
#    && poetry config virtualenvs.create false

# Set work directory
WORKDIR /app

# Copy source code
COPY src/ src/
COPY requirements.txt requirements.txt

# Fix missing README.md for poetry package
RUN if [ ! -f README.md ]; then echo "Placeholder README" > README.md; fi

# Install project dependencies
RUN pip install -r requirements.txt

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

CMD ["/usr/local/bin/python", "-m", "src"]
