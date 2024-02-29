from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from .estados_modelo import GENEROS

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        
        if not email:
            raise ValueError("La Dirección de Correo Electronico es Requerido")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        
        if kwargs.get('is_active') is not True:
            raise ValueError("El super usuario debe estar activo")
        
        if kwargs.get('is_staff') is not True:
            raise ValueError("El super usuario debe ser staff")
        
        if kwargs.get('is_superuser') is not True:
            raise ValueError("No es super usuario")
        
        return self.create_user(email, password, **kwargs)
    
def get_dir_image(instance, filename):
    return 'users/{0}/{1}'.format(instance.pk, filename)

class User(AbstractBaseUser, PermissionsMixin):
    email               = models.EmailField(max_length=250, unique=True)
    first_name          = models.CharField(max_length=250)
    last_name           = models.CharField(max_length=250)
    is_active           = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    image               = models.ImageField(upload_to=get_dir_image, blank=True, null=True)
    rut                 = models.CharField(max_length=50, unique=True, blank=True, null=True)
    celular             = models.CharField(max_length=17, blank=True, null=True)
    genero              = models.CharField(max_length=2, choices=GENEROS, blank=True, null=True)
    fecha_nacimiento    = models.DateField(null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email