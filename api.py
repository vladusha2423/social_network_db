from flask import Flask, jsonify, request
from db import Context
import jwt
import datetime
from functools import wraps
from flask_cors import CORS
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

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
                {'id': curr_user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
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


@app.route('/api/me/postsbyusers')
@token_required
def my_friends_posts(current_user):
    a = []
    for i in current_user.user_subscribers:
        friend = context.user.query.filter_by(id=i.subscriber_id).first()
        for j in friend.user_post_published:
            j.views = float(j.views)
            j.likes = float(j.likes)
            a.append(j)
    return jsonify(context.posts_schema.dump(a))


@app.route('/api/me/feed')
@token_required
def my_feed(current_user):
    c = []
    for i in current_user.user_subscribers:
        friend = context.user.query.filter_by(id=i.subscriber_id).first()
        for j in friend.user_post_published:
            j.views = float(j.views)
            j.likes = float(j.likes)
            c.append(context.posts_schema.dump([j]) + [friend.name + ' ' + friend.surname, friend.avatar])
    for i in current_user.subscriptions:
        for j in i.post_published:
            j.views = float(j.views)
            j.likes = float(j.likes)
            c.append(context.posts_schema.dump([j]) + [i.title, i.avatar])
    return jsonify(c)


@app.route('/api/me/publics')
@token_required
def my_publics(current_user):
    return jsonify(context.publics_schema.dump(current_user.subscriptions))


@app.route('/api/me/subscribers')
@token_required
def my_subscribers(current_user):
    a = []
    for i in current_user.user_subscribers:
        a.append(context.user.query.filter_by(id=i.subscriber_id).first())
    return jsonify(context.users_schema.dump(a))


@app.route('/api/me/chats')
@token_required
def my_chats(current_user):
    for item in current_user.user_chat_member:
        members = context.users_schema.dump(item.chat_join)
        item.count = len(members)
        if item.count == 2:
            if members[0]['id'] == current_user.id:
                item.avatar = members[1]['avatar']
                item.title = members[1]['name'] + ' ' + members[1]['surname']
            else:
                item.avatar = members[0]['avatar']
                item.title = members[0]['name'] + ' ' + members[0]['surname']

    return jsonify(context.chats_schema.dump(current_user.user_chat_member))


@app.route('/api/me/chat/<int:chat_id>')
@token_required
def message_history(current_user, chat_id):
    chat = context.chat.query.filter_by(id=chat_id).first()
    return jsonify(context.messages_schema.dump(chat.chat_messages))


@app.route('/api/me/chat/<int:chat_id>', methods=['POST'])
@token_required
def publish_message(current_user, chat_id):
    flag = False
    for i in current_user.user_chat_member:
        if i.id == chat_id:
            flag = True
    if not flag:
        return 'access denied!'
    data = request.get_json() or {}
    context.ops.appending('message',
                          data['text'],
                          func.now(),
                          current_user.id,
                          chat_id)
    return 'message appended!'


@app.route('/api/me/post/<int:post_id>/<int:public_id>/2public', methods=['POST'])
def connect_post_2_public(post_id, public_id):
    context.check.public_post_published(post_id=post_id, public_id=public_id)
    return 'Post added to public!'


@app.route('/api/me/post/<int:post_id>/2user', methods=['POST'])
@token_required
def connect_post_2_user(current_user, post_id):
    context.check.user_post_published(post_id=post_id, user_id=current_user.id)
    return 'post added!'


@app.route('/api/me/message/<int:message_id>/2user', methods=['POST'])
def connect_message_2_user(message_id):
    data = request.get_json() or {}
    context.check.user2message(message_id=message_id, user_id=data['user_id'])
    return 'message and user are connected!'


@app.route('/api/me/message/<int:message_id>/2user', methods=['POST'])
def connect_message_2_chat(message_id):
    data = request.get_json() or {}
    context.check.chat2message(message_id=message_id, chat_id=data['user_id'])
    return 'message and chat are connected!'


@app.route('/api/me/message/<int:chat_id>', methods=['POST'])
@token_required
def send_message(current_user, chat_id):
    data = request.get_json() or {}
    context.ops.appending('message',
                          data['text'],
                          func.now(),
                          current_user.id,
                          chat_id)
    return 'message appended!'


@app.route('/api/me/public/<int:public_id>/subscribe', methods=['POST'])
@token_required
def subscribe2public(current_user, public_id):
    context.check.public_subscribers(user_id=current_user.id, public_id=public_id)
    return 'you subscribed successfully!'


@app.route('/api/me/user/subscribe/<int:usr_id>', methods=['POST'])
@token_required
def subscribe_user(current_user, usr_id):
    context.ops.appending('friendship', current_user.id, usr_id)
    return 'subscribed!'


@app.route('/api/me/chat/<int:chat_id>/<int:user_id>/join', methods=['POST'])
def join2chat(chat_id, user_id):
    context.check.user_chat_member(user_id=user_id, chat_id=chat_id)
    return 'you joined successfully!'


@app.route('/api/me/chat/<int:public_id>/is_admin', methods=['POST'])
@token_required
def define_admin_of_public(current_user, public_id):
    flag = False
    for i in current_user.public_subscribers:
        print(i)
    #     if i.id == public_id and i.role:
    #         flag = True
    # if not flag:


# USER OPERATIONS


@app.route('/api/users')
def get_users():
    return jsonify(context.users_schema.dump(context.ops.return_table('user')))


@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    return jsonify(context.user_schema.dump(context.user.query.filter_by(id=user_id).first()))


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


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json() or {}
    context.ops.update('user', user_id, data['column'], data['value'])
    return 'user updated!'


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


@app.route('/api/chat/<int:chat_id>')
@token_required
def get_chat(current_user, chat_id):
    item = context.chat.query.filter_by(id=chat_id).first()
    item.members = context.users_schema.dump(item.chat_join)
    item.count = len(item.members)
    if item.count == 2:
        if item.members[0]['id'] == current_user.id:
            item.avatar = item.members[1]['avatar']
            item.title = item.members[1]['name'] + ' ' + item.members[1]['surname']
        else:
            item.avatar = item.members[0]['avatar']
            item.title = item.members[0]['name'] + ' ' + item.members[0]['surname']
    return jsonify(context.chat_schema.dump(item))


@app.route('/api/chats', methods=['POST'])
def create_chat():
    data = request.get_json() or {}
    el = context.ops.appending('chat', data['type'], data['title'], data['avatar'])
    return jsonify({'message': 'chat added successfully', 'chat_id': el.id})


@app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    context.ops.remove('chat', chat_id)
    return 'chat deleted!'


# POSTS OPERATIONS


@app.route('/api/posts/user/<int:user_id>')
def get_posts_by_user(user_id):
    posts = context.user.query.filter_by(id=user_id).first().user_post_published
    for i in posts:
        i.views = float(i.views)
        i.likes = float(i.likes)
    return jsonify(context.posts_schema.dump(posts))


@app.route('/api/posts/public/<int:public_id>')
def get_posts_by_public(public_id):
    posts = context.public.query.filter_by(id=public_id).first().post_published
    for i in posts:
        i.views = float(i.views)
        i.likes = float(i.likes)
    return jsonify(context.posts_schema.dump(posts))


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
    post = context.ops.appending('post',
                                 data['text'],
                                 func.now(),
                                 data['photo'],
                                 data['views'],
                                 data['likes'])
    return jsonify({'message': 'post added successfully', 'post_id': post.id})


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    context.ops.remove('post', post_id)
    return 'post deleted!'


# PUBLICS OPERATIONS


@app.route('/api/publics')
def get_publics():
    return jsonify(context.publics_schema.dump(context.ops.return_table('public')))


@app.route('/api/public/<int:pub_id>')
def get_public(pub_id):
    return jsonify(context.public_schema.dump(context.public.query.filter_by(id=pub_id).first()))


@app.route('/api/publics', methods=['POST'])
def create_public():
    data = request.get_json() or {}
    el = context.ops.appending('public',
                               data['title'],
                               data['description'],
                               data['avatar'])
    return jsonify({'message': 'Public added successfully!', 'public_id': el.id})


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
    app.run(host="localhost", port=int("5500"), debug=False)
