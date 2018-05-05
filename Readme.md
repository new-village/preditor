# Preditor
[![Maintainability](https://api.codeclimate.com/v1/badges/24c93adbb5f02cec1d75/maintainability)](https://codeclimate.com/github/New-Village/preditor/maintainability)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)  
Preditor is a all-in-one Japanese horse race (Keiba) prediction system written by Python.
The system is possible to provide all functions about prediction like extract data, transform, prediction and reporting.


## How to Start
Prerequisites: You have to set up in advance below:
* Python 3.6
* PostgreSQL
* sudo privileges without password

If you would like to start this project in your environment, you have to do below:
1. Clone this project.
2. To set up the environment, execute the following command in terminal:
```console
# Install Libraries
pip install -r requirements.txt --upgrade
```
3. To available of the local setting variables, rename "mysite/local_template.py" to "mysite/local.py".
4. To define the database information, change database connection parameters of "mysite/local.py".
* You have to set up database in advance (I recommend to use PostgreSQL).
5. To set up the Schema, execute the following command in terminal:
```console
# Setup databases
cd ${PYTHON_PROJECT_DIR}
./manage.py migrate
# Create administrator
./manage.py createsuperuser
# Set password of jupyter
jupyter notebook password
```
7. To available of web console, change EXC_USER and VENV_DIR of startup.sh.
```shell
EXC_USER=preditor
VENV_DIR=/home/${EXC_USER}/.venv/preditor
```
8. Execute startup.sh
```console
cd ${PYTHON_PROJECT_DIR}
chmod +x startup.sh
./startup.sh
```
* You can access Django admin view (http://127.0.0.1/admin)
* Also access Jupyter notebook (http://127.0.0.1:8888/)
* After a short time, start collection of latest race data
9. To collect history data, execute the following command in terminal:
```console
# Start Shell
./manage.py collector --from 20170101
```
* 20170101 means collecting race data from January 1, 2017 to This Month. if you would like to collect more, you can set older date formatted at YYYYMMDD.
10. To prediction future races, execute Sample.ipynb from jupyter notebook.


## History
|    Date    | Version | Comment                                                                              |
|:----------:|:-------:|--------------------------------------------------------------------------------------|
| 2018/01/07 |   1.0   | Released Initial Version. It is only possible to collect and enrich horse race data. |
| 2018/02/12 |   1.5   | Support PostgreSQL and Jupter Notebook. Improve crawling logic.                      |
| 2018/05/05 |   2.0   | Adding sample model and operating functions. Improving application architecture.     |


## Reference
#### Data Source
* [NetKeiba.com](http://db.netkeiba.com/) (Japanese Only)
* [SportsNavi](https://keiba.yahoo.co.jp/) (Japanese Only)

#### Development
* [Django documentation](https://docs.djangoproject.com/en/2.0/)
