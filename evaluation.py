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

# evaluating the lyrics based on aspect which can be rhyme_score or syllable_match
def eval(lyrics, aspect, beta = 0.9, a = 0.2, b = 0.1):
    score = 0
    # We assume lyrics is a list of lines
    n = len(lyrics)
    for i in range(1, n): 
        # add a factor for matching consecutive lines only if the don't match line before (+BAA)
        if i-2 < 0 or aspect(lyrics[i-2], lyrics[i-1]) < aspect(lyrics[i-1], lyrics[i]):
            score += aspect(lyrics[i-1], lyrics[i])
        else:
            score += a * aspect(lyrics[i-1], lyrics[i]) # add a factor of 'a' even if they don't differ from the line before
            
        if i > 1: # add a factor for lines two apart matching but not with line in between (+beta * ABA)
            v = aspect(lyrics[i-2], lyrics[i])
            v1 = aspect(lyrics[i-2], lyrics[i-1])
            v2 = aspect(lyrics[i-1], lyrics[i])
            if v > max(v1, v2):
                score += beta * aspect(lyrics[i-2], lyrics[i])
            else:
                score += b * aspect(lyrics[i-1], lyrics[i]) # add a factor of 'b' even if they don't differ from line in between
                
    return score / len(lyrics)