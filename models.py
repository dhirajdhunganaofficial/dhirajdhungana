from extensions import db

class Blog(db.Model):

    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)

    sub_heading = db.Column(db.String(255), default="Wonderful")

    title = db.Column(db.String(255), nullable=False)

    slug = db.Column(db.String(255), unique=True, nullable=False)

    content = db.Column(db.Text, nullable=False)

    country = db.Column(db.String(255), nullable=False)

    youtube_url = db.Column(db.String(500), nullable=True, comment='Standard YouTube video embed URL')

    youtube_short_url = db.Column(db.String(500), nullable=True, comment='YouTube Shorts embed URL')

    tiktok_url = db.Column(db.String(500), nullable=True, comment='TikTok video embed URL')

    facebook_url = db.Column(db.String(500), nullable=True, comment='Facebook Reel/Video embed URL')

    instagram_url = db.Column(db.String(500), nullable=True, comment='Instagram Reel embed URL')

    featured = db.Column(db.Boolean, default=False)

    featured_type = db.Column(db.String(255), nullable=False, default=None)

    has_blog = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    images = db.relationship(
        "Image",
        backref="blog",
        cascade="all, delete",
        lazy=True
    )

class Image(db.Model):

    __tablename__ = "images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("blogs.id"),
        nullable=False
    )

    caption = db.Column(
        db.Text,
        nullable=True
    )

    alt_text = db.Column(
        db.Text,
        nullable=True
    )

    type = db.Column(
        db.String(20),
        nullable=False,
        default="gallery"
    )

    is_thumbnail = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    variants = db.relationship(
        "ImageVariant",
        backref="image",
        cascade="all, delete-orphan",
        lazy=True
    )

class ImageVariant(db.Model):

    __tablename__ = "image_variants"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey("images.id"),
        nullable=False
    )

    image_url = db.Column(
        db.String(500),
        nullable=False
    )

    width = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )