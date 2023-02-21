from dataclasses import dataclass
from typing import List
from collections import defaultdict
import json

from .regex import Regex


@dataclass
class DatasetItem:
    name: str
    keywords: List[str]
    type: str


class Dataset(Regex):

    def __init__(self):
        with open("pii_dataset.json") as f:
            self.dataset = json.load(f)
            super().__init__(self.dataset)

        self.information = defaultdict(list)
        self._dataset_items = None

    @property
    def dataset_items(self) -> List[DatasetItem]:
        if self._dataset_items is None:
            self._dataset_items = [
                DatasetItem(name=name, **data)
                for name, data in self.dataset.items()
                if data["type"] in ("contains", "list")
            ]

        return self._dataset_items

    def check_words(self, words: List[str]):
        check_functions = {
            "contains": self.contains_keywords,
            "list": self.contains_list
        }

        for dataset_item in self.dataset_items:
            function = check_functions[dataset_item.type]
            function(words=words, item=dataset_item)

        for regex_item in self.regex_items:
            result = regex_item.parse(words=words)
            if result:
                self.information[regex_item.name] += result

    def contains_keywords(self, words: List[str], item: DatasetItem):
        for word in words:
            if word in item.keywords:
                self.information[item.name].append(word)

    @staticmethod
    def does_contain_multiple(words: List[str], current_count: int, item: DatasetItem) -> bool:
        for keyword in item.keywords:
            keyword_words = keyword.split()
            iter_count = current_count
            has_broke = False
            for keyword_word in keyword_words:
                if keyword_word not in words[iter_count]:
                    has_broke = True
                    break

                iter_count += 1
            if not has_broke:
                return True

        return False

    def contains_list(self, words: List[str], item: DatasetItem) -> None:
        collection = {"enabled": False, "collected": [], "stop_index": 0}
        for count, word in enumerate(words):
            if word in self.dataset["connectors"]["keywords"]:
                collection["stop_index"] = count + 2

            elif collection["stop_index"] == count and collection["stop_index"] != 0:
                collection["enabled"] = False

            elif self.does_contain_multiple(words=words, current_count=count, item=item):
                collection["enabled"] = True

            elif collection["enabled"]:
                collection["collected"].append(word)

        if collection["collected"]:
            self.information[item.name] += collection["collected"]
