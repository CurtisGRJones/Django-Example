from factory import DjangoModelFactory, Faker

from .models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    first_name = Faker('company')
    last_name = Faker('text')
    website = Faker('url')

    class Meta:
        model = CustomUser