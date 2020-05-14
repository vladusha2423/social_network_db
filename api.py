from flask import Flask, jsonify
from db import Context

app = Flask(__name__)

context = Context(app)


@app.route('/api/users')
def get_users():
    return jsonify(context.users_schema.dump(context.ops.return_table('users')))


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
