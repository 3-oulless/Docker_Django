from rest_framework.test import (
    APIClient,
)
from django.urls import (
    reverse,
)
from datetime import (
    datetime,
)
import pytest
from Account_Module.models import (
    User,
)


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        phone=9182021314,
        email="test@test.com",
        password="admin",
    )
    return user


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestPostApi:
    def test_get_post_response_200_status(
        self,
        api_client,
        common_user,
    ):
        # api_client.force_authenticate(user=common_user)
        url = reverse("post:api_v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_201_status(
        self,
        common_user,
        api_client,
    ):
        url = reverse("post:api_v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(
            url,
            data,
        )
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_status(
        self,
        common_user,
        api_client,
    ):
        url = reverse("post:api_v1:post-list")
        data = {
            "title": "test",
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(
            url,
            data,
        )
        assert response.status_code == 400
