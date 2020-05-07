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
                                                      psql_url='dvv2423.fvds.ru', psql_db='flaskapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False           # silence the deprecation warning

db = SQLAlchemy(app)


public_subscribers = db.Table('PublicSubscribers',                    #работает без ролей
    db.Column('pub_id', db.Integer, db.ForeignKey('public.pub_id')),
    db.Column('u_id', db.Integer, db.ForeignKey('users.u_id')),
    db.Column('ps_role', db.Integer, db.ForeignKey('roles.r_id'))
)

post_published_by_user = db.Table('PostPublishedByUser',                  #работает
    db.Column('pub_id', db.Integer, db.ForeignKey('post.p_id')),
    db.Column('pu_id', db.Integer, db.ForeignKey('users.u_id'))
)

post_published_by_public = db.Table('PostPublishedByPublic',                  #работает
    db.Column('pub_id', db.Integer, db.ForeignKey('post.p_id')),
    db.Column('pu_id', db.Integer, db.ForeignKey('public.pub_id'))
)

chat_members = db.Table('ChatMembers',                                      #работает без ролей
    db.Column('chm_chat', db.Integer, db.ForeignKey('chat.c_id')),
    db.Column('chm_member', db.Integer, db.ForeignKey('users.u_id'))
)

#friends = db.Table('Friends',                                          не работает
#    db.Column('f_id_1', db.Integer, db.ForeignKey('users.u_id')),
#    db.Column('f_id_2', db.Integer, db.ForeignKey('users.u_id'))
#)


class Users(db.Model):
    u_id = db.Column(db.INTEGER, primary_key=True)
    u_nick = db.Column(db.VARCHAR(50), nullable=False)
    u_avatar = db.Column(db.VARCHAR(200))
    u_descr = db.Column(db.VARCHAR(500))
    u_password = db.Column(db.VARCHAR(50), nullable=False)
    u_fl = db.Column(db.VARCHAR(50))

    subscriptions = db.relationship('Public', secondary=public_subscribers,
                                    backref=db.backref('subscribers', lazy='dynamic'))

    user_post_published = db.relationship('Post', secondary=post_published_by_user,
                                          backref=db.backref('published', lazy='dynamic'))

    user_chat_member = db.relationship('Chat', secondary=chat_members,
                                       backref=db.backref('chat_join', lazy='dynamic'))

    user_messages = db.relationship('Message', backref='user_message_owner')

    #followers = db.relationship('Users', secondary=friends,
     #                           backref=db.backref('subscribe', lazy='dynamic'))

    def __init__(self, u_nick, u_avatar,
                 u_descr, u_password, u_fl):

        self.u_nick = u_nick
        self.u_avatar = u_avatar
        self.u_descr = u_descr
        self.u_password = u_password
        self.u_fl = u_fl


class Message(db.Model):
    m_id = db.Column(db.INTEGER, primary_key=True)
    m_time = db.Column(db.DATE, default=func.now(), nullable=False)
    m_text = db.Column(db.VARCHAR(1000), nullable=False)
    m_sentby = db.Column(db.Integer, db.ForeignKey('users.u_id'))
    m_chat = db.Column(db.Integer, db.ForeignKey('chat.c_id'))

    def __init__(self, m_text, m_time=func.now()):
        self.m_text=m_text
        self.m_time=m_time


class Chat(db.Model):
    c_id = db.Column(db.INTEGER, primary_key=True)
    c_type = db.Column(db.VARCHAR(12), nullable=False)
    c_title = db.Column(db.VARCHAR(80), nullable=False)
    c_avatar = db.Column(db.VARCHAR(100))

    chat_messages = db.relationship('Message', backref='chat_message_owner')

    def __init__(self, c_type, c_title,
                 c_avatar=None):
        self.c_type=c_type
        self.c_title=c_title
        self.c_avatar=c_avatar


class Post(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    p_text = db.Column(db.VARCHAR(1000), nullable=False)
    p_photo = db.Column(db.VARCHAR(200))
    p_time = db.Column(db.DATE, default=func.now())
    p_views = db.Column(db.NUMERIC(7), default=0, nullable=False)
    p_likes = db.Column(db.NUMERIC(7), default=0, nullable=False)

    def __init__(self, p_text, p_time=func.now(), p_photo=None,
                 p_views=0, p_likes=0):
        self.p_text = p_text
        self.p_time=p_time
        self.p_photo=p_photo
        self.p_views=p_views
        self.p_likes=p_likes


class Public(db.Model):
    pub_id = db.Column(db.Integer, primary_key=True)
    pub_title = db.Column(db.VARCHAR(80), nullable=False)
    pub_avatar = db.Column(db.VARCHAR(100))
    pub_description = db.Column(db.VARCHAR(200))
    public_post_published = db.relationship('Post', secondary=post_published_by_public,
                                            backref=db.backref('pub_published', lazy='dynamic'))

    def __init__(self, pub_title, pub_description=None, pub_avatar=None):
        self.pub_title = pub_title
        self.pub_description = pub_description
        self.pub_avatar = pub_avatar


class Roles(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_title = db.Column(db.VARCHAR(30), nullable=False)

    def __init__(self, r_title):
        self.r_title=r_title


class Check:
    @staticmethod
    def public_subscribers_checking(UserObject, PublicObject):
        #user = Users(u_nick='nagibator228', u_avatar='', u_descr='dodik', u_password=12345,
        #     u_fl='Martin Iden')
        #public = Public(pub_title='dqrq', pub_avatar='fqt', pub_description='qwtwqtqt')
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
        #user = Users(u_nick='na132', u_avatar='rqwtq', u_descr='dok', u_password=125,
        #         u_fl='Fidel Castro')
        #post = Post(p_text='Cuba is free!')
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
        #public = Public(pub_title='d123')
        #post = Post(p_text='Hello!')
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
            #user = Users(u_nick='VasilyPupkin', u_avatar='rqwqq', u_descr='Vasily', u_password=1225,
            #         u_fl='Vasily Pupkin')
            #chat = Chat(c_type='dialog', c_title='basedata')
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
        #user = Users(u_nick='DonaldTrump', u_avatar='rqdwwqq', u_descr='America', u_password=1225,
        #             u_fl='Hi Clinton')
        #message = Message(m_text='America began operations in Russia!',
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
            #chat = Chat(c_type='dialog', c_title='next')
            #message = Message(m_text='Hi, boys!',
            #              chat_message_owner=chat)
            db.session.add(ChatObject)
            db.session.add(MessageObject)
            db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True


    #def friends_checking():
    #   user1 = Users(u_nick='VasilyPupkin', u_avatar='rqwqq', u_descr='Vasily', u_password=1225,
    #                 u_fl='Vasily Pupkin')
    #   user2 = Users(u_nick='DonaldTrump', u_avatar='rqdwwqq', u_descr='America', u_password=1225,
    #                 u_fl='Hi Clinton')

    #    db.session.add(user1)
    #   db.session.add(user2)
    #  user1.subscribe.append(user2)
    #  db.session.commit()


def return_table(ClassName):
    return ClassName.query.all()

    #Пример:
    #for el in return_table(Users):
    #   print(el.u_nick)


def appending(ClassName, *args):
    try:
        element = ClassName(*args)
    except TypeError:
        raise("Wrong number of table parameters")
    else:
        db.session.add(element)
        db.session.commit()
        return True


def remove(ClassName, id):      #удаление нашел только по id (оно почему-то не удаляет :( )
    try:
        delete = ClassName.query.filter_by(u_id=id).first()
    except ValueError:
        raise ValueError('Либо такого id нет в базе, либо нет такого класса')
    else:
        print(delete)
        db.session.delete(delete)
        db.session.commit()
        return True


def main():
    db.create_all()

    remove(Users, 5)




