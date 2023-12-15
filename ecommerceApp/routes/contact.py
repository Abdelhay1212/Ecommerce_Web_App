from ecommerceApp import mail
from flask_mail import Message
from flask import Blueprint, render_template, request, flash, redirect, url_for


contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
def contact_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        subject = f'New Inquiry from {name}'
        body = f'Email: {email}\n\nMessage: {message}'

        msg = Message(subject, recipients=['abdelhaytaouaf66@gmail.com'])
        msg.body = body

        try:
            mail.send(msg)
            flash("Your message has been sent successfully!", category="success")
        except Exception as e:
            print(e)
            flash("Failed to send your message, please try again!", category='danger')

        return redirect(url_for('contact.contact_route'))

    return render_template("contact.html", title="Contact")
