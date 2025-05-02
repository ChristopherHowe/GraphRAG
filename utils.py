from nltk.tokenize import sent_tokenize
import nltk
from typing import List
from models import triplet
from torch.utils.data import Dataset

def jupyter_print_paragraph(paragraph: str, line_width: int = 80):
    # Could probably improve this to account for spaces but for now this is okay.
    """Prints a paragraph with wrapping every n characters to make it more readable instead of a single line"""
    print("\n".join([paragraph[i:i+line_width] for i in range(0, len(paragraph), line_width)]))




def extract_triplets(text) -> List[triplet]:
    # Source: https://huggingface.co/Babelscape/rebel-large#pipeline-usage
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


class SentenceDataset(Dataset):
    def __init__(self, sentences):
        self.sentences = [s for content_sentences in sentences for s in content_sentences]  # Flatten list
        
    def __len__(self):
        return len(self.sentences)
    
    def __getitem__(self, idx):
        return self.sentences[idx]
    
