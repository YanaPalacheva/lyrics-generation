def rhyme_score(endings):
    line_num = len(endings)
    rhymes_count = 0
    i = 0
    ideal = 0
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


# l = ['hi', 'hi', 'hey', 'hey', 'hey', 'ho', 'hu', 'hu', 'hc', 'hc', 'hc', 'hm', 'hm', 'hi', 'hi', 'hi', 'hi', 'hi']
# print(rhyme_score(l))



