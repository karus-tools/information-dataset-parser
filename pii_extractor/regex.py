import re
from dataclasses import dataclass
from typing import List


@dataclass
class RegexItem:
    name: str
    regex_list: List[str]
    type: str

    def parse(self, words: List[str]) -> List[str]:
        extracted_words = []
        for regex in self.regex_list:
            extracted_words += [
                result
                for word in words
                for result in re.findall(regex, word)
            ]

        return extracted_words


class Regex:

    def __init__(self, dataset):
        self.dataset = dataset
        self._regex_items = None

    @property
    def regex_items(self) -> List[RegexItem]:
        if self._regex_items is None:
            self._regex_items = [
                RegexItem(name=name, **data)
                for name, data in self.dataset.items()
                if data["type"] == "regex"
            ]

        return self._regex_items
