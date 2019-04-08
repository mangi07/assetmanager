# Asset Management System

Copyright Benjamin R. Olson - All Rights Reserved


## pythonanywhere.com setup

1. Open up a shell and clone this repo to your home directory.
2. Create a python virtual environment following the help section
    https://help.pythonanywhere.com/pages/DeployExistingDjangoProject
3. Run database migrations: `python manage.py migrate`
4. Collect static files into static/ under project root: `python manage.py collectstatic`
5. Create superadmin for the website: `python manage.py createsuperuser`

