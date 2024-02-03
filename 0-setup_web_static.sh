#!/usr/bin/env bash
# setting up web servers for the deployment of web_static
apt-get update
apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -s -f /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

service nginx stop

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm 0-index.html my_index.html;
    }

    location /redirect_me {
        return 301 http://www.waza.org/404;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
