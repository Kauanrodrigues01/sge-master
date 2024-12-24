from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import Outflow
from decouple import config
from django.contrib.auth import get_user_model

@receiver(post_save, sender=Outflow)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.quantity > 0:
            product = instance.product
            product.quantity -= instance.quantity
            product.save()


@receiver(post_migrate)
def create_user(sender, **kwargs):
    User = get_user_model()

    # Verifica se o usuário já existe no banco de dados. Se existir, não cria outro.
    if User.objects.exists():
        return

    # Se não existir, cria um novo usuário com as variáveis de ambiente
    username = config('USERNAME_TEST', cast=str)
    email = config('EMAIL', cast=str)
    password = config('PASSWORD', cast=str)
    
    # Criando o usuário com as informações do .env
    t = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print(f'Criado o usuário: {t}')