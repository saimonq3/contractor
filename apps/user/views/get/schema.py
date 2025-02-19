from drf_yasg import openapi

UserListSchema = {
	'operation_summary': 'Поиск пользователя по username или email',
	'operation_description': 'Поиск пользователя по username или email',
	'manual_parameters': [
		openapi.Parameter(
			'query',
			in_=openapi.IN_QUERY,
			type=openapi.TYPE_STRING,
			description='username or email',
			required=False,
		),
	]
}
