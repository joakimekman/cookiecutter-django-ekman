======================
cookiecutter-django-ekman
======================

A simple, properly structured, cookiecutter template with a built-in user app.

Usage
-----

Install **cookiecutter**::

    $ pip install cookiecutter

Run cookiecutter against this repo::

    cookiecutter https://github.com/joakimekman/cookiecutter-django-ekman

Answer the questions prompted to you, and a project will be created.

Then, cd into the project::
  
  $ cd project_name
  
Install requirements::
  
  $ pip install -r requirements.txt
  
Create an **.env** file at root, and define your **SECRET_KEY**.

Customize the user models, views, templates, forms, etc. Then modify the tests, and have them pass. Last but not least, create a git repo and push it there::
  
  $ git init
  $ git add .
  $ git commit -m "first commit"
  $ git remote add origin https://github.com/username/project_name.git
  $ git push -u origin master
  
Due to the template structure, each app that you create should reside in the 2nd project directory::

  $ cd project_name
  $ python ../manage.py startapp myapp
  
Then, add the correct path to **apps.py** of the app::
 
  class MyAppConfig(AppConfig):
    name = "my_project.myapp"
 
