from flask import Flask, flash, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from flask_ckeditor import CKEditor
from forms import *
from typing import Callable
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Text: Callable


db = MySQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CONFIGURING TABLES
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class BlogPost(db.Model):
    __tablename__ = "blog posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, nullable=False)


class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    subtitle = db.Column(db.String)
    image_url = db.Column(db.String, unique=True)


class UpcomingEvent(db.Model):
    __tablename__ = "upcoming events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.String)
    image_url = db.Column(db.String, nullable=False)


class CarouselGuest(db.Model):
    __tablename__ = "carousel guests"
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String, unique=True, nullable=False)
    highlight_sentence = db.Column(db.String, unique=True, nullable=False)
    guest_image = db.Column(db.String, unique=True, nullable=False)


# db.create_all()


# ROUTES ACCESSIBLE TO EVERYBODY
@app.route("/admin-giris", methods=["POST", "GET"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        the_user = User.query.filter_by(username=username).first()
        if the_user is None:
            flash("Kullanıcı adını hatalı girdiniz!")
            return redirect(url_for("admin_login"))
        if password == the_user.password:
            login_user(the_user)
            return redirect(url_for("home"))
        flash("Hatalı şifre girdiniz!")
        return redirect(url_for("admin_login"))

    return render_template("admin-login.html", form=form, current_user=current_user)


@app.route("/")
def home():
    upcoming_events = UpcomingEvent.query.all()
    if upcoming_events:
        upcoming_event = upcoming_events[0]
    else:
        upcoming_event = None
    carousel_guests = CarouselGuest.query.all()
    return render_template("index.html", upcoming_event=upcoming_event,
                           carousel_guests=carousel_guests, current_user=current_user)


@app.route("/takim")
def show_team():
    team_members = Member.query.all()
    return render_template("team.html", team=team_members)


@app.route("/iletisim")
def contact():
    return render_template("contact.html", current_user=current_user)


@app.route("/blog")
def show_blog():
    all_posts = BlogPost.query.all()
    all_posts.reverse()
    return render_template("blog.html", all_posts=all_posts, current_user=current_user)


@app.route("/post/<post_name>")
def show_post(post_name):
    the_post = BlogPost.query.filter_by(title=post_name).first()
    if the_post:
        return render_template("post.html", post=the_post)
    return render_template("404.html", message="Ups! Aradığınız sayfa bulunamadı.")


# LOGIN REQUIRED ROUTES
@login_required
@app.route("/operasyon", methods=["POST", "GET"])
def choose_operation():
    form = OperationForm()
    if form.validate_on_submit():
        operation = int(form.operation.data)
        if operation == 1:
            return redirect(url_for("add_upcoming_event"))
        elif operation == 2:
            return redirect(url_for("edit_team"))
        elif operation == 3:
            return redirect(url_for("update_carousel"))
        return redirect(url_for("add_post"))
    return render_template("operation.html", form=form, current_user=current_user)


@login_required
@app.route("/update-carousel-guests", methods=["POST", "GET"])
def update_carousel():
    form = CarouselGuestForm()
    if form.validate_on_submit():

        # first delete all the existing data in the carousel.
        CarouselGuest.query.delete()
        db.session.commit()

        # now add all the new data to database.
        new_guest_1 = CarouselGuest(
            guest_name=form.g1_name.data,
            highlight_sentence=form.g1_subtitle.data,
            guest_image=form.g1_image_url.data
        )
        new_guest_2 = CarouselGuest(
            guest_name=form.g2_name.data,
            highlight_sentence=form.g2_subtitle.data,
            guest_image=form.g2_image_url.data
        )
        new_guest_3 = CarouselGuest(
            guest_name=form.g3_name.data,
            highlight_sentence=form.g3_subtitle.data,
            guest_image=form.g3_image_url.data
        )
        data = [new_guest_1, new_guest_2, new_guest_3]
        db.session.add_all(data)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update_carousel.html", form=form, current_user=current_user)


@login_required
@app.route("/gelecek-etkinlik-ekle", methods=["POST", "GET"])
def add_upcoming_event():
    form = UpcomingEventForm()
    if form.validate_on_submit():
        title = form.title.data
        date = form.date.data

        # first delete all the existing data in the upcoming events.
        for i in UpcomingEvent.query.all():
            db.session.delete(i)
            db.session.commit()

        # then add the new upcoming event to the database.
        new_upcoming_event = UpcomingEvent(
            title=title,
            description=form.description.data,
            image_url=form.image_url.data,
            date=date.strftime("%d/%m/%Y | %H:%M")
        )
        db.session.add(new_upcoming_event)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_upcoming_event.html", form=form, current_user=current_user)


@login_required
@app.route("/takim-ayarlari", methods=["POST", "GET"])
def edit_team():
    form = TeamMemberForm()
    if form.validate_on_submit():
        operation = int(form.operation.data)
        name = form.name.data
        subtitle = form.subtitle.data
        img = form.image.data

        the_member = Member.query.filter_by(name=name).first()
        # add to team
        if operation == 1:
            if the_member is not None:
                flash("Bu kişi zaten takımda!")
                return redirect(url_for("edit_team"))
            new_member = Member(
                name=name,
                subtitle=subtitle,
                image_url=img
            )
            db.session.add(new_member)
            db.session.commit()
            flash(f"{name} takıma eklendi.")
            return redirect(url_for("edit_team"))
        # remove from team
        elif operation == 2:
            if the_member is None:
                flash("Bu kişi zaten takımda değil!")
                return redirect(url_for("edit_team"))
            db.session.delete(the_member)
            db.session.commit()
            flash(f"{name} takımdan çıkarıldı.")
            return redirect(url_for("edit_team"))
        # update information about the member.
        else:
            if the_member is None:
                flash("Bu kişi takımda değil, bilgilerini güncellemek yerine takıma ekleyin!")
                return redirect(url_for("edit_team"))

            # updating the found user.
            the_member.name = name
            the_member.subtitle = subtitle
            the_member.image_url = img
            db.session.commit()

            flash(f"{name} adlı kişinin bilgileri başarıyla güncellendi!")
            return redirect(url_for("edit_team"))
    return render_template("update_team.html", form=form, current_user=current_user)


# POST RELATED
@login_required
@app.route("/add-post", methods=["POST", "GET"])
def add_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        date = datetime.datetime.today()
        real_date = date.strftime("%d/%m/%Y")
        the_post = BlogPost.query.filter_by(title=form.title.data).first()
        if the_post is not None:
            flash("Bu başlığa sahip bir post zaten var. Farklı bir post ekleyin!")
            return redirect(url_for("add_post"))
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=real_date,
            author=form.writer.data,
            content=form.body.data,
            image_url=form.thumbnail.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("show_post", post_name=new_post.title))
    return render_template("edit-post.html", form=form, post_type="Yeni Post Yaz", current_user=current_user)


@login_required
@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
def edit_post(post_id):
    the_post = BlogPost.query.get(post_id)
    form = BlogPostForm(
        title=the_post.title,
        subtitle=the_post.subtitle,
        writer=the_post.author,
        body=the_post.content,
        thumbnail=the_post.image_url
    )
    if form.validate_on_submit():
        the_post.title = form.title.data
        the_post.subtitle = form.subtitle.data
        the_post.author = form.writer.data
        the_post.content = form.body.data
        the_post.image_url = form.thumbnail.data
        db.session.commit()
        return redirect(url_for("show_post", post_name=the_post.title))
    return render_template("edit-post.html", post_type="Post Editle", form=form, current_user=current_user)


@login_required
@app.route("/delete-post/<int:post_id>", methods=["POST", "GET"])
def delete_post(post_id):
    the_post = BlogPost.query.get(post_id)
    db.session.delete(the_post)
    db.session.commit()
    return redirect(url_for("show_blog"))


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
