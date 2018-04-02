# Preditor
[![Maintainability](https://api.codeclimate.com/v1/badges/24c93adbb5f02cec1d75/maintainability)](https://codeclimate.com/github/New-Village/preditor/maintainability)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)  
Preditor is a all-in-one Japanese horse race (Keiba) prediction system written by Python.
The system is possible to provide all functions about prediction like extract data, transform, prediction and reporting.


## How to Start
If you would like to start your environment, you have to do below.

1. Clone this project.
2. To set up the environment, execute the following command in terminal:
```console
# Install Libraries
pip install -r requirements.txt --upgrade
```
3. To define the database information, rename "mysite/local_template.py" to "mysite/local.py"
4. To set up the database, execute the following command in terminal:
```console
# Setup databases
./manage.py makemigrations
./manage.py migrate
# Create administrator
./manage.py createsuperuser
# Set password of jupyter
jupyter notebook password
```
5. To start data collection, execute the following command in terminal:
```console
# Start Shell
./manage.py collector
./manage.py collector --from YYYYMMDD
```

## Management View
This app can provide data management view. If you would like to access, you have to do below.
```console
# Run server
nohup sudo `which python3` ./manage.py runserver 0.0.0.0:80 &
nohup ./manage.py shell_plus --notebook &
```
* Index View: http://127.0.0.1/
* Jupyter: http://127.0.0.1:8888/


## History
|    Date    | Version | Comment                                                                              |
|:----------:|:-------:|--------------------------------------------------------------------------------------|
| 2018/01/07 |   1.0   | Released Initial Version. It is only possible to collect and enrich horse race data. |
| 2018/02/12 |   1.5   | Support PostgreSQL and Jupter Notebook. Improve crawling logic.                      |
| 2018/04/02 |   2.0   | Refactoring architecture.                                                            |


## Reference
#### Data Source
* [NetKeiba.com](http://db.netkeiba.com/) (Japanese Only)
* [SportsNavi](https://keiba.yahoo.co.jp/) (Japanese Only)

#### Development
* [Django documentation](https://docs.djangoproject.com/en/2.0/)
