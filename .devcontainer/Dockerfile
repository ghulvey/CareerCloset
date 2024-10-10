FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m venv /workspace/venv
ENV PATH="/workspace/venv/bin:$PATH"

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt

RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY . /workspace/

EXPOSE 8000

RUN adduser --disabled-password --gecos "" devcontainer && chown -R devcontainer /workspace
USER devcontainer

RUN echo "source /workspace/venv/bin/activate" >> /home/devcontainer/.bashrc

CMD ["python", "manage.py", "runserver", "0.0.0.0", "8000"]