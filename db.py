from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_filters import apply_filters
from flask_marshmallow import Marshmallow


# friends = db.Table('Friends',                                          не работает
#    db.Column('id_1', db.Integer, db.ForeignKey('users.id')),
#    db.Column('id_2', db.Integer, db.ForeignKey('users.id'))
# )


class Check:
    db = None

    @staticmethod
    def public_subscribers_checking(self, UserObject, PublicObject):
        # user = Users(nick='nagibator228', avatar='', descr='dodik', password=12345,
        #     name='Martin', surname='Iden')
        # public = Public(title='dqrq', avatar='fqt', description='qwtwqtqt')
        try:
            self.db.session.add(UserObject)  # можно использовать self.db.session.add_all([public, user])
            self.db.session.add(PublicObject)
            PublicObject.subscribers.append(UserObject)
            self.db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def user_post_published_checking(self, UserObject, PostObject):
        # user = Users(nick='na132', avatar='rqwtq', descr='dok', password=125,
        #         name='Fidel', surname='Castro')
        # post = Post(text='Cuba is free!')
        try:
            self.db.session.add(UserObject)
            self.db.session.add(PostObject)
            PostObject.published.append(UserObject)
            self.db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def public_post_published_checking(self, PublicObject, PostObject):
        # public = Public(title='d123')
        # post = Post(text='Hello!')
        try:
            self.db.session.add(PublicObject)
            self.db.session.add(PostObject)
            PostObject.pub_published.append(PublicObject)
            self.db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def user_chat_member_checking(self, UserObject, ChatObject):
        try:
            # user = Users(nick='VasilyPupkin', avatar='rqwqq', descr='Vasily', password=1225,
            #         name='Vasily', surname='Pupkin')
            # chat = Chat(type='dialog', title='basedata')
            self.db.session.add(UserObject)
            self.db.session.add(ChatObject)
            ChatObject.chat_join.append(UserObject)
            self.db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def user2message_checking(self, UserObject, MessageObject):
        # user = Users(nick='DonaldTrump', avatar='rqdwwqq', descr='America', password=1225,
        #             name='Hi', surname='Clinton')
        # message = Message(text='America began operations in Russia!',
        #                  user_message_owner=user)
        try:
            self.db.session.add(UserObject)
            self.db.session.add(MessageObject)
            self.db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    @staticmethod
    def chat2message_checking(self, ChatObject, MessageObject):
        try:
            # chat = Chat(type='dialog', title='next')
            # message = Message(text='Hi, boys!',
            #              chat_message_owner=chat)
            self.db.session.add(ChatObject)
            self.db.session.add(MessageObject)
            self.db.session.commit()
        except ValueError:
            print("FAIL")
        else:
            return True

    def __init__(self, database):
        self.db = database

    # def friends_checking():
    #   user1 = Users(nick='VasilyPupkin', avatar='rqwqq', descr='Vasily', password=1225,
    #                 name='Vasily', surname='Pupkin')
    #   user2 = Users(nick='DonaldTrump', avatar='rqdwwqq', descr='America', password=1225,
    #                 name='Hi', surname='Clinton')

    #    db.session.add(user1)
    #   db.session.add(user2)
    #  user1.subscribe.append(user2)
    #  db.session.commit()


class Operations:
    db = None
    tables = None

    def return_row(self, ClassName, id):
        self.tables[ClassName].query.filter_by(id=id).first()

    def return_table(self, ClassName):
        print('cls.tables: ', self.tables)
        return self.tables[ClassName].query.all()

        # Пример:
        # for el in return_table(Users):
        #   print(el.u_nick)

    def appending(self, ClassName, *args):
        try:
            element = self.tables[ClassName](*args)
        except TypeError:
            raise ("Wrong number of table parameters")
        else:
            self.db.session.add(element)
            self.db.session.commit()
            return True

    def remove(self, ClassName, id):  # удаление нашел только по id (оно почему-то не удаляет :( )
        try:
            delete = self.tables[ClassName].query.filter_by(id=id).first()
        except ValueError:
            raise ValueError('Либо такого id нет в базе, либо нет такого класса')
        else:
            self.db.session.delete(delete)
            self.db.session.commit()
            return True

    def update(self, ClassName, id, column_name, value):
        try:
            update = self.tables[ClassName].query.filter_by(id=id).first()
        except ValueError:
            raise ValueError('Либо такого id нет в базе, либо нет такого класса')
        else:
            setattr(update, column_name,
                    value)  # ClassName object is not subscripitable (можно обращаться к update только через точку,
            # а не через [])
            self.db.session.commit()
            return True

    @staticmethod
    def erase(ClassName):
        table = Operations.return_table(ClassName)
        for row in table:
            Operations.remove(ClassName, row.id)
        return True

    def filter(self, ClassName, column, value, operation='=='):  # operation может быть не только '==', но и '<', '>'
        query = self.db.session.query(self.tables[ClassName])
        filter_spec = [{'field': column, 'op': operation, 'value': value}]
        result = apply_filters(query, filter_spec).all()
        return result

    def __init__(self, database, table):
        self.db = database
        self.tables = table


class Context:
    def __init__(self, application):
        self.app = application
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',
                                                                                                  pw='2423',
                                                                                                  url='dvv2423.fvds.ru',
                                                                                                  db='social_network_2')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        self.db = SQLAlchemy(self.app)

        self.ma = Marshmallow(self.app)

        self.public_subscribers = self.db.Table('PublicSubscribers',  # работает без ролей
                                                self.db.Column('pub_id', self.db.Integer,
                                                               self.db.ForeignKey('public.id')),
                                                self.db.Column('u_id', self.db.Integer, self.db.ForeignKey('users.id')),
                                                self.db.Column('ps_role', self.db.Integer,
                                                               self.db.ForeignKey('roles.id'))
                                                )

        self.post_published_by_user = self.db.Table('PostPublisheself.dbyUser',  # работает
                                                    self.db.Column('pub_id', self.db.Integer,
                                                                   self.db.ForeignKey('post.id')),
                                                    self.db.Column('pu_id', self.db.Integer,
                                                                   self.db.ForeignKey('users.id'))
                                                    )

        self.post_published_by_public = self.db.Table('PostPublisheself.dbyPublic',  # работает
                                                      self.db.Column('pub_id', self.db.Integer,
                                                                     self.db.ForeignKey('post.id')),
                                                      self.db.Column('pu_id', self.db.Integer,
                                                                     self.db.ForeignKey('public.id'))
                                                      )

        self.chat_members = self.db.Table('ChatMembers',  # работает без ролей
                                          self.db.Column('chat', self.db.Integer, self.db.ForeignKey('chat.id')),
                                          self.db.Column('member', self.db.Integer, self.db.ForeignKey('users.id'))
                                          )

        class Users(self.db.Model):
            id = self.db.Column(self.db.INTEGER, primary_key=True)
            nick = self.db.Column(self.db.VARCHAR(50), nullable=False)
            avatar = self.db.Column(self.db.VARCHAR(200))
            descr = self.db.Column(self.db.VARCHAR(500))
            password = self.db.Column(self.db.VARCHAR(50), nullable=False)
            name = self.db.Column(self.db.VARCHAR(50))
            surname = self.db.Column(self.db.VARCHAR(50))

            subscriptions = self.db.relationship('Public', secondary=self.public_subscribers,
                                                 backref=self.db.backref('subscribers', lazy='dynamic'))

            user_post_published = self.db.relationship('Post', secondary=self.post_published_by_user,
                                                       backref=self.db.backref('published', lazy='dynamic'))

            user_chat_member = self.db.relationship('Chat', secondary=self.chat_members,
                                                    backref=self.db.backref('chat_join', lazy='dynamic'))

            user_messages = self.db.relationship('Message', backref='user_message_owner')

            # followers = self.db.relationship('Users', secondary=friends,
            #                           backref=self.db.backref('subscribe', lazy='dynamic'))

            def __init__(self, nick, avatar,
                         descr, password, name,
                         surname):
                self.nick = nick
                self.avatar = avatar
                self.descr = descr
                self.password = password
                self.name = name
                self.surname = surname

        class UserSchema(self.ma.Schema):
            class Meta:
                fields = ('nick', 'avatar', 'descr', 'password', 'name', 'surname')

        self.user = Users
        self.user_schema = UserSchema()
        self.users_schema = UserSchema(many=True)

        class Message(self.db.Model):
            id = self.db.Column(self.db.INTEGER, primary_key=True)
            time = self.db.Column(self.db.DATE, default=func.now(), nullable=False)
            text = self.db.Column(self.db.VARCHAR(1000), nullable=False)
            sentby = self.db.Column(self.db.Integer, self.db.ForeignKey('users.id'))
            chat = self.db.Column(self.db.Integer, self.db.ForeignKey('chat.id'))

            def __init__(self, text, time=func.now()):
                self.text = text
                self.time = time

        self.message = Message

        class Chat(self.db.Model):
            id = self.db.Column(self.db.INTEGER, primary_key=True)
            type = self.db.Column(self.db.VARCHAR(12), nullable=False)
            title = self.db.Column(self.db.VARCHAR(80), nullable=False)
            avatar = self.db.Column(self.db.VARCHAR(100))

            chat_messages = self.db.relationship('Message', backref='chat_message_owner')

            def __init__(self, type, title,
                         avatar=None):
                self.type = type
                self.title = title
                self.avatar = avatar

        self.chat = Chat

        class Post(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            text = self.db.Column(self.db.VARCHAR(1000), nullable=False)
            photo = self.db.Column(self.db.VARCHAR(200))
            time = self.db.Column(self.db.DATE, default=func.now())
            views = self.db.Column(self.db.NUMERIC(7), default=0, nullable=False)
            likes = self.db.Column(self.db.NUMERIC(7), default=0, nullable=False)

            def __init__(self, text, time=func.now(), photo=None,
                         views=0, likes=0):
                self.text = text
                self.time = time
                self.photo = photo
                self.views = views
                self.likes = likes

        self.post = Post

        class Public(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            title = self.db.Column(self.db.VARCHAR(80), nullable=False)
            avatar = self.db.Column(self.db.VARCHAR(100))
            description = self.db.Column(self.db.VARCHAR(200))
            post_published = self.db.relationship('Post', secondary=self.post_published_by_public,
                                                  backref=self.db.backref('pub_published', lazy='dynamic'))

            def __init__(self, title, description=None, avatar=None):
                self.title = title
                self.description = description
                self.avatar = avatar

        self.public = Public

        class Roles(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            title = self.db.Column(self.db.VARCHAR(30), nullable=False)

            def __init__(self, title):
                self.title = title

        self.roles = Roles

        self.tables = {'users': Users,
                       'message': Message,
                       'chat': Chat,
                       'post': Post,
                       'public': Public,
                       'roles': Roles}

        self.check = Check(self.db)
        print('self.tables: ', self.tables)
        self.ops = Operations(self.db, self.tables)
        print('self.ops: ', self.ops.tables)
