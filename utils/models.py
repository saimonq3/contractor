def normalize_base_url(uri: str|None) -> str|None:
	if not str:
		return None
	if not uri.endswith('/'):
		return f'{uri}/'
	return uri