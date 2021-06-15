import re
from PIL import Image,ImageTk
import decimal
import json
from flask import render_template, url_for, flash, redirect,request,jsonify,Blueprint,session
from main import app,db,bcrypt,fujs,mail,ALLOWED_EXTENSIONS
from main.forms import (LoginForm,editUser,addPost,RegistrationForm,editPost,SendEmail,RequestResetForm, ResetPassword,ConfirmEmail)
from main.models import User,Images
from flask_login import current_user,login_user,login_required,logout_user
from time import localtime,strftime
from flask_mail import Message
import requests
import secrets
import os
import stripe
from werkzeug.utils import secure_filename
app.config["STRIPE_PUBLIC_KEY"] = "stripe_public_key"
app.config["STRIPE_SECRET_KEY"] = "stripe_secret_key"
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path  = os.path.join(app.root_path,"static/images/",picture_fn)
    
    i = Image.open(form_picture)

    i.save(picture_path)
    newPic = Image.open(picture_path)
   
    newPic.save(picture_path)
    return picture_fn

@app.route("/",methods=["GET","POST"])
@app.route("/home/",methods=["GET","POST"])
def home(): 
    images = Images.query.all()
    query = db.session.query(Images)
    users= User.query.all()
    return render_template("main.html", images=images, User=users)

@app.route("/login/",methods=["GET","POST"])
def login():
    form = LoginForm()
    # if not current_user.is_authenticated:
    #     flash('You are not the admin!','error')
    #     return redirect(url_for("home"))

    if request.method == 'POST':
        
        if form.validate_on_submit():
            print("Valid")
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data) :
                login_user(user)
                flash("Login successfull","success")
                return redirect(url_for("home"))
            else:
                flash("Login Unsuccessful. Please check email and password","error")
                return redirect(url_for("home"))
        else:
            for error in form.errors:
                print(error)
    return render_template("login.html",form=form)


@app.route("/register/",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    # if not current_user.is_authenticated:
    #     flash('You are not the admin!','error')
    #     return redirect(url_for("home"))
    if request.method =="POST":
        print("POST")
        if form.validate_on_submit():
                print("Valid")
                firstname = form.firstname.data
                lastname = form.lastname.data
                email  =form.email.data
                picture = save_picture(form.picture.data)
                password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
                new_user = User(firstname=firstname,email=email,password=password,lastname = lastname,picture=picture)
                db.session.add(new_user)
                db.session.commit()
                flash("Congratulations, account created for {}, you can now sign in.".format(form.firstname.data), "success")
                if current_user.is_authenticated:
                    return redirect(url_for("users"))
                else:
                    return redirect(url_for("login"))
        else:
            flash("An error occurred while creating the account.", "error")
            return render_template("register.html",title="Register",form=form)
    return render_template("register.html",title="Register",form=form)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/add_image/",methods=["GET","POST"])
def add_image():
    form = addPost()
    if request.method=="GET":
        if not current_user.is_authenticated:
            flash('You need an account!','error')
            return redirect(url_for("login"))
    
    if request.method =="POST":
        if form.validate_on_submit():
            title = form.title.data
            text  =form.text.data
            category = form.category.data
            picture = save_picture(form.picture.data)
            new_image = Images(   
                            title=title,
                            description = text,
                            file=picture,
                            category=category,
                            )

            db.session.add(new_image)
            db.session.commit()
            flash("New post created: {}".format(title), "success")
            return redirect(url_for("pictures"))

        elif form.validate_on_submit()==False:
            flash("Error! Post not created", "error")
            return render_template("add_pic.html", form=form)

            
    return render_template("add_pic.html", form=form)



@app.route("/logout/")
def logout():
    logout_user()
    flash("You have been logged out successfully","success")
    return redirect(url_for("home"))


@app.route("/admin/")
def admin():
    
    return render_template('admin.html')


@app.route("/pictures/")
def pictures():
    pictures = Images.query.all()
    return render_template('pictures.html',images=pictures)


@app.route("/users/")
def users():
    users= User.query.all()
    return render_template('users.html',User=users)
@app.route("/edit_user/<id>",methods=["GET","POST"])
def edit_user(id):
  
    user = User.query.get_or_404(id)
    form = editUser()
    if request.method =="GET":
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
    if request.method =="POST":
        if form.validate_on_submit():
            user.firstname = form.firstname.data
            user.lastname =form.lastname.data
            if form.picture.data:
                user.picture = save_picture(form.picture.data)
            db.session.commit()
            flash("Congratulations, user updated", "success")
            return redirect(url_for("users"))
        elif form.validate_on_submit()==False:
            flash("Error! User not updated", "error")
            return render_template("edit_user.html", form=form,user=user)
    return render_template("edit_user.html", user=user,form=form)


@app.route("/edit_image/<id>",methods=["GET","POST"])
def edit_image(id):
    img = Images.query.get_or_404(id)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
    else:
        return redirect(url_for('login'))
    form = editPost()
    if request.method =="GET":
            form.title.data = img.title
            form.text.data = img.description
            form.picture.data = img.file
            form.category.data = img.category  
    if request.method =="POST":
        if form.validate_on_submit():
            img.title = form.title.data
            img.description = form.text.data
            img.category = form.category.data
            if form.picture.data:
                img.file = save_picture(form.picture.data)
            db.session.commit()
            flash("Congratulations, post updated", "success")
            return redirect(url_for("pictures"))
        elif form.validate_on_submit()==False:
            flash("Error! Post not updated", "error")
            return render_template("edit_img.html", form=form,image=img)
        
    return render_template("edit_img.html", form=form,image=img)

@app.route("/sendEmail/<string:id>/<string:post_id>/",methods=["GET","POST"])
@login_required
def send_email(id,post_id):
    form = SendEmail()
    if form.validate_on_submit() and request.method=="POST" :
        recipientUser = User.query.get(id).email
        senderEmail = User.query.get(current_user.id)
        msg = Message("Hey There",recipients="alessiogiovannini@hotmail.it".split(),cc=senderEmail.email.split())
        msg.html = "form.description.data" + str(request.base_url)
        msg.html = "<p>Hello!</p><p></p>"+ senderEmail.firstname + " is interested in your add and I think it would be great if you could exchange more information between you two.</p><p></p><p>Link: "+str(request.base_url) +"</p><p></p><p>Text from "+ senderEmail.firstname +":<p></p>"+ form.description.data +"</p><p></p>"
        mail.send(msg)
        flash("Message sent","success")
        return redirect(url_for("home"))

    if request.method=="GET":
        recipientUser = User.query.get(id).email
        senderEmail = User.query.get(current_user.id)
        form.recipient.data= recipientUser
        return render_template("send_email.html",form=form)
    return render_template("send_email.html",form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",sender="alesisio982017@gmail.com",recipients=[user.email])
    msg.body = """To reset your password, visit the following link:
{}

If you did not make this request then simply ignore this email and no change will be made.

""".format(url_for("reset_token",token=token,_external = True))
    mail.send(msg)



@app.route("/reset_password/",methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.","success")
        return redirect(url_for("login"))
    return render_template("request_reset_password.html",title="Reset Password",form=form)


@app.route("/reset_password/<token>",methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token","error")
        return redirect(url_for("reset_password"))
    form = ResetPassword()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hash_password
        db.session.commit()
        flash("The password has been updated","success")
        return redirect(url_for("login"))

    return render_template("reset_password.html",title="Reset Password",form=form)

