from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError as DjValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_validation_error,
    }

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context)
    return exception_handler(exc, context)


def _handle_validation_error(exc, context):
    response = exception_handler(exc, context)
    errors = as_serializer_error(exc)
    # if exception from django itself
    if isinstance(exc, DjValidationError):
        # Access the error messages for each field
        message_dict = exc.message_dict

        # Convert the message_dict to a format that DRF understands
        drf_error_dict = {field: error[0] for field, error in message_dict.items()}

        # Create a DRFValidationError with the updated error dictionary
        response = exception_handler(DRFValidationError(detail=drf_error_dict), context)

        # Update the errors variable with the DRFValidationError details
        errors = as_serializer_error(DRFValidationError(detail=drf_error_dict))

    if response is not None:
        response.data = {"status_code": response.status_code, "errors": []}
        make_pretty_error(response.data, errors)
    return response


def make_pretty_error(data, errors):
    for error in errors:
        if isinstance(errors[error], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, {er: errors[error][er]})
        elif isinstance(errors[error], list) and isinstance(errors[error][0], ErrorDetail) and len(errors[error]) == 1:
            data["errors"].append({"code": f"{error}_{errors[error][0].code}", "message": errors[error][0]})
        elif isinstance(errors[error][0], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, er)
        else:
            data["errors"].append({"code": f"{error}_{errors[error].code}", "message": errors[error]})
