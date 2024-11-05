# from django.contrib import admin
# from .models import Question, Company, Report

# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['question_text', 'question_type']

# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ['name', 'unique_url']

# class ReportAdmin(admin.ModelAdmin):
#     list_display = ['user', 'health_risk_score', 'report_type']

# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Company, CompanyAdmin)
# admin.site.register(Report, ReportAdmin)


from django.contrib import admin
from .models import Question, Company, Report

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type']
    search_fields = ['question_text']
    list_filter = ['question_type']
    ordering = ['question_text']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'unique_url']
    search_fields = ['name']
    ordering = ['name']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'health_risk_score', 'report_type']
    search_fields = ['user__username', 'report_type']  # Assuming user is a ForeignKey to a User model
    list_filter = ['report_type']
    ordering = ['-health_risk_score']  # Order by descending health risk score

admin.site.register(Question, QuestionAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Report, ReportAdmin)
