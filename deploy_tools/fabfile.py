import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/vamosviendo/superlistas.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    """ Si se trata de un deploy nuevo, ejecuta un 'git clone'.
        Si se trata de un deploy existente:
            - ejecuta un 'git fetch' para descargar los cambios.
            - ejecuta un 'git reset --hard' para eliminar cualquier cambio
              que se haya producido localmente en el servidor.
    """
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('vlistas/bin/pip'):
        run(f'python3.8 -m venv vlistas')
    run ('./vlistas/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('./vlistas/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./vlistas/bin/python manage.py migrate --noinput')
