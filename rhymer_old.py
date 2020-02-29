import re
import pronouncing
import nltk


def create_rhymescheme(line):
    word = re.sub(r"\W+", '', line.split(" ")[-1]).lower()
    rhymeslist = pronouncing.rhymes(word)
    rhymeslistends = []
    for i in rhymeslist:
        rhymeslistends.append(i[-2:])
    try:
        rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
    except Exception:
        rhymescheme = word[-2:]
    return rhymescheme


class RhymerOld:
    def __init__(self, identifier):
        self.rhyme_filename = f"rhymes/{identifier}.rhymes"
        self.lyrics_filename = f"data/{identifier}.txt"
        self.entries = nltk.corpus.cmudict.entries()

    def rhymeindex(self, lyrics):
        rhyme_master_list = []
        print("Building list of rhymes:")
        for line in lyrics:
            rhymescheme = create_rhymescheme(line)
            rhyme_master_list.append(rhymescheme)

        rhyme_master_list = list(set(rhyme_master_list))
        reverselist = [x[::-1] for x in rhyme_master_list]
        reverselist = sorted(reverselist)
        rhymelist = [x[::-1] for x in reverselist]

        print("List of Sorted 2-Letter Rhyme Ends:")
        print(rhymelist)
        f = open(self.rhyme_filename, "w", encoding='utf-8')
        f.write("\n".join(rhymelist))
        f.close()
        return rhymelist

    def rhyme(self, i, line, rhyme_list, generated=False):
        rhymescheme = create_rhymescheme(line)
        float_rhyme = rhyme_list.index(rhymescheme)
        if rhyme_list:
            float_rhyme = float_rhyme / float(len(rhyme_list))
            return float_rhyme
        else:
            return 0
