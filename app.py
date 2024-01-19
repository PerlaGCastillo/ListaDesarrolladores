from os import environ

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras

load_dotenv()
app = Flask(__name__)

host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn


@app.get('/developers')
def get_devs():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM developers')
    list = cur.fetchall()
    return jsonify(list)


@app.post('/developers')
def create_devs():
    new_dev = request.get_json()
    name = new_dev['name']
    age = new_dev['age']
    languages = new_dev['languages']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO developers (name, age, languages) VALUES(%s, %s, %s) RETURNING * ',
                (name, age, languages))
    created_dev = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(created_dev)


@app.get('/developers/<id>')
def get_dev(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM developers WHERE id = %s', (id,))
    dev = cur.fetchone()
    cur.close()
    conn.close()

    if dev is None:
        return jsonify({'message': 'La persona no fue encontrada'}), 404
    return jsonify(dev)


@app.put('/developers/<id>')
def update_dev(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_dev = request.get_json()
    name = new_dev['name']
    age = new_dev['age']
    languages = new_dev['languages']

    cur.execute('UPDATE developers SET name = %s, age = %s, languages = %s WHERE id = %s RETURNING *',
                (name, age, languages, id))
    updated = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    if updated is None:
        return jsonify({'message': 'Persona no encontrada'}), 404
    return jsonify(updated)


@app.delete('/developers/<id>')
def delete_dev(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('DELETE FROM developers WHERE id = %s RETURNING *', (id,))
    dev = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if dev is None:
        return jsonify({'message': 'Persona no encontrada'}), 404
    return jsonify(dev)


@app.get('/')
def home():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
