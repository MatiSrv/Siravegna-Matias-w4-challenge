from pydantic import BaseModel, Field

import random
import string


# Definicion de clases con pydantic
# Story campo id generado automaticamente, campo title y content requeridos
class Story(BaseModel):
    id: str 
    title: str = Field(..., min_length=3, max_length=100, description="Title of the story")
    content: str = Field(..., min_length=10, description="Content of the story")

    @classmethod
    def generate_id(cls, length=5):
        """Genera un ID alfanumérico de la longitud especificada."""
        characters = string.digits  #  dígitos
        return ''.join(random.choices(characters, k=length))

    @classmethod
    def create(cls, title: str, content: str):
        return cls(id=cls.generate_id(), title=title, content=content)
    
# Clase para poder enviar la request de creacion de una historia
class StoryRequest(BaseModel):
    title: str
    content: str