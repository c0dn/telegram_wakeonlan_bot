import pickle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pythonping import ping


def load_hosts(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []


def save_hosts(filename, hosts):
    with open(filename, "wb") as f:
        pickle.dump(hosts, f)


def build_host_list_markup(prefix):
    kb_markup = []
    host_list = load_hosts("hosts.pkl")
    for host in host_list:
        kb_markup.append([InlineKeyboardButton(host["name"], callback_data=f'{prefix}_{host["name"]}')])
    return InlineKeyboardMarkup(kb_markup)


def parse_host_info(message):
    lines = message.split("\n")
    if len(lines) != 3:
        return None
    return {
        "name": lines[0],
        "mac": lines[1],
        "ip": lines[2]
    }


def check_if_up(ip_address):
    res = ping(ip_address, count=1)
    if res.packets_lost == 0:
        return True
    else:
        return False
