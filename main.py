import os
import subprocess
from pathlib import Path


########  Edit!!! ########

TERMINAL = 'xfce4-terminal'

##########################

BASE_DIC = os.getcwd()
project_name = None
folder = ""

list_apps = ["users", "core"]
requirements = ["django", "psycopg2"]
requirements_text = ""
apps_commands = ""
install_all = ""

urls_system = f'''from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]'''

urls_core = '''from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
'''

core_views = '''from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

'''

def wellcome():
    print("Bem vindo!!")
    print("Este script automatiza parte do processo de criação de projetos com django\n")
    get_requirements()


def get_requirements():
    global folder, project_name
    project_name = input('Digite o nome do projeto:\n')
    folder = f"{BASE_DIC}/{project_name}/"
    query = input('Digite os requisitos do seu projeto separados por espaços\n')
    r = query.split()
    requirements.extend(r)
    get_apps()


def get_apps():
    query = input('Digite o nome dos apps para adicionar a seu projeto separados por espaços\n'
                  'apps padrao: core e users\n')
    a = query.split()
    list_apps.extend(a)
    create_project_folder()


def create_project_folder():
    path = Path(folder)
    Path.mkdir(path)
    create_venv()


def create_venv():
    global apps_commands, install_all
    apps_commands = create_apps()
    install_all = create_requirements_commands()
    create_project = f' django-admin startproject system .; touch .gitignore; cd system/;' \
                     f' echo "{urls_system}" > urls.py; {apps_commands}'
    subprocess.call([f"{TERMINAL}", "-x", "sh", "-c", f"cd {folder}; {install_all}; {create_project}"])



def create_apps():
    apps = [create_app_commands(x) for x in list_apps]
    return "".join(apps)


def create_app_commands(item):
    if item == 'users':
        text = f'cd {folder}; django-admin startapp {item}; cd {item}/; touch urls.py; touch forms.py; ' \
               f'mkdir templates/; mkdir static/;'
    else:
        text = f'cd {folder}; django-admin startapp {item}; cd {item}/; echo "{urls_core}" > urls.py;' \
               f' echo "{core_views}" > views.py; mkdir templates/; mkdir static/;'
    return text


def create_requirements_commands():
    global requirements_text
    r = [f"{item}\n" for item in requirements]
    requirements_text = "".join(r)
    return f'python3 -m venv venv; source venv/bin/activate; echo "{requirements_text}" > requirements.txt;' \
                  f' pip install -r requirements.txt'


wellcome()
