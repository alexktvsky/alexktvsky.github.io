import os
import json
import requests
import shutil
from pathlib import Path
from hashlib import sha256
from mako.template import Template


class ReadingPage:

    ROOT_PATH = Path('pages/reading')
    IMAGES_PATH = Path('./img')
    BOOKS_IMAGES_PATH = IMAGES_PATH / 'books'

    def render(self, file):

        books = json.loads(
            ReadingPage._read_text_file(
                ReadingPage.ROOT_PATH / 'books.json'
            )
        )

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

            book_html = book_template.render(
                image=self._generate_cover(book),
                name=self._create_book_name(book),
                date=book['date'],
                rating=book['rating'],
                review=book['review']
            )

            result_list.append(book_html)

            print('[ReadingPage]: {}'.format(book['title']))

        reading_html = reading_template.render(books=''.join(result_list))

        ReadingPage._write_text_to_file(file, reading_html)

    def _create_book_name(self, book):

        if book['authors'] == '':
            return book['title']

        return '{} by {}'.format(book['title'], book['authors'])

    def _generate_cover(self, book):

        filename = self._generate_cover_filename(book)
        full_filename = ReadingPage.BOOKS_IMAGES_PATH / filename

        if os.path.exists(full_filename):
            return full_filename

        if not os.path.exists(ReadingPage.BOOKS_IMAGES_PATH):
            os.mkdir(ReadingPage.BOOKS_IMAGES_PATH)

        try:
            self._download_cover_file(book['isbn'], full_filename)
        except RuntimeError:
            shutil.copyfile(
                ReadingPage.IMAGES_PATH / 'cover_not_available.png',
                full_filename
            )

        return full_filename

    def _generate_cover_filename(self, book):

        filename = '_'.join([book['authors'], book['title'], book['isbn']])
        filename = filename.lower()
        filename = filename.replace(' ', '_')

        return sha256(filename.encode('UTF-8')).hexdigest()

    def _download_cover_file(self, isbn, filename):

        cover_url = (
            'https://covers.openlibrary.org/b/isbn/{}-M.jpg?default=false'
        ).format(isbn)

        cover = requests.get(cover_url)
        if not cover.ok:
            raise RuntimeError('Failed to download book\'s cover')

        open(filename, 'wb').write(cover.content)

    @staticmethod
    def _read_text_file(filename):
        with open(filename, 'r') as file:
            return file.read()

    @staticmethod
    def _write_text_to_file(filename, text):
        with open(filename, 'w') as file:
            file.write(text)
