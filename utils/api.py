import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer as DrfJsonResponse


class JsonSuccessResponse(JsonResponse):
    """
    Успешный ответ сервиса
    """
    pass


class JsonErrorResponse(JsonResponse):
    """
    Неуспешный ответ сервиса
    """
    pass


class ApiJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


class JsonRenderer(DrfJsonResponse):
    def render(self, data, *args, **kwargs):
        data = {'result': data}
        return super().render(data, *args, **kwargs)


def response(result, encoder=ApiJSONEncoder):
    """
    Успешный ответ API.
    """
    body = {'result': result}
    return JsonSuccessResponse(body, encoder=encoder, status=200)


def error_response(tag=None, message=None, user_message=None, data=None, *, code='', status=200):
    """
    Ошибочный ответ API.
    """
    error = {}
    if tag is not None:
        error['error'] = tag
    if code is not None:
        error['code'] = code
    if message is not None:
        error['message'] = message
    if user_message is not None:
        error['user_message'] = user_message
    if data is not None:
        error['data'] = data

    body = {'error': error}
    return JsonErrorResponse(body, encoder=ApiJSONEncoder, status=status)