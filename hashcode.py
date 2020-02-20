from typing import List, Tuple
from random import randint


class Library:
    id: int
    signup_days: int
    book_by_day: int
    books: List[int]


def parse_input(input_path: str):
    with open(input_path) as f:
        content = f.read().split("\n")

    book_number, library_number, max_day_number = map(int, content[0].split(" "))
    book_scores = list(map(int, content[1].split(" ")))

    content = content[2:]
    libraries = []
    book_added = set()

    for i in range(library_number):
        book_number, days, book_by_day = map(int, content[i * 2].split(" "))
        books = list(map(int, content[i * 2 + 1].split(" ")))

        # books_with_score = []
        # for book in books:
        #     if book not in book_added:
        #         book_added.add(book)
        #         books_with_score.append((book_scores[book], book))
        # books_with_score = sorted(books_with_score, reverse=True)
        books_with_score = sorted([(book_scores[book], book) for book in books], reverse=True)
        scores, book_sorted = list(zip(*books_with_score))

        # scores = -days + sum(scores) * book_number / book_by_day

        scoreValueBook = (book_number / book_by_day) * (sum(scores) / book_number)

        libraries.append((
            -days, scoreValueBook, randint(0, 100),
            i, days, book_by_day, books, book_sorted))

    return book_number, library_number, max_day_number, libraries


def compute_simple(book_number: int, library_number: int, max_day_number: int, libraries: List[Tuple[int, int, int, List[int], List[int]]], output: str):
    lib_in_progress = None
    lib_signup = {}
    computed_books = set()
    libs_output = {}

    for current_day in range(max_day_number):
        if lib_in_progress is not None:  # avant ou après la boucle
            idx, day_start = lib_in_progress
            i, days, book_by_day, books, book_sorted = libraries[idx]
            if day_start + days <= current_day:
                lib_signup[idx] = []
                lib_in_progress = None

        if lib_in_progress is None:
            for i, days, book_by_day, books, book_sorted in libraries:
                if i == lib_in_progress or i in lib_signup:
                    continue
                if current_day + days <= max_day_number:
                    lib_in_progress = i, current_day
                    break

        for i, books_done in lib_signup.items():
            i, days, book_by_day, books, book_sorted = libraries[i]
            for _ in range(book_by_day):
                for book in book_sorted:
                    if book in computed_books:
                        continue
                    computed_books.add(book)
                    if i not in libs_output:
                        libs_output[i] = []
                    libs_output[i].append(book)

    out = f"{len(libs_output)}"
    for idx, books in libs_output.items():
        out += f"\n{idx} {len(books)}\n"
        out += " ".join(map(str, books))

    with open(output, "w") as f:
        f.write(out)





    # for i, days, book_by_day, books, book_sorted in libraries:
    #     if day_number + days <= max_day_number:
    #         day_number += days


def compute_stupid(book_number: int, library_number: int, max_day_number: int, libraries: List[Tuple[int, int, int, List[int], List[int]]], output: str):
    computed_books = set()
    libs_output = {}
    for _, _, _, i, days, book_by_day, books, book_sorted in sorted(libraries, reverse=True):
        book_filtered = []
        for book in book_sorted:
            if book not in computed_books:
                computed_books.add(book)
                book_filtered.append(book)

        libs_output[i] = book_filtered

    out = ""
    for idx, books in libs_output.items():
        if len(books) < 1:
            continue
        out += f"\n{idx} {len(books)}\n"
        out += " ".join(map(str, books))

    ll = len(out.split('\n'))
    out = f"{int(ll / 2)}{out}"

    with open(output, "w") as f:
        f.write(out)


names = [
    "a_example.txt",
    "b_read_on.txt",
    "c_incunabula.txt",
    "d_tough_choices.txt",
    "e_so_many_books.txt",
    "f_libraries_of_the_world.txt",
]

for name in names:
    print(name)
    l = parse_input("in/" + name)
    compute_stupid(*l, f"out/{name}.out")

