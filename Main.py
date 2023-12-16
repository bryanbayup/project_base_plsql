from flask import Flask, request, jsonify, send_from_directory
from Crypto.Cipher import AES
import base64
import psycopg2
import os

app = Flask(__name__)

# Fungsi Enkripsi dan Dekripsi menggunakan AES
def encrypt(text, key):
    key = key.ljust(32)
  # Sesuaikan panjang kunci menjadi 32 byte
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(text.ljust(32).encode('utf-8'))
    return base64.b64encode(cipher.iv + ciphertext)

def decrypt(encrypted_text, key):
    key = key.ljust(32)
  # Sesuaikan panjang kunci menjadi 32 byte
    encrypted_text = base64.b64decode(encrypted_text)
    iv = encrypted_text[:16]
    ciphertext = encrypted_text[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(ciphertext).rstrip().decode('utf-8')

# Koneksi ke PostgreSQL
conn = psycopg2.connect(
    database="db_uts",
    user="postgres",
    password="bayubryan",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Endpoint untuk handle root URL
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the microservice application!"})

# Endpoint untuk handle favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Endpoint untuk CRUD User
@app.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_user():
    if request.method == 'POST':
        # Create User
        data = request.get_json()
        username = data['username']
        password = data['password']
        encrypted_password = encrypt(password, b'secret_key')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, encrypted_password))
        conn.commit()
        return jsonify({"message": "User created successfully"})

    elif request.method == 'GET':
        # Read User
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        decrypted_users = [{"username": user[1], "password": decrypt(user[2], b'secret_key')} for user in users]
        return jsonify({"users": decrypted_users})

    elif request.method == 'PUT':
        # Update User
        data = request.get_json()
        username = data['username']
        new_password = data['new_password']
        encrypted_password = encrypt(new_password, b'secret_key')
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (encrypted_password, username))
        conn.commit()
        return jsonify({"message": "User updated successfully"})

    elif request.method == 'DELETE':
        # Delete User
        data = request.get_json()
        username = data['username']
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
