"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

def create_and_configure_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "2023blogly"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    debug = DebugToolbarExtension(app)

    connect_db(app)

    with app.app_context():
        db.create_all()

    return app

app = create_and_configure_app()

@app.route('/')
def home():
    """Redirect to list of users"""
    return redirect("/users")

@app.route('/users')
def users_index():
    """Show list of users"""
    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None  # use None if the field is empty
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')

    else:
        return render_template('users/new.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show detail about user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Show edit form and handle edit"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] or None
        db.session.commit()

        return redirect(f'/users/{user_id}')

    else:
        return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

if __name__ == "__main__":
    app.run(debug=True)
