# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
RUN pip install --no-cache-dir pandas==1.0.5
RUN pip install --no-cache-dir SQLAlchemy==1.3.18 
RUN apt-get -y update
RUN apt-get -y install libpq-dev python-dev gcc && \
    apt-get clean
RUN pip install --no-cache-dir psycopg2

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["/bin/sh","-c","/app/wait-for-it.sh db:5432 -t 30 -- python app.py"]