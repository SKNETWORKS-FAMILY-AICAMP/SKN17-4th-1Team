from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Message(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, db_index=True, blank=True, default="")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]  # 오래된→최신

    def __str__(self):
        who = self.user.username if self.user_id else (self.session_key or "guest")
        return f"{who}: {self.content[:20]}"

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

class TempPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temp_pw = models.CharField(max_length=128)  # 암호화된 비밀번호 저장 가능
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self, minutes=30):
        return timezone.now() > self.created_at + timedelta(minutes=minutes)

    def __str__(self):
        return f"{self.user.email} / used={self.is_used}"