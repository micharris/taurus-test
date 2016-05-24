from locust import HttpLocust, TaskSet, task

class MyTaskSet(TaskSet):

    @task(1)
    def task1(self):
        self.client.get("/story/life/music/2016/05/16/police-chicago-suburb-looking-missing-sinead-oconnor/84440592/")

    @task(1)
    def task2(self):
        self.client.get("/news/")

   
class MyLocust(HttpLocust):
    task_set = MyTaskSet
