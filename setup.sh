#!/data/data/com.termux/files/usr/bin/bash

pkg update -y && pkg install -y python git unzip
pip install flask

cd ~/BROKEN_ETHICS_REPO || exit 1

[ ! -f database.db ] && python3 -c "import sqlite3; sqlite3.connect('database.db').execute('CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, item TEXT, email TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')"

nohup python3 server.py &
echo "Server running on 10.0.0.223:5000"
