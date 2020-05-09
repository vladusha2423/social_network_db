if __name__ == '__main__':
    from sqlalchemy.sql import func
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy


def db_connection(user, password, psql_url, psql_db):                                       #Индивидуально для каждого
    db_url = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=user, pw=password,           #Пример: postgresql://scott:tiger@localhost/mydatabase
                                                          url=psql_url, db=psql_db)         # (база данных уже должна быть создана)
    return db_url                                                                           # (У меня Ubuntu, для Винды может быть другой способ подключения)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection(user='postgres', password='2423',
                                                      psql_url='dvv2423.fvds.ru', psql_db='social_network_2')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False           # silence the deprecation warning

db = SQLAlchemy(app)


public_subscribers = db.Table('PublicSubscribers',                    #работает без ролей
    db.Column('pub_id', db.Integer, db.ForeignKey('public.id')),
    db.Column('u_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('ps_role', db.Integer, db.ForeignKey('roles.id'))
)

post_published_by_user = db.Table('PostPublishedByUser',                  #работает
    db.Column('pub_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('pu_id', db.Integer, db.ForeignKey('users.id'))
)

post_published_by_public = db.Table('PostPublishedByPublic',                  #работает
    db.Column('pub_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('pu_id', db.Integer, db.ForeignKey('public.id'))
)

chat_members = db.Table('ChatMembers',                                      #работает без ролей
    db.Column('chat', db.Integer, db.ForeignKey('chat.id')),
    db.Column('member', db.Integer, db.ForeignKey('users.id'))
)

#friends = db.Table('Friends',                                          не работает
#    db.Column('id_1', db.Integer, db.ForeignKey('users.id')),
#    db.Column('id_2', db.Integer, db.ForeignKey('users.id'))
#)


class Users(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    nick = db.Column(db.VARCHAR(50), nullable=False)
    avatar = db.Column(db.VARCHAR(200))
    descr = db.Column(db.VARCHAR(500))
    password = db.Column(db.VARCHAR(50), nullable=False)
    name = db.Column(db.VARCHAR(50))
    surname = db.Column(db.VARCHAR(50))

    subscriptions = db.relationship('Public', secondary=public_subscribers,
                                    backref=db.backref('subscribers', lazy='dynamic'))

    user_post_published = db.relationship('Post', secondary=post_published_by_user,
                                          backref=db.backref('published', lazy='dynamic'))

    user_chat_member = db.relationship('Chat', secondary=chat_members,
                                       backref=db.backref('chat_join', lazy='dynamic'))

    user_messages = db.relationship('Message', backref='user_message_owner')

    #followers = db.relationship('Users', secondary=friends,
     #                           backref=db.backref('subscribe', lazy='dynamic'))

    def __init__(self, nick, avatar,
                 descr, password, name,
                 surname):

        self.nick = nick
        self.avatar = avatar
        self.descr = descr
        self.password = password
        self.name = name
        self.surname = surname


class Message(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    time = db.Column(db.DATE, default=func.now(), nullable=False)
    text = db.Column(db.VARCHAR(1000), nullable=False)
    sentby = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat = db.Column(db.Integer, db.ForeignKey('chat.id'))

    def __init__(self, text, time=func.now()):
        self.text=text
        self.time=time


class Chat(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    type = db.Column(db.VARCHAR(12), nullable=False)
    title = db.Column(db.VARCHAR(80), nullable=False)
    avatar = db.Column(db.VARCHAR(100))

    chat_messages = db.relationship('Message', backref='chat_message_owner')

    def __init__(self, type, title,
                 avatar=None):
        self.type=type
        self.title=title
        self.avatar=avatar


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.VARCHAR(1000), nullable=False)
    photo = db.Column(db.VARCHAR(200))
    time = db.Column(db.DATE, default=func.now())
    views = db.Column(db.NUMERIC(7), default=0, nullable=False)
    likes = db.Column(db.NUMERIC(7), default=0, nullable=False)

    def __init__(self, text, time=func.now(), photo=None,
                 views=0, likes=0):
        self.text = text
        self.time=time
        self.photo=photo
        self.views=views
        self.likes=likes


class Public(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(80), nullable=False)
    avatar = db.Column(db.VARCHAR(100))
    description = db.Column(db.VARCHAR(200))
    post_published = db.relationship('Post', secondary=post_published_by_public,
                                            backref=db.backref('pub_published', lazy='dynamic'))

    def __init__(self, title, description=None, avatar=None):
        self.title = title
        self.description = description
        self.avatar = avatar


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(30), nullable=False)

    def __init__(self, title):
        self.title=title


class Check:
    @staticmethod
    def public_subscribers_checking(UserObject, PublicObject):
        #user = Users(nick='nagibator228', avatar='', descr='dodik', password=12345,
        #     name='Martin', surname='Iden')
        #public = Public(title='dqrq', avatar='fqt', description='qwtwqtqt')
        try:
            db.session.add(UserObject)                                                              #можно использовать db.session.add_all([public, user])
            db.session.add(PublicObject)
            PublicObject.subscribers.append(UserObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def user_post_published_checking(UserObject, PostObject):
        #user = Users(nick='na132', avatar='rqwtq', descr='dok', password=125,
        #         name='Fidel', surname='Castro')
        #post = Post(text='Cuba is free!')
        try:
            db.session.add(UserObject)
            db.session.add(PostObject)
            PostObject.published.append(UserObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def public_post_published_checking(PublicObject, PostObject):
        #public = Public(title='d123')
        #post = Post(text='Hello!')
        try:
            db.session.add(PublicObject)
            db.session.add(PostObject)
            PostObject.pub_published.append(PublicObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def user_chat_member_checking(UserObject, ChatObject):
        try:
            #user = Users(nick='VasilyPupkin', avatar='rqwqq', descr='Vasily', password=1225,
            #         name='Vasily', surname='Pupkin')
            #chat = Chat(type='dialog', title='basedata')
            db.session.add(UserObject)
            db.session.add(ChatObject)
            ChatObject.chat_join.append(UserObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def user2message_checking(UserObject, MessageObject):
        #user = Users(nick='DonaldTrump', avatar='rqdwwqq', descr='America', password=1225,
        #             name='Hi', surname='Clinton')
        #message = Message(text='America began operations in Russia!',
        #                  user_message_owner=user)
        try:
            db.session.add(UserObject)
            db.session.add(MessageObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def chat2message_checking(ChatObject, MessageObject):
        try:
            #chat = Chat(type='dialog', title='next')
            #message = Message(text='Hi, boys!',
            #              chat_message_owner=chat)
            db.session.add(ChatObject)
            db.session.add(MessageObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True


    #def friends_checking():
    #   user1 = Users(nick='VasilyPupkin', avatar='rqwqq', descr='Vasily', password=1225,
    #                 name='Vasily', surname='Pupkin')
    #   user2 = Users(nick='DonaldTrump', avatar='rqdwwqq', descr='America', password=1225,
    #                 name='Hi', surname='Clinton')

    #    db.session.add(user1)
    #   db.session.add(user2)
    #  user1.subscribe.append(user2)
    #  db.session.commit()


class Operations:

    def __init__(self):
        pass

    @staticmethod
    def return_row(ClassName, id):
        ClassName.query.filter_by(id=id).first()

    @staticmethod
    def return_table(ClassName):
        return ClassName.query.all()

        #Пример:
        #for el in return_table(Users):
        #   print(el.u_nick)

    @staticmethod
    def appending(ClassName, *args):
        try:
            element = ClassName(*args)
        except TypeError:
            raise("Wrong number of table parameters")
        else:
            db.session.add(element)
            db.session.commit()
            return True

    @staticmethod
    def remove(ClassName, id):      #удаление нашел только по id (оно почему-то не удаляет :( )
        try:
            delete = ClassName.query.filter_by(id=id).first()
        except ValueError:
            raise ValueError('Либо такого id нет в базе, либо нет такого класса')
        else:
            db.session.delete(delete)
            db.session.commit()
            return True

    @staticmethod                                           #не работает
    def update(ClassName, id, column_name, value):
        try:
            update = ClassName.query.filter_by(id=id).first()
        except ValueError:
            raise ValueError('Либо такого id нет в базе, либо нет такого класса')
        else:
            setattr(update, column_name, value)               #ClassName object is not subscripitable (можно обращаться к update только через точку, а не через [])
            db.session.commit()
            return True


def main():  #Кто опять будет тупить и не запустит эту функцию перед запуском скрипта - тот здохнед
    db.create_all()

    Operations.appending(Users, 'VP', 'rqwqtqt', 'Happy',
                         228, 'Petr', 'Semenov')
    Operations.return_table(Users)
    Operations.return_row(Users, 4)
    Operations.update(Users, id=5, column_name="name", value="Dop")
    Operations.remove(Users, id=5)

