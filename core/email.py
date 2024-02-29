from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = 'email-djoser/activation.html'
    
class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email-djoser/password_reset.html'