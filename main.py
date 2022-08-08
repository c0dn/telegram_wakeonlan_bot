from pyrogram import Client, idle, filters
import os
import pickle
from pyrogram.types import BotCommand, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from wakeonlan import send_magic_packet

from custom_filters import whitelist_filter, callback_data_filter
from utils import load_hosts, parse_host_info, save_hosts, build_host_list_markup, check_if_up

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
try:
    bot_token = os.environ["BOT_TOKEN"]
except KeyError:
    bot_token = None
try:
    session_str = os.environ["SESSION_STR"]
except KeyError:
    session_str = None

if session_str:
    app = Client("tg_wol", session_string=session_str)
else:
    app = Client("tg_wol", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)


async def main():
    async with app:
        if not session_str:
            s_str = await app.export_session_string()
            print("Please save session string and use it in the future:")
            print(s_str)
        else:
            # Setting bot commands
            await app.set_bot_commands([
                BotCommand("start", "use this command to restart the bot if it's not responding"),
                BotCommand("add_host", "Add new host to list"),
                BotCommand("remove_host", "Remove host from list"),
                BotCommand("list_hosts", "List all hosts"),
                BotCommand("wake_host", "Wake host"),
            ])
            print("Bot is running")
            await idle()


@app.on_message(filters.command("start") & whitelist_filter)
async def welcome(_client: Client, message: Message):
    await message.reply_text("Welcome!")


@app.on_message(filters.command("add_host") & whitelist_filter)
async def add_host(_client: Client, message: Message):
    m = "Please send the host details in the following format:\n" \
        "Host name\n" \
        "MAC address\n" \
        "IP address\n" \
        "Example:\n" \
        "rogpc\n2C:54:91:88:C9:E3\n192.168.50.23"
    await message.reply_text(m)


@app.on_message(filters.command("remove_host") & whitelist_filter)
async def remove_host(client: Client, message: Message):
    await client.send_message(message.chat.id, "Please select the hostname to remove",
                              reply_markup=build_host_list_markup("remove"))


@app.on_message(filters.command("list_hosts") & whitelist_filter)
async def list_hosts(client: Client, message: Message):
    m = ""
    host_list = load_hosts("hosts.pkl")
    for host in host_list:
        m += f"**{host['name']}**\n"
        m += f"MAC: {host['mac']}\n"
        m += f"IP: {host['ip']}\n"
        if check_if_up(host['ip']):
            m += "Host is up\n"
        else:
            m += "Host is down\n"
        m += "\n"
    if m == "":
        m += "No hosts saved"
    await message.reply_text(m)


@app.on_message(filters.command("wake_host") & whitelist_filter)
async def wake_host(client: Client, message: Message):
    await client.send_message(message.chat.id, "Please select the host to wake",
                              reply_markup=build_host_list_markup("wake"))


@app.on_callback_query(callback_data_filter(None, "remove") & whitelist_filter)
async def remove_host_callback(_client: Client, callback_query: CallbackQuery):
    hostname = callback_query.data.split("_")[1]
    host_list = load_hosts("hosts.pkl")
    new_host_list = [h for h in host_list if h["name"] != hostname]
    save_hosts("hosts.pkl", new_host_list)
    await callback_query.edit_message_text(f"Removed host {hostname} successfully!")


@app.on_callback_query(callback_data_filter(None, "wake") & whitelist_filter)
async def wake_host_callback(_client: Client, callback_query: CallbackQuery):
    hostname = callback_query.data.split("_")[1]
    host_list = load_hosts("hosts.pkl")
    host = [h for h in host_list if h["name"] == hostname][0]
    if check_if_up(host['ip']):
        await callback_query.edit_message_text(f"Host {hostname} is already up!")
    else:
        mac_parsed = host["mac"].replace(":", ".")
        send_magic_packet(mac_parsed)
        await callback_query.edit_message_text(f"Magic packet sent sucessfully to {hostname} ({host['mac']})!")


@app.on_message(whitelist_filter)
async def handle_host_info(_client: Client, message: Message):
    host_list = load_hosts("hosts.pkl")
    host_info = parse_host_info(message.text)
    if host_info:
        host_list.append(host_info)
        save_hosts("hosts.pkl", host_list)
        await message.reply_text("Host added successfully!")
    else:
        await message.reply_text("Invalid host details!")


app.run(main())
