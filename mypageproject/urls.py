
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.decorators import login_required
from mypageapp.views import IndexView,SignUpView,ActivateView,AboutmeView,ContactFormView,ContactResultView,DailyCreateView,DailyListView
#画像を表示させるためのimport
from django.conf import settings
from django.conf.urls.static import static
#こちらでも可
# from . import settings
# from django.contrib.staticfiles.urls import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    #ログイン済みならこっちへ
    path('',login_required(IndexView.as_view()), name='index'),
    #ログインしてなければこっちへ
    #djangoが元々用意しているURLが入力されると飛ぶように設定
    path('',include('django.contrib.auth.urls')),
    path('signup/',SignUpView.as_view(), name = 'signup'),
    path('activate/<uidb64>/<token>/',ActivateView.as_view(),name='activate'),
    path('aboutme/',AboutmeView.as_view(), name = 'aboutme'),
    path('contact/',ContactFormView.as_view(), name='contact_form'),
    path('contact/result/',ContactResultView.as_view(),name='contact_result'),
    path('daily_create/',DailyCreateView.as_view(),name='daily_create'),
    path('daily_list/',DailyListView.as_view(),name='daily_list'),
]
#画像を表示させるため
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#こちらでも可
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
