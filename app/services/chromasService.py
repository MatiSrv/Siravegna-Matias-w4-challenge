from chromadb import chromadb
from services.cohereService import MyEmbeddingFunction, get_llm_answer
from utils.chunking import getChuncking

import json

# Crea una instancia del cliente de ChromaDB
client = chromadb.Client()

# Crea una colección usando la función de embeddings personalizada
collection = client.create_collection(name="Stories",
                                      embedding_function=MyEmbeddingFunction(),
                                       metadata={"hnsw:space": "ip"}
                                     )

# funcion para subir un documento a la bd
def upload_story_to_chroma(document_id:str,title: str, content: str):
    # chunkear el texto
    chunks = getChuncking(title,content)

    # preparalo para enviar a chroma db
    documents = []
    metadatas = []
    ids = []
    i = 0
    for i, chunk in enumerate(chunks):
        documents.append(chunk)  
        ids.append(f"ID{i}")   
        metadatas.append({"title": title,"document_id": document_id})

    collection.upsert(
        documents= documents,
        metadatas= metadatas,
        ids= ids
    )
    return {"message": f"Embedding generated succesfully for document {document_id}"}


# Funcion para hacer querys a la bd y resultados por busqueda de similaridad y semantica
# respuesta: Documento mas similar junto con su id y titulo      
def query_chroma_db(query:str):
    query_results = collection.query(
        query_texts= [query],
        n_results=1
    )
    metadatas = query_results["metadatas"]
    document_id = metadatas[0][0]["document_id"]
    title = metadatas[0][0]["title"]
    context = query_results["documents"][0][0] 
    similarity_score = query_results["distances"][0][0]
    llm_answer =  get_llm_answer(query, context)

    results = []
    results.append({"document_id": document_id, "title": title, "content_snippet": llm_answer, "similarity_score": similarity_score})

    return results

def get_answer(query:str):
    result = query_chroma_db(query)
    llm_answer = result[0]["content_snippet"]  # Obtén el contenido del LLM
    return llm_answer




