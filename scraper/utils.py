AUTHORS = []


def get_author_id(author: str) -> int:
    """Replace author account name by id"""
    if author not in AUTHORS:
        AUTHORS.append(author)
    return AUTHORS.index(author)


def replace_authors(text: str) -> str:
    """Replace name of authors/accounts in text"""
    for author in AUTHORS:
        text = text.replace(f" {author} ", f" {get_author_id(author)}")
        text = text.replace(f"@{author}", f"@{get_author_id(author)}")
    return text
