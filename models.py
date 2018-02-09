from google.appengine.ext import ndb

class Message(ndb.Model):
    asunto = ndb.StringProperty()
    email = ndb.StringProperty()
    texto = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()



class User(ndb.Model):
    user_id = ndb.StringProperty()
    nickname = ndb.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

