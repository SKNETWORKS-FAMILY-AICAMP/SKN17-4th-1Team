from django.urls import path
from app import views
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('sign/', views.sign, name='sign'),
    path('chat/', views.chat, name='chat'),
    path('email/', views.email, name='email'),         # 이메일 입력
    path('password/', views.password, name='password'),    # 새 비밀번호 입력
    path('terms/', views.terms, name='terms'),  # ✅ 약관 보기
    path("chat/api/send/", views.chat_send, name="chat_send"),
    path("chat/api/list/", views.chat_list, name="chat_list"),
    path("test-email/", views.test_email),
    path("email/send-code/", views.ajax_send_code, name="ajax_send_code"),
    path("email/verify-code/", views.ajax_verify_code, name="ajax_verify_code"),
]