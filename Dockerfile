FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY backend /app

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]