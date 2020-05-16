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
    return jsonify(context.user_schema.dump(current_user))


# USER OPERATIONS


@app.route('/api/users')
def get_users():
    return jsonify(context.users_schema.dump(context.ops.return_table('user')))


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    context.ops.appending('user',
                          data['nick'],
                          data['avatar'],
                          data['descr'],
                          data['password'],
                          data['name'],
                          data['surname'])
    return 'user appended!'


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    context.ops.remove('user', user_id)
    return 'user deleted!'


"""
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id, column_name, value):
    context.ops.update('user', user_id, column_name, value)
    return 'user updated!'
"""


# MESSAGE OPERATIONS


@app.route('/api/messages')
def get_messages():
    return jsonify(context.messages_schema.dump(context.ops.return_table('message')))


@app.route('/api/messages', methods=['POST'])
def create_messages():
    data = request.get_json() or {}
    context.ops.appending('message',
                          data['id'],
                          data['time'],
                          data['text'],
                          data['sentby'],
                          data['chat'])
    return 'message appended!'


@app.route('/api/messages/<int:user_id>', methods=['DELETE'])
def delete_messages(message_id):
    context.ops.remove('message', message_id)
    return 'message deleted!'


# CHAT OPERATIONS


@app.route('/api/chats')
def get_chats():
    return jsonify(context.chats_schema.dump(context.ops.return_table('chat')))


@app.route('/api/chats', methods=['POST'])
def create_chat():
    data = request.get_json() or {}
    context.ops.appending(data['chat'], data['id'], data['type'], data['title'], data['avatar'])
    return 'chat appended!'


@app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    context.ops.remove('chat', chat_id)
    return 'chat deleted!'


# POSTS OPERATIONS


@app.route('/api/posts')
def get_posts():
    return jsonify(context.posts_schema.dump(context.ops.return_table('post')))


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json() or {}
    context.ops.appending(data['post'],
                          data['text'],
                          data['time'],
                          data['photo'],
                          data['views'],
                          data['likes'])
    return ' appended!'


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    context.ops.remove('post', post_id)
    return ' deleted!'


# PUBLICS OPERATIONS


@app.route('/api/publics')
def get_publics():
    return jsonify(context.publics_schema.dump(context.ops.return_table('public')))


@app.route('/api/publics', methods=['POST'])
def create_public():
    data = request.get_json() or {}
    context.ops.appending(data['public'],
                          data['id'],
                          data['title'],
                          data['avatar'],
                          data['description'])
    return 'public appended!'


@app.route('/api/publics/<int:public_id>', methods=['DELETE'])
def delete_public(public_id):
    context.ops.remove('public', public_id)
    return 'public deleted!'


# ROLES OPERATIONS


@app.route('/api/roles')
def get_roles():
    return jsonify(context.roles_schema.dump(context.ops.return_table('role')))


@app.route('/api/roles', methods=['POST'])
def create_role():
    data = request.get_json() or {}
    context.ops.appending('role', data['id'], data['title'])
    return 'role appended!'


@app.route('/api/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    context.ops.remove('role', role_id)
    return 'role deleted!'


if __name__ == "__main__":
    app.run()
