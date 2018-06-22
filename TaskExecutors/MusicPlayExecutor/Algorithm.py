import math


class Algorithm:

    SIMPLE_EXPONENTIAL_SEARCH = 0

    # The algorithm which searches for chunks of the text of search_for inside search_in string and provides a score.
    # This score increases exponentially with sequential matches in the same chunk.
    # Total score will be returned after iterating through every possible chunk of search_for
    # TODO #1:
    # This does not work well with the small search_for
    # TODO #2:
    # Optimize this algorithm by adding a method to recognize the letters which sounds nearly as the letter
    # in the search_in does.
    @staticmethod
    def score_simple_exponential_search_alg(search_in, search_for):
        total_score = 0.0
        for chunk_real_start_index in range(len(search_in)):
            chunk_real_end_index = chunk_real_start_index + len(search_for)

            if chunk_real_end_index <= len(search_in):
                chunk_real_artist = search_in[chunk_real_start_index:chunk_real_end_index]

                iteration_score = 0.0
                for iteration_index in range(1, len(search_for) + 1):
                    chunk_heard_artist = search_for[0:iteration_index]

                    comparator_score = 0.0
                    next_exponent_positive = 1
                    next_exponent_negative = 1
                    for letter_index in range(len(chunk_heard_artist)):
                        if chunk_real_artist[letter_index] == chunk_heard_artist[letter_index]:
                            comparator_score += math.pow(math.e, next_exponent_positive)
                            next_exponent_positive += 1
                        else:
                            comparator_score -= math.pow(math.e, next_exponent_negative)
                            next_exponent_negative += 1

                    if comparator_score > 0:
                        iteration_score += comparator_score

                total_score += iteration_score
            else:
                break

        return total_score

    # Used to normalize / map a value which exists within one range to another range.
    @staticmethod
    def get_normalized_value(value, old_min, old_max, new_min, new_max):
        return new_min + ((value - old_min) / (old_max - old_min)) * (new_max - new_min)
