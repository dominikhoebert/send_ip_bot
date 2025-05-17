# send_ip_telegrambot

This is a simple python script that sends the public and/or local IP address of the machine to a notification service using Apprise.

## Simple Install using pipx

[pipx Installation](https://pipx.pypa.io/latest/installation/)

```bash
pipx install git+https://github.com/dominikhoebert/send_ip_telegrambot.git
```
## Usage

```bash
sendiptelegrambot --help

usage: Send IP [-h] [-s FILE] [-n NAME] [-f] [-i] [-e] token chat

Script can send the internal and/or external IP Adress to a Telegram channel using a Telegram Bot

positional arguments:
  url                   the Apprise URL to send the notification to

options:
  -h, --help            show this help message and exit
  -s FILE, --file FILE  the file where to store the last ip
  -n NAME, --name NAME  device name to send in the message
  -f, --force           set flag to force send message, even if IP did not change
  -i, --internal        set flag to send the internal IP
  -e, --external        set flag to send the external IP
```

```bash
sendiptelegrambot "apprise://telegram://API_TOKEN/CHAT_ID" -i -e
```

```bash
sendiptelegrambot "apprise://telegram://API_TOKEN/CHAT_ID" -f
```
