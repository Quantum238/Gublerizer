import urllib.error
import urllib.request as url
import re
from random import randint
from math import ceil




def get_lyrics(song,band):

    base = r'http://www.azlyrics.com/lyrics'
    full = base + '/' + band + '/' + song + '.html'

    try:
        full_page_obj = url.urlopen(full)
    except urllib.error.HTTPError:
        return [],0,0
    full_page_text = full_page_obj.read().decode()

  
    
    start = full_page_text.find('<!-- start of lyrics -->')
    end = full_page_text.find('<!-- end of lyrics -->')
    #the length of the start string is 24 characters.  The index from
    #find will give me the location of the opening <, so I jump ahead 24
    lyrics = full_page_text[start + 24:end]
    lyrics = re.sub(r'<br />','',lyrics)
    lyrics_list = lyrics.splitlines()
    lyrics_list.pop(0) #first element is always empty
    lyrics_list = [x.split() for x in lyrics_list]
    total_words = sum([len(x) for x in lyrics_list])
    average_line_length = ceil(total_words / len(lyrics_list))
    #lyrics list is now a list of lists - lines and then words
    return lyrics_list,total_words,average_line_length

def is_valid(word):
    """Defines what counts as a replaceable word.  To help give the
code a semblance of intelligence, it should not replace prepositions and
articles - ideally it would replace only nouns and certain verb tenses,
but this is enough to give it the appearance of much more complicated logic."""

    invalid = ['aboard', 'about', 'above', 'across', 'after', 'against',
               'along', 'amid', 'among', 'anti', 'around', 'as', 'at',
               'before', 'behind', 'below', 'beneath', 'beside', 'besides',
               'between', 'beyond', 'but', 'by', 'concerning', 'considering',
               'despite', 'down', 'during', 'except', 'excepting', 'excluding',
               'following', 'for', 'from', 'in', 'inside', 'into', 'like',
               'minus', 'near', 'of', 'off', 'on', 'onto', 'opposite',
               'outside', 'over', 'past', 'per', 'plus', 'regarding',
               'round', 'save', 'since', 'than', 'through', 'to', 'toward',
               'towards', 'under', 'underneath', 'unlike', 'until', 'up',
               'upon', 'versus', 'via', 'with', 'within', 'without','the',
               'it','a','an','is','be','are','am','and']

    return word in invalid
        
        
def gub_a_line(line,avg,start):
    '''Returns the gublerization of a line.  Changes every few words
    (randomly jumps forward by an amount governed by average line length) to
    'Gubler'.  If jump would move past the line length, returns the gublerized
    line and the number of words past the end of the line, so that the next line
    can begin a few words in (this keeps up the appearance of every few words
    being changed in the overall song - without this 'carry' capacity, there is
    larger tendency for gubler to appear in the beginning of each line,
    ruining the organic nature of the song'''
    

    mark = start
    #pointer to keep track of position in line.  Is either 0 or the carry
    #from the previous line

    while mark < len(line):
        advance = randint(0,ceil(avg/2))
        mark = mark+advance
        
        if mark >= len(line):
            return line,mark - len(line)
        else:
            #Don't want there to be two Gublers in a row
            if mark!=0 and line[mark-1]!='Gubler' and is_valid(line[mark]):
                line[mark] = 'Gubler'
        
if __name__ == '__main__':

    band = input('Band Name: ')
    band = band.lower().replace(' ','') #lightly santize for the url 
    song = input('Song Title: ')
    song = song.lower().replace(' ','') #same
    
    lyrics_list,total_words,average_line_length = get_lyrics(song,band)

    if total_words == 0:
        print('Song Not Found')

    else:
            
        new_lyrics_list = []
        carry = 0
        
        for x in lyrics_list:
            try:
                new_line,carry = gub_a_line(x,average_line_length,carry)
                new_lyrics_list.append(new_line)
                
            except TypeError:
                #Occasionally, a line will be None, which then can
                #not be indexed in the gub function.  I suspect this is
                #due to improper scrubbing of html in certain songs,
                #but I haven't been able to isolate the bug.  This
                #allows for problematic lines to simply be skipped
                pass
        
        string_list = [' '.join(x) for x in new_lyrics_list]
        #put words back together into lines
        gubics = '\n'.join(string_list)
        #compile individual lines into one string, with breaks
        print(gubics)
        
        
