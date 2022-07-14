# from turtle import color
from flask import render_template, redirect, url_for, flash, request
from decalog import app
from decalog.models import FoodMenu, User, Classes, Log
from decalog.forms import FoodMenuForm, LoginForm, RegisterForm, ClassesForm
from decalog import db
from flask_login import login_user, logout_user, login_required, current_user
import datetime



@app.route('/')
@app.route('/decalog')
def index():
    return render_template('index.html')


@app.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    cform=ClassesForm() # Instance of ClassForm. This is what's being passed into the html form
    db.create_all()

    # Collects information for verification
    if cform.validate_on_submit():
        class_update = Classes(name=cform.name.data,
                                location=cform.location.data)

        try:
            db.session.add(class_update)
            db.session.commit()
        except:
            db.session.rollback()
            flash(f"Something went wrong!", category='danger')

    classes = Classes.query.all()
    return render_template('classes.html', classes = classes, cform = cform)


@app.route('/availability_update', methods=['GET', 'POST'])
@login_required
def availability_update():
    cform=ClassesForm()
    db.create_all()

    id = request.form.get('id')

    row = Classes.query.filter_by(id=id).first()

    # If the previous color was green, change it to red.
    if row.color == 'green':
        try:
            row.color = 'red'
            row.class_status = 'In use'

            db.session.commit()
        except:
            db.session.rollback()
            flash(f"Something went wrong!", category='danger')
    else:
        # If color was red, change to green
        try:
            row.color = 'green'
            row.class_status = 'Available'

            db.session.commit()            
        except:
            db.session.rollback()
            flash(f"Something went wrong!", category='danger')

    classes = Classes.query.all()
    return render_template('classes.html', classes=classes, cform=cform)



@app.route('/user_availability', methods=['GET', 'POST'])
@login_required
def user_availability():
    id = request.form.get('id')

    # querying for the user info
    # row = User.query.all().filter_by(id=id).first()
    row = User.query.filter_by(id=id).first()
    names = row.names
    lastname = row.lastname

    #formating the date and time
    dt = datetime.datetime.now()
    date = dt.strftime("%x")
    day = dt.strftime("%A")
    time = dt.strftime("%X")

    # if the previous was Available, change it to Unavailable.
    if row.status == 'Available':
        try:
            row.status = 'Unavailable'
            db.session.commit()
            # signout
            dev = Log(day=day, date=date, names=names, lastname=lastname, signout_time=time, signin_time="", user_id=id)
            db.session.add(dev)
            db.session.commit()

        except:
            db.session.rollback()
            flash(f"Something went wrong!", category='danger')
    else: 
        # if Unavailable, change to Available
        try:
            row.status = 'Available'
            db.session.commit()

            #signin
            # fetching the last time they signed out 
            fetch_user = db.session.query(Log).order_by(Log.id.desc()).first()
            
            # checking if they signed in on a different day
            # if yes, create a new row with new sign in details
            if fetch_user.day != day:
                dev = Log(day=day, date=date, names=names, lastname=lastname, signout_time="", signin_time=time, user_id=id)
                db.session.add(dev)
                db.session.commit()

            else:
                # if same day
                # if fetch_user.signin_time == "":
                fetch_user.signin_time = time  

                db.session.commit()  
        except:
            db.session.rollback()
            flash(f"Something went wrong!", category='danger')

    users = User.query.all()
    return render_template('decadevs.html', users = users)



@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    # selects all occupants by room number
    room_401 = User.query.filter_by(room_number='401').all()
    room_402 = User.query.filter_by(room_number='402').all()
    room_403 = User.query.filter_by(room_number='403').all()
    room_404 = User.query.filter_by(room_number='404').all()

    room_501 = User.query.filter_by(room_number='501').all()
    room_502 = User.query.filter_by(room_number='502').all()
    room_503 = User.query.filter_by(room_number='503').all()
    room_504 = User.query.filter_by(room_number='504').all()

    room_601 = User.query.filter_by(room_number='601').all()
    room_602 = User.query.filter_by(room_number='602').all()
    room_603 = User.query.filter_by(room_number='603').all()
    room_604 = User.query.filter_by(room_number='604').all()

    return render_template('rooms.html', room_numbers = [room_401, room_402, room_403, room_404, room_501, room_502, room_503, room_504, room_601, room_602, room_603, room_604])



@app.route('/decadevs', methods=['GET', 'POST'])
@login_required
def decadevs():
    users = User.query.all() # selects all data in the Person table

    # eform populate for the empty form
    # items populates for the table
    return render_template('decadevs.html', users=users)



@app.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    log = Log.query.all()
    # items populate for the table
    return render_template('log.html', log=log)



@app.route('/foodmenu', methods=['GET', 'POST'])
@login_required
def foodmenu():
    menu_form=FoodMenuForm()
    db.create_all()

    if menu_form.validate_on_submit():
        menu_update = FoodMenu(date=menu_form.date.data,
                                brunch=menu_form.brunch.data,
                                dinner=menu_form.dinner.data)

        try:
            db.session.add(menu_update)
            db.session.commit()

        except:
            db.session.rollback()
            flash(f"Something went wrong!", category='danger')

    items = FoodMenu.query.all()
    return render_template('meal-table.html', items=items, menu_form=menu_form)
        




@app.route('/delete/<int:id>')
def delete(id):
    user_delete = FoodMenu.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        flash(f"Successfully deleted!", category='success')
        return redirect(url_for('foodmenu'))
    except:
        flash(f"Something went wrong!", category='danger')



@app.route('/food_edit/<int:id>', methods=['POST', 'GET'])
def food_edit(id):
    food_e = FoodMenu.query.get_or_404(id)

    if request.method == 'POST':
        food_e.date = request.form['date']
        food_e.brunch = request.form['brunch']
        food_e.dinner = request.form['dinner']

        try:
            db.session.commit()
            flash(f"Successfully edited!", category='success')
            return redirect(url_for('foodmenu'))
        except:
            flash(f"Something went wrong!", category='danger')
    
    return render_template('food_edit.html', food_e=food_e)


@app.route('/user_edit/<int:id>', methods=['POST', 'GET'])
def user_edit(id):
    user_e = User.query.get_or_404(id)

    if request.method == 'POST':
        user_e.names = request.form['names']
        user_e.lastname = request.form['lastname']
        user_e.phone = request.form['phone']
        user_e.email_address = request.form['email']
        user_e.stack = request.form['stack']
        user_e.room_number = request.form['room']

        try:
            db.session.commit()
            flash(f"Successfully edited!", category='success')
            return redirect(url_for('decadevs'))
        except:
            flash(f"Something went wrong!", category='danger')
    
    return render_template('user_edit.html', user_e=user_e)



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    db.create_all()

    if form.validate_on_submit():
        user_to_create = User(names=form.names.data,
                            lastname=form.lastname.data,
                            phone=form.phone.data,
                            username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Your account has been successfully created', category='success')

        return redirect(url_for('decadevs'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)



admin = "Admin"
admin = admin.strip()
@app.route('/sign-in', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        admin_user = User.query.filter_by(username=admin).first()
        if admin_user and admin_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(admin_user)
            flash(f'You are now logged in as Administrator!.', category='success')
            return redirect(url_for('index'))

        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are now logged in.', category='success')
            return redirect(url_for('decadevs'))
        else:
            flash('Invalid username or password! Please try again', category='danger')

    return render_template('login.html', form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("index"))