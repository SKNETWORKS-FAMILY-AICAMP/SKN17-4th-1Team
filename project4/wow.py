# views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Message, EmailVerification
import re

# 이메일 발송에 필요한 것들
from django.core.mail import send_mail
from django.utils import timezone
import random

def generate_code(length: int = 6) -> str:
    """6자리 숫자 코드 생성 (000000 가능)"""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def send_verification_email(email: str, code: str) -> None:
    """인증번호 이메일 발송"""
    subject = "[CHATIVE] 이메일 인증번호 안내"
    message = (
        f"안녕하세요.\n\n"
        f"요청하신 인증번호는 {code} 입니다.\n"
        f"유효시간: 5분\n\n"
        f"본인이 요청하지 않았다면 이 메일을 무시하셔도 됩니다."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)


@require_POST
def ajax_send_code(request):
    """
    이메일 인증 코드 발송 (AJAX)
    - POST: email
    """
    email = (request.POST.get("email") or "").strip().lower()
    if not email:
        return JsonResponse({"status": "error", "message": "이메일을 입력해주세요."})

    # 최근 60초 이내 재요청 제한
    recent = EmailVerification.objects.filter(email=email).order_by("-created_at").first()
    if recent and (timezone.now() - recent.created_at).total_seconds() < 60:
        return JsonResponse({"status": "error", "message": "너무 자주 요청했습니다. 잠시 후 다시 시도하세요."})

    # 코드 생성 & 저장
    code = generate_code(6)
    EmailVerification.objects.create(email=email, code=code)

    # 메일 발송
    try:
        send_verification_email(email, code)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"메일 발송 실패: {e}"})

    return JsonResponse({"status": "ok", "message": "인증번호를 전송했습니다."})

# models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
class EmailVerification(models.Model):
    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self, minutes=5):
        """5분 후 만료"""
        return timezone.now() > self.created_at + timedelta(minutes=minutes)

    def __str__(self):
        return f"{self.email} / {self.code} / used={self.is_used}"