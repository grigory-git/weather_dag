sudo apt install python3 python3-pip
sudo apt install python3-pip
sudo apt-get update
sudo apt install python3 python3-pip
lsb_release -a
python3 -m venv airflow_venv
source airflow_venv/bin/activate
sudo apt update
sudo service networking restart
sudo apt update
sudo apt install python3.10-venv
source airflow_venv/bin/activate
cd ~
python3 -m venv airflow_venv
source airflow_venv/bin/activate
pip install apache-airflow
airflow db init
airflow webserver --port 8080
ps aux | grep airflow
sudo kill -9 2617
sudo reboot
sudo adduser airflow
sudo usermod -aG sudo airflow
su - airflow
source /home/grigory/airflow_venv/bin/activate
airflow webserver
airflow db init
airflow webserver
which airflow
whereis airflow
pip show apache-airflow
dpkg -l | grep airflow
find / -name "airflow" 2>/dev/null
