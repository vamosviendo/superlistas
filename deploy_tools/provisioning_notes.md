Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.8
* virtualenv + pip
* git

por ej, en Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudl apt update
    sudo apt install nginx git python3.8 python3.8-venv

## Nginx Virtual Host config

* Ver nginx.template.conf
* Reemplazar DOMAIN por, por ejemplo, staging.mi-dominio.com

## Systemd service

* Ver gunicorn-systemd.template.service
* Reemplazar DOMAIN por, por ejemplo, staging.mi-dominio.com

## Estructura de carpetas

Suponiendo que tenemos una cuenta de usuario en /home/nando

    /home/nando
    └── sites
        ├── DOMAIN1
        │    ├── .env
        │    ├── db.sqlite3
        │    ├── manage.py etc
        │    ├── static
        │    └── virtualenv
        └── DOMAIN2
             ├── .env
             ├── db.sqlite3
             ├── etc

