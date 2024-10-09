import requests
import time
import json
from datetime import datetime

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']  # Personal account token
CHANNEL_ID = config['CHANNEL_ID']  # Channel ID
LOG_WEBHOOK_URL = config['LOG_WEBHOOK_URL']  # Webhook URL for logs
PERSONAL_MESSAGE = config['PERSONAL_MESSAGE']  # Personal message to send
DELAY_SECONDS = config.get('DELAY_SECONDS', 60)  # Delay from config or default to 60 seconds

# Start time (for uptime tracking)
start_time = datetime.now()

# Initialize message count
message_count = 0

# Function to format and calculate uptime
def format_uptime(start_time):
    uptime_duration = datetime.now() - start_time
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

# Function to send a message using a personal account with an enhanced embed
def send_message_personal(content):
    global message_count  # Use the global message count
    url = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
    }

    # Calculate uptime in a formatted way
    formatted_uptime = format_uptime(start_time)

    # Create a more visually appealing embed
    embed = {
        "title": "🔔 Auto Post Information",
        "description": content,
        "color": 808080,
        "fields": [
            {
                "name": "📅 Uptime",
                "value": formatted_uptime,
                "inline": True
            },
            {
                "name": "⏱️ Delay",
                "value": f"{DELAY_SECONDS} detik",
                "inline": True
            },
            {
                "name": "💬 Channel",
                "value": f"<#{CHANNEL_ID}>",  # Format for channel mention
                "inline": True
            },
            {
                "name": "📊 Message Count",
                "value": str(message_count + 1),  # Increment message count
                "inline": True
            },
            {
                "name": "📌 Note",
                "value": "This message is sent automatically. Please do not reply.",
                "inline": False
            }
        ],
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1287019453921493103/1293534663041876060/1728202990241.jpg?ex=6707b988&is=67066808&hm=1c995747e4cbc8a028bd36090492ddf6677e7c2fd2980b0cc265935b7defde49&"
        },
        "image": {
            "url": "https://cdn.discordapp.com/attachments/1287019453921493103/1293534663041876060/1728202990241.jpg"  # Example image URL
        },
        "footer": {
            "text": "Auto Post By Void Server © 2024",
            "icon_url": "https://cdn.discordapp.com/attachments/1287019453921493103/1292401890813939764/images_1.jpg"
        },
        "timestamp": str(datetime.now())
    }

    # Send embed in JSON payload
    json_data = {
        'content': content,
        'embeds': [embed]
    }

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        message_count += 1  # Increment message count on successful send
        log_message(embed, channel_id=CHANNEL_ID)  # Log embed directly
    elif response.status_code == 429:
        # Handle rate limit error
        retry_after = response.json().get('retry_after', 0) / 1000  # Get retry time in seconds
        print(f"Rate limit hit! Retrying after {retry_after:.2f} seconds.")
        time.sleep(retry_after)  # Wait before retrying
        send_message_personal(content)  # Retry sending the message
    else:
        # Log error message as a string
        log_message(f"Pesan pribadi gagal dikirim: {content} - Status Code: {response.status_code} - {response.text}",
                    status="Error", channel_id=CHANNEL_ID)

# Function to log messages using Webhook
def log_message(log_content, status="Success", channel_id=None, message_content=None):
    log_data = {}
    
    # Handle successful and error logs
    if isinstance(log_content, dict):
        # Create log embed for successful messages
        log_embed = {
            "title": "🟢 **Void Room's**",
            "description": "Pesan berhasil dikirim.",
            "color": 5763719,  # Greenish color for success
            "fields": [
                {
                    "name": "**Original Message:**",
                    "value": log_content["description"] if message_content is None else message_content,
                    "inline": False
                },
                {
                    "name": "📅 **Uptime**",
                    "value": format_uptime(start_time),
                    "inline": True
                },
                {
                    "name": "🔔 **Status**",
                    "value": status,  # Status: Success
                    "inline": True
                },
                {
                    "name": "💬 **Channel**",
                    "value": f"<#{channel_id}>" if channel_id else "N/A",  # Mention channel
                    "inline": True
                }
            ],
            "thumbnail": {
                "url": "https://cdn.discordapp.com/attachments/1287019453921493103/1293534663041876060/1728202990241.jpg"  # Example thumbnail URL
            },
            "footer": {
                "text": "Auto post by Void Server",
                "icon_url": "https://cdn.discordapp.com/attachments/1287019453921493103/1293534663041876060/1728202990241.jpg?ex=6707b988&is=67066808&hm=1c995747e4cbc8a028bd36090492ddf6677e7c2fd2980b0cc265935b7defde49&"
            },
            "timestamp": str(datetime.now())
        }
    else:
        # Create log embed for error messages
        log_embed = {
            "title": "🔴 **Void Room's**",
            "description": log_content,  # Take error message as description
            "color": 15158332,  # Red color for errors
            "fields": [
                {
                    "name": "**Original Message:**",
                    "value": message_content if message_content else "N/A",
                    "inline": False
                },
                {
                    "name": "📅 **Uptime**",
                    "value": format_uptime(start_time),
                    "inline": True
                },
                {
                    "name": "🔔 **Status**",
                    "value": status,  # Status: Error
                    "inline": True
                },
                {
                    "name": "💬 **Channel**",
                    "value": f"<#{channel_id}>" if channel_id else "N/A",  # Mention channel
                    "inline": True
                }
            ],
            "thumbnail": {
                "url": "https://cdn.discordapp.com/attachments/1287019453921493103/1293534663041876060/1728202990241.jpg"  # Example thumbnail URL
            },
            "footer": {
                "text": "Auto Post Logs!",
                "icon_url": "https://cdn.discordapp.com/attachments/1287019453921493103/1292401890813939764/images_1.jpg"
            },
            "timestamp": str(datetime.now())
        }

    log_data = {
        "embeds": [log_embed],
        "username": "Auto Post Logs"  # Log sender name
    }

    response = requests.post(LOG_WEBHOOK_URL, json=log_data)

    if response.status_code == 204:
        print("Log berhasil dikirim!")
    else:
        print(f"Terjadi kesalahan saat mengirim log: {response.status_code} - {response.text}")

if __name__ == "__main__":
    while True:
        # Send message using personal account
        send_message_personal(PERSONAL_MESSAGE)
        
        # Delay based on configured interval
        time.sleep(DELAY_SECONDS)
