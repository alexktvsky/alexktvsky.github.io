import os
import re
import requests
import shutil
from hashlib import sha256
from typing import List
from pathlib import Path
from configparser import ConfigParser

from mako.template import Template

from pages.reading.book import Book
from pages.reading.bibtex_extractor import BibTexExtractor


class ReadingPage:

    TAG = u'\u2705'  # ✅
    ROOT_PATH = Path('pages/reading')
    IMAGES_PATH = Path('./img')
    BOOKS_IMAGES_PATH = IMAGES_PATH / 'books'
    CONFIG_FILENAME = 'pages/reading/config/config.ini'

    def render(self, file: str) -> None:

        config = ConfigParser()
        config.read(ReadingPage.CONFIG_FILENAME)

        bibtex_file = config['settings']['bibtex_file']

        bibtex_extractor = BibTexExtractor(bibtex_file)

        books = bibtex_extractor.get_books_by_tag(ReadingPage.TAG)

        book_template = Template(
            ReadingPage._read_text_file(
                ReadingPage.ROOT_PATH / 'book.html.in'
            )
        )

        reading_template = Template(
            ReadingPage._read_text_file(
                ReadingPage.ROOT_PATH / 'reading.html.in'
            )
        )

        result_list = []

        for book in books:

            if len(book.authors) != 0:
                authors = ', '.join([str(author) for author in book.authors])
                name = '{} - by {}'.format(book.title, authors)
            else:
                name = book.title
            date = self._get_date_read_from_notes(book.notes)

            book_html = book_template.render(
                image=self._generate_cover(book),
                 name=name,
                date=date,
                rating=self._get_rating_read_from_notes(book.notes),
                review=self._generate_review_from_notes(book.notes)
            )

            result_list.append(
                {
                    'html': book_html,
                    'date': date
                }
            )

            print('[ReadingPage]: {}'.format(name))

        result_list.sort(key=lambda x: x['date'], reverse=True)

        books_html = ''.join([x['html'] for x in result_list])

        reading_html = reading_template.render(books=books_html)

        ReadingPage._write_text_to_file(file, reading_html)

    def _get_rating_read_from_notes(self, notes: List[str]) -> str:

        info_line = self._get_info_line_from_notes(notes)

        if info_line is None:
            return ''

        rating = re.search(
            r'How strongly I recommend it: (.*?)\/10', info_line
        )
        if rating is None:
            raise RuntimeError('Failed to obtain rating from info line')

        return rating.group(1)

    def _get_date_read_from_notes(self, notes: List[str]) -> str:

        info_line = self._get_info_line_from_notes(notes)

        # Try to get a date in format %Y-%m-%d
        date_read = re.search(r'\b(\d{4}-\d{2}-\d{2})', info_line)

        # Try to get a date in format %Y-%m, if previous attempt failed
        if date_read is None:
            date_read = re.search(r'\b(\d{4}-\d{2})', info_line)

        # Try to get a date in format %Y, if previous attempt failed
        if date_read is None:
            date_read = re.search(r'\b(\d{4})', info_line)

        # Return empty string if all attempts failed
        if date_read is None:
            raise RuntimeError('Failed to obtain date read from info line')

        return date_read.group(0)

    def _generate_review_from_notes(self, notes: List[str]) -> str:

        info_line = self._get_info_line_from_notes(notes)

        if info_line is None:
            return ''

        notes = ' '.join(notes)
        notes = notes.replace(info_line, '')
        notes = notes.replace('\n', '', 1)
        notes = notes.replace('\n', '<br>\n')

        return notes

    def _get_info_line_from_notes(self, notes: List[str]) -> str:
        if len(notes) == 0:
            raise RuntimeError('Failed to obtain info line from notes')

        return notes[0].split('\n', 1)[0]

    def _generate_cover(self, book: Book) -> str:

        filename = self._generate_cover_filename(book)
        full_filename = ReadingPage.BOOKS_IMAGES_PATH / filename

        if os.path.exists(full_filename):
            return full_filename

        if not os.path.exists(ReadingPage.BOOKS_IMAGES_PATH):
            os.mkdir(ReadingPage.BOOKS_IMAGES_PATH)

        try:
            self._download_cover_file(book.isbn, full_filename)
        except RuntimeError:
            shutil.copyfile(ReadingPage.IMAGES_PATH / 'cover_not_available.png', full_filename)

        return full_filename

    def _download_cover_file(self, isbn: str, filename: str) -> None:

        cover_url = (
            'https://covers.openlibrary.org/b/isbn/{}-M.jpg?default=false'
        ).format(isbn)

        cover = requests.get(cover_url)
        if not cover.ok:
            raise RuntimeError('Failed to download book\'s cover')

        open(filename, 'wb').write(cover.content)

    def _generate_cover_filename(self, book: Book) -> str:
        authors = ', '.join([str(author) for author in book.authors])

        filename = '_'.join([authors, book.title, book.isbn])
        filename = filename.lower()
        filename = filename.replace(' ', '_')

        return sha256(filename.encode('UTF-8')).hexdigest()

    @staticmethod
    def _read_text_file(filename: str) -> str:
        with open(filename, 'r') as file:
            return file.read()

    @staticmethod
    def _write_text_to_file(filename: str, text: str) -> str:
        with open(filename, 'w') as file:
            file.write(text)
