from typing import List


class Book:
    def __init__(
            self,
            authors: List[str],
            title: str,
            isbn: str,
            notes: List[str]
    ) -> None:
        self.authors = authors
        self.title = title
        self.isbn = isbn
        self.notes = notes
