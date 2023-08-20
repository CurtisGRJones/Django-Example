from factory import DjangoModelFactory, Faker

from .models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    first_name = Faker('john')
    last_name = Faker('doe')
    website = Faker('email@email.com')

    class Meta:
        model = CustomUser