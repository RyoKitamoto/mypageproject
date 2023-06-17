from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.mail import send_mail



#createsuperuserができなくなってしまったので
# 復讐も兼ねてAbstructUserじゃなくAbstructBaseUserとPermissionMixinで作り直す
# class User(AbstractUser):
#     email = models.EmailField('メールアドレス', unique=True,)
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

    # def create_superuser(self, email, password):
    #     user = self.create_user(
    #         email,
    #         password=password,
    #     )
    #     user.staff = True
    #     user.admin = True
    #     user.save(using=self._db)
    #     return user

#2.カスタマイズしたUserクラスを扱うためにUserManagerクラスを上書きする
#create_user,create_staffuser,create_superuserという三つのメゾットを上書きする
class UserManager(BaseUserManager):
    #一つ目、emailでのユーザ登録を可能にするための上書き
    def create_user(self,email,password=None):
        #メールが入力されなければエラーを出す
        if not email:
            raise ValueError('登録にはメールアドレスが必要です。いれてね')
        #normalizeで正しいemailにしてuserというインスタンスを作成
        user = self.model(email=self.normalize_email(email),)
        #パスワードをセットして
        user.set_password(password)
        #使っているDBに保存をする
        user.save(using=self._db)
        return user
    
    #一つ目のメゾットをつかってstaffを作る場合、superuserを作る場合を設定
    #二つ目
    def create_staffuser(self,email,password):
        user = self.create_user(
            email,
            password=password,
        )
        #staff権限をTrueに
        user.staff=True
        user.save(using=self._db)
        return user
    #三つ目
    def create_superuser(self,email,password):
        user=self.create_user(
            email,
            password=password,
        )
        #staff権限とsuperuser権限を持たせる
        user.staff=True
        user.admin=True
        user.save(using=self._db)
        return user
    
#1.AbstractBaseUserを継承したカスタマイズしたUserクラスを作る
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Eメールアドレス',max_length=255,unique=True)
    #4.forms.pyでusernameを設定してるためcreatesuperuserでエラーがでたのでusernameを追加してみる
    #5.とおもったけど認証に使うものは最低限にするほうが好ましい、usernameを持たせたいなら
    #OneToOneFieldで新しいクラスをつくって紐づけるほうがいいらしいからusernameは消しておく
    # username=models.CharField(verbose_name='お名前',max_length=40)
    #権限の設定３つ
    active = models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    #認証にemailを使用する
    USERNAME_FIELD='email'

    #3.UserManagerを紐付け
    objects=UserManager()

    #インスタンスを作った時の名前をemailに
    def __str__(self):
        return self.email
    #管理者権限がある場合ない場合でTrue/Falseを返す関数
    def has_perm(self, perm, obj=None):
        return self.admin
    #管理者権限がある場合ない場合でTrue/Falseを返す関数
    def has_module_perms(self, app_label):
        return self.admin
    #値にアクセスしやすいようにプロパティを設定３つ
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    # @property
    # def is_active(self):
    #     return self.active

    #AbstractBaseUserにはemail_userメゾットが提供されてないため設定してあげる

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

#Dailyページ作成
from django.utils import timezone
from django.conf import settings
from django import forms

class Daily(models.Model):
    title = models.CharField(verbose_name = 'タイトル',max_length=40)
    content = models.TextField(verbose_name='コンテンツ',max_length=200)
    created_at=models.DateTimeField(verbose_name='作成日時',default=timezone.now)
    updated_at=models.DateTimeField(verbose_name='更新日時',blank=True,null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

#6/17 UserモデルをOneToOneをつかって拡張するモデルクラスを作成
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(verbose_name='ニックネーム',max_length=40)
