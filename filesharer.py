import os
from dotenv import load_dotenv
from filestack import Client


load_dotenv()

class FileSharer:
    """
    Uploads the file to the cloud and provides the link to the user to view the uploaded files.
    """

    def __init__(self, filepath, api_key=os.getenv('API_KEY')):
        self.api_key = api_key
        self.filepath = filepath

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
