from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os

# Create Flask app instance
app = Flask(__name__)

# Get the absolute path for the database file
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'notes.db')

# Initialize database
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Routes for the notes app
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content', '')
    if content.strip():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": note_id, "content": content}), 201
    return jsonify({"error": "Content cannot be empty"}), 400

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note deleted"}), 200

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def edit_note(note_id):
    data = request.json
    content = data.get('content', '')
    if content.strip():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE notes SET content = ? WHERE id = ?', (content, note_id))
        conn.commit()
        conn.close()
        return jsonify({"id": note_id, "content": content}), 200
    return jsonify({"error": "Content cannot be empty"}), 400

if __name__ == '__main__':
    app.run(debug=True)
