import telebot
import requests
import argparse
import socket
import json
from datetime import datetime

parser = argparse.ArgumentParser(
    prog="Send IP",
    description="Script can send the internal and/or external IP Adress to a Telegram channel using a Telegram Bot",
)

parser.add_argument("token", help="the telegram API Token from Botfather", type=str)
parser.add_argument(
    "chat", help="the telegram chat ID to send the messages to", type=str
)
parser.add_argument(
    "-s",
    "--file",
    help="the file where to store the last ip",
    type=str,
    default="last_ips.json",
)
parser.add_argument(
    "-n",
    "--name",
    help="device name to send in the message",
    type=str,
    default="Device",
)
parser.add_argument(
    "-f",
    "--force",
    help="set flag to force send message, even if IP did not change",
    action="store_true",
)
parser.add_argument(
    "-i", "--internal", help="set flag to send the internal IP", action="store_true"
)
parser.add_argument(
    "-e", "--external", help="set flag to send the external IP", action="store_true"
)
args = parser.parse_args()
# print(args)
# Replace with your Telegram bot API token from BotFather
API_TOKEN = args.token
# Replace with your chat ID
CHAT_ID = args.chat

# Set up the bot
bot = telebot.TeleBot(API_TOKEN)

file_name = args.file
force_send = args.force


def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except requests.RequestException as e:
        return f"Error retrieving external IP address: {e}"


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    # print(socket.gethostbyname(socket.gethostname()))
    return ip


def compare_last_ip(ip):
    try:
        with open(file_name, "r") as file:
            last_ip = file.read()
            print("last:", last_ip)
            if last_ip != ip:
                with open(file_name, "w") as file:
                    file.writelines(ip)
            return last_ip != ip, last_ip
    except FileNotFoundError:
        with open(file_name, "w") as file:
            file.writelines(ip)
        return True, "No IP"


def send_ip_address():
    try:
        with open(file_name, "r") as ips_json_file:
            last_ips = json.load(ips_json_file)
    except FileNotFoundError:
        last_ips = {"internal": "No IP", "external": "No IP", "timestamp": None}

    message = None

    if args.internal:
        new_internal = get_internal_ip()
        print(f"Internal: {new_internal} ⬅️ {last_ips['internal']}")
        if new_internal != last_ips["internal"] or force_send:
            message = f"\nInternal: `{new_internal}` ⬅️ `{last_ips['internal']}`"
            last_ips["internal"] = new_internal

    if args.external:
        new_external = get_external_ip()
        print(f"External: {new_external} ⬅️ {last_ips['external']}")
        if new_external != last_ips["external"] or force_send:
            if message is None:
                message = ""
            message += f"\nExternal: `{new_external}` ⬅️ `{last_ips['external']}`"
            last_ips["external"] = new_external

    if message is not None:
        message = (
            f"📡 **{args.name} IP Address** 🌐"
            + message
            + f"\nSince: {last_ips['timestamp']}"
        )
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")
        last_ips["timestamp"] = str(datetime.now())
        with open(file_name, "w") as outfile:
            json.dump(last_ips, outfile)


if __name__ == "__main__":
    send_ip_address()
