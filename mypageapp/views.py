from django.views.generic import TemplateView,ListView

class IndexView(TemplateView):
    template_name = 'registration/index.html'

#新規登録周りを実装
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm

#forms.pyの内容を表示
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

#5.ユーザが新規登録して有効化して認証完了ページを表示する
from .forms import activate_user

class ActivateView(TemplateView):
    template_name = 'registration/activate.html'

    def get(self,request,uidb64,token,*args,**kwargs):
        # 正しく認証されればresultにTrueがはいる
        result = activate_user(uidb64,token)
        #コンテキスト情報としてTrueの結果を渡す
        #Trueを載せる理由はactivate.htmlでresultが
        # Trueなら認証成功と表示させるようにするため
        return super().get(request,result=result,**kwargs)

#Aboutmeページを表示
class AboutmeView(TemplateView):
    template_name = 'registration/aboutme.html'

#コンタクトページを表示

# from django.urls import reverse_lazy
# from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'contact/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context
    
#Daily作成ページを表示
from .forms import DailyForm
class DailyCreateView(CreateView):
    template_name = 'daily/daily_create.html'
    form_class = DailyForm
    success_url = reverse_lazy('daily_list')

    #モデルで外部キーを設定している場合、ログインしているユーザの情報を渡すため
    #form_validをオーバーライドする必要がある
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#Daily一覧ページを表示
from .models import Daily
class DailyListView(ListView):
    model = Daily
    template_name = 'daily/daily_list.html'
    