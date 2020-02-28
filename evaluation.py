def syllables(line):
    count = 0
    for word in line.split(" "):
        vowels = 'aeiouy'
#        word = word.lower().strip("!@#$%^&*()_+-={}[];:,.<>/?")
        word = word.lower().strip(".:;?!")
        if word[0] in vowels:
            count +=1
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count+=1
        if count == 0:
            count +=1
    return count / maxsyllables

# scoring equality of syllalbe numbers between two lines
def syllable_match(line1, line2):
    if syllables(line1) == syllables(line2):
        return 1
    else:
        return 0

# evaluating the lyrics based on parameter which can be rhyme_score or syllable_match
def eval(lyrics, parameter, beta = 0.9):
    score = 0
    # We assume lyrics is a list of lines
    n = len(lyrics)
    for i in range(n): 
        # add a factor for matching consecutive lines only if the don't match line before (+BAA)
        if i-2 < 0 or parameter(lyrics[i-2], lyrics[i-1]) < parameter(lyrics[i-1], lyrics[i]):
            score += parameter(lyrics[i-1], lyrics[i])
        if i > 1: # add a factor for lines two apart matching but not with line in between (+beta * ABA)
            v = parameter(lyrics[i-2], lyrics[i])
            v1 = parameter(lyrics[i-2], lyrics[i-1])
            v2 = parameter(lyrics[i-1], lyrics[i])
            if v > max(v1, v2):
                score += beta * parameter(lyrics[i-2], lyrics[i])
                
    return score / len(lyrics)