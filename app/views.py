from flask import render_template, flash, redirect
from app import app, db, models
from .forms import LoginForm, BarkForm, RegistrationForm
from .models import User, Bark
from datetime import datetime
from flask.ext.bcrypt import Bcrypt

activeUser =''
bcrypt = Bcrypt(app)

# home page route
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	# display the bark form and feed
	form = BarkForm()

	# checks activeUser global variable to see if someone is logged in
	user = activeUser #models.User.query.get(1)
	if form.validate_on_submit():
	# 	record bark in database and attach to active user
		bark = Bark(barkBody=form.barkBody.data, timestamp=datetime.utcnow(), author=user)
		db.session.add(bark) 
		db.session.commit() #commit database add
		form.barkBody.data='' #clear form field for bark

	# display all the barks in the database - <<< will need to filter to own posts and friends posts only >>>
	barks = models.Bark.query.all()

	return render_template('index.html', 
							title='Home',
							user=user,
							barks=barks,
							form=form, activeUser=activeUser)
							

# login page							
@app.route("/login", methods=['GET', 'POST'])
def login():
	# show the login form
	form = LoginForm()

	if form.validate_on_submit():
		userEmail = form.email.data # entered email address for login
		userPassword = form.password.data # entered password for login
	
		allUsers = models.User.query.all() # get all registered users
		
		currentUser=1 # variable to 
		for user in allUsers:
			if userEmail == user.email: # look at email field for each user
				# if userPassword == user.password: #verify password matches - plain text
				if bcrypt.check_password_hash(user.password, userPassword): # returns True if hashed password matches
				
				# flash message to display to the user - for debugging only
					# flash('Valid Login requested for email="%s", password=%s' %
					# (userEmail, userPassword))
					
					global activeUser # set active User
					activeUser= user
					return redirect('/index')
				else:
					# flash message - for debugging only
					#flash('Invalid Login requested for email="%s", password=%s' %
					#(userEmail, userPassword))
					return redirect('/invalid')
			else:
				if currentUser < len(allUsers): # if there are still more users to check, don't return invalid
					pass
				else:
					# flash message - for debugging only
					flash('Invalid Login requested for email="%s", password=%s' %
					(userEmail, userPassword))
					return redirect('/invalid')
			currentUser+=1 #increment currentUser variable
	return render_template('login.html', 
							title='Sign In', 
							form=form)

# redirect page for invalid logins    
@app.route("/logout")
def logout():
	global activeUser
	flash('%s %s has successfully logged out.' %
					(activeUser.firstName, activeUser.lastName))
	activeUser = ''
	form = LoginForm()
	return render_template('login.html', 
							title='Sign In', 
							form=form)

# redirect page for invalid logins    
@app.route("/invalid")
def invalid():
	return render_template('invalid.html', title='Invalid Login Attempt')
	
	
@app.route("/admin", methods=['GET', 'POST']) # temporary way to manually view and add users
def admin():
	form = RegistrationForm()
	
	if form.validate_on_submit():
	# 	record bark in database and attach to active user
		pw_hash = bcrypt.generate_password_hash(form.password.data) #generate hash for password
		user = User(firstName=form.firstName.data, 
					lastName=form.lastName.data, 
					email=form.email.data,
					password=pw_hash)
					
		db.session.add(user) 
		db.session.commit() #commit database add
		# form.barkBody.data='' #clear form field for bark
	allUsers = models.User.query.all() # get all registered users
	return render_template('admin.html', title='Admin Page', allUsers=allUsers, form=form)
	
	