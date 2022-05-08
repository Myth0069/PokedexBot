import numpy as np

characters = 'abcdefghijklmnopqrstuvwxyz 0123456789'

def wordScore(inputText): #defines a score for a word, stored in a numpy array
    inputText = inputText.lower()
    score = np.zeros(len(characters))
    step = 0
    for letter in inputText:
        index = 0
        for symbol in characters:
            if symbol == letter:
                score[index] += np.absolute(step - ((len(inputText)-1)/2))/len(inputText) + np.absolute(step - (2/(len(inputText)-1)))/len(inputText) #this adjusts score based on letter placement
            index += 1
        step += 1
    return score

def spellCheck(inputText, knownDict):
    score = wordScore(inputText)
    bestScore = 9999999 #an extremely high value to intialize min
    for word in knownDict:
        #Looks at the entries for each word, then lookas the the wordScore for that word and compares it inputText
        try:
            currentScore = np.dot(score - knownDict[word]['wordScore'], score - knownDict[word]['wordScore']) #the square of the length between the inputText and candidate word
        except: #This runs in the event that the wordscore for the dictionary wasn't pre-generated
            knownDict['wordScore'] = wordScore(str(word))
            currentScore = np.dot(score - knownDict[word]['wordScore'], score - knownDict[word]['wordScore'])
        if currentScore < bestScore:
            closestMacth = word
            bestScore = currentScore
    return str(closestMacth)