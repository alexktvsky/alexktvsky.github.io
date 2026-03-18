import { createHash } from "node:crypto";

export type RawBook = {
    title: string;
    authors: string;
    isbn: string;
    date: string;
    rating: string;
    review: string;
};

export type Book = RawBook & {
    name: string;
    cover: string;
};

export function createBookName(book: RawBook): string {
    if (!book.authors) {
        return book.title;
    }

    return `${book.title} by ${book.authors}`;
}

export function generateCoverFilename(book: RawBook): string {
    let filename = [book.authors, book.title, book.isbn].join("_");
    filename = filename.toLowerCase();
    filename = filename.replaceAll(" ", "_");

    return `${createHash("sha256").update(filename, "utf8").digest("hex")}.jpg`;
}

export function enrichBook(book: RawBook): Book {
    const filename = generateCoverFilename(book);

    return {
        ...book,
        name: createBookName(book),
        cover: `/img/books/${filename}`,
    };
}
