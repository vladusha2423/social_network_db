from flask import Flask, jsonify
from db import Context

app = Flask(__name__)

context = Context(app)


@app.route('/api/users')
def index():
    return jsonify(context.users_schema.dump(context.ops.return_table('users')))


if __name__ == "__main__":
    app.run()
