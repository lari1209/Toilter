from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user
from app import app, db, login_manager  # Variável importada do módulo app em __init__.py
from app.models.tables import User
from app.models.forms import LoginForm, RegisterForm, EditForm, DeleteForm, Query_session


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route('/index/<user>')
@app.route('/', defaults={'user': None})
def index(user):
    return render_template('index.html', user=user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            session['user'] = user.id
            user_name = form.username.data
            flash(f'Logged in! Welcome {user_name}')
            return redirect(url_for('index'))
        elif 'user' in session or session['user'] is not None:
            flash('Already Logged In!')
        else:
            flash('Invalid Login!')
            if form.errors:
                print(form.errors)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for('index'))


@app.route('/create', methods=["GET", "POST"])  # Criação do registro pelo form action do register.html
def create_user():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.username)
        user = User(form.username.data, form.password.data, form.name.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('registered successful!')
        return redirect(url_for('login'))
    if form.errors:
        flash('Error, try again!')
        print(form.errors)
    return render_template('register.html', form=form)


# Lista de cadastrados
@app.route('/list')
def list_users():
    user = User.query.all()
    return render_template('list.html', user=user)


@app.route('/delete', methods=["GET", "POST"])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if user and user.password == form.password.data:
            db.session.delete(user)
            db.session.commit()
            flash('The email excluded successful!')
            return redirect(url_for('index'))
        if user.password is not form.password.data:
            flash(f'do not successful deleted, verify password!')
            return redirect(url_for('delete'))
    return render_template('delete.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm()
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        user.password = form.password.data
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash('Atualizado')
        return redirect('/')
    return render_template('edit.html', form=form, id=session['user'])



#delete0
# @app.route('/delete', methods=["GET", "POST"])
# def delete():
#     form = DeleteForm()
#     if form.validate_on_submit:
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.password == form.password.data and session['user']:
#             db.session.delete(user)
#             db.session.commit()
#             flash('The email excluded!')
#             return redirect(url_for('index'))
#         if not form.password.data:
#             flash(f'do not successful deleted, verify username and password!')
#             return redirect(url_for('delete'))
#     return render_template('delete.html', form=form, session_user=session['user'])
#delete1
# @app.route('/delete', methods=["GET", "POST"])
# def delete():
#     form = DeleteForm()
#     if request.method == 'POST':
#         user = User.query.get(current_user.id)
#         if user.password == form.password.data and session['user']:
#             db.session.delete(user)
#             db.session.commit()
#             flash('The email excluded successful!')
#             return redirect(url_for('index'))
#         if not form.password.data:
#             flash(f'do not successful deleted, verify username and password!')
#             return redirect(url_for('delete'))
#     return render_template('delete.html', form=form)


#HTML DELETE
# {% extends 'base.html' %}
# {% block title %}{{ super() }}-Delete account{% endblock %}
# {% block content %}
# <div class="row">
#     <form action="{{ url_for('delete') }}" method="POST">
#         <div class="col-md-4 col-md-offset-4">
#             <h2>Confirm Delete</h2>
#             {{ form.csrf_token }}
#         <div class="form-group">
#             <label>Username</label>
#             {{ form.username(class='form-control', placeholder='seu_usuario') }}
#             {% if form.errors.username %}
#             <div class="alert alert-danger" role="alert">
#                 <ul>
#                 {% for e in form.errors.username %}
#                 <li>{{ e }}</li>
#                 {% endfor %}
#                 </ul>
#             </div>
#             {% endif %}
#         </div>
#         <div class="form-group">
#             <label>Password</label>
#             {{ form.password(class='form-control', placeholder='*******') }}
#             {% if form.errors.password %}
#             <div class="alert alert-danger" role="alert">
#                 <ul>
#                 {% for e in form.errors.password %}
#                 <li>{{ e }}</li>
#                 {% endfor %}
#                 </ul>
#             </div>
#             {% endif %}
#         </div>
#         <button type="submit" class="btn btn-primary btn-sm">Delete</button>
#         </div>
#     </form>
# </div>
# {% endblock %}