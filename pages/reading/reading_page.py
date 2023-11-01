import json
import requests
from pathlib import Path
from hashlib import sha256
from mako.template import Template


class ReadingPage:

    ROOT_PATH = Path('pages/reading')
    IMAGES_PATH = Path('./img')
    BOOKS_IMAGES_PATH = IMAGES_PATH / 'books'

    def render(self, page_path):
        template_path = ReadingPage.ROOT_PATH / 'reading.html.in'
        template = Template(open(template_path).read())
        books = self._create_books_list()
        page = template.render(books=books)
        open(page_path, 'w').write(page)

    def _create_books_list(self):
        books = json.load(open(ReadingPage.ROOT_PATH / 'books.json'))
        for book in books:
            book['cover'] = self._generate_cover(book)
            book['name'] = self._create_book_name(book)
        return books

    def _create_book_name(self, book):
        if book['authors'] == '':
            return book['title']
        return '{} by {}'.format(book['title'], book['authors'])

    def _generate_cover(self, book):
        filename = self._generate_cover_filename(book)
        cover_path = ReadingPage.BOOKS_IMAGES_PATH / filename
        if cover_path.exists():
            return cover_path
        if not ReadingPage.BOOKS_IMAGES_PATH.exists():
            ReadingPage.BOOKS_IMAGES_PATH.mkdir()
        try:
            self._download_cover_image(book['isbn'], cover_path)
        except RuntimeError:
            default_cover_path = ReadingPage.IMAGES_PATH / 'cover_not_available.png'
            default_cover_path.copy_to(cover_path)
        return cover_path

    def _generate_cover_filename(self, book):
        filename = '_'.join([book['authors'], book['title'], book['isbn']])
        filename = filename.lower()
        filename = filename.replace(' ', '_')
        return sha256(filename.encode('UTF-8')).hexdigest()

    def _download_cover_image(self, isbn, filename):
        url = f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false'
        cover = requests.get(url)
        if not cover.ok:
            raise RuntimeError('Failed to download book\'s cover')
        open(filename, 'wb').write(cover.content)
