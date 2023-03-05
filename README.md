# Fake CSV Generator
Django online service for generating CSV files with fake data.

# Check it out!
[Project deployed to PythonAnywhere](http://skantor.pythonanywhere.com/schemas/)

Test User
- Login: admin
- password: admin

## Installation

Python3 must be already installed

```shell
git clone https://github.com/KantorSerhiy/fake-csv-generator.git
python -m venv venv
venv\Scripts\activate (on Windows)
venv\bin\activate (on Linux)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
