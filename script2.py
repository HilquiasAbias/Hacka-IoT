import time
import requests
from io import BytesIO
from tkinter import Tk, Label
from PIL import Image, ImageTk

class DigitalPhotoFrame:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.image_urls = []
        self.current_image_index = 0
        
        # Configuração da janela
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Fecha o app ao pressionar ESC
        
        # Label para exibir as imagens
        self.label = Label(self.root, bg="black")
        self.label.pack(expand=True, fill="both")

        # Inicia o ciclo de atualização das imagens
        self.update_images()
        
    def fetch_images_from_endpoint(self):
        """Faz uma requisição ao endpoint e atualiza a lista de URLs de imagens."""
        try:
            response = requests.get(self.endpoint)
            response.raise_for_status()
            data = response.json()
            # Extrai as URLs das imagens do campo "moments"
            self.image_urls = [moment['image'] for moment in data.get('moments', [])]
            if not self.image_urls:
                print("Nenhuma imagem encontrada.")
                return False
            return True
        except Exception as e:
            print(f"Erro ao carregar as imagens do endpoint: {e}")
            return False

    def fetch_image_from_url(self, url):
        """Faz o download da imagem a partir de uma URL e retorna uma imagem PIL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
            return None

    def show_image(self):
        """Exibe a imagem atual no label."""
        if not self.image_urls:
            return  # Não há imagens para mostrar

        image_url = self.image_urls[self.current_image_index]
        img = self.fetch_image_from_url(image_url)

        if img:
            # Ajusta a imagem para o tamanho da tela
            img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.label.config(image=photo)
            self.label.image = photo

        # Passa para a próxima imagem após 8 segundos
        self.current_image_index = (self.current_image_index + 1) % len(self.image_urls)
        self.root.after(8000, self.show_image)

    def update_images(self):
        """Atualiza a lista de imagens a cada 2 segundos."""
        if self.fetch_images_from_endpoint():
            # Se novas imagens foram carregadas, reinicia o índice da imagem atual
            self.current_image_index = 0
            if self.image_urls:  # Se houver imagens, inicia a exibição
                self.show_image()
        
        # Repetir a atualização após 2 segundos
        self.root.after(2000, self.update_images)

    def run(self):
        """Inicia o loop principal do aplicativo."""
        self.root.mainloop()

if __name__ == "__main__":
    # Substitua pelo URL do seu endpoint que retorna os momentos com imagens
    endpoint = "https://seu-endpoint.com/api/moments"
    app = DigitalPhotoFrame(endpoint)
    app.run()
