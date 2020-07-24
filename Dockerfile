# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
RUN apt-get -y update && \
    apt-get -y install python3-dev libpq-dev gcc && \
    apt-get clean
    
RUN pip install --no-cache-dir pandas==1.0.5
RUN pip install --no-cache-dir SQLAlchemy==1.3.18 
RUN pip install --no-cache-dir psycopg2

RUN apt-get -y --purge autoremove python3-dev gcc

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
RUN chmod +x /app/wait-for-it.sh
LABEL Name=grasindo.api.seeder Version=0.0.1
CMD ["/bin/sh","-c","/app/wait-for-it.sh grasindo.api.products:1337 -t 30 -- python app.py"]
