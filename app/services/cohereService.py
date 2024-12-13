import cohere
from chromadb import Documents, EmbeddingFunction, Embeddings
from utils.config import COHERE_API_KEY

# crear cliente de chroma db y cohere
co = cohere.ClientV2(COHERE_API_KEY)

# definir la funcion de embedding de cohere
def get_embeddings(textos):
    response = co.embed(
        texts=textos,
        model="embed-multilingual-v3.0",
        input_type="search_document",
        embedding_types=["float"],
    )
    return response.embeddings.float_  # Cohere devuelve embeddings como una lista de listas


# Crea la clase personalizada de EmbeddingFunction para ChromaDB
class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Llama a la función de Cohere para obtener las embeddings
        return get_embeddings(input)  # input es una lista de textos
    

#  Interaccion con cohere para recibir respuestas a preguntas sobre las historias
# definicion de promts
system_prompt = """ sos un asistente que responde sobre historias de niños. Tu trabajo es responder al contexto que 
    te proporciono. Tienes que responder siempre en español. Si no sabes la respuesta di "No puedo responderte :("
    """

instructions = """ 
        1. Responde de manera amigable y con tono entusiasta, como si le hablaraas a un niño
        2. Responde en máximo 3 oraciones
        3. Agrega emojis a la respuesta
        4. Responde siempre en español
        5. Solo utiliza el contexto brindado
    """

# funcion para obtener la respuesta de cohere sobre una pregunta en base al contexto
def get_llm_answer(query, context):
    
    prompt = f"""
        instrucciones: {instructions}  

        Contexto: {context}

        pregunta: {query}
    """
    respuesta = co.chat(
    model="command-r-plus-08-2024",
    messages=[
        {"role": "system", "content":system_prompt},
        {"role": "user", "content": prompt}
    ],
        seed = 10
        
    )

    return respuesta.message.content[0].text
