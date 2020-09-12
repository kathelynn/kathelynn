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
        
def _numinput(limit, question):
    try:
        while True:
            try:
                test = int(input(f'{question} (1-{str(limit)}): '))
                if 0 < test < (limit+1): return test
                else: raise(ValueError)
            except EOFError as e: print(e)
            except ValueError: print('Please type 1-10')
    except KeyboardInterrupt: quit()
            
def addTitle(name):
    clear()
    try:
        print('\nRefer to the whiteboard for more details and graphs\n\nName: %s' % name)
        _pq1 = _numinput(10, '\nAudiovisual Presentation')
        _pq2 = _numinput(10, """\n⇩ Instrument/Sound\n⇩ Voice\n⇩ Tone\n⇩ Mood\n⇩ Clarity\n⇩ Appeal\nAudio Quality""")
        _pq3 = _numinput(10, """\n⇩ Hand-drawn animation\n⇩ Computer-generated imagery\n⇩ Cleanliness\n⇩ Image\n⇩ Clarity\n⇩ Appeal\nAnimation Quality""")
        _pq4 = _numinput(10, """\n⇩ Screentime\n⇩ Pacing\n⇩ Improvisation\n⇩ Clarity\n⇩ Distinction\nScriptwriting and Screenplay""")
        _pqscore = (_pq1 + _pq2 + _pq3 + _pq4) / 40 * 50
        print('\nProduction Quality score: ' + str(int(_pqscore))+'/50')
        _ei1 = _numinput(10, '\nEffort')
        _ei2 = _numinput(10,'\nInnovation')
        _eiscore = int(_ei1 + _ei2) / 20 * 10
        print('\nEffort and Innovation score: ' + str(int(_eiscore))+'/10')
        _d1 = _numinput(10, """\n⇩ Audience\n⇩ Genre\n⇩ Statement\n⇩ Distribution\n⇩ Consideration\nDigestibility""")
        _dscore = int(_d1) / 10 * 15
        print('\nDigestibility score: ' + str(int(_dscore))+'/15')
        _po1 = _numinput(10, '\nEngagement')
        _po2 = _numinput(10, '\nEnjoyment')
        _po3 = _numinput(10, '\nImpact')
        _po4 = _numinput(10, """\n⇩ Studio Placement\n⇩ Advertising\n⇩ Cast\n⇩ Distribution\nPlaying Field""")
        _poscore = int(_po1 + _po2 + _po3 + _po4) / 40 * 25
        print('\nPersonal Opinion score: ' + str(int(_poscore))+'/25')
        _avgscore = _pqscore + _eiscore  + _dscore + _poscore
        print('\nAverage score: ' + str(int(_avgscore))+'/100')
        array.append(animeTitle(name, _avgscore, [_pqscore, _pq1, _pq2, _pq3, _pq4], [_eiscore, _ei1, _ei2], _dscore, [_poscore, _po1, _po2, _po3, _po4]))
        input('\nPress Enter to continue...')
    except KeyboardInterrupt: quit()

while True:
    clear()
    try:
        print("""
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Kathy Anime Submissions                                             #
        #                                                                     #
        # To submit new anime, add ! on the first character                   #
        # Please name it in full! Levenshtein's distance can only get so far  #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        """)
        print('Animes submitted: ' + str(len(array)))
        try: print('Recent anime listed: ('+str(len(array))+') ' + array[len(array) - 1].name)
        except: pass
        searchInput = input('\nSearch: ')
        if len(searchInput) < 1: continue
        elif searchInput[0] == '!':
            clear()
            print('\nIs this correct:\n' + searchInput[1:])
            while True:
                yn = input('\ny/n: ')
                if yn is 'y':
                    addTitle(searchInput[1:])
                    break
                elif yn is 'n': break
        elif searchInput.isdigit():
            try:
                if int(searchInput) > 0:
                    print(vars(array[int(searchInput) - 1]))
                    input('\nPress Enter to continue...')
            except: pass
    except KeyboardInterrupt: quit()
