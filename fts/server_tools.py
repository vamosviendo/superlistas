from fabric.api import run
from fabric.context_managers import settings, shell_env


def _encontrar_manage_punto_py(host):
    return f'~/sites/{host}/vlistas/bin/python ~/sites/{host}/manage.py'


def _obtener_vars_env_server(host):
    env_lines = run(f'cat ~/sites/{host}/.env').splitlines()
    return dict(l.split('=') for l in env_lines if l)


def reset_database(host):
    manage_pto_py = _encontrar_manage_punto_py(host)
    with settings(host_string=f'nando@{host}'):
        run(f'{manage_pto_py} flush --noinput')


def crear_sesion_en_server(host, email):
    manage_pto_py = _encontrar_manage_punto_py(host)
    with settings(host_string=f'nando@{host}'):
        env_vars = _obtener_vars_env_server(host)
        with shell_env(**env_vars):
            session_key = run(f'{manage_pto_py} create_session {email}')
            return session_key.strip()