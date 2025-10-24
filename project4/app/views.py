from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from datetime import datetime
from .models import Message, EmailVerification  # ★ EmailVerification 함께 import
import re

# 이메일 발송에 필요한 것들
from django.core.mail import send_mail
from django.utils import timezone
import random


# ---------------------------
# 공용 유틸 (views.py 안에 포함)
# ---------------------------
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

def index(request):
    return render(request, 'app/index.html')


def login(request):
    if request.method == "POST":
        raw_id  = (request.POST.get("username") or request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        if not raw_id or not password:
            messages.error(request, "아이디(또는 이메일)와 비밀번호를 모두 입력하세요.")
            return render(request, "app/login.html")

        # 이메일/아이디 구분
        if "@" in raw_id:
            try:
                username_for_auth = User.objects.get(email=raw_id).username
            except User.DoesNotExist:
                messages.error(request, "등록되지 않은 이메일입니다.")
                return render(request, "app/login.html")
        else:
            # 아이디로 로그인
            try:
                username_for_auth = User.objects.get(username=raw_id).username
            except User.DoesNotExist:
                messages.error(request, "등록되지 않은 아이디입니다.")
                return render(request, "app/login.html")

        # Django 인증
        user = authenticate(request, username=username_for_auth, password=password)
        if user and user.is_active:
            auth_login(request, user)
            request.session.cycle_key()  # 세션 고정화 방지
            return redirect("app:chat")
        else:
            messages.error(request, "아이디/이메일 또는 비밀번호가 올바르지 않습니다.")
            return render(request, "app/login.html")

    # GET
    return render(request, "app/login.html")

def chat(request):
    email = request.session.get("user_email", "익명")
    return render(request, 'app/chat.html', {"email": email})


def sign(request):
    if request.method == "POST":
        username  = request.POST.get("username", "").strip()
        email     = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        agree     = request.POST.get("agree")  # 약관 동의 체크박스 ('yes')

        # --- 기본 검증 ---
        if not username or not email or not password1 or not password2:
            messages.error(request, "모든 항목을 입력하세요.")
        elif not agree:
            messages.error(request, "이용약관에 동의해야 회원가입이 가능합니다.")
        elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            messages.error(request, "유효한 이메일 형식을 입력하세요.")
        elif password1 != password2:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "이미 사용 중인 사용자명입니다.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "이미 사용 중인 이메일입니다.")
        else:
            # --- 유저 생성 ---
            user = User.objects.create_user(username=username, email=email, password=password1)

            # (옵션) 바로 로그인
            # user = authenticate(request, username=username, password=password1)
            # if user:
            #     auth_login(request, user)
            #     return redirect("app:chat")

            messages.success(request, "회원가입이 완료되었습니다. 로그인 해주세요.")
            return redirect("app:login")

        # 실패 시 입력값 일부 유지
        return render(request, "app/sign.html", {
            "prefill": {"username": username, "email": email},
        })

    # GET
    return render(request, "app/sign.html")


def terms(request):
    return render(request, 'app/terms.html')


# --- 비밀번호 재설정(임시) ---
def email(request):
    # 이메일 입력 화면(버튼 누르면 코드 입력 화면으로 이동)
    return render(request, 'app/email.html')

def ajax_verify_code(request):
    email = (request.POST.get("email") or "").strip().lower()
    code  = (request.POST.get("code")  or "").strip()

    if not email or not code:
        return JsonResponse({"status": "error", "message": "이메일과 코드를 모두 입력하세요."})

    rec = EmailVerification.objects.filter(email=email, is_used=False).order_by("-created_at").first()
    if not rec:
        return JsonResponse({"status": "error", "message": "인증 요청 기록이 없습니다."})
    if rec.is_expired(5):
        return JsonResponse({"status": "error", "message": "인증번호가 만료되었습니다. 다시 요청하세요."})
    if rec.code != code:
        return JsonResponse({"status": "error", "message": "인증번호가 올바르지 않습니다."})

    # 코드 사용 처리 + 세션 플래그 세팅
    rec.is_used = True
    rec.save()
    request.session["email_verified"] = True
    request.session["verified_email"] = email

    return JsonResponse({"status": "ok", "message": "인증이 완료되었습니다."})

from django.contrib.auth import authenticate, login as auth_login

def password(request):
    if request.method == "POST":
        pw1 = request.POST.get("password1","")
        pw2 = request.POST.get("password2","")
        if not pw1 or not pw2:
            messages.error(request,"새 비밀번호를 모두 입력하세요.")
        elif pw1 != pw2:
            messages.error(request,"두 비밀번호가 일치하지 않습니다.")
        elif not request.session.get("email_verified"):
            messages.error(request,"이메일 인증이 필요합니다.")
            return redirect("app:email")
        else:
            email = request.session.get("verified_email")
            try:
                user = User.objects.get(email=email)
                user.set_password(pw1)    # ← 해시로 저장
                user.is_active = True
                user.save()
            except User.DoesNotExist:
                # 아직 유저가 없다면 새로 생성 (아이디=이메일 전략)
                user = User.objects.create_user(username=email, email=email, password=pw1)
                user.is_active = True
                user.save()

            # 세션 정리
            request.session.pop("email_verified", None)
            request.session.pop("verified_email", None)

            messages.success(request, "비밀번호가 설정되었습니다. 로그인해 주세요.")
            return redirect("app:login")

    return render(request, "app/password.html")

# ---------------------------
# 채팅 API
# ---------------------------
def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


@require_POST
def chat_send(request):
    """메시지 저장 API (로그인 없어도 동작)"""
    session_key = _ensure_session_key(request)
    content = (request.POST.get("content") or "").strip()
    if not content:
        return JsonResponse({"ok": False, "error": "내용이 비었습니다."}, status=400)

    msg = Message.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=session_key,
        content=content,
    )
    return JsonResponse({
        "ok": True,
        "item": {
            "id": msg.id,
            "content": msg.content,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "me": True,
        }
    })


def chat_list(request):
    """최근 50개 메시지 조회"""
    qs = Message.objects.order_by("-id")[:50]
    items = [
        {
            "id": m.id,
            "content": m.content,
            "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "me": (request.user.is_authenticated and m.user_id == request.user.id)
                  or (m.session_key and m.session_key == request.session.session_key),
        }
        for m in reversed(qs)  # 오래된→최신
    ]
    return JsonResponse({"ok": True, "items": items})


# ---------------------------
# 메일 테스트 & 인증코드 발송
# ---------------------------
def test_email(request):
    to = "spaingogo2@gmail.com"  # ← 본인 실제 이메일로 변경!
    sent = send_mail(
        subject="[테스트] Django 이메일 발송 확인",
        message="이메일 설정이 정상 작동합니다.",
        from_email=settings.DEFAULT_FROM_EMAIL,  # settings에 설정된 발신자
        recipient_list=[to],
        fail_silently=False,  # 실패 시 예외 발생 → 콘솔에서 원인 확인 가능
    )
    return HttpResponse(f"✅ send_mail 반환값: {sent} (1이면 성공) / 받는이={to}")


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