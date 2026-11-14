from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import re

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
    blogs = Blog.query.filter_by(featured = False).order_by(Blog.created_at.desc()).all()
    featuredBlog = Blog.query.filter_by(featured = True).all()
    print(featuredBlog)
    print(blogs)

    primaryFeaturedBlog = None
    secondaryFeaturedBlog = []

    for blog in featuredBlog:
        if (blog.featured_type == 'primary'):
            primaryFeaturedBlog = blog
        else:
            secondaryFeaturedBlog.append(blog)
        print(blog.title)
        print(blog.has_blog)

    # for blog in blogs:
    #     original_date = blog.created_at
    #     date_obj = datetime.strptime(str(original_date), "%Y-%m-%d %H:%M:%S")
    #     formatted_date = date_obj.strftime("%B %d, %Y")
    #     blog.created_at = formatted_date

    return render_template('blogs.html', title='Dhungana Dhungana - Blogs', blogs=blogs, primaryFeaturedBlog=primaryFeaturedBlog, secondaryFeaturedBlog=secondaryFeaturedBlog)

@app.route('/blog/<slug>')
def blog(slug):
    blog = Blog.query.filter_by(slug=slug).first()

    print(blog)
    print(blog.title)
    print(blog.has_blog)

    blog_images = Image.query.filter_by(
        blog_id=blog.id,
        type="blog"
    )

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

    return render_template('blog.html', title=blog.title, blog=blog, thumbnail=thumbnail, blog_images=blog_images, story_images=story_images, gallery_images=gallery_images)

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

def validateContactForm(form):

    # 1. Retrieve submitted values
    name = form.get('Full Name', '').strip()
    email = form.get('Email', '').strip()
    phoneNumber = form.get('Phone Number', '').strip()
    subject = form.get('Subject', '').strip()
    message = form.get('Message', '').strip()

    # 2. Validate required fields
    if not name:
        return "Full Name is required!"

    if not email:
        return "Email is required!"

    if not message:
        return "Message is required!"

    # 3. Validate maximum character lengths
    if len(name) > 100:
        return "Name cannot exceed 100 characters!"

    if len(email) > 254:
        return "Email address is too long!"

    if len(subject) > 150:
        return "Subject cannot exceed 150 characters!"

    if len(message) > 5000:
        return "Message cannot exceed 5000 characters!"

    # 4. Validate email format
    emailPattern = r'^[A-Za-z0-9_%+-]+(?:\.[A-Za-z0-9_%+-]+)*@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$'

    if not re.fullmatch(emailPattern, email):
        return "Please provide a valid email address!"

    # 5. Validate phone number (optional)
    if phoneNumber:

        # Allow digits, spaces, +, brackets and hyphens
        if not re.fullmatch(r'[0-9+\s()-]+', phoneNumber):
            return "Invalid phone number!"

        # Count actual digits
        digits = re.sub(r'\D', '', phoneNumber)

        if not 7 <= len(digits) <= 15:
            return "Phone number must contain 7–15 digits!"

    # 6. All validations passed
    return None

@app.route("/contactInformation", methods=['POST'])
def notifyAboutContactInformation():

    # 1. Check honeypot field exists
    if 'BotChaiyena' not in request.form:
        return "Invalid submission!", 400

    # 2. Check honeypot field is empty
    botField = request.form.get('BotChaiyena', '')

    if botField.strip():
        return "Bot detected!", 400

    # 3. Validate all submitted form fields
    error = validateContactForm(request.form)

    if error:
        return error, 400

    # 4. Retrieve validated information
    name = request.form.get('Full Name', '').strip()
    email = request.form.get('Email', '').strip()
    phoneNumber = request.form.get('Phone Number', '').strip()
    subject = request.form.get('Subject', '').strip()
    message = request.form.get('Message', '').strip()

    # 5. Send email
    sendEmail.sendEmail(name, email, phoneNumber, subject, message)
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