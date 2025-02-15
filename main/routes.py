import re
import decimal
import json
from flask import render_template, url_for, flash, redirect,request,jsonify,Blueprint,session
from main import app,db,bcrypt,fujs,mail,ALLOWED_EXTENSIONS
from main.forms import (addCategory,editCategory,LoginForm,editUser,addPost,editCategory,RegistrationForm,editPost,SendEmail,RequestResetForm, ResetPassword,ConfirmEmail)
from main.models import User,Images,Category
from flask_login import current_user,login_user,login_required,logout_user
from time import localtime,strftime
from flask_mail import Message
import requests
import stripe
from werkzeug.utils import secure_filename
import secrets
from PIL import Image,ImageTk
import os


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path  = os.path.join(app.root_path,"static/images/",picture_fn)
    pic_size = (500,500)
    i = Image.open(form_picture)
    i.resize(pic_size)
    i.save(picture_path)
    newPic = Image.open(picture_path)
    newPic.save(picture_path)
    return picture_fn




@app.route("/",methods=["GET","POST"])
@app.route("/home/",methods=["GET","POST"])
def home(): 
    category_form = editCategory()
    contact_form = SendEmail()
    images = Images.query.all()
    query = db.session.query(Images)
    users= User.query.all()
    form = SendEmail()
    categories = Category.query.all()

    # Send email from contact form
    if form.validate_on_submit() and request.method=="POST" :
        from_email = form.customer_email.data
        from_name = form.name.data
        from_surname = form.surname.data
        from_phnumber = form.phoneno.data
        text = form.text.data
        msg = Message("Hey There",recipients="alessiogiovannini@hotmail.it".split())
        msg.html = "form.description.data" + str(request.base_url)
        msg.html = "<p>Hello!</p><p></p>"+ from_name + " would like to be contacted!</p><p></p><p> Client email: </p><p> "+ from_email+"</p><p></p><p> Client Phone No.:  </p><p>" + from_phnumber+"</p><p></p><p> Client name No.:  </p><p>" + from_name+ ":<p></p> Message: </p><p>"+ text +"</p><p></p>"
        mail.send(msg)
        flash("Your message has been succesfully sent! We'll contact you soon.","success")
        return redirect(url_for("home"))
    else:
        for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print(err)



    return render_template("main.html", images=images, User=users,contact_form=contact_form,categories=categories)
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
@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/add_category/",methods=["GET","POST"])
def add_category():
    form = addCategory()
    if request.method == 'POST':
            if form.validate_on_submit():
                title = form.title.data
                description = form.description.data
                picture = save_picture(form.picture.data)
                alt_text = form.alt_text.data
                category = Category(title=title,description=description,picture=picture,alt_text=alt_text)
                db.session.add(category)
                db.session.commit()
                flash("New category created: {}".format(title), "success")
            else:
                flash('Error! Category not added','error')
    return render_template('add_category.html',form=form)
def is_filled(data):
   if data == None:
      return False
   if data == '':
      return False
   if data == []:
      return False
   return True
@app.route("/edit_category/")
@app.route("/edit_category/<id>",methods=["GET","POST"])
def edit_category(id=None):
    if id == None:
        flash("No category selected",'error')
        return redirect(url_for("home"))
    form = editCategory()
    category = Category.query.get_or_404(id)

    if request.method == 'GET':
        form.title.data = category.title
        form.description.data = category.description
        form.alt_text.data = category.alt_text

    if request.method == 'POST':
            if form.validate_on_submit():
                title = form.title.data
                description = form.description.data
                if is_filled(form.picture.data):
                    picture = save_picture(form.picture.data)
                else:

                    picture = category.picture
                alt_text = form.alt_text.data
                category = Category(title=title,description=description,picture=picture,alt_text=alt_text)
                db.session.add(category)
                db.session.commit()
                flash("Category updated: {}".format(title), "success")
                return redirect(url_for('home'))
            else:
                flash('Error! Category not updated','error')
    return render_template('edit_category.html',form=form)

@app.route("/delete_category/")
@app.route("/delete_category/<id>",methods=["GET","POST"])
def delete_category(id=None):
    if id == None:
        flash('Missing image ID','error')
        return redirect(url_for('home'))
    Category.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Congratulations, category deleted", "success")     
    return redirect(url_for('home'))




@app.route("/gallery/<category>",methods=["GET","POST"])
@app.route("/gallery/",methods=["GET","POST"])
def gallery(category = None):
    if category == None:
        images = Images.query.all()
        total_img = len(images)
    else:
        images = Images.query.filter(Images.category == category).all()
        total_img = len(images)
  
    form = addPost()

    if request.method =="POST":
        if form.validate_on_submit():
            title = form.title.data
            text  =form.text.data
            category = form.category.data
            column = form.column.data
            picture = save_picture(form.picture.data)
            alt_text = form.alt_text.data
            new_image = Images( title=title,
                                description = text,
                                file=picture,
                                category=category,
                                alt_text = alt_text,
                                column = column
                            )
            db.session.add(new_image)
            db.session.commit()
            flash("New photo added : {}".format(title), "success")
            return redirect(url_for("gallery"))

        elif form.validate_on_submit()==False:
            flash("Error! Photo not created", "error")
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print(err)
            return render_template("add_pic.html", form=form,images=images,total_img=total_img)
    return render_template('gallery.html',images=images,form=form,total_img = total_img)


@app.route("/edit_image/")
@app.route("/edit_image/<id>",methods=["GET","POST"])
def edit_image(id=None):
    if id == None:
        flash('Missing image ID','error')
        return redirect(url_for('home'))
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
            form.column.data = img.column
            form.alt_text.data = img.alt_text
    if request.method =="POST":
        if form.validate_on_submit():
            img.title = form.title.data
            img.description = form.text.data
            img.category = form.category.data
            img.column = form.column.data
            img.alt_text = form.alt_text.data
            if form.picture.data:
                img.file = save_picture(form.picture.data)
            db.session.commit()
            flash("Congratulations, photo updated", "success")
            return redirect(url_for("gallery"))
        elif form.validate_on_submit()==False:
            flash("Error! Photo not updated", "error")
            return render_template("edit_img.html", form=form,image=img)
        
    return render_template("edit_img.html", form=form,image=img)
@app.route("/delete_image/")
@app.route("/delete_image/<id>",methods=["GET","POST"])
def delete_image(id=None):
    if id == None:
        flash('Missing image ID','error')
        return redirect(url_for('pictures'))
    Images.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Congratulations, post updated", "success")     
    return redirect(url_for('pictures'))

@app.route("/register/",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    # if not current_user.is_authenticated:
    #     flash('You are not the admin!','error')
    #     return redirect(url_for("home"))
    if request.method =="POST":
        print("POST")
        if form.validate_on_submit():
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

@app.route("/edit_user/",methods=["GET","POST"])    
@app.route("/edit_user/<id>",methods=["GET","POST"])
def edit_user(id=None):
    if id ==None:
        return redirect(url_for('users'))
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

@app.route("/send_email/",methods=["GET","POST"])
def send_email():
    form = SendEmail()
    if form.validate_on_submit() and request.method=="POST" :
        from_email = form.customer_email.data
        from_name = form.name.data
        from_surname = form.surname.data
        from_phnumber = form.phoneno.data
        text = form.text.data
        msg = Message("Hey There",recipients="alessiogiovannini@hotmail.it".split())
        msg.html = "form.description.data" + str(request.base_url)
        msg.html = "<p>Hello!</p><p></p>"+ from_name + " would like to be contacted!</p><p></p><p> Client email:  "+ from_email+"</p><p></p><p> Client Phone No.:  " + from_phnumber+"</p><p></p><p> Client name No.:  " + from_name+ ":<p></p>"+ form.description.data +"</p><p></p>"
        mail.send(msg)
        flash("Your message has been succesfully sent! We'll contact you soon.","success")
        return redirect(url_for("home"))
    else:
        for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print(err)

    return render_template("main.html",form=form)
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
