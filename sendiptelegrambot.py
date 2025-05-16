# /// script
# dependencies = ["pyTelegramBotAPI"]
# ///


import telebot
import requests
import argparse
import socket
import json
from datetime import datetime
import time


def parse_args():
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
    return args
    # Replace with your Telegram bot API token from BotFather


def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except requests.RequestException as e:
        return f"Error retrieving external IP address: {e}"


def get_internal_ip():
    retries = 10
    for attempt in range(retries):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except OSError as e:
            if e.errno == 101:  # Network is unreachable
                print(f"Attempt {attempt + 1}/{retries}: Network is unreachable. Retrying in 10 seconds...")
                time.sleep(10)
            else:
                raise
    print("Network is still unreachable after 10 attempts. Returning 0.0.0.0.")
    return "0.0.0.0"


def send_ip_address():
    args = parse_args()

    API_TOKEN = args.token
    CHAT_ID = args.chat
    bot = telebot.TeleBot(API_TOKEN)

    file_name = args.file
    force_send = args.force

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
