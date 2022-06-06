FROM tiangolo/uwsgi-nginx-flask:python3.10
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
ENV NGINX_WORKER_PROCESSES 1
ENV UWSGI_INI /app/uwsgi.ini
COPY ./app /app
