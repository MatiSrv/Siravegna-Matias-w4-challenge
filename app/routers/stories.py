from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from models.story import Story, StoryRequest
from services.chromasService import upload_story_to_chroma, query_chroma_db, get_answer



router = APIRouter(prefix="/stories", tags=["stories"])

# diccionario de historias
stories: List[Dict[str, Any]] = []  

# carga un nuevo documento en el sistema
@router.post("/upload") 
async def upload_story(story: StoryRequest):
    # Valido si ya existe una historia con el mismo título
    existing_story = next((s for s in stories if s["title"] == story.title), None)
    if existing_story:
        raise HTTPException(
            status_code=400,
            detail=f"A story with the title '{story.title}' already exists."
        )
    
    # Crear una nueva historia y agregarla a la lista de historias
    new_story = Story.create(story.title, story.content)
    stories.append(new_story.model_dump())
    return {"message": "Document uploaded succesfully", "document_id": new_story.id} 

# genera los embeddings de los documentos
@router.post("/generate_embeddings") 
async def generate_embeddings(id:str):
    # Buscar la historia por ID
    story = next((story for story in stories if story["id"] == id), None)
    
    # Validar si existe la historia
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    return upload_story_to_chroma(story["id"],story["title"],story["content"])


# busca documentos similares
# Busqueda Semantica 
@router.post("/search") 
async def search(query:str):
    try:
        return query_chroma_db(query)
    except Exception as e: # manejo de errores
        raise HTTPException(status_code=500, detail=f"Error while generating answer: {str(e)}")


# genera una respuesta a una pregunta utilizando documentos relevantes
# Respuesta en base a los documentos
@router.post("/ask") 
async def ask(query:str):
    try:
        return get_answer(query)
    except Exception as e: # manejo de errores
        raise HTTPException(status_code=500, detail=f"Error while generating answer: {str(e)}")