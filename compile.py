#!/usr/bin/env python3

from pathlib import Path

from pages.projects.projects_page import ProjectsPage
from pages.reading.reading_page import ReadingPage


OUTPUT_DIR = Path('./')


def main():
    ProjectsPage().render(OUTPUT_DIR / 'projects.html')
    ReadingPage().render(OUTPUT_DIR / 'reading.html')


if __name__ == '__main__':
    main()
