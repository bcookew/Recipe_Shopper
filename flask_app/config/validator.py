import re
from flask import session, redirect, flash

####################  Email Validations  ####################

class Email:
    valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    
    @classmethod
    def inspect(cls, email):
        return cls.valid_email.match(email)

####################  Password Validations  ####################

class Password:
    valid_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%^&*<>])[A-Za-z\d!#$%^&*<>]{8,}$')
    
    @classmethod
    def inspect(cls, password, confirm_password):
        if not cls.valid_password.match(password):
            flash("Password must be at least 8 characters long and contain at least 1 number and special character")
            return False
        if password != confirm_password:
            flash("Passwords must match")
            return False
        return True

class Text_Field:
    def __init__(self, min_length, max_length=255) -> None:
        self.valid_text_field = re.compile(r'^[\s\dA-Za-z]{' + str(min_length) + ',' + str(max_length) + '}')

    def inspect(self, text_input):
        return self.valid_text_field.match(text_input)

class Logged_in:
    def checker():
        if 'user_id' not in session:
            flash("Access Denied!\nYou must log in!")
            return False
        return True

class Money:
    def __init__(self, min) -> None:
        self.min = min
        self.valid_amount = re.compile(r'^\S[0-9]{0,10}([\.,][0-9]{2,2})?$')
    
    def inspect(self, amount):
        if self.valid_amount.match(amount):
            if float(amount) > self.min:
                return True
        return False