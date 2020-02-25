from typing import List, Tuple, Set, Any
from operator import itemgetter

LibraryType = Tuple[int, int, int, List[Tuple[int, int]]]
LibrariesType = List[LibraryType]
ListBooksWithScoreType = List[Tuple[int, int]]
ListBooks = List[int]
ListOutputType = List[Tuple[int, List[int]]]

# max with books
# Trier les livres par ceux qui ont le plus de points
# trouver tous les doubles et récupérer là ou c'est le mieux


def max_score_for_lib(max_day: int, signup: int, books_with_score: List[Tuple[int, int]], book_by_day: int, book_already_done: Set[int]) -> Tuple[int, ListBooksWithScoreType]:
    books_with_score = list(
        filter(
            lambda x: x not in book_already_done,
            books_with_score,
        )
    )
    books_with_score = sorted(books_with_score, reverse=True)
    days_for_book_scan = max_day - signup
    if days_for_book_scan < 1:
        return 0, []
    books = books_with_score[:days_for_book_scan * book_by_day]
    return sum(map(itemgetter(0), books)), books


def compute(max_day_number: int, libraries: LibrariesType):
    already_done: Set[int] = set()
    nbr_days = 0
    output: ListOutputType = []

    def compute_max_score_for_lib(lib: LibraryType) -> Tuple[int, ListBooksWithScoreType, LibraryType]:
        i, signup_days, book_by_day, books_with_score = lib
        score, books = max_score_for_lib(max_day_number, signup_days, books_with_score, book_by_day, already_done)
        return score, books, lib

    libs = sorted(list(map(compute_max_score_for_lib, libraries)), reverse=True)

    while nbr_days < max_day_number and len(libs) > 0:
        (score, books, lib), *libs = libs
        i, signup_days, book_by_day, books_with_score = lib
        nbr_days += signup_days
        already_done.update(set(map(itemgetter(1), books)))
        output.append((i, list(map(itemgetter(1), books))))

    return output


def parse_input(input_path: str) -> Tuple[int, int, int, LibrariesType]:
    with open(input_path) as f:
        content = f.read().split("\n")

    book_number, library_number, max_day_number = map(int, content[0].split(" "))
    book_scores = list(map(int, content[1].split(" ")))

    content = content[2:]
    libraries: LibrariesType = []

    for i in range(library_number):
        book_number, signup_days, book_by_day = map(int, content[i * 2].split(" "))
        books = list(map(int, content[i * 2 + 1].split(" ")))
        books_with_score = sorted([(book_scores[book], book) for book in books], reverse=True)
        libraries.append((i, signup_days, book_by_day, books_with_score))

    return book_number, library_number, max_day_number, libraries


def write_output(output_name: str, output: ListOutputType):
    out = f"{len(output)}"
    for idx, books in output:
        out += f"\n{idx} {len(books)}\n"
        out += " ".join(map(str, books))

    with open(output_name, "w") as f:
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
    _, _, max_day, libraries = parse_input("in/" + name)
    output = compute(max_day, libraries)
    write_output(f"out/{name}.out", output)


