
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main import login_manager,db,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(50),  nullable=False)
    lastname = db.Column(db.String(50),  nullable=False)
    email = db .Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000),nullable=False)
    picture = db.Column(db.String(60),nullable=True)
    def get_reset_token(self,expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return "User({},{},{},{})".format(self.id,self.firstname,self.email,self.password)

class Images(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(500), nullable=False)
    file = db.Column(db.String(60),nullable=True)
    def __repr__(self):
        return "Post({},{},{},{},{},{},{})".format(self.id,self.title,self.description,self.category,self.file)
