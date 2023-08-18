from django.test import TestCase

from django.test import TestCase

from .serializers import CustomUserSerializer
from .factories import CompanyFactory


class CustomUserSerializer(TestCase):
    def test_model_fields(self):
        company = CompanyFactory()
        for field_name in [
            'id', 'name', 'description', 'website', 'street_line_1', 'street_line_2',
            'city', 'state', 'zipcode'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(company, field_name)
            )
