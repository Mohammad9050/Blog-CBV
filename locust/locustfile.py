from locust import HttpUser, task, between


class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post("accounts/api/v1/jwt/create/", data={
            "email":"debra00@example.net",
            "password": "admin100"
        }).json()
        self.client.headers = {'Authorization': f"Bearer {response.get('access')}"}
    
    @task
    def post_list(self):
        self.client.get("api/v1/posts/")

    @task
    def category_list(self):
        self.client.get("api/v1/category/")