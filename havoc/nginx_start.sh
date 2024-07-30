#!/bin/bash

# install nginx
sudo apt-get update
sudo apt-get install -y nginx

# copy config file
echo "server {
        listen 80;
        listen [::]:80;

        server_name malware-training.us.to;

        root /opt/malware-training.us.to/;
        index index.html;

        location / {
                try_files $uri $uri/ =404;
        }
}" > /etc/nginx/sites-available/malware-training.us.to-test

# enable site
sudo ln -s /etc/nginx/sites-available/malware-training.us.to-test /etc/nginx/sites-enabled/

# restart nginx
sudo systemctl restart nginx
