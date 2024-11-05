from django.apps import AppConfig

class AssessmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assessment'
    verbose_name = "Assessment Management"  # Human-readable name for the app

    def ready(self):
        # Code to run when the app is ready
        # For example, signal registrations can go here
        pass
