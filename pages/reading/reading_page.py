import json
import requests
import shutil
from pathlib import Path
from hashlib import sha256
from mako.template import Template
from PIL import Image
from requests.exceptions import ConnectTimeout

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
        except (RuntimeError, ConnectTimeout):
            default_cover_path = ReadingPage.IMAGES_PATH / 'cover_not_available.jpg'  # noqa: E501
            shutil.copy(default_cover_path, cover_path)
        return cover_path

    def _generate_cover_filename(self, book):
        filename = '_'.join([book['authors'], book['title'], book['isbn']])
        filename = filename.lower()
        filename = filename.replace(' ', '_')
        filename = sha256(filename.encode('UTF-8')).hexdigest()
        filename = f'{filename}.jpg'
        return filename

    def _convert_image_to_jpg(self, input_path, output_path):
        image = Image.open(input_path)
        image.save(output_path, quality=70)

    def _download_cover_image(self, isbn, file_path, convert=False):
        url = f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false'  # noqa: E501
        response = requests.get(url)
        if not response.ok:
            raise RuntimeError('Failed to download book\'s cover')
        if convert:
            tmp_file_path = ReadingPage.BOOKS_IMAGES_PATH / 'tmp_image'
            open(tmp_file_path, 'wb').write(response.content)
            self._convert_image_to_jpg(tmp_file_path, file_path)
            tmp_file_path.unlink()
        else:
            open(file_path, 'wb').write(response.content)
