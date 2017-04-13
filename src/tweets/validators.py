from django.core.exceptions import ValidationError

def validate_content(value):
	content = value
	if content == "123":
		raise ValidationError("Content cannot be 123")
	return value