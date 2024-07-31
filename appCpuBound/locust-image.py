from locust import HttpUser, task, between
import random
import os

class ImageUploadUser(HttpUser):
    wait_time = between(1, 5)  # Tempo de espera entre as tarefas

    @task
    def upload_image(self):
        # Diretório onde suas imagens de teste estão localizadas
        image_dir = 'test_images'

        # Verifica se o diretório de imagens existe
        if not os.path.exists(image_dir):
            print(f"Diretório de imagens não encontrado: {image_dir}")
            return

        image_files = os.listdir(image_dir)
        
        if not image_files:
            print(f"Não há imagens no diretório: {image_dir}")
            return
        
        # Escolher uma imagem aleatória
        image_file = random.choice(image_files)
        image_path = os.path.join(image_dir, image_file)
        
        with open(image_path, 'rb') as f:
            # Enviar o POST request para o endpoint '/upload'
            response = self.client.post(
                '/upload',
                files={'file': (image_file, f, 'image/jpeg')}
            )

            # Verifique o status da resposta para garantir que o upload foi bem-sucedido
            if response.status_code == 200:
                print(f'Successfully uploaded {image_file}')
            else:
                print(f'Failed to upload {image_file}, Status code: {response.status_code}')
