# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import LoginView 
# from .views import (
#     submit_form,
#     collective_report,
#     additional_analytics,
#     get_company_form,
#     export_responses_to_excel,
#     company_analytics,
#     HealthRiskAssessmentViewSet,
#     CustomAuthToken,
#     UserStatsView,
#     UserLogsView,
#     FormResponsesView
# )



# router = DefaultRouter()
# router.register(r'health-assessments', HealthRiskAssessmentViewSet)

# # Consolidated URL patterns
# urlpatterns = [
#     path('api/login/', LoginView.as_view(), name='login'),
#     path('api/forms/submit/', submit_form, name='submit_form'), 
#     path('submit/', submit_form, name='submit_form'),
#     path('collective-report/', collective_report, name='collective_report'),
#     path('additional-analytics/', additional_analytics, name='additional_analytics'),
#     path('form/<str:url>/', get_company_form, name='get_company_form'),
#     path('export-responses/<int:company_id>/', export_responses_to_excel, name='export_responses_to_excel'),
#     path('company-analytics/<int:company_id>/', company_analytics, name='company_analytics'),
#     path('api/assessment/', include(router.urls)),  # Updated base path for the API
#     path('api/assessment/auth/login/', CustomAuthToken.as_view(), name='api_login'),  # Updated path
#     path('api/assessment/user-stats/', UserStatsView.as_view(), name='user-stats'),  # Updated path
#     path('api/assessment/user-logs/', UserLogsView.as_view(), name='user-logs'),  # Updated path
#     path('api/assessment/form-responses/', FormResponsesView.as_view(), name='form-responses'),  # Updated path
# ]































from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    submit_form,
    collective_report,
    additional_analytics,
    get_company_form,
    export_responses_to_excel,
    company_analytics,
    HealthRiskAssessmentViewSet,
    CustomAuthToken,
    UserStatsView,
    UserLogsView,
    FormResponsesView,
)

router = DefaultRouter()
router.register(r'health-assessments', HealthRiskAssessmentViewSet)

# Consolidated URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/export-responses/<int:company_id>/', export_responses_to_excel, name='export_responses_to_excel'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/forms/submit/', submit_form, name='submit_form'),
    path('api/v1/collective-report/', collective_report, name='collective_report'),
    path('api/v1/additional-analytics/', additional_analytics, name='additional_analytics'),
    path('api/v1/form/<str:url>/', get_company_form, name='get_company_form'),
    path('api/v1/export-responses/<int:company_id>/', export_responses_to_excel, name='export_responses_to_excel'),
    path('api/v1/company-analytics/<int:company_id>/', company_analytics, name='company_analytics'),
    path('api/v1/assessment/', include(router.urls)),
    path('api/v1/assessment/auth/login/', CustomAuthToken.as_view(), name='api_login'),
    path('api/v1/assessment/user-stats/', UserStatsView.as_view(), name='user-stats'),
    path('api/v1/assessment/user-logs/', UserLogsView.as_view(), name='user-logs'),
    path('api/v1/assessment/form-responses/', FormResponsesView.as_view(), name='form-responses'),
]
