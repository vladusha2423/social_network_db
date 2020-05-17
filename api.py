from flask import Flask, jsonify, request
from db import Context
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'

context = Context(app)
context.create_db()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = context.user.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if 'login' in data and 'password' in data:
        curr_user = context.user.query.filter_by(nick=data['login']).first()
        if curr_user.password == data['password']:
            token = jwt.encode(
                {'id': curr_user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})
        else:
            return 'Неверный пароль'
    else:
        return 'Не все данные введены'


@app.route('/api/me')
@token_required
def me(current_user):
    return jsonify(context.user_schema.dump(current_user))


@app.route('/api/me/postsbypublics')
@token_required
def my_publics_posts(current_user):
    a = []
    for i in current_user.subscriptions:
        for j in i.post_published:
            j.views = float(j.views)
            j.likes = float(j.likes)
            a.append(j)
    return jsonify(context.posts_schema.dump(a))


# аще агонь, там только смержить работу двух функций и отсортировать, и будет фид
# можно похожую тему сделать кароче в чатах, чтобы не чисто по алфавиту были раскиданы, но это если успеем
@app.route('/api/me/postsbyusers')
@token_required
def my_friends_posts(current_user):
    a = []
    for i in current_user.user_subscribers:
        friend = context.user.query.filter_by(id=i.subscriber_id).first()
        print(friend.nick)
        for j in friend.user_post_published:
            j.views = float(j.views)
            j.likes = float(j.likes)
            a.append(j)
    return jsonify(context.posts_schema.dump(a))


# работает только с пустыми параметрами, на всё остальное ругается, поди рвзбери почему
@app.route('/api/me/publics')
@token_required
def my_publics(current_user):
    public = current_user.subscriptions
    print(public)
    # a = []
    # for i in current_user.subscriptions:
    #     pub = context.public.query.filter_by(id=i.id).first()
    #     a.append(str(pub.description))
    #     print(pub.description)
    # print(context.publics_schema.dump(a))
    return jsonify(context.publics_schema.dump(public))


# работает как конфетка просто
@app.route('/api/me/subscribers')
@token_required
def my_subscribers(current_user):
    a = []
    for i in current_user.user_subscribers:
        a.append(context.user.query.filter_by(id=i.subscriber_id).first())
    return jsonify(context.users_schema.dump(a))


# заебись работает
@app.route('/api/me/chats')
@token_required
def my_chats(current_user):
    return jsonify(context.chats_schema.dump(current_user.user_chat_member))


# вроде не роняет ничего, надо проверить
@app.route('/api/me/chat/<int:chat_id>')
@token_required
def message_history(current_user, chat_id):
    chat = context.chat.query.filter_by(id=chat_id).first()
    return jsonify(context.messages_schema.dump(chat.chat_messages))


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


@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
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
    a = []
    for i in context.ops.return_table('post'):
        i.views = float(i.views)
        i.likes = float(i.likes)
        a.append(i)
    return jsonify(context.posts_schema.dump(a))


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json() or {}
    context.ops.appending(data['post'],
                          data['text'],
                          data['time'],
                          data['photo'],
                          data['views'],
                          data['likes'])
    return 'post appended!'


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    context.ops.remove('post', post_id)
    return 'post deleted!'


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
