from nltk.tokenize import sent_tokenize
import nltk
from IPython.core.display import HTML
from typing import Callable



def jupyter_print_paragraph(paragraph: str, line_width: int = 80):
    # Could probably improve this to account for spaces but for now this is okay.
    """Prints a paragraph with wrapping every n characters to make it more readable instead of a single line"""
    print("\n".join([paragraph[i:i+line_width] for i in range(0, len(paragraph), line_width)]))


class Sentence_Extractor:
    def __init__(self):
        nltk.download('punkt_tab')

    def get_sentences(self,text):
        return sent_tokenize(text)

# class SentenceDataset(Dataset):
#     def __init__(self, sentences):
#         self.sentences = [s for content_sentences in sentences for s in content_sentences]  # Flatten list
        
#     def __len__(self):
#         return len(self.sentences)
    
#     def __getitem__(self, idx):
#         return self.sentences[idx]
    

def display_prompt_and_output(full_prompt: str, response: str, display_func: Callable[[HTML], None]):
    '''Creates a html table displaying the prompt and response using the display func (typically provided by jupyter notebook)'''
    html_content = f"""
    <table style="width:100%; border: 1px solid black; border-collapse: collapse;">
        <tr>
            <th style="border: 1px solid black; padding: 10px; text-align: left;">Full Prompt</th>
            <th style="border: 1px solid black; padding: 10px; text-align: left;">Response</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 10px; white-space: pre-wrap; text-align: left; vertical-align: top;">{full_prompt}</td>
            <td style="border: 1px solid black; padding: 10px; white-space: pre-wrap; text-align: left; vertical-align: top;">{response}</td>
        </tr>
    </table>
    """
    display_func(HTML(html_content))