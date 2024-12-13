from langchain.text_splitter import RecursiveCharacterTextSplitter


# esta función se encarga de dividir el contenido en chunks de 1000 caracteres
# para su posterior embedding
def getChuncking(title,content):
    results = []
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1250,         
    chunk_overlap=50,     
    separators=["\n\n", ".",],  # Priorizo párrafos, luego frases y palabras
    length_function=len,    
    )
    chunks = text_splitter.split_text(title + content)

    return chunks