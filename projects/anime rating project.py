import threading as th
import os
array = []
clear = lambda: os.system('clear')

class animeTitle:
    def __init__(self, name, avgscore, pqscore, eiscore, dscore, poscore):
        self.name = name
        self.avgscore = avgscore
        self.pqscore = pqscore
        self.eiscore = eiscore
        self.dscore = dscore
        self.poscore = poscore
        
def _numinput(limit, question):
    while True:
        global debugMode
        global cancelAdd
        if debugMode:
            return 10
        elif cancelAdd:
            return -1
        try:
            test = int(input(f'{question} (1-{str(limit)}): '))
            if test == 'debug':
                debugMode = True
                return 10
            if 0 < test < (limit+1):
                return test
            else:
                raise(ValueError)
        except KeyboardInterrupt:
            cancelAdd = True
            return -1
        except EOFError as e:
            print(e)
        except ValueError:
            print('Please type 1-10')
            
def addTitle(name):
    clear()
    global debugMode
    global cancelAdd
    debugMode = False
    cancelAdd = False
    print('\nRefer to the whiteboard for more details and graphs')
    print('\nName: %s' % name)
    print()
    _pq1 = _numinput(10, '\nAudiovisual Presentation')
    _pq2 = _numinput(10, """
⇩ Instrument/Sound
⇩ Voice
⇩ Tone
⇩ Mood
⇩ Clarity
⇩ Appeal
Audio Quality""")
    _pq3 = _numinput(10, """
⇩ Hand-drawn animation
⇩ Computer-generated imagery
⇩ Cleanliness
⇩ Image
⇩ Clarity
⇩ Appeal
Animation Quality""")
    _pq4 = _numinput(10, """
⇩ Screentime
⇩ Pacing
⇩ Improvisation
⇩ Clarity
⇩ Distinction
Scriptwriting and Screenplay""")
    print(int(_pq1 + _pq2 + _pq3 + _pq4))
    _pqscore = (_pq1 + _pq2 + _pq3 + _pq4) / 40 * 50
    print('\nProduction Quality score: ' + str(int(_pqscore))+'/50')
    _ei1 = _numinput(10, '\nEffort')
    _ei2 = _numinput(10,'\nInnovation')
    _eiscore = int(_ei1 + _ei2) / 20 * 10
    print('\nEffort and Innovation score: ' + str(int(_eiscore))+'/10')
    _d1 = _numinput(10, """
⇩ Audience
⇩ Genre
⇩ Statement
⇩ Distribution
⇩ Consideration
Digestibility""")
    _dscore = int(_d1) / 10 * 15
    print('\nDigestibility score: ' + str(int(_dscore))+'/15')
    _po1 = _numinput(10, '\nEngagement')
    _po2 = _numinput(10, '\nEnjoyment')
    _po3 = _numinput(10, '\nImpact')
    _po4 = _numinput(10, """
⇩ Studio Placement
⇩ Advertising
⇩ Cast
⇩ Distribution
Playing Field""")
    _poscore = int(_po1 + _po2 + _po3 + _po4) / 40 * 25
    print('\nPersonal Opinion score: ' + str(int(_poscore))+'/25')
    _avgscore = _pqscore + _eiscore  + _dscore + _poscore
    print('\nAverage score: ' + str(int(_avgscore))+'/100')
    if cancelAdd == False:
        array.append(animeTitle(name, _avgscore, [_pqscore, _pq1, _pq2, _pq3, _pq4], 
                                [_eiscore, _ei1, _ei2], _dscore, [_poscore, _po1, _po2, _po3, _po4]))
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
    print('Animes submitted: ' + str(len(array))) ## This will try to print recently added anime if it exists. Will clean up this code later.
    try:
        print('Recent anime listed: ('+str(len(array))+') ' + array[len(array) - 1].name)
    except IndexError: 
        pass
    searchInput = input('\nSearch: ') ## Grab input
    if len(searchInput) < 1: ## If there is nothing for input, reset
        continue
    elif searchInput.isdigit(): ## If input is a digit, print based on array position
        try:
            if int(searchInput) > 0:
                print(int(searchInput) - 1)
                print(vars(array[int(searchInput) - 1]))
                input('\nPress Enter to continue...')
                continue
        except IndexError:
            print('\nList index out of range')
            input('Press Enter to continue...')
        #except Exception as e:
            #print(e)
            #input()
    elif searchInput[0] == '!': ## If input has ! prefix, initiate adding title
        clear()
        print('\nIs this name case-sensitive and has no mispelling:\n'
            + searchInput[1:])
        while True:
            _yesorno = input('\ny/n: ')
            if _yesorno is 'y':
                addTitle(searchInput[1:])
                break
            elif _yesorno is 'n':
                break
            else:
                pass

    else:
        continue
