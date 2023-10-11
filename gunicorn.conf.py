worker_class = "gevent"
workers = 3
timeout = 2000
bind = "0.0.0.0:5000"
wsgi_app = "wsgi:app"
# errorlog = "logging/error.log"
capture_output = True
# loglevel = "debug"

