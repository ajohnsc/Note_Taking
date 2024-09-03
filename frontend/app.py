from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)
api_url = os.getenv('API_URL')

@app.route('/notes')
def list_notes():
    response = requests.get(f'{api_url}/notes')
    notes = response.json()
    return render_template('index.html', notes=notes)

@app.route('/notes/new', methods=['POST'])
def new_note():
    title = request.form['title']
    body = request.form['body']
    response = requests.post(f'{api_url}/notes', json={'title': title, 'body': body})
    return redirect(url_for('list_notes'))

@app.route('/notes/edit/<int:id>', methods=['POST'])
def edit_note(id):
    title = request.form['title']
    body = request.form['body']
    requests.put(f'{api_url}/notes/{id}', json={'title': title, 'body': body})
    return redirect(url_for('list_notes'))

@app.route('/notes/delete/<int:id>', methods=['POST'])
def delete_note(id):
    requests.delete(f'{api_url}/notes/{id}')
    return redirect(url_for('list_notes'))

if __name__ == "__main__":
    app.run(debug=True)
