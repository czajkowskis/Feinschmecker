"""
Gunicorn configuration for Feinschmecker API production deployment.

This configuration provides production-ready settings for the WSGI server.
"""

import multiprocessing
import os

# Server socket
bind = f"{os.getenv('GUNICORN_BIND', '0.0.0.0')}:{os.getenv('GUNICORN_PORT', '8000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')  # '-' for stdout
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')    # '-' for stderr
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'feinschmecker-api'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Application
wsgi_app = 'backend.website:app'

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Feinschmecker API server")

def on_reload(server):
    """Called to recycle workers during a reload."""
    server.log.info("Reloading Feinschmecker API server")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info(f"Feinschmecker API server is ready. Listening on {bind}")

def on_exit(server):
    """Called just before exiting."""
    server.log.info("Shutting down Feinschmecker API server")

