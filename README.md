# STM32U5_AWS_QuickConnect for ST 2022 DevCon and TT workshop

Create IAM user

Install AWS CLI

AWS configure and setup the default profile. The script requires a AWS CLI profile called **default**

git clone https://github.com/SlimJallouli/ST_DevCon_2022_AWS_Workshop.git

cd ST_DevCon_2022_AWS_Workshop

cd STM32U5_AWS_QuickConnect

pip install -r requirements.txt

Connect your STM32U5 IoT Discovery node to your PC

python STM32U5_AWS_QuickConnect.py --ssid=MYSSID --password=MYPASSWORD
