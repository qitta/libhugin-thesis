
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

def string_similarity_ratio(s1, s2):
    """
    A string compare function, using the Redcliff-Obershelp algorithm. For
    further details see: http://docs.python.org/3.3/library/difflib.html
    TODO: Levenshtein might be better for this purpose.

    :params s1, s2: Two input strings which will be compared
    :returns: A ratio between 0.0 (not similar at all) and 1.0 (probably the
    same string).

    """
    if s1 and s2:
        return 1 - normalized_damerau_levenshtein_distance(
            _clean_movie_title(s1),
            _clean_movie_title(s2)
        )


def _clean_movie_title(title):
    if title:
        title = title.lower()
        title = title.replace(',', ' ')
        title = title.replace(':', ' ')
        title = title.replace(';', ' ')
        title = title.replace('-', ' ')

        word_list = title.split()
        word_list.sort()
        return ' '.join(word_list)
