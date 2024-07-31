from locust import HttpUser, TaskSet, task, between

class FileUploadTaskSet(TaskSet):
    @task
    def upload_file(self):
        # Simula a seleção e o upload de um arquivo
        with open('test_file.txt', 'rb') as file:
            files = {'file': ('test_file.txt', file, 'text/plain')}
            self.client.post("/upload", files=files)

class WebsiteUser(HttpUser):
    tasks = [FileUploadTaskSet]
    wait_time = between(1, 2)  # Tempo de espera entre as requisições
