from rest_framework.test import APIClient
from users.models import User
from django.test import TestCase
from users.services.token_services import generate_access_token
from core.models import Page

class TestUserViewSet(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="user",
            password="user",
            email="user@gmail.com"
        )
        self.moderator = User.objects.create(
            username="moderator",
            password="moderator",
            email="moderator@gmail.com",
            role=User.Roles.MODERATOR
        )
        self.admin = User.objects.create(
            username="admin",
            password="admin",
            email="admin@gmail.com",
            role=User.Roles.ADMIN
        )
        self.page1 = Page.objects.create(
            name="test_name",
            description="test description",
            owner=self.user,
        )
        self.page2 = Page.objects.create(
            name="test_name",
            description="test description",
            owner=self.user,
        )
        self.user_token = generate_access_token(self.user)
        self.admin_token = generate_access_token(self.admin)
        self.moderator_token = generate_access_token(self.moderator)


    def test_create_user_anonymous(self):

        """ positive testcase anonymous user creates user  """

        client = APIClient()
        data = {
            "password": "testpassword",
            "username": "testuser",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "email": "testuser@gmail.com",
        }
        response = client.post("/api/v1/users/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username="testuser").count(), 1)


    def test_create_user_authenticated(self):

        """ positive testcase authenticated user creates another user """

        client = APIClient(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "password": "testpassword",
            "username": "testuser",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "email": "testuser@gmail.com",
        }
        response = client.post("/api/v1/users/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username="testuser").count(), 1)

    def test_create_user_authenticated_with_readonly_field(self):

        """ negative testcase authenticated user creates another user with read only field
            assures that readonly field value is ignored and set default value
        """

        client = APIClient(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "password": "testpassword",
            "username": "testuser",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "email": "testuser@gmail.com",
            "is_superuser": True
        }
        response = client.post("/api/v1/users/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.get(username="testuser").is_superuser, False)

    def test_admin_block_user(self):

        """ assures that admin can block user """


        client = APIClient(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "is_blocked": True
        }
        response = client.patch(f"/api/v1/users/{self.user.id}/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_blocked"], True)
