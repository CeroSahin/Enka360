from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, URL, Length

style = {"class": "ourClasses", "style": "margin: 10px;"}


class AdminLoginForm(FlaskForm):
    username = StringField("Kullanıcı Adı", validators=[DataRequired()], render_kw=style)
    password = PasswordField("Şifre", validators=[DataRequired()], render_kw=style)
    submit = SubmitField("Giriş!", render_kw=style)


class BlogPostForm(FlaskForm):
    title = StringField("Başlık", validators=[DataRequired()], render_kw=style)
    subtitle = StringField("Altbaşlık", validators=[DataRequired()], render_kw=style)
    thumbnail = StringField("Ana Resim URL'si", validators=[DataRequired(), URL()], render_kw=style)
    writer = StringField("Yazar", validators=[DataRequired()], render_kw=style)
    body = CKEditorField("Post", validators=[DataRequired()], render_kw=style)
    submit = SubmitField("Yayınla!", render_kw=style)


class TeamMemberForm(FlaskForm):
    name = StringField("Takım Üyesinin Adı", validators=[DataRequired()], render_kw=style)
    subtitle = StringField("Görevi", render_kw=style)
    image = StringField("Üye Fotoğraf URL'si", validators=[URL()], render_kw=style)
    operation = SelectField("Operasyon", validators=[DataRequired()],
                            choices=[(1, "Takıma Ekle"), (2, "Takımdan Çıkar"), (3, "Kişiyi Düzenle")], render_kw=style)
    submit = SubmitField("Güncelle", render_kw=style)


class UpcomingEventForm(FlaskForm):
    title = StringField("Etkinlik Başlığı", validators=[DataRequired()], render_kw=style)
    date = DateTimeField("Tarih & Saat (dd/mm/yyyy hh:mm formatında girin örneğin 08/09/2021 09:30",
                         format="%d/%m/%Y %H:%M", render_kw=style)
    description = TextAreaField("Kısa Açıklama (max 300 harf)",
                                validators=[DataRequired(), Length(max=300)], render_kw=style)
    image_url = StringField("Etkinlik Görseli URL'si", validators=[URL()], render_kw=style)
    submit = SubmitField("Ekle", render_kw=style)


class CarouselGuestForm(FlaskForm):
    g1_name = StringField("Konuk 1 Adı", validators=[DataRequired()], render_kw=style)
    g1_subtitle = StringField("Konuk 1 Altyazı", validators=[DataRequired()], render_kw=style)
    g1_image_url = StringField("Konuk 1 Fotoğraf URL'si", validators=[DataRequired(), URL()], render_kw=style)
    
    g2_name = StringField("Konuk 2 Adı", validators=[DataRequired()], render_kw=style)
    g2_subtitle = StringField("Konuk 2 Altyazı", validators=[DataRequired()], render_kw=style)
    g2_image_url = StringField("Konuk 2 Fotoğraf URL'si", validators=[DataRequired(), URL()], render_kw=style)
    
    g3_name = StringField("Konuk 3 Adı", validators=[DataRequired()], render_kw=style)
    g3_subtitle = StringField("Konuk 3 Altyazı", validators=[DataRequired()], render_kw=style)
    g3_image_url = StringField("Konuk 3 Fotoğraf URL'si", validators=[DataRequired(), URL()], render_kw=style)
    
    submit = SubmitField("Güncelle", render_kw=style)


class OperationForm(FlaskForm):
    operation = SelectField("İşlem Türü", validators=[DataRequired()], choices=[
        (1, "Ana Sayfaya Gelecek Etkinlik Ekleme"), (2, "Takım Üyesi Ekleme/Çıkarma"),
        (3, "Ana Sayfanın Geçmiş Konukları Slaytını Düzenleme"), (4, "Yeni Blogpostu Oluşturma")
    ], render_kw=style)
    submit = SubmitField("Seç", render_kw=style)
