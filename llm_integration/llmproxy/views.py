import os
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from pathlib import Path
import html
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from .utils.llm_client import LLMClient
from .utils.storage import upload_file
from .utils.pdf_to_md import pdf_bytes_to_markdown


def _ensure_session_key(request: HttpRequest) -> str:
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def landing(request: HttpRequest):
    # Use top-level templates (TEMP migrated) and expose auth state
    return render(request, "main.html", {"is_authenticated": request.user.is_authenticated})


def chat_page(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/llm/")
    return render(request, "chat.html")


@login_required
def chat_history(request: HttpRequest):
    session_key = _ensure_session_key(request)
    conv_id = request.GET.get("conversation_id")
    qs = Conversation.objects.filter(user=request.user)
    if conv_id:
        try:
            conv = qs.get(pk=conv_id, user=request.user)
        except Conversation.DoesNotExist:
            return JsonResponse({"ok": False, "error": "conversation not found"}, status=404)
    else:
        conv = qs.order_by("-updated_at", "-id").first()
        if not conv:
            # create an empty conversation for the session
            conv = Conversation.objects.create(user=request.user, session_key=session_key, title="New Chat")

    last50 = list(conv.messages.all().order_by("-id")[:50])
    last50.reverse()
    items = [
        {"id": m.id, "role": m.role, "content": m.content, "file_url": m.file_url, "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        for m in last50
    ]
    return JsonResponse({
        "ok": True,
        "conversation_id": conv.id,
        "title": conv.title,
        "uploaded_pdf_url": conv.uploaded_pdf_url,
        "items": items
    })


@require_POST
@login_required
@transaction.atomic
def chat_send(request: HttpRequest):
    session_key = _ensure_session_key(request)
    content = (request.POST.get("message") or "").strip()
    conv_id = request.POST.get("conversation_id")

    if not content:
        return JsonResponse({"ok": False, "error": "message is empty"}, status=400)

    # resolve conversation
    if conv_id:
        try:
            conv = Conversation.objects.get(pk=conv_id, user=request.user)
        except Conversation.DoesNotExist:
            return JsonResponse({"ok": False, "error": "conversation not found"}, status=404)
    else:
        conv = Conversation.objects.filter(user=request.user).order_by("-updated_at", "-id").first()
        if not conv:
            conv = Conversation.objects.create(user=request.user, session_key=session_key, title="New Chat")

    # save user message
    Message.objects.create(conversation=conv, role="user", content=content)
    # set title from first question if empty
    if not conv.title:
        conv.title = content[:10]
        conv.save(update_fields=["title", "updated_at"])

    # collect last few messages for context
    history = [
        {"role": m.role, "content": m.content}
        for m in conv.messages.all().order_by("-id")[:10][::-1]
    ]

    client = LLMClient()
    import time
    start = time.time()
    attachments = None
    if conv.uploaded_pdf_url and not conv.pdf_context_attached and conv.pdf_context_md:
        attachments = [{"type": "markdown", "content": conv.pdf_context_md, "name": "uploaded.pdf.md"}]

    try:
        result = client.chat(messages=history, attachments=attachments, max_tokens=1024)
        ai = result.get("choices", [{}])[0].get("message", {})
        reply = ai.get("content", "")
    except Exception as e:
        reply = f"LLM error: {e}"
    elapsed_ms = int((time.time() - start) * 1000)

    # save assistant message
    msg = Message.objects.create(conversation=conv, role="assistant", content=reply)
    if attachments:
        conv.pdf_context_attached = True
        conv.save(update_fields=["pdf_context_attached", "updated_at"])

    return JsonResponse({
        "ok": True,
        "conversation_id": conv.id,
        "item": {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_ms": elapsed_ms,
        },
    })


@require_POST
@login_required
def file_upload(request: HttpRequest):
    f = request.FILES.get("file")
    if not f:
        return JsonResponse({"ok": False, "error": "no file"}, status=400)
    if f.size > 10 * 1024 * 1024:
        return JsonResponse({"ok": False, "error": "파일 크기 제한(10MB) 초과"}, status=400)
    conv_id = request.POST.get("conversation_id")
    if not conv_id:
        # create conv if absent
        session_key = _ensure_session_key(request)
        conv = Conversation.objects.create(user=request.user, session_key=session_key, title="")
    else:
        try:
            conv = Conversation.objects.get(pk=conv_id, user=request.user)
        except Conversation.DoesNotExist:
            return JsonResponse({"ok": False, "error": "conversation not found"}, status=404)
    if conv.uploaded_pdf_url:
        return JsonResponse({"ok": False, "error": "이미 PDF가 업로드되었습니다."}, status=400)
    # read bytes first for parsing, then reset for upload
    data_bytes = None
    try:
        data_bytes = f.read()
        if hasattr(f, 'seek'):
            f.seek(0)
    except Exception:
        data_bytes = None

    url = upload_file(f, f.name)
    # set title to pdf name (first 10 chars)
    base_name = f.name.rsplit("/", 1)[-1]
    title_from_pdf = base_name[:10]
    conv.uploaded_pdf_url = url
    conv.title = title_from_pdf
    # try parse PDF to markdown (one-time context)
    try:
        if data_bytes:
            conv.pdf_context_md = pdf_bytes_to_markdown(data_bytes)
            conv.pdf_context_attached = False
    except Exception:
        pass
    conv.save(update_fields=["uploaded_pdf_url", "title", "updated_at"])
    return JsonResponse({"ok": True, "url": url, "conversation_id": conv.id, "title": conv.title})


def _read_policy_file(filename: str) -> str:
    base: Path = settings.BASE_DIR
    p = base / "docs" / filename
    try:
        txt = p.read_text(encoding="utf-8")
        # escape then convert newlines to <br> for safe HTML display
        safe = html.escape(txt).replace("\n", "<br>")
        return f"<div class='text-sm leading-relaxed whitespace-normal'>{safe}</div>"
    except Exception as e:
        return f"<div class='text-sm text-red-600'>문서를 불러오지 못했습니다: {html.escape(str(e))}</div>"


def policy_terms(request: HttpRequest):
    return JsonResponse({"ok": True, "html": _read_policy_file("서비스이용약관.txt")})


def policy_privacy(request: HttpRequest):
    return JsonResponse({"ok": True, "html": _read_policy_file("개인정보동의.txt")})


@login_required
def conversations_list(request: HttpRequest):
    session_key = _ensure_session_key(request)
    qs = Conversation.objects.filter(user=request.user).order_by("-updated_at", "-id")
    data = [
        {"id": c.id, "title": c.title or "새 채팅", "updated_at": c.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
        for c in qs
    ]
    return JsonResponse({"ok": True, "items": data})


@require_POST
@login_required
def conversations_new(request: HttpRequest):
    session_key = _ensure_session_key(request)
    conv = Conversation.objects.create(user=request.user, session_key=session_key, title="새 채팅")
    return JsonResponse({"ok": True, "id": conv.id, "title": conv.title})


@require_POST
@login_required
def conversations_rename(request: HttpRequest):
    conv_id = request.POST.get("id")
    title = (request.POST.get("title") or "").strip()[:255]
    try:
        conv = Conversation.objects.get(pk=conv_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({"ok": False, "error": "conversation not found"}, status=404)
    conv.title = title or "새 채팅"
    conv.save(update_fields=["title", "updated_at"])
    return JsonResponse({"ok": True})


@require_POST
@login_required
def conversations_delete(request: HttpRequest):
    conv_id = request.POST.get("id")
    try:
        conv = Conversation.objects.get(pk=conv_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({"ok": False, "error": "conversation not found"}, status=404)
    conv.delete()
    return JsonResponse({"ok": True})
