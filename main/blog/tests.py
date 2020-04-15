import json
from django.http   import HttpResponse , JsonResponse
from django.test   import TestCase , Client
from unittest.mock import patch , MagicMock
from django.http   import HttpResponse, JsonResponse


class SignUp(TestCase):
    def setUp(self):
        return
