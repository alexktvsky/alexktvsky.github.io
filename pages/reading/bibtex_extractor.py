from pybtex.database.input import bibtex
from pybtex.database import Entry
from typing import List

from pages.reading.book import Book
from pages.reading.author import Author


class BibTexExtractor:

    def __init__(self, filename: str) -> None:
        self._filename = filename

    def _remove_curly_brackets(self, s: str) -> str:

        s = s.replace('{', '')
        s = s.replace('}', '')
        return s

    def _extract_authors(self, entry: Entry) -> List[Author]:

        authors = []

        try:
            for x in entry.persons['author']:

                first_name = x.first_names[0] if len(x.first_names) else ''
                middle_name = x.middle_names[0] if len(x.middle_names) else ''
                last_name = x.last_names[0] if len(x.last_names) else ''

                # Well, that's a slight oversimplification.
                # We store middle name together with first name.
                if middle_name:
                    first_name = '{} {}'.format(first_name, middle_name)

                first_name = self._remove_curly_brackets(first_name)
                last_name = self._remove_curly_brackets(last_name)

                authors.append(Author(first_name, last_name))

        except KeyError:
            pass

        return authors

    def _check_tag(self, tag: str, entry: Entry) -> bool:

        try:
            tags = entry.fields['keywords'].split(',')
        except KeyError:
            return False

        return tag in tags

    def get_books_by_tag(self, tag: str) -> List[Book]:

        books = []

        parser = bibtex.Parser()
        bib_data = parser.parse_file(self._filename)

        for entry in bib_data.entries.values():

            if entry.type != 'book':
                continue

            if not self._check_tag(tag, entry):
                continue

            authors = self._extract_authors(entry)

            title = self._remove_curly_brackets(entry.fields['title'])

            try:
                isbn = self._remove_curly_brackets(entry.fields['isbn'])
            except KeyError:
                isbn = ''

            try:
                notes = self._remove_curly_brackets(entry.fields['note'])
                notes = notes.split(' \\par ')
            except KeyError:
                notes = []

            books.append(Book(authors, title, isbn, notes))

        return books
