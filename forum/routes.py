from flask import render_template, flash, url_for, request, redirect
from forum import app, bcrypt, db
from flask_login import current_user, login_user, logout_user, login_required
from forum.forms import LoginForm, RegistrationForm, PostForm
from forum.models import User, Post, Comment


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered. Enjoy', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('discussions'))
        else:
            flash('Check email and password. Login Unsuccessful','failure')
    return render_template('login.html', form=form)

@app.route('/discussions', methods=['GET'])
def discussions():
    posts = Post.query.all()
    return render_template('discussions.html',posts=posts)

# creating a conversation
@app.route('/post/new', methods=['GET','POST'])
def post():
    form = PostForm()
    if request.method == 'POST':
        post = Post(topic=form.topic.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added.','success')
        return redirect(url_for('discussions'))
    return render_template('post.html', form=form)

# going to a specific route
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def goto_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        comment = request.form['comment']
        comment_post = Comment(comment=comment, post_id=post.id, author=current_user)
        db.session.add(comment_post)
        db.session.commit()
    comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('post_comments.html',post=post,comments=comments)
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

