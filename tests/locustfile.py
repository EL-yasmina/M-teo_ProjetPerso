from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)  # Temps d'attente entre les requêtes en secondes

    @task
    def test_recommandation(self):
        cities = ["Paris", "London", "New York"]
        for city in cities:
            self.client.get(f"/recommandation/{city}")

    @task
    def test_previsions(self):
        cities_and_days = [("Paris", 3), ("London", 5), ("New York", 7)]
        for city, days in cities_and_days:
            self.client.get(f"/previsions/{city}/{days}")

    @task
    def test_infos(self):
        cities = ["Paris", "London", "New York"]
        for city in cities:
            self.client.get(f"/infos/{city}")
