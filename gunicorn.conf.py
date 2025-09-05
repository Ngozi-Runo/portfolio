# Gunicorn configuration file

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "portfolio_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/portfolio.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
