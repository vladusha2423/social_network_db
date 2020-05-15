from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from db import Context

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'

context = Context(app, UserMixin)
context.create_db()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return context.user.query.get(int(user_id))


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if 'login' in data and 'password' in data:
        curr_user = context.user.query.filter_by(nick=data['login']).first()
        print(curr_user)
        if curr_user.password == data['password']:
            login_user(curr_user)
            return 'Вы успешно авторизованы'
        else:
            return 'Неверный пароль'
    else:
        return 'Не все данные введены'


@app.route('/api/logout')
def logout():
    logout_user()
    return 'Вы успешно вышли из системы'


@app.route('/api/me')
@login_required
def me():
    return jsonify(current_user)


@app.route('/api/users')
def get_users():
    return jsonify(context.users_schema.dump(context.ops.return_table('user')))


@app.route('/api/messages')
def get_messages():
    return jsonify(context.messages_schema.dump(context.ops.return_table('message')))


@app.route('/api/chats')
def get_chats():
    return jsonify(context.chats_schema.dump(context.ops.return_table('chat')))


@app.route('/api/posts')
def get_posts():
    return jsonify(context.posts_schema.dump(context.ops.return_table('post')))


@app.route('/api/publics')
def get_publics():
    return jsonify(context.publics_schema.dump(context.ops.return_table('public')))


@app.route('/api/roles')
def get_roles():
    return jsonify(context.roles_schema.dump(context.ops.return_table('role')))


if __name__ == "__main__":
    app.run()
