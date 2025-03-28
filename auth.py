from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nickname = request.form['nickname']
        
        print(nickname)
        
        if password != confirm_password:
            flash('Le password non coincidono!', 'danger')
            print('registration failed by password')
            return redirect(url_for('auth.registration'))
        
        existing_user = User.query.filter_by(username=username).first()
        print(existing_user)
        if existing_user:
            flash('Il login esiste già!', 'danger')
            print('registration failed by username')
            return redirect(url_for('auth.registration'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, nickname=nickname)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione completata! Puoi accedere.', 'success')
        print('registrazione completata')
        return redirect(url_for('auth.login'))
    
    return render_template('registration.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            flash('Accesso effettuato con successo!', 'success')
            print('login completato')
            return redirect(url_for('routes.home'))
        else:
            flash('Credenziali errate. Riprova.', 'danger')
            print('login fallito')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sei stato disconnesso.', 'info')
    return redirect(url_for('routes.login'))
