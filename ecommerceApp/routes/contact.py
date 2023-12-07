from flask_mail import Message
from flask import Blueprint, render_template, request, flash, redirect, url_for


contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
def contact_route():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        message = request.form['message']

        subject = f'New Inquiry from {name}'
        body = f'Email: {email}\n\nMessage: {message}'

        msg = Message(subject, recipients=['ettaouafabdelhay87@gmail.com'])
        msg.body = body

        #mail.send(msg)
        flash("Your message has been sent successfully!", category="success")
        return redirect(url_for('contact.contact_route'))

    return render_template("contact.html", title="Contact")
