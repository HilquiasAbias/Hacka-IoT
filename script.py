import time
import requests
from io import BytesIO
from tkinter import Tk, Label
from PIL import Image, ImageTk

class DigitalPhotoFrame:
    def __init__(self, image_urls):
        self.image_urls = image_urls
        self.current_image_index = 0
        if not self.image_urls:
            raise ValueError("Nenhuma URL de imagem fornecida.")
        
        # Configuração da janela
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Fecha o app ao pressionar ESC
        
        # Label para exibir as imagens
        self.label = Label(self.root, bg="black")
        self.label.pack(expand=True, fill="both")

        self.show_image()

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

    def run(self):
        """Inicia o loop principal do aplicativo."""
        self.root.mainloop()

if __name__ == "__main__":
    # Substitua pelos URLs das imagens que deseja exibir
    image_urls = [
        "https://images.pexels.com/photos/4790267/pexels-photo-4790267.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "https://images.pexels.com/photos/15470542/pexels-photo-15470542/free-photo-of-tecnologia-equipamento-maquinario-aparelhos.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "https://images.pexels.com/photos/10635975/pexels-photo-10635975.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "https://images.pexels.com/photos/22610381/pexels-photo-22610381/free-photo-of-smartphone-internet-conexao-ligacao.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    ]
    try:
        app = DigitalPhotoFrame(image_urls)
        app.run()
    except ValueError as e:
        print(e)
