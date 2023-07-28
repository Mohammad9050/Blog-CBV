import pytest 
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User, Profile

@pytest.fixture
def client_api():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email = "user@user.com", password="admin100")
    return user


@pytest.mark.django_db
class TestApi:

    def test_api_post_get_list_response(self, client_api):
        url = reverse("blog:posts")
        response = client_api.get(url)
        assert response.status_code == 200

    # def test_api_post_get_detail_response(self, client_api, common_user):4
    #     client_api.force_login(user = common_user)
    #     response = client_api.get(url)
    #     assert response.status_code == 200

    def test_api_post_create_response(self, client_api, common_user):
        url = reverse("blog:api:post-list")
       # url = 'http://127.0.0.1:8000/api/v1/posts/'
        client_api.force_login(user = common_user)

        # data = {
        #     'user' :common_user,
        #     'first_name': 'test',
        #     'last_name': 'testy',
        #     'description': 'hiii'

        # }
        # profile = Profile.objects.create(
        #     user= common_user,
        #     first_name= 'test',
        #     last_name = 'testy',
        #     description = 'hiiii'

        # )
        data ={
            "title": "string",
            "content": "string",
            "status": True

}
        response = client_api.post(url, data=data)

        
        assert response.status_code == 201

    


# class TestPostApi:
#     def test_get_post_response_200(self):
#         assert 1 == 1