# Books I Read

**This repository is arhived and will not be updated**

This was my personal project used to help me learn Flask and CSS. It's outdated and was not finished.

Simple [Flask](https://flask.palletsprojects.com/) app to track and review books that I am currently reading.

![screenshot](https://user-images.githubusercontent.com/2103126/91102376-b7f1ee00-e671-11ea-84cc-fec0257dd5ba.png)

## Installation and initialization

```bash
git clone https://github.com/droptune/books-i-read.git /path/to/app
cd /path/to/app

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize application
export FLASK_APP=bir
flask init-db
# Add user account
flask add-user username password
```

## Run with uwsgi

1. Cd to app directory and activate virtual environment.

2. Install uwsgi:

    ```bash
    pip install uWSGI
    ```

3. Create `bir.ini` in app directory:

    ```
    module = bir:create_app()
    master = true
    processes = 4
    socket = /var/run/books-i-read/bir.sock
    chmod-socket = 660
    vacuum = true
    die-on-term = true
    uid = 994
    gid = 991
    ```

4. Create systemd unit file `/etc/systemd/system/books-i-read.service`:

```
[Unit]
Description=uWSGI Books I Read
After=network.target

[Service]
User=nginx
Group=nginx
WorkingDirectory=/opt/bir/
Environment="PATH=/opt/bir/.venv/bin"
ExecStart=/opt/bir/.venv/bin/uwsgi --ini bir.ini

[Install]
WantedBy=multi-user.target
```

5. Run application

```bash
sudo systemctl start books-i-read
```

6. Install nginx and add configuration file into respective directory (e.g. `/etc/nginx/conf.d`):

```nginx
server {
    error_log /var/log/nginx/bir_error.log;
    access_log  /var/log/nginx/bir_access.log  main;
    listen       443 ssl http2;
    server_name www.domain.com;
    ssl_session_cache shared:SSL:1m;

	 # If you use Let's Encrypt certificate
    ssl_certificate /etc/letsencrypt/live/www.domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / { try_files $uri @bir; }
    location @bir {
        include uwsgi_params;
        uwsgi_pass unix:/var/run/books-i-read/bir.sock;
    }
}

# Listen on 80 port and redirect to https
server {
    listen 80;
    server_name www.domain.com;

    if ($host = www.domain.com) {
        return 301 https://$host$request_uri;
    }

    return 404;
}
```

7. Add `/etc/nginx/uwsgi_params` file if it is not present:

```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```

8. Reload nginx configuration

```bash
sudo systemctl reload nginx
```
