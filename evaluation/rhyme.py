def rhyme_score(endings):
    """
    Computes two rhyme scores: rhyme percentage and rhyming lines percentage.

    Rhyme percentage is defined as following:
        rhyme_count / (2*line_num/4),
    where rhyme_count is the number of existing rhymes within 4-line chunks,
    (2*line_num/4) is the maximum ("perfect") number of rhymes in lyrics:
    line_num/4 is the number of 4-line chunks in lyrics,
    2 is the maximum number of different rhymes in a 4-line chunk (aabb, abab).

    Rhyming lines percentage is a number of lines that rhymed with another line within the 4-line chunk
    divided by total number of lines.

    :param endings: list of endings for the last word of each line, str[].
    :return: two rhyme scores: rhyme percentage and rhyming lines percentage.
    """
    line_num = len(endings)
    rhymes_count = 0
    i = 0
    while i < len(endings):
        curr_ending = endings[i]
        chunk = endings[i:i+4]
        if chunk.count(curr_ending) > 1:
            new_endings = ['' if x == curr_ending else x for x in chunk]
            endings = endings[0:i] + new_endings + endings[i+4:]
            if '' in new_endings:
                rhymes_count += 1
        i += 1
        while i < len(endings) and endings[i] == '':
            i += 1
    return 2*rhymes_count/line_num, endings.count('')/line_num



