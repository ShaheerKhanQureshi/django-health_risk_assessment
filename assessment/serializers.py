# from rest_framework import serializers
# from assessment.models import *  # Adjust as necessary
# from django.contrib.auth import get_user_model  # Import user model

# User = get_user_model()  # Get the custom user model

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ['id', 'name', 'unique_url']

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Question
#         fields = ['id', 'question_text', 'question_type', 'score', 'company']

# class AnswerSerializer(serializers.ModelSerializer):
#     question = QuestionSerializer()  # Nested relationship to get question details
    
#     class Meta:
#         model = Answer
#         fields = ['id', 'question', 'answer_text', 'score', 'form_session']

# class FormSessionSerializer(serializers.ModelSerializer):
#     answers = AnswerSerializer(many=True)  # Include related answers for the session

#     class Meta:
#         model = FormSession
#         fields = ['id', 'user', 'company', 'completed', 'answers']

# class ReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Report
#         fields = ['id', 'user', 'health_risk_score', 'bmi', 'generated_at', 'report_type']

# class HealthRiskAssessmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HealthRiskAssessment
#         fields = '__all__'  # Adjust fields as necessary

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User  # Use the imported User model
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Adjust as necessary

from rest_framework import serializers
from assessment.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'unique_url']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Question
        fields = ['id', 'question_text', 'question_type']

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()  # Nested relationship to get question details
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text', 'score']

class FormSessionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)  # Include related answers for the session

    class Meta:
        model = FormSession
        fields = ['id', 'user', 'company', 'completed', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        form_session = FormSession.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(form_session=form_session, **answer_data)
        return form_session

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'health_risk_score', 'generated_at', 'report_type']

class HealthRiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRiskAssessment
        fields = '__all__'  # Adjust fields as necessary

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
