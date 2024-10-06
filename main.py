import requests
import time
import json
from datetime import datetime, timedelta

# Membaca konfigurasi dari config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']  # Token akun pribadi
CHANNEL_ID = config['CHANNEL_ID']  # ID channel
LOG_WEBHOOK_URL = config['LOG_WEBHOOK_URL']  # URL Webhook untuk log
PERSONAL_MESSAGE = config['PERSONAL_MESSAGE']  # Pesan pribadi yang ingin dikirim
DELAY_SECONDS = config.get('DELAY_SECONDS', 60)  # Ambil delay dari config atau gunakan default 60 detik

# Waktu mulai (untuk uptime)
start_time = datetime.now()

# Fungsi untuk menghitung dan merapikan uptime
def format_uptime(start_time):
    uptime_duration = datetime.now() - start_time
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_uptime = f"{days}d {hours}h {minutes}m {seconds}s"
    return formatted_uptime

# Fungsi untuk mengirim pesan menggunakan akun pribadi dengan embed
def send_message_personal(content):
    url = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'
    headers = {
        'Authorization': f'{TOKEN}',
        'Content-Type': 'application/json',
    }

    # Hitung uptime dengan format yang rapi
    formatted_uptime = format_uptime(start_time)

    # Buat embed dengan uptime, delay (interval), thumbnail, dan footer
    embed = {
        "title": "Auto post Information",
        "description": content,  # Ambil text dari personal_message
        "color": 5814783,  # Warna embed dalam format desimal (contoh: hijau)
        "fields": [
            {
                "name": "Uptime",
                "value": formatted_uptime,  # Menampilkan uptime yang rapi
                "inline": True
            },
            {
                "name": "Delay",
                "value": f"{DELAY_SECONDS} detik",  # Menampilkan delay dari config.json
                "inline": True
            }
        ],
        "thumbnail": {
            "url": "https://your-thumbnail-url.com/thumbnail.png"  # URL gambar untuk thumbnail
        },
        "footer": {
            "text": "Auto Post By Void Server © 2024",  # Informasi tambahan di footer
            "icon_url": "https://cdn.discordapp.com/attachments/1287019453921493103/1292401890813939764/images_1.jpg?ex=67039a8e&is=6702490e&hm=6be1e3a2aed5900184937bac30225d2b3bf3e7fda7c5442e9ac58ebdf2ece246&"  # URL gambar untuk icon footer
        },
        "timestamp": str(datetime.now())  # Waktu sekarang sebagai timestamp
    }

    # Kirim embed dalam payload JSON
    json_data = {
        'content': content,  # Menyertakan konten sebagai fallback
        'embeds': [embed]    # Hanya embed
    }

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        log_message(embed)  # Log embed secara langsung
    else:
        # Kirim pesan error ke log_message sebagai string
        log_message(f"Pesan pribadi gagal dikirim: {content} - Status Code: {response.status_code} - {response.text}")

# Fungsi untuk mencatat log menggunakan Webhook
def log_message(log_content):
    if isinstance(log_content, dict):
        # Jika log_content adalah dict (embed), buat embed log untuk pengiriman
        log_embed = {
            "title": "Messages Logs",
            "description": "Pesan berhasil dikirim.",
            "color": 5814783,  # Warna embed
            "fields": [
                {
                    "name": "Original Message",
                    "value": log_content["description"],  # Ambil deskripsi dari embed asli
                    "inline": False
                },
                {
                    "name": "Uptime",
                    "value": format_uptime(start_time),  # Uptime yang rapi
                    "inline": True
                },
                {
                    "name": "Status",
                    "value": "Success",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Auto post by Void Server",
                "icon_url": "https://cdn.discordapp.com/attachments/1287019453921493103/1292401890813939764/images_1.jpg?ex=67039a8e&is=6702490e&hm=6be1e3a2aed5900184937bac30225d2b3bf3e7fda7c5442e9ac58ebdf2ece246&"  # Gambar di footer log
            },
            "timestamp": str(datetime.now())
        }

        log_data = {
            "embeds": [log_embed],  # Mengirim embed sebagai log
            "username": "LogBot"  # Nama pengirim log
        }
    else:
        # Jika log_content adalah string (pesan error)
        log_embed = {
            "title": "Log Kesalahan",
            "description": log_content,  # Ambil pesan error
            "color": 16711680,  # Warna merah untuk kesalahan
            "footer": {
                "text": "Log Bot",
                "icon_url": "https://cdn.discordapp.com/attachments/1287019453921493103/1292401890813939764/images_1.jpg?ex=67039a8e&is=6702490e&hm=6be1e3a2aed5900184937bac30225d2b3bf3e7fda7c5442e9ac58ebdf2ece246&"  # Gambar di footer log
            },
            "timestamp": str(datetime.now())
        }

        log_data = {
            "embeds": [log_embed],
            "username": "LogBot"  # Nama pengirim log
        }

    response = requests.post(LOG_WEBHOOK_URL, json=log_data)

    if response.status_code == 204:
        print("Log berhasil dikirim!")
    else:
        print(f"Terjadi kesalahan saat mengirim log: {response.status_code} - {response.text}")

if __name__ == "__main__":
    while True:
        # Kirim pesan menggunakan akun pribadi
        send_message_personal(PERSONAL_MESSAGE)
        
        # Interval waktu berdasarkan konfigurasi delay
        time.sleep(DELAY_SECONDS)
