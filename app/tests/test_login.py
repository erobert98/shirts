from app.models import User
from flask_login import login_user, current_user, logout_user
from app import app, db
from flask import url_for, request
from app.forms import LoginForm



def test_login(client):
    with app.test_request_context():
        form = LoginForm(username = 'admin', password='admin')
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            login_user(user, force=True)
            assert request.path == '/index'

def test_logout(client):
    with app.test_request_context():
        user = User.query.first()
        check = login_user(user, force=True)
        assert check is True
        logout_user()
        assert current_user.is_anonymous is True


def test_doubleLogin(client):
    with app.test_request_context():
        login(client, 'user', 'user')
        response = client.get('/login')
        var = response.data
        assert b''  in response.data 

#all tests are dogshit good job emile, never stores shit 