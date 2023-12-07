from ecommerceApp.models import db


class NewsLetter(db.Model):
    newsletter_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
