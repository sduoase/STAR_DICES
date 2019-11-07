import random
import os

class Die:
    def __init__(self, faces, theme):
        if not faces:
            raise ValueError("You must at least specify a face.")
        self.faces = faces
        self.urls = ["static/" + theme + "/" + face + ".PNG" for face in faces]

    def throw(self):
        face = random.randint(0, len(self.faces) - 1)
        return (self.faces[face], self.urls[face])

    def serialize(self):
        return self.faces

    def __str__(self):
        return str(self.faces)
