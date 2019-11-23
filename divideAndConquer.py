from random import randint
import math
import time

def f(x0,x1,x2): #This is my function depending on x0 x1 and x2
    if x0 == 0 and x1 == 0 and x2 == 0:
        return 0
    elif x0 == 0 and x1 == 0 and x2 == 1:
        return 1
    elif x0 == 0 and x1 == 1 and x2 == 0:
        return 0
    elif x0 == 0 and x1 == 1 and x2 == 1:
        return 0
    elif x0 == 1 and x1 == 0 and x2 == 0:
        return 1
    elif x0 == 1  and x1 == 0 and x2 == 1:
        return 1
    elif x0 == 1 and x1 == 1  and x2 == 0:
        return 1
    else:
        return 0

def divide_and_conquer():
    start = time. time()
    output = [0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,0,0,1,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,1,0,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1,1,1,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,0,1,1,0,1,0,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,1,1,1,0,0,1,0,1,0,1,1,1,0,0,1,0,0,1,0]
    lfsrList = [LFSR((0,1,4,7)) , LFSR((0,1,7,11)) , LFSR((0,2,3,5))]
    
    states = [[], [], []] #It will be the state for lfsr1, lfsr2,lfsr3
    
    states[0] = lfsrList[0].BestCorrLfsr(0.75,output) #Firslty, we try to find a key with a value near to 0.75
    states[1] = lfsrList[1].BestCorrLfsr(0.25,output) #Secondly, we try to find a key with a value near to 0.25

    #From here, I do a brute force to find the last key2 
    for i in range (int(math.pow(2,16))): #2 power 16 becausewe have 2^16 combination possible
        states[2] = [int(n) for n in "{0:b}".format(i).zfill(16)] 
        
        lfsrList[0].setState(states[0]) #Here we update each lfsr due to shift
        lfsrList[1].setState(states[1])
        lfsrList[2].setState(states[2])

        myOutput = [] 
        for i in range(200):#We "execute" each lfsr to find the corresponding output. Thus, we have our key2
            x0 = lfsrList[0].shift()
            x1 = lfsrList[1].shift()
            x2 = lfsrList[2].shift()
            myOutput.append(f(x0, x1, x2)) #We calculate the ouptut using the f function

        """for i in range(35):#The same with 35 bits is enough
            x0 = lfsrList[0].shift()
            x1 = lfsrList[1].shift()
            x2 = lfsrList[2].shift()
            myOutput.append(f(x0, x1, x2)) 
        output = output[:35]"""



        if myOutput == output:
            #print myOutput
            print ("key 0: ")
            print states[0]
            print ("\nkey 1: ")
            print states[1]
            print ("\nkey 2: ")
            print states[2]

    end = time. time() #I calculate the lapsed time ...
    print("Time elapsed: ")
    print end - start # ... And print it

class LFSR(object):
    def __init__(self, taps):
        self.taps = taps
        self.state = []

    def BestCorrLfsr(self,percent, output): #Calculate the best correlation (Depend if it is 0.75 or 0.25)
        bestCorr = 0 #We start with a correlation of 0
        bestSeq = [] #Empty temporary sequence
        for i in range (int(math.pow(2,16))):
            
            generatedBin = [int(n) for n in "{0:b}".format(i).zfill(16)] 
            corr = 0
            self.setState(generatedBin) #We set the state of this lfsr to use it with shift
            sequence = [None]*200
            for k in range(200): #We generate the sequence from this (possible initial) state
                sequence[k] = self.shift() 

            for i in range(200):
                if str(sequence[i])==str(output[i]): #We compare each bits
                    corr +=1
            corr = corr*1.0/200

            if self.compareMostNear(bestCorr,corr,percent): #In this part we store the best sequence and the best correlation (to compare again)
                bestSeq = generatedBin
                bestCorr = corr
        return bestSeq

    def setState(self, state):
        self.state = state

    def shift(self): #This function allows to "execute" a lfsr
        out = self.state[0] #The output of our lfsr
        In = 0 # Our input in our lfsr
        for t in self.taps: #We application xor operation on the corresponding taps
            In = In^self.state[t]
        self.state = self.state[1:] #New state is equal to the previous list( minus the first)
        self.state.append(In) # And we add the ne one (which is the first one xored with taps)
        return out

    def compareMostNear(self,a,b,x):
        if abs(a-x) < abs(b-x):
            return False #a is more near to x than b
        else:
            return True

divide_and_conquer() 
         

