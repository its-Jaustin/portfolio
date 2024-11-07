import random
import math

cF = [1, 0, 0, 0, 0, 0, 2, 1]
alter_cF = [1, 0, 0, 0, 0, 0, 2, 1]
cP_Treble = [1, 0, 0, 0, 0, 0, 7, 8]
cP_Bass = [-7, 0, 0, 0, 0, 0, -8, -7]
numberedNotes = [0, 1, 2, 3, 4, 5, 6, 7]
letterNotes = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C']
#                  0    1    2    3     4    5     6    7    8     9    10    11   12
noteNamesSharp = ('B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#')
noteNamesFlat = ('B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb')

increase = False
goodInput = False
key = None
scale = None
isSharp = True
copy_flats = [x.upper() for x in noteNamesFlat]
while goodInput == False:
    isSharp = True
    key = input('Input a Key: ').upper()
    if key not in noteNamesSharp:
        if key not in copy_flats:
            print('Not a valid key\n')
            continue
        isSharp = False
        key = noteNamesFlat[copy_flats.index(key.upper())]
    scale = input('Input a Scale: ').lower()
    if scale not in ['major', 'minor']:
        print('Not a valid key\n')
        continue
    break
# l1 = []
# l2 = []
# l3 = []
# l4 = []
# l5 = []
# l6 = []
# l7 = []
# l8 = []
# l9 = []
def cantusFirmus(cF):
    good = False
    while not good:
        good = generateCF(cF)
    #print('Cantus Firmus:\t', cF)
    n = 0
    while n < len(cF):
        if(cF[n] < 1):
            alter_cF[n] = cF[n] + 7
        else:
            alter_cF[n] = cF[n]
        n+=1
    #print('Cantus Firmus:\t',alter_cF)

def generateCF(cF):
    jump = False
    n = 1
    while n < len(cF) - 2:
        increase = bool(random.randint(0,1))

        if (jump): ##if it just did a jump, then it wont again
            jump = False
        else: ##else if it hasn't just jumped, there is a 1/3 chance it will
            jump = not (bool(random.randint(0, 2)))

        if jump:
            if increase:
                cF[n] = cF[n-1] + random.randint(2, 4)
            else:
                cF[n] = cF[n-1] + random.randint(2, 4)
        else:
            if increase:
                cF[n] = cF[n-1] + 1
            else:
                cF[n] = cF[n-1] -1
        n+=1

    if(checkDim5th(cF)):
        return False
    if(not onlyOneHighpoint(cF)):
        return False
    if(repeatingNotes(cF)):
        return False
    if(jumpTooBig(cF)):
        return False
    if(tooMany1s(cF)):
        return False
    return True
def checkDim5th(cF):
    n = 1
    while n < len(cF)-2:
        if cF[n] == 4 or cF[n] == -3:
            x = n
            direction = cF[x] < cF[x+1] ## true means increasing
            while x < len(cF)-2:
                if cF[x] < cF[x+1] == direction:
                    if(cF[x+1] == 7 or cF[x+1] == 0):
                        return True
                else:
                    break
                x+=1
        elif(cF[n] == 7 or cF[n] == 0):
            x = n
            direction = cF[x] < cF[x+1] ## true means increasing
            while x < len(cF)-2:
                if cF[x] < cF[x+1] == direction:
                    if(cF[n+1] == 4 or cF[n+1] == -3):
                        return True
                else:
                    break
                x+=1
        n+=1
    return False

def highpointIndex(cF):
    highestNum = 0
    highestIndex = 0
    n = 1
    while n < len(cF) - 1:
        if(cF[n]>=highestNum):
            highestNum = cF[n]
            highestIndex = n
        n+=1
    #print(f"Highpoint: cf[{highestIndex}] = {highestNum}")
    return highestIndex
def onlyOneHighpoint(cF):
    n =highpointIndex(cF)
    while n < len(cF)-1:
        if cF[n] < cF[n+1]:
            return False
        n+=1
    return True
def repeatingNotes(cF):
    if(cF[- 2] == cF[- 3]):
        return True
    return False
def jumpTooBig(cF):
    if(math.fabs(cF[-3] - cF[-2]) > 5):
        return True
    return False
def tooMany1s(nums):
    numOnes = sum([1 for x in nums if x == 1])
    if numOnes > 3:
        return True
    return False
def cfToNumbered(nums) -> list:
    relativeNum = 0
    multi = [0, 0, 0, 0, 0, 0, 0, 0]
    my_numbersNotes = [0, 0, 0, 0, 0, 0, 0, 0]
    tonic_index = None
    if isSharp:
        tonic_index = noteNamesSharp.index(key)
    else:
        tonic_index = noteNamesFlat.index(key)
    my_scale = []
    if scale == 'major':
                  #[1, 2, 3, 4, 5, 6,  7,  8] #cF num
        my_scale = [0, 2, 4, 5, 7, 9, 11, 12] #major scale
                  #[0, 1, 2, 3, 4, 5,  6,  7] #index
    elif scale == 'minor':
                  #[1, 2, 3, 4, 5, 6,  7,  8]
        my_scale = [0, 2, 3, 5, 7, 8, 11, 12] #harmonic minor

    for n in range(len(nums)):
        scale_num  = nums[n]
        if scale_num > 7: scale_num -= 7
        elif scale_num < 1: scale_num += 7
        my_numbersNotes[n] = (tonic_index + my_scale[scale_num-1]) % 12
    return my_numbersNotes
def keyShiftNumbers(nums):
    return

    print('Numbered notes: ', numberedNotes)

def cFToLetters(nums) -> list:
    #takes cantus firmus converts to letters
    my_nums = cfToNumbered(nums)
    my_letter_Notes = []
    for n in range(len(nums)):
        if isSharp:
            my_letter_Notes.append(noteNamesSharp[my_nums[n]])
        else:
            my_letter_Notes.append(noteNamesFlat[my_nums[n]])
    return my_letter_Notes







def printStaffC_clef(numberedNotes):
    return
    l1 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l3 = ['|', '|', '\\', '_', '_', '_', '_', '_']
    l4 = ['|', '|', '/', '_', '_', '_', '_', '_']
    l5 = ['|', '|', '_', '_', '_', '_', '_', '_']
    l6 = ['|', '|', '\\', '_', '_', '_', '_', '_']
    l7 = ['|', '|', '/', '_', '_', '_', '_', '_']
    l8 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l9 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


    staffNotes = []
    n = 0
    while n < len(cF):
        staffNotes.append(numberedNotes[n])
        n+=1
    n=0
    while n < len(cF):
        if staffNotes[n] == 9 or staffNotes[n] == 10:
            if len(letterNotes[n]) == 2:
                l1.append('_')
                l1.append('_')
                l1.append[letterNotes[n]]
                l1.append('_')
            else:
                l1.append('_')
                l1.append('_')
                l1.append[letterNotes[n]]
                l1.append('_')
                l1.append('_')
        break









    printStaff(l1, l2, l3, l4, l5, l6, l7, l8, l9)
def printStaffTrebble(numberedNotes):
    return
    l1 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l3 = ['_', '_', '_', '|', '\\', '_', '_', '_']
    l4 = ['_', '_', '_', '|', '/', '_', '_', '_']
    l5 = ['_', '_', '/', '|', '_', '_', '_', '_']
    l6 = ['_', '/', '_', '|', '\\', '_', '_', '_']
    l7 = ['_', '_', '\\', '|', '/', '_', '_', '_']
    l8 = [' ', ' ', ' ', '|', ' ', ' ', ' ', ' ']
    l9 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    n = 0
    while n < len(cF)*7:
        l1.append(' ')
        l2.append(' ')
        l3.append('_')
        l4.append('_')
        l5.append('_')
        l6.append('_')
        l7.append('_')
        l8.append(' ')
        l9.append(' ')
        n+=1
    printStaff(l1, l2, l3, l4, l5, l6, l7, l8, l9)
def printStaffBass(numberedNotes):
    return
    l1 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l3 = [' ', '_', '_',  ' ', ' ', '_', '_', '_']
    l4 = ['/', '_', '_',  '\\', '_', '.', '_', '_']
    l5 = ['_', '_', '_', '/', '_', '.', '_', '_']
    l6 = ['_', '_', '/', '_', '_', '_', '_', '_']
    l7 = ['_', '/', '_', '_', '_', '_', '_', '_']
    l8 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    l9 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    n = 0
    while n < len(cF)*7:
        l1.append(' ')
        l2.append(' ')
        l3.append('_')
        l4.append('_')
        l5.append('_')
        l6.append('_')
        l7.append('_')
        l8.append(' ')
        l9.append(' ')
        n+=1

    printStaff(l1, l2, l3, l4, l5, l6, l7, l8, l9)
def printStaff(l1, l2, l3, l4, l5, l6, l7, l8, l9):

    return
    n=0
    while n < len(cF)*7:
        print(l1[n], end='')
        n+=1
    print('')
    n=0
    while n < len(cF)*7:
        print(l2[n], end='')
        n+=1
    print('')
    n=0
    while n < len(cF)*7:
        print(l3[n], end='')
        n+=1
    print('||')
    n=0
    while n < len(cF)*7:
        print(l4[n], end='')
        n+=1
    print('||')
    n=0
    while n < len(cF)*7:
        print(l5[n], end='')
        n+=1
    print('||')
    n=0
    while n < len(cF)*7:
        print(l6[n], end='')
        n+=1
    print('||')
    n=0
    while n < len(cF)*7:
        print(l7[n], end='')
        n+=1
    print('||')
    n=0
    while n < len(cF)*7:
        print(l8[n], end='')
        n+=1
    print('')
    n=0
    while n < len(cF)*7:
        print(l9[n], end='')
        n+=1

#(1)
#(2)
#(3)___|\___ ____________________________________________________
#(4)___|/___ _____|___|__________________________________________
#(5)__/|____ _____|___|___.__#O__b.______________________________
#(6)_/_|\___ ____.___O___|___|___|_______________________________
#(7)__\|/___ ____________|___|___|_______________________________
#(8)   |
#(9)
#(1)
#(2)
#(3)||\_____ __________________________________________________
#(4)||/_____ ___|___|__________________________________________
#(5)||______ ___|___|___.__#O__b.______________________________
#(6)||\_____ __.___O___|___|___|_______________________________
#(7)||/_____ __________|___|___|_______________________________
#(8)
#(9)
#(1)
#(2)
#(3)__--____ __________________________________________________
#(4)/____\_. _____|___|__________________________________________
#(5)____/__. _____|___|___.__D#__b.______________________________
#(6)___/____ ____B___A___|__|___|_______________________________
#(7)__/_____ ____________|__|___|_______________________________
#(8)
#(9)

cantusFirmus(cF)
highpointIndex(cF)
print(key, scale, [1,2,3,4,5,6,7,8])
print(key, scale, cFToLetters([1,2,3,4,5,6,7,8]))
print('\n---- Generated Cantus Firmus ----')
print(f'Scale Degree -->\t', cF)
print(f'Notes -->\t', cFToLetters(cF))

cFToLetters(cF)
# printStaffTrebble(cF)
#printStaffC_clef(numberedNotes)
# printStaffBass(cF)

