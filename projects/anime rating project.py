# as far as i know, people use keyboard interrupt to terminate their programs, so i have implemented that, its easy to remove if you wish

import os
array = []
clear = lambda: os.system('clear') # if on windows change the command to "cls" instead of "clear"

class animeTitle:
    def __init__(self, name, avgscore, pqscore, eiscore, dscore, poscore):
        self.name = name
        self.avgscore = avgscore
        self.pqscore = pqscore
        self.eiscore = eiscore
        self.dscore = dscore
        self.poscore = poscore
        
def numinput(limit, question):
    while True:
        try:
            num = int(input(f'{question} (1-{str(limit)}): '))
            if 0 < num < (limit+1): return num
            else: raise(ValueError)
        except ValueError: print('Please type 1-10')
            
def addTitle(name):
    clear()
    fs = lambda f: str(int(f)) # float to string

    print(f'\nRefer to the whiteboard for more details and graphs\n\nName: {name}')
    pq1 = numinput(10, '\nAudiovisual Presentation')
    pq2 = numinput(10, '\n⇩ Instrument/Sound\n⇩ Voice\n⇩ Tone\n⇩ Mood\n⇩ Clarity\n⇩ Appeal\nAudio Quality')
    pq3 = numinput(10, '\n⇩ Hand-drawn animation\n⇩ Computer-generated imagery\n⇩ Cleanliness\n⇩ Image\n⇩ Clarity\n⇩ Appeal\nAnimation Quality')
    pq4 = numinput(10, '\n⇩ Screentime\n⇩ Pacing\n⇩ Improvisation\n⇩ Clarity\n⇩ Distinction\nScriptwriting and Screenplay')
    pqscore = (pq1 + pq2 + pq3 + pq4) / 40 * 50
    print(f'\nProduction Quality score: {fs(pqscore)}/50')
    ei1 = numinput(10, '\nEffort')
    ei2 = numinput(10,'\nInnovation')
    eiscore = int(ei1 + ei2) / 20 * 10
    print(f'\nEffort and Innovation score: {fs(eiscore)}/10')
    d1 = numinput(10, '\n⇩ Audience\n⇩ Genre\n⇩ Statement\n⇩ Distribution\n⇩ Consideration\nDigestibility')
    dscore = int(d1) / 10 * 15
    print(f'\nDigestibility score: {fs(dscore)}/15')
    po1 = numinput(10, '\nEngagement')
    po2 = numinput(10, '\nEnjoyment')
    po3 = numinput(10, '\nImpact')
    po4 = numinput(10, '\n⇩ Studio Placement\n⇩ Advertising\n⇩ Cast\n⇩ Distribution\nPlaying Field')
    poscore = int(po1 + po2 + po3 + po4) / 40 * 25

    print(f'\nPersonal Opinion score: {fs(poscore)}/25')
    avgscore = pqscore + eiscore  + dscore + poscore
    print(f'\nAverage score: {fs(avgscore)}/100')
    array.append(animeTitle(name, avgscore, [pqscore, pq1, pq2, pq3, pq4], [eiscore, ei1, ei2], dscore, [poscore, po1, po2, po3, po4]))
    input('\nPress Enter to continue...')

while True:
    clear()

    print("""
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Kathy Anime Submissions                                             #
    #                                                                     #
    # To submit new anime, add ! on the first character                   #
    # Please name it in full! Levenshtein's distance can only get so far  #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    """)

    print(f'Animes submitted: {(len(array))}')
    try: print('Recent anime listed: ({}) {}'.format(len(array), array[len(array) - 1].name))
    except: pass
    searchInput = input('\nSearch: ')
    if len(searchInput) < 1: continue
    elif searchInput[0] == '!':
        searchInput = searchInput[1:]
        clear()
        print(f'\nIs this correct:\n {searchInput}')
        while True:
            yn = input('\ny/n: ')
            if yn is 'y':
                addTitle(searchInput)
                break
            elif yn is 'n': break
    elif searchInput.isdigit():
        try:
            if int(searchInput) > 0:
                print(vars(array[int(searchInput) - 1]))
                input('\nPress Enter to continue...')
        except: pass