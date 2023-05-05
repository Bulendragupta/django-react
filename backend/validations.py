from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

UserModel = get_user_model()

def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('Please provide an email address.')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('Please provide a username.')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('Please provide a password.')
    return True

def custom_validation(data):
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    google_id = data.get('google_id', '').strip()
    errors = {}
    
    if not email:
        errors['email'] = 'Please provide an email address.'
    elif UserModel.objects.filter(email=email).exists():
        errors['email'] = 'This email address is already in use. Please choose another one.'
    
    if not password and not google_id:
        errors['password'] = 'Please provide a password.'
    elif not password and google_id:
        password = google_id
    
    if password and len(password) < 8:
        errors['password'] = 'Please choose a password that is at least 8 characters long.'
    
    if not username:
        errors['username'] = 'Please provide a username.'
    elif UserModel.objects.filter(username=username).exists():
        errors['username'] = 'This username is already taken. Please choose another one.'
    
    if errors:
        raise ValidationError(errors)
    
    data['password'] = make_password(password) 
    return data

