from typing import List, Tuple
from pydantic import BaseModel

class NamedEntity(BaseModel):
    name : str
    tag : str

class Annotation(BaseModel):
    span : Tuple[int, int]
    tag : str

def get_spans(document: str, text: str):
    start = document.find(text)

    while start != -1: 
        yield start
        start = document.find(text, start + 1)

def create_annotations(text: str, entity_list: List[NamedEntity]) -> List[Annotation]:
    entity = NamedEntity(**entity_list[0]) 
    
    spans = [(start, start + len(entity.name)) for start in get_spans(text, entity.name)]

    annotated_text = []
    prev_span = (0,0)
    for span in spans:
        annotated_text.append(text[prev_span[1]:span[0]])
        entity_tuple = (entity.name, entity.tag)
        print(type(entity_tuple))
        annotated_text.append(entity_tuple)
        prev_span = span

    annotated_text.append(text[prev_span[1]:])

    return annotated_text 

"""
    Eltero cimkeju, azonban azonos szoalaku entitasokat egyelore nem tud megkulonboztetni!
    TODO: ezt mihamarabb javitani! Pelda hibara: Csontvary es Csontvary-100 konf.
    BIO format?
"""

