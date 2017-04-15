from django.contrib import messages


def display_validation_errors(request, form):
    for error_key in form._errors:
        for error in form._errors[error_key]:
            messages.error(request, error)
