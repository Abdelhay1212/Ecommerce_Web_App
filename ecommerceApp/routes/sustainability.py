from flask import Blueprint, render_template


sustainability = Blueprint('sustainability', __name__)

@sustainability.route('/sustainability')
def sustainability_route():
    return render_template("sustainability.html", title="Sustainability")
