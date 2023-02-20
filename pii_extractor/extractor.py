from .dataset import Dataset
from typing import Dict, List


class Extractor(Dataset):

    def __init__(self, words: List[str]) -> None:
        super().__init__()
        self.words = words

    @classmethod
    def from_text(cls, text_words: str):
        return cls(words=text_words.split())

    def run(self) -> Dict[str, List[str]]:
        self.check_words(words=self.words)
        return dict(self.information)
