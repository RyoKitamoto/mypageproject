from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

#新規登録時のメールアドレス認証のためのimport
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


User = get_user_model()

#新規登録時のメールに関する内容
#1.メール本文
subject = '登録確認'
message_template = """
ご登録ありがとうございます。
以下URLをクリックして登録を完了してください。
"""

#2.URLを生成
def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + '/activate/{}/{}/'.format(uid, token)


from .models import Profile
from django import forms
class SignUpForm(UserCreationForm):
    #6/17 OneToOneでUserモデルを拡張してみる
    name = forms.CharField(label='ニックネーム',max_length=40)

    class Meta:
        model = User
        #認証にemailとpasswordのみにするためfieldからusernameを削除
        #6/17 ニックネームを追加する
        fields = ('email','name','password1','password2')
        
    def save(self, commit=True):
        #まだDBに登録させないためにcommit=False
        user = super().save(commit=False)
        user.email= self.cleaned_data['email']

        #3.書き換え。認証完了までログイン不可にする
        # user.save()
        # return user
        # user.is_active =False
        #AttributeErrorの解決策模索中。user.active=Falseにしてみて変わるかどうかを試す
        user.active =False

        #ユーザがフォームを送信するとcommit=Trueになり動き出す
        if commit:
            user.save()

            #6/17 Profileモデルを作成・保存する
            name = self.cleaned_data['name']
            profile=Profile(user=user, name=name)
            profile.save()

            #関数でURLを生成
            activate_url = get_activate_url(user)
            #メッセージをくっつける
            message = message_template + activate_url
            #一人にメールをおくる
            user.email_user(subject,message)
            #最後にユーザを保存
            user.save()
        return user
    
#4.送られてきたメールのURLを検証してユーザを有効化する
def activate_user(uidb64,token):
    try:
        #URLからuidをdecode(復元)する
        uid = urlsafe_base64_decode(uidb64).decode()
        #復元したuidのユーザをさがす
        user = User.objects.get(pk=uid)
    #見つからなければFalseを返す
    except Exception:
        return False
    
    #userとtokenを検証する
    if default_token_generator.check_token(user,token):
        #OKなら有効化して
        user.active = True
        #DBに保存して
        user.save()
        #Trueを返す
        return True
    #だめならFalseを返す
    return False

# コンタクトフォーム

from django import forms
# from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class ContactForm(forms.Form):
    name = forms.CharField(
        label = '',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'お名前',
        }),
    )
    
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "Ryo's Mypageからのお問い合わせ"
        message = f"メールアドレス：{self.cleaned_data['email']}\n\nお名前:{self.cleaned_data['name']}\n\nお問い合わせ内容:\n{self.cleaned_data['message']}"
        from_email = self.cleaned_data['email']
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message,from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

#Dailyページを作成
from .models import Daily
class DailyForm(forms.ModelForm):
    class Meta:
        model = Daily
        fields = ('title','content',)