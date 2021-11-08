from app import app, db, allowed_file
from flask import url_for, redirect, render_template, request, jsonify, session, flash
from models import User
from methods import login_user, user_logged
from form import LoginForm, RegistrationForm, ComplaintForm
from werkzeug.utils import secure_filename
import os

@app.route('/')
def home_page():
    return render_template("index.html", current=110)


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if "logged_in" in session.keys() and session['logged_in'] is True:
        return redirect("/")
    else:
        if request.method == "POST":
            data = request.form.to_dict()
            user = User.query.filter_by(username=data['username'], password=data['password']).first()
            if user:
                login_user(data)
                flash(f'User has been successfully registered', 'success')
                return redirect("/")
            else:
                flash(f'Incorrect User/Password', 'danger')
                return redirect("/login")
        else:
            return render_template("login.html", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register_page():
    form = RegistrationForm()
    if request.method == "POST":
        data = request.form.to_dict()
        if User.query.filter_by(username=data['username']).first():
            flash("User is already registered", "danger")
            return redirect("/register")
        user = User(data['username'], data['password'])
        db.session.add(user)
        db.session.commit()
        flash(f'User has been successfully registered', 'success')
        return redirect("/login")

    else:
        return render_template("/register.html", form=form)


@app.route("/send_complaint", methods=['POST', 'GET'])
def send_complaint():
    if user_logged() or 1 == 1:
        form = ComplaintForm()
        if request.method == "POST":
            if True is True:
                print(request.files)
                files = request.files['media[]']
                print(files)
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                flash('File(s) successfully uploaded')
                return redirect('/complaint')
            else:
                flash("Please Complete Form", "danger")
                return redirect("/send_complaint")

        else:
            return render_template("send_complaint.html", form=form)
    else:
        return redirect("/unauthorized")


@app.route("/complaint", methods=['GET'])
def complaint():
    if request.args.get("show") is "resolved":
        return render_template("complaint.html")
    else:
        return render_template("complaint.html")


@app.route("/logout")
def logout():
    del session['logged_in']
    del session['username']
    del session['password']
    return redirect("/login")


@app.route("/unauthorized")
def unauthorized():
    return "unauthorized user"
