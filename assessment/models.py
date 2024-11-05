from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# assessment/models.py
from .models import Response  # Adjust based on the actual model name

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models

class Response(models.Model):
    # Define your fields here
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    data = models.JSONField()  # Example field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response for {self.company}'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    usage = models.IntegerField()

class FormResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.IntegerField()

class HealthRiskAssessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Company(models.Model):
    name = models.CharField(max_length=100)
    unique_url = models.CharField(max_length=10, unique=True, default=get_random_string)
    code = models.CharField(max_length=10, default=get_random_string) 

class Question(models.Model):
    QUESTION_TYPES = [
        ('open', 'Open-Ended'),
        ('closed', 'Closed-Ended'),
    ]
    question_text = models.TextField()
    question_type = models.CharField(max_length=6, choices=QUESTION_TYPES)

    def __str__(self):
        return self.question_text

class FormSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

class Answer(models.Model):
    session = models.ForeignKey(FormSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.session.user.username} - {self.question.question_text}"

class Report(models.Model):
    REPORT_TYPES = [
        ('short', 'Short'),
        ('detailed', 'Detailed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    health_risk_score = models.FloatField()
    report_type = models.CharField(max_length=8, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.user.username} - {self.health_risk_score}"

def calculate_risk(total_score):
    """Determine health risk category based on total score."""
    if total_score > 70:
        return 'High'
    elif total_score > 40:
        return 'Medium'
    return 'Low'

def send_thank_you_email(user):
    """Send a thank you email to the user."""
    subject = 'Thank You for Your Submission'
    message = f'Dear {user.username}, thank you for completing the assessment.'
    user.email_user(subject, message)

@api_view(['POST'])
def submit_form(request, session_id):
    session = get_object_or_404(FormSession, id=session_id)

    if session.completed:
        return Response({"error": "Form already submitted"}, status=400)

    data = request.data
    answers = data.get('answers', [])
    if not answers:
        return Response({"error": "No answers provided"}, status=400)

    total_score = sum(answer_data.get('score', 0) for answer_data in answers)

    for answer_data in answers:
        Answer.objects.create(session=session, question_id=answer_data['question'], score=answer_data.get('score'))

    session.completed = True
    session.save()

    health_risk_score = calculate_risk(total_score)
    Report.objects.create(user=session.user, health_risk_score=health_risk_score)
    send_thank_you_email(session.user)

    return Response({"message": "Form submitted successfully", "health_risk_score": health_risk_score})

class Company(models.Model):
    name = models.CharField(max_length=100)
    unique_url = models.CharField(max_length=10, unique=True, default=get_random_string)
    code = models.CharField(max_length=10, default=get_random_string) 

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class FormSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='form_sessions')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='form_sessions')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.company.name}"

# Signal for sending thank you email
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Report)
def send_report_email(sender, instance, created, **kwargs):
    if created:
        send_thank_you_email(instance.user)

# Improved API view with better error handling
@api_view(['POST'])
def submit_form(request, session_id):
    session = get_object_or_404(FormSession, id=session_id)

    if session.completed:
        return Response({"error": "Form already submitted"}, status=400)

    data = request.data
    answers = data.get('answers', [])
    if not answers:
        return Response({"error": "No answers provided"}, status=400)

    total_score = 0
    try:
        for answer_data in answers:
            answer = Answer.objects.create(
                session=session,
                question_id=answer_data['question'],
                score=answer_data.get('score', 0)
            )
            total_score += answer.score or 0  # Accumulate score

    except Exception as e:
        return Response({"error": str(e)}, status=500)

    session.completed = True
    session.save()

    health_risk_score = calculate_risk(total_score)
    Report.objects.create(user=session.user, health_risk_score=health_risk_score)

    return Response({"message": "Form submitted successfully", "health_risk_score": health_risk_score})
from django.db import models

class Response(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response for {self.company}'
