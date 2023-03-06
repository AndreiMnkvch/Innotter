from rest_framework.test import APITestCase, APIRequestFactory
from core.views import PageViewSet
from users.models import User
from rest_framework.test import force_authenticate
from core.models import Page, Tag, Post
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIClient as Client
from users.services.token_services import generate_access_token


class TestPageViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser",
            password="testuser",
            email="testuser@gmail.com"
        )
        self.page = Page.objects.create(
            name="test_name",
            description="test description",
            owner=self.user,
        )
        self.user1 = User.objects.create(
            username="testuser1",
            password="testuser1",
            email="testuser1@gmail.com"
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
        self.user_token = generate_access_token(self.user)
        self.user1_token = generate_access_token(self.user1)
        self.tag = Tag.objects.create(name="testtag")

    def test_create_page_anonymous(self):
        """ assures that only authenticatesd users can create a page"""
        c = Client()
        response = c.post(f"/api/v1/pages/")
        self.assertEqual(response.status_code, 403)

    def test_pages_list_ananymous(self):
        """ assures that anonymous user can't see pages list """

        c = Client()
        response = c.get(f"/api/v1/pages/")
        self.assertEqual(response.status_code, 403)

    def test_page_list_user(self):
        """ assures that authenticated user can see pages list """

        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = c.get("/api/v1/pages/")
        self.assertEqual(response.status_code, 200)

    def test_pages_detail_ananymous(self):
        """assures if anonymous user can't see page"""

        c = Client()
        response = c.get(f"/api/v1/pages/{self.page.uuid}/")
        self.assertEqual(response.status_code, 403)

    def test_page_detail_user(self):
        """ assures if authenticated user can see self page """

        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = c.get(f"/api/v1/pages/{self.page.uuid}/")
        self.assertEqual(response.status_code, 200)

    def test_add_page_tag(self):
        """positive testcase"""

        view = PageViewSet.as_view({"patch": "add_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG"
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/add_page_tag/", data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.page.tags.last()), "TESTTAG".lower())

    def test_add_page_tag_multiple(self):
        """Checks if multiple tags has been added to page by owner"""

        view = PageViewSet.as_view({"patch": "add_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG"
                },
                {
                    "name": "ANOTHERTAG"
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/add_page_tag/", data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.page.tags.last()), "ANOTHERTAG".lower())
        self.assertEqual(len(self.page.tags.all()), 2)

    def test_add_page_tag_strip_lower(self):
        """Checks if tags has been stripped and lowered"""

        view = PageViewSet.as_view({"patch": "add_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG   "
                },
                {
                    "name": "   ANOTHERTAG  "
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/add_page_tag/", data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.page.tags.last()), "anothertag")
        self.assertEqual(str(self.page.tags.get(name="testtag")), "testtag")

    def test_add_page_2_same_tags(self):
        """ Checks if added only one of the 2 same tags """

        view = PageViewSet.as_view({"patch": "add_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG   "
                },
                {
                    "name": "TESTTAG   "
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/add_page_tag/", data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page.tags.all().count(), 1)

    def test_add_page_tag_moderator(self):
        """check if moderator cannot add tag to page"""

        view = PageViewSet.as_view({"patch": "add_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG"
                }
            ]
        }
        request = self.factory.patch(
            "/api/v1/pages/add_page_tag/", data=data, format='json')
        request.user = self.moderator
        force_authenticate(request, user=self.moderator)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 403)

    def test_add_page_tag_admin(self):
        """check if admin cannot add tag to page"""

        view = PageViewSet.as_view({"patch": "add_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG"
                }
            ]
        }
        request = self.factory.patch("/api/v1/pages/add_page_tag/", data=data)
        request.user = self.admin
        force_authenticate(request, user=self.admin)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 403)

    def test_remove_page_tag(self):
        """positive testcase"""

        self.page.tags.set((self.tag,))
        view = PageViewSet.as_view({"patch": "remove_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG"
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/remove_page_tag/", data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.page.tags.all()), 0)

    def test_remove_page_tag_empty(self):
        """returns 200 even if no tags to delete provided"""

        view = PageViewSet.as_view({"patch": "remove_page_tag"})
        data = {
            "tags": []
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/remove_page_tag/", data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.page.tags.all()), 0)

    def test_remove_page_tag_not_owner(self):
        """tests that other user cannot delete tags"""

        self.page.tags.set((self.tag,))
        view = PageViewSet.as_view({"patch": "remove_page_tag"})
        data = {
            "tags": [
                {
                    "name": "TESTTAG"
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/remove_page_tag/", data=data, format='json')
        request.user = self.user1
        force_authenticate(request, user=self.user1)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(self.page.tags.all()), 1)

    def test_remove_page_tag_not_exist(self):
        """tests if requested tag doesn't exist - request should be skipped"""

        self.page.tags.set((self.tag,))
        view = PageViewSet.as_view({"patch": "remove_page_tag"})
        data = {
            "tags": [
                {
                    "name": "ANOTHERTAG"
                }
            ]
        }
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/remove_page_tag/", data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.page.tags.all()), 1)

    def test_subscribe(self):
        """positive testcase DOESNT WORK DONT KNOW WHY!!!"""

        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = c.patch(f"/api/v1/pages/{self.page.uuid}/subscribe/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page.followers.count(), 1)

    def test_subscribe_self_page(self):
        """positive testcase"""

        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = client.patch(f"/api/v1/pages/{self.page.uuid}/subscribe/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.page.followers.all()), 1)

    def test_subscribe_anonymous(self):
        """tests if anonymous user can't subscribe"""

        view = PageViewSet.as_view({"patch": "subscribe"})
        request = self.factory.patch(
            f"/api/v1/pages/{self.page.uuid}/subscribe/", format='json')

        request.user = AnonymousUser()
        force_authenticate(request, user=AnonymousUser())
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(self.page.followers.all()), 0)

    def test_subscribe_follower_yet(self):
        """ tests if page's follower won't be subscribed twice """

        self.page.followers.set((self.user1,))
        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = client.patch(f"/api/v1/pages/{self.page.uuid}/subscribe/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page.followers.count(), 1)

    def test_follow_requests(self):
        """ positive testcase e.g owner can see follow requests to his page """

        self.page.follow_requests.set((self.user1,))
        view = PageViewSet.as_view({"get": "follow_requests"})
        request = self.factory.get(
            f"/api/v1/pages/{self.page.uuid}/follow_requests/", format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.page.follow_requests.all()), 1)

    def test_follow_requests_anonymous_user(self):
        """anonymous user can't see follow requests to other page"""

        self.page.follow_requests.set((self.user1,))
        view = PageViewSet.as_view({"get": "follow_requests"})
        request = self.factory.get(
            f"/api/v1/pages/{self.page.uuid}/follow_requests/", format='json')
        request.user = AnonymousUser()
        force_authenticate(request, user=AnonymousUser())
        response = view(request, pk=self.page.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(self.page.follow_requests.all()), 1)

    def test_follow_requests_another_user(self):
        """ user can't see follow requests to other page """

        self.page.follow_requests.set((self.user1,))
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = c.get(f"/api/v1/pages/{self.page.uuid}/follow_requests/",

                         )
        self.assertEqual(response.status_code, 403)

    def test_approve_follow_requests(self):
        """positive testcase"""

        self.page.is_private = True
        self.page.follow_requests.set((self.user1,))
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = c.patch(
            f"/api/v1/pages/{self.page.uuid}/approve_follow_requests/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page.followers.count(), 1)

    def test_approve_follow_requests_by_another_user(self):
        """negative testcase"""

        self.page.is_private = True
        self.page.follow_requests.set((self.user1,))
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = c.patch(
            f"/api/v1/pages/{self.page.uuid}/approve_follow_requests/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.page.follow_requests.count(), 1)

    def test_approve_follow_requests_by_anonymous_user(self):
        """negative testcase"""

        self.page.is_private = True
        self.page.follow_requests.set((self.user1,))
        c = Client()
        response = c.patch(
            f"/api/v1/pages/{self.page.uuid}/approve_follow_requests/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.page.follow_requests.count(), 1)

    def test_decline_follow_requests(self):
        """positive testcase"""

        self.page.is_private = True
        self.page.follow_requests.set((self.user1,))
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = c.patch(
            f"/api/v1/pages/{self.page.uuid}/decline_follow_requests/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page.followers.count(), 0)
        self.assertEqual(self.page.follow_requests.count(), 0)

    def test_decline_follow_requests_by_another_user(self):
        """negative testcase"""

        self.page.is_private = True
        self.page.follow_requests.set((self.user1,))
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = c.patch(
            f"/api/v1/pages/{self.page.uuid}/decline_follow_requests/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.page.follow_requests.count(), 1)

    def test_decline_follow_requests_by_anonymous_user(self):
        """negative testcase"""

        self.page.is_private = True
        self.page.follow_requests.set((self.user1,))
        c = Client()
        response = c.patch(
            f"/api/v1/pages/{self.page.uuid}/approve_follow_requests/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.page.follow_requests.count(), 1)

    def test_update_page_name_by_owner(self):

        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "name": "new user page name"
        }
        response = c.patch(f"/api/v1/pages/{self.page.uuid}/", data=data,)
        self.assertEqual(response.status_code, 200)

    def test_update_page_name_by_another_user(self):
        """ assures that another user cannot update name of user page"""

        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        data = {
            "name": "new user page name"
        }
        response = c.patch(f"/api/v1/pages/{self.page.uuid}/", data=data,)
        self.assertEqual(response.status_code, 403)

    def test_delete_page_by_owner(self):
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = c.delete(f"/api/v1/pages/{self.page.uuid}/")
        self.assertEqual(response.status_code, 204)

    def test_delete_page_by_another_user(self):
        c = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = c.delete(f"/api/v1/pages/{self.page.uuid}/")
        self.assertEqual(response.status_code, 403)


class TestPostViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            password="testuser",
            email="testuser@gmail.com"
        )
        self.user1 = User.objects.create(
            username="testuser1",
            password="testuser1",
            email="testuser1@gmail.com"
        )
        self.user_page = Page.objects.create(
            name="test_name",
            description="test description",
            owner=self.user,
        )
        self.user_post = Post.objects.create(
            page=self.user_page,
            content="test content"
        )

        self.user_token = generate_access_token(self.user)
        self.user1_token = generate_access_token(self.user1)

    def test_create_post_ananymous(self):
        """ assures that anonymous user cannot create a post"""

        client = Client()
        response = client.post(f"/api/v1/posts/")
        self.assertEqual(response.status_code, 403)

    def test_create_post_wo_reply_to(self):
        """ positive testcase (user can create post without 'reply_to' field) """

        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        data = {
            "content": "test post",
            "page": self.user_page.uuid,
        }
        response = client.post(f"/api/v1/posts/", data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_post_with_reply_to(self):
        """ positive testcase (user can create post with 'reply_to' field) """

        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")

        data = {

            "content": "test post",
            "page": self.user_page.uuid,
            "reply_to": self.user_post.id
        }
        response = client.post(f"/api/v1/posts/", data=data)
        self.assertEqual(response.status_code, 201)

    def test_posts_list_user_no_pages(self):
        """ assures that no posts recieved for user without self posts and followed pages from feed"""

        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = client.get(f"/api/v1/posts/")
        self.assertEqual(response.content, b'[]')

    def test_posts_list_self_posts(self):
        """ assures that user with self posts and no followed pages gets just self posts from feed"""

        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = client.get(f"/api/v1/posts/")
        self.assertEqual(len(response.json()), 1)

    def test_posts_list_self_posts_and_followed_pages(self):
        """ assures that user with self post and one post from followed pages gets both posts from feed"""

        user1_page = Page.objects.create(
            name="test_name",
            description="test description",
            owner=self.user1,
        )
        user1_post = Post.objects.create(
            page=user1_page,
            content="test content"
        )
        user1_page.followers.set((self.user,))
        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = client.get(f"/api/v1/posts/")
        self.assertEqual(len(response.json()), 2)

    def test_like(self):
        """ positive testcase user likes another's user post """

        user1_page = Page.objects.create(
            name="test_name",
            description="test description",
            owner=self.user,
        )
        user1_post = Post.objects.create(
            page=user1_page,
            content="test content"
        )
        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = client.patch(f"/api/v1/posts/{user1_post.id}/like/")
        self.assertEqual(response.status_code, 200)


class TestTagViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            password="testuser",
            email="testuser@gmail.com"
        )
        self.user_token = generate_access_token(self.user)

    def test_create_tag(self):
        """ postive testcase """

        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "name": "test tag"
        }
        response = client.post(f"/api/v1/tags/", data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_existing_tag(self):
        """ assures that tag with the same name wouldn't be created twice """

        Tag.objects.create(
            name="testtag"
        )
        client = Client(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "name": "testtag"
        }
        response = client.post(f"/api/v1/tags/", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Tag.objects.all().count(), 1)
