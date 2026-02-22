bind = 'unix:/run/cmda/gunicorn.sock'
workers = 3
timeout = 30
accesslog = '/var/log/cmda/gunicorn-access.log'
errorlog = '/var/log/cmda/gunicorn-error.log'
