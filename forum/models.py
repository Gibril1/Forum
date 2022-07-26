from forum import db, login_manager, admin, ModelView
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(20), nullable = False, unique=True)
        email = db.Column(db.String(60), nullable = False, unique=True)
        password = db.Column(db.String(60), nullable = False)
        posts = db.relationship('Post', backref = 'author', lazy = True)
        comment = db.relationship('Comment', backref = 'author', lazy = True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comments = db.relationship('Comment', backref='poster', lazy = True)


    def __repr__(self):
        return f'Post({self.topic})'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))

        