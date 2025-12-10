from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import os
import pickle
import subprocess
from flask import make_response
import base64

app = Flask(__name__)
app.secret_key = 'insecure_secret_key_123'  # Intentional: Hardcoded secret

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                  username TEXT, 
                  password TEXT,
                  email TEXT,
                  is_admin INTEGER DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS secrets
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  secret_data TEXT)''')
    
    # Add default users
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@vulnfriend.com', 1)")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password123', 'alice@test.com', 0)")
    conn.commit()
    conn.close()

init_db()

# Vulnerabilities included:
# 1. SQL Injection
# 2. XSS
# 3. CSRF (no tokens)
# 4. Insecure Direct Object Reference
# 5. Command Injection
# 6. Insecure Deserialization
# 7. XXE (simulated)
# 8. Broken Authentication
# 9. Security Misconfiguration
# 10. Sensitive Data Exposure

@app.route('/')
def index():
    return render_template('index.html')

# VULN 1: SQL Injection
@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Intentional SQL Injection vulnerability
    c.execute(f"SELECT * FROM users WHERE username LIKE '%{query}%'")
    results = c.fetchall()
    conn.close()
    return jsonify(results)

# VULN 2: Broken Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # VULN: No password hashing
        c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[4]
            return redirect('/dashboard')
    
    return render_template('login.html')

# VULN 3: Insecure Direct Object Reference
@app.route('/profile/<int:user_id>')
def profile(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = c.fetchone()
    conn.close()
    return jsonify(user)

# VULN 4: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host', '127.0.0.1')
    # Intentional command injection vulnerability
    cmd = f"ping -c 1 {host}"
    result = subprocess.check_output(cmd, shell=True)
    return result

# VULN 5: Insecure Deserialization
@app.route('/cookie')
def set_cookie():
    data = request.args.get('data', '')
    # Intentional insecure deserialization
    try:
        decoded = base64.b64decode(data)
        obj = pickle.loads(decoded)
        return "Deserialized!"
    except:
        return "Invalid data"

# VULN 6: XSS
@app.route('/comment', methods=['POST'])
def comment():
    comment = request.form['comment']
    # Intentional XSS vulnerability (no sanitization)
    return f"<div>Your comment: {comment}</div>"

# VULN 7: CSRF (no protection)
@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user_id' not in session:
        return redirect('/login')
    
    amount = request.form['amount']
    to_user = request.form['to']
    # No CSRF token check
    return f"Transferred ${amount} to {to_user}"

# VULN 8: File Upload Vulnerability
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file"
    
    file = request.files['file']
    # VULN: No file validation
    file.save(f"uploads/{file.filename}")
    return "File uploaded!"

# VULN 9: Information Disclosure
@app.route('/debug')
def debug():
    # Exposes debug information
    return jsonify({
        'database_path': os.path.abspath('database.db'),
        'secret_key': app.secret_key,
        'users': session
    })

# VULN 10: XXE (simulated)
@app.route('/xml', methods=['POST'])
def xml_parse():
    data = request.data
    # Simulated XXE vulnerability
    if 'ENTITY' in str(data):
        return "XXE detected! Try to read /etc/passwd"
    return "XML processed"

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # VULN: Debug mode in production