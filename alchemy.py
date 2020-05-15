from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def db_connection(user, password, psql_url, psql_db):                                       #Индивидуально для каждого
    db_url = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=user, pw=password,           #Пример: postgresql://scott:tiger@localhost/mydatabase
                                                          url=psql_url, db=psql_db)         # (база данных уже должна быть создана)
    return db_url                                                                           # (У меня Ubuntu, для Винды может быть другой способ подключения)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection(user='postgres', password='2423',
                                                      psql_url='dvv2423.fvds.ru', psql_db='flaskapp')

db = SQLAlchemy(app)


class Example(db.Model):
    __tablename__ = 'example'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.VARCHAR)

    def __init__(self, id, data):
        self.id = id
        self.data = data


def appending(ClassName, *args):
    try:
        element = ClassName(*args)
    except TypeError:
        raise("Wrong number of table parameters")
    else:
        db.session.add(element)
        db.session.commit()
        return True


def main():
    db.create_all()


main()
