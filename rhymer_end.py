import re
import pronouncing
from utils import split_file, get_last_word


class RhymerEnd:
    def __init__(self, identifier, generated=False):
        self.rhyme_filename = f"rhymes/{identifier}.rhymes"
        if generated:
            self.scheme_filename = f"schemes/{identifier}_generated.schemes"
            self.lyrics_filename = f"generated_lyrics/{identifier}_generated.txt"
        else:
            self.scheme_filename = f"schemes/{identifier}.schemes"
            self.lyrics_filename = f"data/{identifier}.txt"

    def line_rhymescheme(self, line):
        word = re.sub(r"\W+", '', get_last_word(line)).lower()
        rhymeslist = pronouncing.rhymes(word)
        rhymeslistends = []
        for i in rhymeslist:
            rhymeslistends.append(i[-2:])
        try:
            rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
        except Exception:
            rhymescheme = word[-2:]
        return rhymescheme

    def create_rhymescheme(self):
        lyrics = split_file(self.lyrics_filename)
        schemes = []
        for i, line in enumerate(lyrics):
            schemes.append(self.line_rhymescheme(line))
        with open(self.scheme_filename, "w", encoding='utf-8') as f:
            f.write('\n'.join(schemes) + '\n')

    def rhymeindex(self, lyrics):
        rhyme_master_list = []
        print("Building list of rhymes:")
        for line in lyrics:
            rhymescheme = self.line_rhymescheme(line)
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
        rhymescheme = self.line_rhymescheme(line)
        float_rhyme = rhyme_list.index(rhymescheme)
        if rhyme_list:
            float_rhyme = float_rhyme / float(len(rhyme_list))
            return float_rhyme
        else:
            return 0
