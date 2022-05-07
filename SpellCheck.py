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

def spellCheck(inputText, knownList, key):
    score = wordScore(inputText)
    min = 9999999 #an extremely high value to intialize min
    for candidate in list:
        sim = np.dot(score - wordScore(key), score - wordScore(key)) #the square of the length between the inputText and candidate word
        if sim < min:
            answer = candidate
            min = sim
    return str(answer)