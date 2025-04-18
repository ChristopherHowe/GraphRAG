from nltk.tokenize import sent_tokenize
import nltk
from typing import List
from models import triplet


def extract_triplets(text) -> List[triplet]:
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append(triplet(head=subject.strip(), type=relation.strip(), tail=object_.strip()))
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append(triplet(head=subject.strip(), type=relation.strip(), tail=object_.strip()))
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append(triplet(head=subject.strip(), type=relation.strip(), tail=object_.strip()))
    return triplets


class Sentence_Extractor:
    def __init__(self):
        nltk.download('punkt_tab')

    def get_sentences(self,text):
        return sent_tokenize(text)
