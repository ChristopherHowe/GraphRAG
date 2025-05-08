from typing import List
from models import triplet
from transformers import pipeline


class ER_Extractor:
    def __init__(self):
        self.triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')
    
    def extract_ERs(self, sentences: List[str]):
        tokens = self.triplet_extractor(sentences, return_tensors=True, return_text=False)
        token_ids = [token["generated_token_ids"] for token in tokens]
        extracted_text = self.triplet_extractor.tokenizer.batch_decode(token_ids)  # Takes by far the longest out of all the operations here
        return [triplet for text in extracted_text for triplet in self._extract_triplets(text)]

    def _extract_triplets(self, text) -> List[triplet]:
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