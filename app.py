from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Crypto.PublicKey import RSA

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from models import KeyPair

@app.route('/')
def index():
    key_pairs = KeyPair.query.all()
    return render_template('index.html', key_pairs=key_pairs)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        bits = int(request.form['bits'])
        key = RSA.generate(bits)
        public_key = key.publickey().export_key().decode('utf-8')
        private_key = key.export_key().decode('utf-8')

        key_pair = KeyPair(public_key=public_key, private_key=private_key)
        db.session.add(key_pair)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/read/<int:id>')
def read(id):
    key_pair = KeyPair.query.get_or_404(id)
    return render_template('read.html', key_pair=key_pair)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    key_pair = KeyPair.query.get_or_404(id)
    if request.method == 'POST':
        key_pair.public_key = request.form['public_key']
        key_pair.private_key = request.form['private_key']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', key_pair=key_pair)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    key_pair = KeyPair.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(key_pair)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', key_pair=key_pair)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
