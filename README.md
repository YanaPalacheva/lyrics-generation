# Song lyrics generation

Based on [RNN Markov Poetry Generator](https://www.kaggle.com/paultimothymooney/poetry-generator-rnn-markov)

## Implemented features:
- Extended rhyming: based on 2-morpheme endings instead of 2-letter endings (based on [Ghostwriter](https://github.com/dns-mcdaid/Ghostwriter) Rhyming Algorithm). Rhyming morphemes are grouped by phonetic properties: similar sounds, stress, paired consonants.
- Works for different artists and genres (samples from the MetroLyrics dataset are in *data* folder).
- Evaluation functions for rhyme and grammar that allow to evaluate generated lyrics.
- User interface. It allows to mix two artists together or simply generate lyrics based on a single artist or genre. It also allows to change generation parameters: depth of the RNN, max number of syllables per lyne, max overlap ratio for Markov sequences, desired number of generated lines.

## Working with dataset
The repository contains a set of preprocessed initial dataset files and generated lyrics for your convinience. But you are welcome to try new artists and genres. For that, you would have to do the following: 

- Download the MetroLyrics dataset from [Kaggle](https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics), extract it and put *lyrics.csv* in the working (project) folder. Then use *preprocessing.py* to add genres and artists, to preprocess the data, to calculate average syllables and/or to create rhyming schemes for evaluation. After this run *lyrics_generation.py* to launch the GUI and enjoy the results.

## GUI guide
First of all, choose the base data for lyrics generation: **artists** or **genres**.

**Genres**: choose one of the genres from a drop-down list on the "Genres" tab.  
**Artists**: choose one of the artist on the "Artists" tab. If you want to generate lyrics based on two artists, check the "Shuffle with" box and choose the second artist.

**Parameters**: You can run the generation with default parameters, for that just check the "Use default parameters" box and hit "Generonimo!" :)

If you want to go deeper, you can manually adjust the following parameters:
- *Num of lines*: number of lines to be generated.
- *NN depth*: number of hidden layers of the RNN.
- *Max. overlap*: maximum overlap ratio for Markov sequences (degree of similarity to the original data).
- *Max. syllables*: maximum number of syllables per generated line (default values are average syllable numbers per line calculated for each artist).

To reduce computational complexity, maximize *Max. syllables* and *Max. overlap*. Note that computational time will increase dramatically when *Max. syllables* is less that 8 and when *Max. overlap* is less than 0.5. The lower is "Max. syllables" value, the higher should be *Max. overlap*, as with less syllables per line Markov model requires more freedom in line generating provided by max overlap ratio. 

**Evaluation**: If you want to evaluate rhyme in the generated lyrics, you can use the "Evaluate rhyme" button. Evaluation returns two scores: rhyme score and rhyming lines score, both values are in range(0,1).

Rhyme score is defined as following:  
> *rhyme_count / (2\*line_num/4)*  

where *rhyme_count* is the number of existing rhymes within 4-line chunks, *(2\*line_num/4)* is the maximum ("perfect") number of rhymes in lyrics: *line_num/4* is the number of 4-line chunks in lyrics, *2* is the maximum number of different rhymes in a 4-line chunk (aabb, abab).

Rhyming lines score is a number of lines that rhymed with another line within the 4-line chunk divided by total number of lines:
> *rhymed_line_num / line_num*

## Additional features

**Grammaticality evaluation**: to be added. 
