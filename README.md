**Auto post discord**

# Deskripsi file
- `main.py`: file utama dalam auto post!
- `config.json`: adalah konfigurasi untuk auto post!


# Instalasi
- Clone repositori ini: `git clone https://github.com/Yasurooo/Yasurooo.git`
Masuk ke direktori proyek: `cd Yasurooo`


# Konfigurasi
- edit pada `config.json`: untuk mengatur token, channel, webhook, pesan, kecepatan

# Jalankan
- pastikan anda sudah menginstall Python sebelummnya
- install dependensi `requests` dengan cara `pip install requests`
- jalankan main dengan cara `python main.py`

# Configuration
```json
{
    "TOKEN": "INPUT_UR_TOKEN",
    "CHANNELS": [
        {
            "id": "YOUR_ID_CHANNEL",
            "delay": 1, // 1 minutes because * 60 seconds
            "message": "INPUT_YOUR_MESSAGE"
            
        },
        {
            "id": "YOUR_ID_CHANNEL",
            "delay": 1, // 1 minutes because * 60 seconds
            "message": "INPUT_YOUR_MESSAGE"
        }
    ],
    "LOG_WEBHOOK_URL": "INPUT_URL_WEBHOOK"
}
```
