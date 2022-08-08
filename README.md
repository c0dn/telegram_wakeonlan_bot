[![Python 3.7](https://img.shields.io/badge/Python-3.7%20or%20newer-blue.svg)](https://www.python.org/downloads/)
# Telegram Wake On Lan bot
This telegram bot allows you to wake up any computer on your network by sending a magic packet. Simply setup this bot on
a raspberry pi (or any SBC) and add your Telegram user id to the whitelist.

## Setup and Installation
### Add your telegram user id to the whitelist
custom_filters.py
```python
from pyrogram import filters
whitelist_user_ids = [] # Put whitelisted user ids here


def f_func(__, _, msg):
    if msg.from_user.id in whitelist_user_ids:
        return True
    else:
        return False


whitelist_filter = filters.create(f_func)
...
...
```
Only whitelisted users will be allowed to wake up computers on your network.
To get your telegram user id you can use [GetMyID bot](https://t.me/getmyid_bot) on Telegram.

### Get your API hash , API id and Bot token
Get your API hash and ID from [Telegram](https://my.telegram.org/auth). \
Login and create an application to get the API hash and ID. \
Get your bot token by creating a bot on [BotFather](https://t.me/botfather).

### Create virtual enviroment and install dependencies
The following commands should work for debian based systems. \
Python 3 should be installed on your system.

```bash
sudo apt-get install python3-pip python3-venv git
python3 -m venv venv
source venv/bin/activate
git clone https://github.com/c0dn/telegram_wakeonlan_bot.git
cd telegram_wakeonlan_bot
pip install -r requirements.txt
```
### First run setup
Ensure your virtual env is active.
```bash
source venv/bin/activate
```
Set the required enviroment variables.
```bash
export API_HASH=<your api hash>
export API_ID=<your api id>
export BOT_TOKEN=<your bot token>
```
Run the bot.
```bash
cd telegram_wakeonlan_bot
python3 main.py
```
The bot will quit after printing a session string. Save this string, you will need it to setup the bot.

### Creating the systemd service
Create a systemd service file. (example is provided below)
```bash
sudo vi /etc/systemd/system/wol_bot.service
```
Creating the overide folder and conf. (example is provided below)
```bash
sudo mkdir /etc/systemd/system/wol_bot.service.d
sudo vi /etc/systemd/system/wol_bot.service.d/override.conf
```

### Start the bot and enable the service
```bash
sudo systemctl daemon-reload
sudo systemctl start wol_bot
sudo systemctl enable wol_bot
```

### Example systemd service file
```systemd
[Unit]
Description=Telegram WOL bot
After=multi-user.target

[Service]
Type=simple
ExecStart=/home/pi/venv/bin/python3 /home/pi/telegram_wakeonlan_bot/main.py

[Install]
WantedBy=multi-user.target
```
### Example override.conf file (env variables)
```
[Service]
Environment="API_HASH=<YOUR_API_HASH>"
Environment="API_ID=<YOUR_API_ID>"
Environment="SESSION_STR=<YOUR_SESSION_STR>"
```
