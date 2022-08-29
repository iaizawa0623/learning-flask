import logging
import os

from flask import (
	Flask,
	render_template,
	url_for,
	current_app,
	g,
	request,
	redirect,
	flash,
	make_response,
	session,
)
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = '2AZSMss3p5QPbcY2hBsJ'
app.logger.setLevel(logging.DEBUG)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
toolbar = DebugToolbarExtension(app)

@app.get('/contact')
def contact():
	response = make_response(render_template('contact.html'))
	response.set_cookie('flaskbook key', 'flaskbook value')
	session['usename'] = 'ichiro'
	return response

@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		description = request.form['description']

		is_valid = True

		if not username:
			flash('ユーザー名は必須です')
			is_valid = False
		
		if not email:
			flash('メールアドレスは必須です')
			is_valid = False

		try:
			validate_email(email)
		except EmailNotValidError:
			flash('メールアドレスの形式で入力してください')
			is_valid = False

		if not description:
			flash('お問い合わせ内容は必須です')
			is_valid = False

		if not is_valid:
			return redirect(url_for('contact'))

		send_mail(
			email,
			'問い合わせありがとうございました。',
			'contact_mail',
			username=username,
			description=description,
		)
		flash('問い合わせ内容はメールにて送信しました。問い合わせありがとうございました。')
		return redirect(url_for('contact_complete'))
	return render_template('contact_complete.html')

def send_mail(to, subject, template, **kwargs):
	"""メールを送信する関数"""
	msg = Message(subject, recipients=[to])
	msg.body = render_template(template + ".txt", **kwargs)
	msg.html = render_template(template + ".html", **kwargs)
	mail.send(msg)
