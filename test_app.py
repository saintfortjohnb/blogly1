import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, User

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_users_index(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'image_url': 'https://example.com/image.jpg'
        }
        response = self.app.post('/users/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_user_detail(self):
        user = User(first_name='Jane', last_name='Smith', image_url='https://example.com/image.jpg')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            response = self.app.get(f'/users/{user.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Jane Smith', response.data)

    def test_edit_user(self):
        user = User(first_name='Jane', last_name='Smith', image_url='https://example.com/image.jpg')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            data = {
                'first_name': 'Janet',
                'last_name': 'Johnson',
                'image_url': 'https://example.com/new_image.jpg'
            }
            response = self.app.post(f'/users/{user.id}/edit', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Janet Johnson', response.data)

if __name__ == '__main__':
    unittest.main()
