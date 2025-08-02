from asyncio import open_connection
from flask import Flask, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',     # replace with your MySQL username
    'password': '123456',  # replace with your MySQL password
    'host': 'localhost',
    'database': 'quickdesk'
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create Ticket | QuickDesk</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .ticket-form {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 0 20px #0ff;
            border: 1px solid #0ff;
        }

        h2 {
            text-align: center;
            color: #00ffe7;
            margin-bottom: 25px;
        }

        input[type="text"],
        input[type="email"],
        textarea,
        select {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: none;
            outline: none;
            background: #1e1e2f;
            color: #fff;
            font-size: 1rem;
            margin-bottom: 15px;
            box-shadow: inset 0 0 5px #00ffe7;
        }

        input[type="file"] {
            margin-bottom: 15px;
        }

        .submit-btn {
            width: 100%;
            padding: 12px;
            background: #00ffe7;
            color: #000;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .submit-btn:hover {
            background: #00bfa6;
        }
    </style>
</head>
<body>

    <div class="ticket-form">
        <h2>Create a Ticket</h2>
        <form action="/create_ticket.py" method="POST" enctype="multipart/form-data">
            <label for="subject">Subject:</label>
            <input type="text" id="subject" name="subject" required>

            <label for="description">Description:</label>
            <textarea id="description" name="description" rows="4" required></textarea>

            <label for="category">Category:</label>
            <select id="category" name="category" required>
                <option value="Technical Support">Technical Support</option>
                <option value="Billing">Billing</option>
                <option value="General Inquiry">General Inquiry</option>
                <option value="Feedback">Feedback</option>
            </select>

            <label for="attachment">Attachment (optional):</label>
            <input type="file" id="attachment" name="attachment">

            <button type="submit" class="submit-btn">Submit Ticket</button>
        </form>
    </div>

</body>
</html>

    '''
@app.route('/create_ticket', methods=['POST'])
def submit():
        data=(request.form['subject'], 
              request.form['description'], 
              request.form['category'])
        conn= open_connection()
        cursor=conn.cursor()
def create_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR(255) NOT NULL,
            attachment VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
def create_ticket(subject, description, category, attachment=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    sql_query = '''
        INSERT INTO tickets (subject, description, category, attachment)
        VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql_query, (subject, description, category, attachment))
    conn.commit()
    ticket_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return ticket_id


    
    attachment = None
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file.filename != '':
            attachment = os.path.join('uploads', file.filename)
            file.save(attachment)
    
    ticket_id = create_ticket(subject, description, category, attachment)
    
    return f'Ticket created successfully! Ticket ID: {ticket_id}'

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
