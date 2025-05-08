# bind = "127.0.0.1:8000"
# loglevel = "info"
# worker_class = "uvicorn.workers.UvicornWorker"
# gunicorn.conf.py
bind = "0.0.0.0:8082"
workers = 2
loglevel = "info"
accesslog = "-"
errorlog = "-"
 