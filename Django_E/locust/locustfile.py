from locust import HttpUser, task


class QuickstartUser(HttpUser):
    def on_start(self):
        responses = self.client.post(
            "account/api/v1/jwt/create/",
            json={"phone": "9182021310", "password": "Admin@5847"},
        ).json()
        self.client.headers = {
            "Authorization": f"Bearer {responses.get('access', None)}"
        }

    @task
    def post_list(self):
        self.client.get("api/v1/post/")

    @task
    def post_category(self):
        self.client.get("api/v1/category/")
