import os
import subprocess
from pathlib import Path
import art

urls_system = f'''from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]'''

urls_base = '''from django.urls import path

from . import views


urlpatterns = [
    path('', views, name=''),
]
'''

class DjangoScript:
    def __init__(self):
      #### Edit this ####################

        self.terminal = 'xfce4-terminal'

      ###################################

        self.BASE_DIC = os.getcwd()
        self.project_name = None
        self.folder = ""

        self.list_apps = ["users", "core"]
        self.requirements = ["django", "psycopg2"]
        self.requirements_text = ""
        self.apps_commands = ""
        self.install_all = ""

    def wellcome(self):
        art.tprint(f'{" " * 5} DjangoForge', 'tarty1')
        print(f"{'-' * 36} https://github.com/plotzZzky {'-' * 36}\n")
        print("Este script automatiza parte do processo de criação de projetos com django\n")
        self.get_requirements()

    def get_requirements(self):
        self.project_name = input('Digite o nome do projeto:\n')
        self.folder = f"{self.BASE_DIC}/{self.project_name}/"
        query = input('Digite os requisitos do seu projeto separados por espaços\n')
        r = query.split()
        self.requirements.extend(r)
        self.get_app_list()

    def get_app_list(self):
        query = input('Digite o nome dos apps para adicionar a seu projeto separados por espaços\n'
                      'apps padrao: core e users\n')
        a = query.split()
        self.list_apps.extend(a)
        self.create_project_folder()

    def create_project_folder(self):
        path = Path(self.folder)
        Path.mkdir(path)
        self.create_venv()

    def create_venv(self):
        front_command = f"npx create-react-app front; cd front/src/; mkdir elements/"
        self.apps_commands = self.create_apps()
        install_all = self.create_requirements_commands()
        create_project = f' django-admin startproject system .; touch .gitignore; cd system/;' \
                         f' echo "{urls_system}" > urls.py; {self.apps_commands}'
        subprocess.call([f"{self.terminal}", "-x", "sh", "-c", f"cd {self.folder}; {front_command}; cd {self.folder};"
                        f"mkdir back/; cd back/; {install_all}; {create_project}"])

    def create_apps(self):
        apps = [self.create_app_commands(x) for x in self.list_apps]
        return "".join(apps)

    # Gera o comando para criar cada django-app
    def create_app_commands(self, item):
        if item == 'users':
            text = f'cd {self.folder}/back/; django-admin startapp {item}; cd {item}/; echo "{urls_base}" > urls.py;'
        else:
            text = f'cd {self.folder}/back/; django-admin startapp {item}; cd {item}/; echo "{urls_base}" > urls.py;'
        return text

    # gera a lista com as dependências do projeto
    def create_requirements_commands(self):
        r = [f"{item}\n" for item in self.requirements]
        self.requirements_text = "".join(r)
        return f'python3 -m venv venv; source venv/bin/activate; echo "{self.requirements_text}" > requirements.txt;' \
               f' pip install -r requirements.txt'


app = DjangoScript()
app.wellcome()