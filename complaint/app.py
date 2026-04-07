from flask import Flask, render_template, request, redirect, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'replace_with_secure_random_key'

# 🔗 MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",   # put your mysql password
    database="complaint"
)

cursor = db.cursor(dictionary=True)

# 🏠 Home → Login Page
@app.route('/')
def home():
    return render_template('login.html')


# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, role))
        db.commit()

        return redirect('/')

    return render_template('register.html')


# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'citizen')

        query = "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s"
        cursor.execute(query, (email, password, role))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user.get('user_id', 1)
            session['role'] = role
            session['email'] = email
            
            # Role-based redirect
            if role == 'police':
                return redirect('/police_dashboard')
            else:
                return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template('login.html')


# 📊 Dashboard
@app.route('/dashboard')
def dashboard():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/login')
        
        query = "SELECT complaint_id, title, description, location, status, type as category FROM complaints WHERE user_id=%s ORDER BY complaint_id DESC"
        cursor.execute(query, (user_id,))
        complaints = cursor.fetchall()
        return render_template('dashboard.html', complaints=complaints)
    except Exception as e:
        print(f"Dashboard Error: {e}")
        return render_template('dashboard.html', complaints=[])


# 👮 Police Dashboard
@app.route('/police_dashboard')
def police_dashboard():
    try:
        # Check if user is authenticated and is police
        if session.get('role') != 'police':
            return redirect('/login')
        
        query = "SELECT complaint_id, user_id, title, description, location, status, type as category FROM complaints ORDER BY complaint_id DESC"
        cursor.execute(query)
        complaints = cursor.fetchall()
        return render_template('police_dashboard.html', complaints=complaints)
    except Exception as e:
        print(f"DEBUG - Police Dashboard Error: {e}")  # For console debugging
        return f"<h1>Error loading Police Dashboard</h1><p>Error: {str(e)}</p><p>Check MySQL connection and 'complaints' table</p><a href='/'>Back to Login</a>", 500


# 🔄 Update Complaint Status (Police Only)
@app.route('/update_complaint_status', methods=['POST'])
def update_complaint_status():
    data = request.json
    complaint_id = data.get('complaint_id')
    status = data.get('status')
    
    if session.get('role') != 'police':
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        query = "UPDATE complaints SET status=%s WHERE complaint_id=%s"
        cursor.execute(query, (status, complaint_id))
        db.commit()
        return jsonify({"success": True, "message": "Status updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# � Complaint Page
@app.route('/complaint')
def complaint():
    return render_template('complaint.html')


# 🚨 Submit Complaint
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    title = request.form['title']
    description = request.form['description']
    location = request.form['location']
    complaint_type = request.form.get('category', 'General')  # Use 'type' in DB
    user_id = session.get('user_id', 1)

    try:
        query = """INSERT INTO complaints 
                   (user_id, title, description, location, type, status) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, title, description, location, complaint_type, "Pending"))
        db.commit()
    except mysql.connector.Error as err:
        error_msg = str(err).lower()
        if 'unknown column' in error_msg or "column count doesn't match" in error_msg or 'column count' in error_msg:
            query = """INSERT INTO complaints 
                       (user_id, title, description, location, status) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (user_id, title, description, location, "Pending"))
            db.commit()
        else:
            return f"Database error: {err}"

    complaint_id = cursor.lastrowid
    return redirect(f'/complaint_submitted/{complaint_id}')


# 🔍 Track Complaint
@app.route('/track', methods=['GET'])
def track():
    complaint_id = request.args.get('id')
    if complaint_id:
        try:
            query = "SELECT complaint_id, title, description, location, type as category, status FROM complaints WHERE complaint_id=%s"
            cursor.execute(query, (complaint_id,))
            result = cursor.fetchone()

            if result:
                return jsonify(result)
            else:
                return jsonify({"status": "Not Found"})
        except Exception as e:
            return jsonify({"status": "Not Found"})

    return render_template('track.html')


# ✅ Complaint Submitted
@app.route('/complaint_submitted/<int:complaint_id>')
def complaint_submitted(complaint_id):
    return render_template('complaint_submitted.html', complaint_id=complaint_id)


# 🔒 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ▶ Run App
if __name__ == '__main__':
    app.run(debug=True)