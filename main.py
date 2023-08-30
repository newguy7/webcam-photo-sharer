from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

import time
import webbrowser

from filesharer import FileSharer

# import/load the kv file
Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes Button text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops camera and changes Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False        
        self.ids.button.text = 'Start Camera'
        # remove the last capture when camera is stopped
        self.ids.camera.texture = None

    def capture(self):
        """Creates a filename with the current time and captures & saves 
        a photo image under that filename"""
        # Create a filename with the current time in the filename; stringfromtime(strftime)
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f"App-4-Webcam-Photo-Sharer/files/{current_time}.png"
        # Capture frame from the camera
        self.ids.camera.export_to_png(self.filepath)
        #switch the current screen to another screen
        self.manager.current = 'image_screen'
        # show the captured image in the new screen(image screen)
        self.manager.current_screen.ids.img.source = self.filepath

class ImageScreen(Screen):

    error_message = "No any Link found, Create it first"

    def create_link(self):
        """Accesses the photo filepath, uploads it to the web,
        and inserts the link in the Label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = FileSharer(filepath=file_path)
        # adding self.url to url makes it available to other methods in the class
        self.url = filesharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """Copy the url from the Label widget to the clipboard available"""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.error_message

    def open_link(self):
        """Opens the url created in a default browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.error_message

class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()

MainApp().run()