from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

ADMIN_USERNAME = "Admin404"
ADMIN_PASSWORD = "11221122aA@"
EMAIL_ALERT = "BrokenEthicsMarket@cyberservices.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy', methods=['POST'])
def buy():
    item = request.form.get('item')
    email = request.form.get('email')

    # Save sale
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO sales (item, email) VALUES (?, ?)", (item, email))
        conn.commit()

    # Send alert email
    try:
        msg = MIMEText(f"New order placed:\nItem: {item}\nEmail: {email}")
        msg['Subject'] = "New Sale - BrokenEthics"
        msg['From'] = EMAIL_ALERT
        msg['To'] = EMAIL_ALERT

        s = smtplib.SMTP('smtp.cyberservices.com')
        s.send_message(msg)
        s.quit()
    except Exception as e:
        print("Email failed:", e)

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute("SELECT * FROM sales ORDER BY timestamp DESC")
        sales = cur.fetchall()
    return render_template('admin.html', sales=sales)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        with sqlite3.connect("database.db") as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, item TEXT, email TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    app.run(host='0.0.0.0', port=5000)
