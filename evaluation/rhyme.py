def rhyme_score(endings):
    rhymes_count = 0
    # for i in range(len(endings)-3):
        # ending = endings[i]
        # endings_to_compare = [endings[j] for j in range(i+1, i+4)]
        # for e in endings_to_compare:
        #     if ending == e:
        #         rhymes_count += 1
        #         break
    line_num = len(endings)
    start_endings = endings
    rhymes_count = 0
    cnt = 0
    ideal = 0
    while len(endings) != len(set(endings)):
        start_len = len(endings)
        new_endings = endings[cnt:cnt+4]
        curr_ending = endings[cnt]
        if new_endings.count(curr_ending) > 1:
            while curr_ending in new_endings:
                new_endings.remove(curr_ending)
            endings = endings[0:cnt] + new_endings + endings[cnt+4:]

        if start_len == len(endings):
            cnt += 1
        else:
            rhymes_count += 1
        ideal += 1
    print(ideal)
    print(line_num)
    return rhymes_count/ideal, 1-len(endings)/line_num


l = ['hi', 'hi', 'hey', 'hem', 'ho', 'ho', 'hu', 'hu', 'hc', 'hc', 'hj', 'hj', 'hi', 'hi', 'hj', 'hg', 'hi', 'hi']
print(rhyme_score(l))



