"""
photolog.py
===========
This is a simple example app for Flask-Uploads. It uses Flask-CouchDB as well,
because I like CouchDB. It's a basic photolog app that lets you submit blog
posts that are photos.
"""
import os
import datetime
import uuid
from flask import (Flask, request, url_for, redirect, render_template, flash,
                   session, g)
from flaskext.couchdb import (CouchDBManager, Document, TextField, DateTimeField, ViewField)
from flaskext.uploads import (UploadSet, configure_uploads, IMAGES, UploadNotAllowed)
from werkzeug.security import check_password_hash
from webconfig import DevConfig, ProdConfig
from image_classifier import ImageClassifier


# application
app = Flask(__name__)
app.config.from_object(DevConfig)

# uploads
uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

# documents
db = CouchDBManager()

image_classifier = ImageClassifier()

def unique_id():
    return hex(uuid.uuid4().time)[2:-1]


class Post(Document):
    doc_type = 'post'
    title = TextField()
    filename = TextField()
    location = TextField()
    semantic = TextField()
    scene = TextField()
    caption = TextField()
    published = DateTimeField(default=datetime.datetime.utcnow)

    @property
    def imgsrc(self):
        return uploaded_photos.url(self.filename)

    all = ViewField('Citizen Sensor', '''\
        function (doc) {
            if (doc.doc_type == 'post')
                emit(doc.published, doc);
        }''', descending=True)


db.add_document(Post)
db.setup(app)

# utils
def to_index():
    return redirect(url_for('index'))

@app.before_request
def login_handle():
    g.logged_in = bool(session.get('logged_in'))

# views
@app.route('/')
def index():
    posts = Post.all()
    return render_template('index.html', posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        photo = request.files.get('photo')
        caption = request.form.get('caption')
        if not photo:
            flash("Photo must be present")
        else:
            try:
                filename = uploaded_photos.save(photo)
            except UploadNotAllowed:
                flash("The upload was not allowed")
            else:
                filepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
                result = image_classifier.identify_image(filepath)

                location = '' if not result['location'] else result['location']
                semantic = ', '.join([r[0] for r in result['semantic_categories']])
                scene = ', '.join([r[0] for r in result['scene_attributes']])
                post = Post(title=filename, location=location, semantic=semantic, scene=scene, caption=caption, filename=filename)
                post.id = unique_id()
                post.store()

                flash("Classification completed")
                return to_index()
    return render_template('new.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        flash("You are already logged in")
        return to_index()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_password_hash(app.config['ADMIN_USERNAME'], username) and check_password_hash(app.config['ADMIN_PASSWORD'], password):
            session['logged_in'] = True
            flash("Successfully logged in")
            return to_index()
        else:
            flash("Those credentials were incorrect")
    return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        flash("Successfully logged out")
    else:
        flash("You weren't logged in to begin with")
    return to_index()


if __name__ == '__main__':
    app.run()
