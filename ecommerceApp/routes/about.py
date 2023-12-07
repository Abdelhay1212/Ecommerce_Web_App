from flask import Blueprint, render_template


about = Blueprint('about', __name__)

@about.route('/about')
def about_route():
    return render_template("about.html", title="About")
