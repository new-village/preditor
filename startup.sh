#!/bin/sh

EXC_USER=centos
VENV_DIR=/home/${EXC_USER}/.venv/preditor/
SHL_NAME=`echo ${0##*/}|sed -e "s/.sh//g"`
SHL_DIR=$(cd $(dirname $0); pwd)
SHL_FILE=${SHL_DIR}/${SHL_NAME}.sh

cd ${SHL_DIR}
source ${VENV_DIR}/bin/activate
sudo `which python` ${SHL_DIR}/manage.py runserver --insecure 0.0.0.0:80 &
sudo -u ${EXC_USER} `which python` ${SHL_DIR}/manage.py shell_plus --notebook &
sudo -u ${EXC_USER} `which python` ${SHL_DIR}/manage.py collector &

exit
