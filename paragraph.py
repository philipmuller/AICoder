import re

class Paragraph:
    type: str
    text: str
    sentences: [str]

    def __init__(self, type, text):
        self.type = type
        self.text = text
        self.sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    def provideContext(self, sentence: str) -> str:
        contextSentence = ""
        for s in self.sentences:
            if s != sentence:
                contextSentence = contextSentence+s
            else:
                return contextSentence
        return contextSentence
    
    def __str__(self):
        return f"type: {self.type}, text: {self.text}"

        