# from django.shortcuts import render, get_object_or_404
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.db.models import Avg, Count
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import viewsets, status
# from rest_framework.views import APIView
# import csv
# import logging
# from xhtml2pdf import pisa
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate, login
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from django.contrib.auth.models import User

# class LoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         token = Token.objects.get(user__username=request.data['username'])
#         return Response({'token': token.key})


# from .models import (
#     Question, Answer, Report, Company, User,
#     FormSession, HealthRiskAssessment, ActivityLog, FormResponse
# )
# from .serializers import (
#     QuestionSerializer, ReportSerializer,
#     HealthRiskAssessmentSerializer, UserProfileSerializer
# )

# logger = logging.getLogger(__name__)

# # Helper Functions
# def calculate_risk(total_score):
#     """Determine health risk category based on total score."""
#     if total_score > 70:
#         return 'High'
#     elif total_score > 40:
#         return 'Medium'
#     return 'Low'


# def send_thank_you_email(user):
#     """Send a thank you email to the user after form submission."""
#     subject = 'Thank You for Submitting the Health Risk Assessment'
#     message = f'Dear {user.username},\n\nThank you for completing the health risk assessment. Your report is now available.'
#     send_mail(subject, message, 'no-reply@mentorhealth.com', [user.email])


# def generate_pdf(report, answers, detailed=False):
#     """Generate a PDF report from the given data using xhtml2pdf."""
#     template_name = 'detailed_report_template.html' if detailed else 'short_report_template.html'
#     html_string = render_to_string(template_name, {'report': report, 'answers': answers})

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'

#     pisa_status = pisa.CreatePDF(html_string, dest=response)
#     if pisa_status.err:
#         return HttpResponse('PDF generation error', status=500)

#     return response


# # API Views
# class UserStatsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Retrieve total user count."""
#         user_stats = {
#             "total_questions": Question.objects.count(),
#             "total_reports": Report.objects.count(),
#             "total_users": User.objects.count(),
#         }
#         return Response(user_stats, status=status.HTTP_200_OK)


# class IsAdminOrReadOnly(IsAdminUser):
#     """Custom permission class to allow read-only access for non-admin users."""
#     def has_permission(self, request, view):
#         return request.method in ['GET', 'HEAD', 'OPTIONS'] or request.user.is_staff


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_user_profile(request):
#     """Update user profile information."""
#     user = request.user
#     serializer = UserProfileSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)


# @api_view(['POST'])
# def submit_form(request):
#     """Submit the health assessment form."""
#     if 'answers' not in request.data:
#         return Response({"error": "Answers are required"}, status=400)

#     user = request.user
#     total_score = 0
#     answers = []

#     for answer_data in request.data['answers']:
#         question_id = answer_data.get('question')
#         score = answer_data.get('score')

#         if question_id is None or score is None:
#             return Response({"error": "Question ID and score must be provided"}, status=400)

#         answer = Answer.objects.create(user=user, question_id=question_id, score=score)
#         answers.append(answer)
#         total_score += score

#     health_risk_score = calculate_risk(total_score)
#     report_type = request.data.get('report_type', 'short')
#     report = Report.objects.create(user=user, health_risk_score=health_risk_score, report_type=report_type)

#     pdf_response = generate_pdf(report, answers, detailed=(report_type == 'detailed'))
#     if pdf_response.status_code == 500:
#         return Response({"error": "Failed to generate PDF"}, status=500)

#     send_thank_you_email(user)
#     return pdf_response


# class UserLogsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Retrieve user activity logs."""
#         logs = ActivityLog.objects.all()
#         log_data = [{"user": log.user.username, "activity": log.activity, "usage": log.usage} for log in logs]
#         return Response(log_data)

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         user = authenticate(request, username=email, password=password)
        
#         if user is not None:
#             return Response({'token': 'your_token_here'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
# class FormResponsesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Retrieve all form responses."""
#         responses = FormResponse.objects.all()
#         response_data = [{"user": response.user.username, "answer": response.answer, "score": response.score} for response in responses]
#         return Response(response_data)


# class CustomAuthToken(ObtainAuthToken):
#     """Custom token authentication."""
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})


# class HealthRiskAssessmentViewSet(viewsets.ModelViewSet):
#     queryset = HealthRiskAssessment.objects.all()
#     serializer_class = HealthRiskAssessmentSerializer
#     permission_classes = [IsAuthenticated]


# @api_view(['GET'])
# def collective_report(request):
#     """Generate a collective report for a company's employees."""
#     company_id = request.GET.get('company')
#     employees = User.objects.filter(company=company_id)

#     total_respondents = employees.count()
#     avg_age = employees.aggregate(Avg('age'))['age__avg']
#     male_count = employees.filter(gender='Male').count()
#     female_count = employees.filter(gender='Female').count()
#     male_to_female_ratio = male_count / female_count if female_count else 'N/A'
#     avg_bmi = employees.aggregate(Avg('bmi'))['bmi__avg']

#     high_risk_conditions = Answer.objects.filter(score__gte=15) \
#         .values('question__question_text') \
#         .annotate(count=Count('id'))

#     collective_data = {
#         'total_respondents': total_respondents,
#         'avg_age': avg_age,
#         'male_to_female_ratio': male_to_female_ratio,
#         'avg_bmi': avg_bmi,
#         'high_risk_conditions': high_risk_conditions
#     }

#     return Response(collective_data)


# @api_view(['GET'])
# def demographic_analysis(request):
#     """Analyze user demographics."""
#     total_users = User.objects.count()
#     male_count = User.objects.filter(gender='Male').count()
#     female_count = User.objects.filter(gender='Female').count()
#     other_count = User.objects.filter(gender='Other').count()

#     return Response({
#         'total_users': total_users,
#         'gender_distribution': {
#             'Male': male_count,
#             'Female': female_count,
#             'Other': other_count
#         }
#     })


# class ReportViewSet(viewsets.ModelViewSet):
#     """Viewset for managing health risk reports."""
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer
#     permission_classes = [IsAdminUser]


# @api_view(['GET'])
# def get_company_form(request, url):
#     """Retrieve the company and its related questions."""
#     company = get_object_or_404(Company, unique_url=url)
#     questions = Question.objects.all()
#     serialized_questions = QuestionSerializer(questions, many=True)

#     return Response({'company': company.name, 'questions': serialized_questions.data})


# @api_view(['GET'])
# def additional_analytics(request):
#     """Provide additional analytics based on employee responses."""
#     employees = User.objects.all()
#     unaware_conditions_count = employees.filter(answers__question__question_text="Do you have diabetes?", answers__answer_text="No").count()
#     opd_expenditures = employees.aggregate(Avg('opd_expenditure'))['opd_expenditure__avg']
#     ipd_expenditures = employees.aggregate(Avg('ipd_expenditure'))['ipd_expenditure__avg']

#     analytics = {
#         'unaware_conditions': unaware_conditions_count,
#         'avg_opd_expenditures': opd_expenditures,
#         'avg_ipd_expenditures': ipd_expenditures,
#     }

#     return Response(analytics)



# @api_view(['POST'])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return JsonResponse({'message': 'Login successful'}, status=200)
#     return JsonResponse({'message': 'Invalid credentials'}, status=400)

# @api_view(['POST'])
# def submit_form_session(request, session_id):
#     """Submit the form associated with a specific session."""
#     session = get_object_or_404(FormSession, id=session_id)

#     if session.completed:
#         return Response({"error": "Form already submitted"}, status=400)

#     data = request.data
#     total_score = sum(answer_data.get('score', 0) for answer_data in data['answers'])

#     for answer_data in data['answers']:
#         Answer.objects.create(session=session, question_id=answer_data['question'], score=answer_data.get('score'))

#     session.completed = True
#     session.save()

#     health_risk_score = calculate_risk(total_score)
#     report = Report.objects.create(user=session.user, health_risk_score=health_risk_score)
#     send_thank_you_email(session.user)

#     pdf_response = generate_pdf(report, data['answers'], detailed=False)
#     if pdf_response.status_code == 500:
#         return Response({"error": "Failed to generate PDF"}, status=500)

#     return pdf_response


# @api_view(['GET'])
# def export_responses_to_excel(request, company_id):
#     """Export health assessment responses to a CSV file."""
#     company = get_object_or_404(Company, id=company_id)
#     answers = Answer.objects.filter(session__company=company)

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="{company.name}_responses.csv"'
    
#     writer = csv.writer(response)
#     writer.writerow(['User', 'Question', 'Answer', 'Score'])

#     for answer in answers:
#         writer.writerow([answer.session.user.username, answer.question.question_text, answer.answer_text, answer.score])
    
#     return response



# @api_view(['GET'])
# def company_analytics(request, company_id):
#     """Generate analytics for a specific company."""
#     company = get_object_or_404(Company, id=company_id)
#     avg_health_score = Answer.objects.filter(session__company=company).aggregate(Avg('score'))['score__avg']
#     risk_distribution = Answer.objects.filter(session__company=company) \
#         .values('score') \
#         .annotate(count=Count('id'))

#     return Response({
#         'avg_health_score': avg_health_score,
#         'risk_distribution': risk_distribution
#     })


# @api_view(['POST'])
# def submit_form_with_bmi(request, session_id):
#     """Submit the form with BMI information."""
#     session = get_object_or_404(FormSession, id=session_id)
#     data = request.data

#     total_score = sum(answer_data.get('score', 0) for answer_data in data['answers'])
#     bmi = calculate_bmi(session.user)  # Assume calculate_bmi function is defined elsewhere
#     prevalent_conditions = identify_high_risk_conditions(session.user)  # Assume function defined elsewhere
#     health_risk_score = calculate_risk(total_score)

#     report = Report.objects.create(
#         user=session.user,
#         health_risk_score=health_risk_score,
#         bmi=bmi,
#         prevalent_conditions=prevalent_conditions,
#         opd_expenditure=data.get('opd_expenditure', 0),
#         ipd_expenditure=data.get('ipd_expenditure', 0)
#     )

#     pdf_response = generate_pdf(report, data['answers'], detailed=True)
#     if pdf_response.status_code == 500:
#         return Response({"error": "Failed to generate PDF"}, status=500)

#     return pdf_response

import os
import csv
import logging
from pathlib import Path
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db.models import Avg, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from xhtml2pdf import pisa
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import (
    Question, Answer, Report, Company,
    FormSession, HealthRiskAssessment, ActivityLog, FormResponse
)
from .serializers import (
    QuestionSerializer, ReportSerializer,
    HealthRiskAssessmentSerializer, UserProfileSerializer
)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import YourModel  # Adjust this import based on your actual model

@api_view(['GET'])
def export_responses_to_excel(request, company_id):
    # Your logic for exporting responses to Excel goes here
    return Response({'message': 'Export functionality not yet implemented'})


logger = logging.getLogger(__name__)

# Helper Functions
def calculate_risk(total_score):
    """Determine health risk category based on total score."""
    if total_score > 70:
        return 'High'
    elif total_score > 40:
        return 'Medium'
    return 'Low'

def send_thank_you_email(user):
    """Send a thank you email to the user after form submission."""
    subject = 'Thank You for Submitting the Health Risk Assessment'
    message = f'Dear {user.username},\n\nThank you for completing the health risk assessment. Your report is now available.'
    send_mail(subject, message, 'no-reply@mentorhealth.com', [user.email])

def generate_pdf(report, answers, detailed=False):
    """Generate a PDF report from the given data using xhtml2pdf."""
    template_name = 'detailed_report_template.html' if detailed else 'short_report_template.html'
    html_string = render_to_string(template_name, {'report': report, 'answers': answers})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error', status=500)

    return response

# API Views
class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve total user count."""
        user_stats = {
            "total_questions": Question.objects.count(),
            "total_reports": Report.objects.count(),
            "total_users": User.objects.count(),
        }
        return Response(user_stats, status=status.HTTP_200_OK)

class IsAdminOrReadOnly(IsAdminUser):
    """Custom permission class to allow read-only access for non-admin users."""
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or request.user.is_staff

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update user profile information."""
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def submit_form(request):
    """Submit the health assessment form."""
    if 'answers' not in request.data:
        return Response({"error": "Answers are required"}, status=400)

    user = request.user
    total_score = 0
    answers = []

    for answer_data in request.data['answers']:
        question_id = answer_data.get('question')
        score = answer_data.get('score')

        if question_id is None or score is None:
            return Response({"error": "Question ID and score must be provided"}, status=400)

        answer = Answer.objects.create(user=user, question_id=question_id, score=score)
        answers.append(answer)
        total_score += score

    health_risk_score = calculate_risk(total_score)
    report_type = request.data.get('report_type', 'short')
    report = Report.objects.create(user=user, health_risk_score=health_risk_score, report_type=report_type)

    pdf_response = generate_pdf(report, answers, detailed=(report_type == 'detailed'))
    if pdf_response.status_code == 500:
        return Response({"error": "Failed to generate PDF"}, status=500)

    send_thank_you_email(user)
    return pdf_response

class UserLogsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve user activity logs."""
        logs = ActivityLog.objects.all()
        log_data = [{"user": log.user.username, "activity": log.activity, "usage": log.usage} for log in logs]
        return Response(log_data)

class LoginView(ObtainAuthToken):
    """Custom Login View to handle user authentication."""
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

class FormResponsesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all form responses."""
        responses = FormResponse.objects.all()
        response_data = [{"user": response.user.username, "answer": response.answer, "score": response.score} for response in responses]
        return Response(response_data)

class HealthRiskAssessmentViewSet(viewsets.ModelViewSet):
    queryset = HealthRiskAssessment.objects.all()
    serializer_class = HealthRiskAssessmentSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
def collective_report(request):
    """Generate a collective report for a company's employees."""
    company_id = request.GET.get('company')
    employees = User.objects.filter(company=company_id)

    total_respondents = employees.count()
    avg_age = employees.aggregate(Avg('age'))['age__avg']
    male_count = employees.filter(gender='Male').count()
    female_count = employees.filter(gender='Female').count()
    male_to_female_ratio = male_count / female_count if female_count else 'N/A'
    avg_bmi = employees.aggregate(Avg('bmi'))['bmi__avg']

    high_risk_conditions = Answer.objects.filter(score__gte=15) \
        .values('question__question_text') \
        .annotate(count=Count('id'))

    collective_data = {
        'total_respondents': total_respondents,
        'avg_age': avg_age,
        'male_to_female_ratio': male_to_female_ratio,
        'avg_bmi': avg_bmi,
        'high_risk_conditions': high_risk_conditions
    }

    return Response(collective_data)

@api_view(['GET'])
def demographic_analysis(request):
    """Analyze user demographics."""
    total_users = User.objects.count()
    male_count = User.objects.filter(gender='Male').count()
    female_count = User.objects.filter(gender='Female').count()
    other_count = User.objects.filter(gender='Other').count()

    return Response({
        'total_users': total_users,
        'gender_distribution': {
            'Male': male_count,
            'Female': female_count,
            'Other': other_count
        }
    })

class ReportViewSet(viewsets.ModelViewSet):
    """Viewset for managing health risk reports."""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]

@api_view(['GET'])
def get_company_form(request, url):
    """Retrieve the company and its related questions."""
    company = get_object_or_404(Company, unique_url=url)
    questions = Question.objects.all()
    serialized_questions = QuestionSerializer(questions, many=True)

    return Response({'company': company.name, 'questions': serialized_questions.data})

@api_view(['GET'])
def additional_analytics(request):
    """Provide additional analytics based on employee responses."""
    employees = User.objects.all()
    unaware_conditions_count = employees.filter(answers__question__question_text="Do you have diabetes?", answers__answer_text="No").count()
    opd_expenditures = employees.aggregate(Avg('opd_expenditure'))['opd_expenditure__avg']
    ipd_expenditures = employees.aggregate(Avg('ipd_expenditure'))['ipd_expenditure__avg']

    analytics = {
        'unaware_conditions': unaware_conditions_count,
        'avg_opd_expenditures': opd_expenditures,
        'avg_ipd_expenditures': ipd_expenditures,
    }

    return Response(analytics)

@api_view(['POST'])
def submit_form_session(request, session_id):
    """Submit the form associated with a specific session."""
    session = get_object_or_404(FormSession, id=session_id)

    if session.completed:
        return Response({"error": "Form already submitted"}, status=400)

    data = request.data
    total_score = sum(answer_data.get('score', 0) for answer_data in data['answers'])

    for answer_data in data['answers']:
        Answer.objects.create(session=session, question_id=answer_data['question'], score=answer_data.get('score'))

    session.completed = True
    session.save()

    health_risk_score = calculate_risk(total_score)
    Report.objects.create(session=session, health_risk_score=health_risk_score)

    return Response({"message": "Form submitted successfully."}, status=201)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Response  # Make sure this matches the actual model name

@api_view(['GET'])
def export_responses_to_excel(request, company_id):
    # Logic to fetch and export responses
    responses = Response.objects.filter(company_id=company_id)
    # Add logic for exporting to Excel here
    return Response({'message': 'Export functionality not yet implemented'})

