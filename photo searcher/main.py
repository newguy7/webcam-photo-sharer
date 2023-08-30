from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

import wikipedia
import requests

# import/load the kv file
Builder.load_file('frontend.kv')

class FirstScreen(Screen):
    # perform this when the button is pressed. Linked in kv file
    def get_image_link(self):
        # get user input/query from the TextInput widget
        query = self.manager.current_screen.ids.user_query.text
        
        # to open the image file from the project folder in the first screen
        # self.manager.current_screen.ids.img.source = 'files/sunny.jpg'

        # Get wikipedia page and first image url
        page = wikipedia.page(query)
        # Grab the first image link from the list of image links
        image_link = page.images[0]
        return image_link
    
    def download_image(self):        
        # Download the image
        headers = {
            "User-Agent": "Photo Searcher" 
        }
        req = requests.get(self.get_image_link(), headers=headers)
        # Create an empty image file, open it as writable and download the image
        imagepath = 'App-4-Webcam-Photo-Sharer/photo searcher/files/image.jpg'
        with open(imagepath, 'wb') as file:
            file.write(req.content)
            return imagepath

    def set_image(self):  
        # Set the image in the Image Widget
        self.manager.current_screen.ids.img.source = self.download_image()


class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

MainApp().run()