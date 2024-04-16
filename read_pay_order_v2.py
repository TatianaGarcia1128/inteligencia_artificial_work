import fitz  
import spacy
from spacy import displacy
import re

def read_pdf():

    with fitz.open("orden_operacion.pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
            
    text = text.replace('�','')
    texto_limpio_saltos = re.sub(r'\n', ' ', text)
    texto_limpio_saltos = texto_limpio_saltos.replace('$', '')
    texto_limpio_saltos = texto_limpio_saltos.replace('.', '')
    return texto_limpio_saltos

def model(text):
    # Cargar el modelo de lenguaje en español de spaCy
    nlp = spacy.load('es_core_news_sm')


    # Procesar el texto con spaCy
    doc = nlp(text)

    for token in doc:

        if (token.lemma_.lower() == 'fideicomiso' ):
            for child in token.children:
                if (child.dep_ == 'nummod'):
                    cuenta_bancaria = child.text
                   
                if (child.dep_ == 'flat' and child.text != 'DEBITAR'):
                    if (child.text == 'Ahorros' or child.text == 'Corriente'):
                        tipo_cuenta = child.text
                    else:
                        nombre = child.text
                    
                    for ch in child.children:
                        banco = ch.text
        
        if (token.lemma_.lower() == 'penalidad' ):
            for child2 in token.children:
                if (child2.dep_ == 'obj' and child2.pos_ =='ADJ'):
                    nit = child2.text

                    for ch2 in child2.children:
                        tipo_identificacion = ch2.text
                        break


        if (token.lemma_.lower() == 'bruto' ):
            for child3 in token.children:
                if (child3.dep_ == 'obl' and child3.pos_ == 'NUM' and child3.text.find(',')>0):
                    valor = child3.text

    print('tipo de ceunta', tipo_cuenta)
    print('Banco', banco)
    print('Número cuenta', cuenta_bancaria)                  
    print('NIT', nit)  
    print('Tipo de identificación', tipo_identificacion)      
    print('Nombre del fideicomiso', nombre)   
    print('Valor', valor)     

def visualization(text):
    nlp = spacy.load('es_core_news_sm')

    # Procesar el texto con spaCy
    doc = nlp(text)

    # displacy.serve(doc, style='ent', port=4200)
    displacy.serve(doc, style='dep', port=4200, options={"distance":170})




lines = read_pdf() 
model(lines)
# visualization(lines)
# search_cuenta(lines)