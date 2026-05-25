from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from flask_migrate import Migrate
from config import Config

import sendEmail,createQRCode

app = Flask(__name__)
app.config.from_object(Config)
from extensions import db
db.init_app(app)
migrate = Migrate(app, db)

from models import Blog, Image, ImageVariant

@app.route('/')
def index():
    return render_template('index.html', title='Dhiraj Dhungana', alert=False)

@app.route('/blogs')
def blogs():
    blogs = Blog.query.filter_by(featured = False).all()
    featuredBlog = Blog.query.filter_by(featured = True).all()
    print(featuredBlog)

    primaryFeaturedBlog = None
    secondaryFeaturedBlog = []

    for blog in featuredBlog:
        if (blog.featured_type == 'primary'):
            primaryFeaturedBlog = blog
        else:
            secondaryFeaturedBlog.append(blog)

    for blog in blogs:
        original_date = blog.created_at
        date_obj = datetime.strptime(str(original_date), "%Y-%m-%d %H:%M:%S")
        formatted_date = date_obj.strftime("%B %d, %Y")
        blog.created_at = formatted_date

    return render_template('blogs.html', title='Dhungana Dhungana - Blogs', blogs=blogs, primaryFeaturedBlog=primaryFeaturedBlog, secondaryFeaturedBlog=secondaryFeaturedBlog)

@app.route('/newblog/<slug>')
def newblog(slug):
    blog = Blog.query.filter_by(slug=slug).first()

    print(blog)

    story_images = Image.query.filter_by(
        blog_id=blog.id,
        type="story"
    ).all()

    gallery_images = Image.query.filter_by(
        blog_id=blog.id,
        type="gallery"
    ).all()

    thumbnail = next(
        (
            image
            for image in blog.images
            if image.is_thumbnail
        ),
        None
    )

    return render_template('newblog.html', title=blog.title, blog=blog, thumbnail=thumbnail, story_images=story_images, gallery_images=gallery_images)

@app.route('/travel_blog/<slug>')
def new_blog(slug):

    blog = Blog.query.filter_by(slug=slug).first()

    story_images = Image.query.filter_by(
        blog_id=blog.id,
        type="story"
    ).all()

    gallery_images = Image.query.filter_by(
        blog_id=blog.id,
        type="gallery"
    ).all()

    thumbnail = next(
        (
            image
            for image in blog.images
            if image.is_thumbnail
        ),
        None
    )

    return render_template('travel_blog.html', title=blog.title, blog=blog, thumbnail=thumbnail, story_images=story_images, gallery_images=gallery_images)

@app.route('/oldSite')
def oldSite():
    return render_template('oldSite.html')

@app.route("/contactInformation", methods=['POST'])
def notifyAboutContactInformation():
    name=request.form['Full Name']
    email=request.form['Email']
    phoneNumber=request.form['Phone Number']
    subject=request.form['Subject']
    message=request.form['Message']
    botField = request.form['BotChaiyena']
    print("botField")
    print(botField)
    sendEmail.sendEmail(botField,name,email,phoneNumber,subject,message)
    return redirect(url_for('index'))

@app.route('/qrCode')
def qrCode():
    return render_template('qrCode.html', title='QR Code Generator')

@app.route("/qrCode", methods=['POST'])
def generateQRCode():
    url=request.form['url']
    qrCode = createQRCode.generateQRCode(url)
    return render_template('qrCode.html', qrCode = qrCode)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)