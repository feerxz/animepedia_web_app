
#Función para sacar una descripción corta de los animes
def make_short_synopsis(synopsis):
    words = synopsis.split()
    word_limit= len(words)//2
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    else:
        return synopsis
    
