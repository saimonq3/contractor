import decimal

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.renderers import JSONRenderer as DrfJsonResponse
from rest_framework.response import Response


class JsonSuccessResponse(Response):
	"""
	Успешный ответ сервиса
	"""
	pass


class JsonErrorResponse(Response):
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


def response(result):
	"""
	Успешный ответ API.
	"""
	body = {'result': result}
	return Response(body, status=200)


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

	body = {
		'result': {'error': error}
	}
	return JsonErrorResponse(body, status=status)
