import sys
import math
import numpy as np
import random
from operator import add

#Notes:
    #If the enemy moves to laboratory, he has enough to turn in his samples

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
mti = {"A":0,"B":1,"C":2,"D":3,"E":4}
itm = {v:k for k,v in mti.items()}
def main():

    '''    
    a = [0,1,2,3,4,5]
    b = [False,True,True]
    c = b.index(True)
    print(b)
    print(a[c])
    return
    '''
    projects = []
    project_count = int(input())
    for i in range(project_count):
        a, b, c, d, e = [int(j) for j in input().split()]
        projects.append(np.array([a,b,c,d,e]))

    [eprint(p) for p in projects]
    robots = []
    # game loop
    turn = -1
    while True:
        turn+=1
        robots = []#[0:target, 1:eta, 2:score, 3:storage, 4:exp]
        for i in range(2):
            target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
            eta = int(eta)
            score = int(score)
            storage_a = int(storage_a)
            storage_b = int(storage_b)
            storage_c = int(storage_c)
            storage_d = int(storage_d)
            storage_e = int(storage_e)
            storage = np.array([storage_a,storage_b,storage_c,storage_d,storage_e])
            expertise_a = int(expertise_a)
            expertise_b = int(expertise_b)
            expertise_c = int(expertise_c)
            expertise_d = int(expertise_d)
            expertise_e = int(expertise_e)
            expertise = np.array([expertise_a,expertise_b,expertise_c,expertise_d,expertise_e])
            robots.append([target,eta,score,storage,expertise])
        #eprint(robots)
        
        available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
        sample_count = int(input())
        samples = [] #[0:id, 1:carriedby, 2:rank, 3:exp gain, 4:health,5:cost]
        for i in range(sample_count):
            sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
            sample_id = int(sample_id)
            carried_by = int(carried_by)
            rank = int(rank)
            health = int(health)
            cost_a = int(cost_a)
            cost_b = int(cost_b)
            cost_c = int(cost_c)
            cost_d = int(cost_d)
            cost_e = int(cost_e)
            cost = np.array([cost_a,cost_b,cost_c,cost_d,cost_e])
            samples.append([sample_id,carried_by,rank,expertise_gain,health,cost])
        eprint("TURN",turn)
        [eprint(r) for r in robots]
        eprint("All samples:")
        [eprint(s) for s in samples]
        
        moves = availablemoves(robots,samples)
        eprint("available moves:")
        [eprint(m) for m in moves]
        ownedsamples = [s for s in samples if s[1]==0]
        ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
        possible_turnin(robots,ownedsamples)
        if(any(possible_turnin)):
            order = getorder_turnin(robots,samples)
            print(order)
            continue
        ''' 
        if(turn == 0):
            print("GOTO SAMPLES")
            continue
        
        elif(turn>=2 and turn<=4):
            print("CONNECT 1")
            continue
        
        elif(turn==5):
            print("GOTO DIAGNOSIS")
            continue
        else:
            print(random.choice(moves))
            continue
        
        elif(turn>=8 and turn <=10):
            print("CONNECT",turn-8)
            continue
        elif(turn==11):
            print("GOTO MOLECULES")
            continue
        
        
        if(turn>=14 and turn <18):
            print("CONNECT C")
            continue
        if(turn==18):
            print("GOTO LABORATORY")
            continue
        if(turn==21):
            print("CONNECT 0")
            continue
        if(turn==22):
            print("GOTO MOLECULES")
            continue
        if(turn>=25 and turn <27):
            print("CONNECT E")
            continue
        if(turn==27):
            print("GOTO LABORATORY")
            continue
        if(turn==30):
            print("CONNECT 2")
            continue
        '''
        
        
        '''
        #at the start, go get samples
        if(robots[0][0] == "START_POS"):
            print("GOTO SAMPLES")
            continue
        ownedsamples = [s for s in samples if s[1]==0]
        ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
        
        if(robots[0][0] == "SAMPLES"):
            #if we dont have enough samples, collect a sample
            if(len(ownedsamples)<3):
                if(all([s[2]!=2 for s in samples if s[1]==0])):    
                    print("CONNECT",2)
                    continue
                else:
                    print("CONNECT",1)
                    continue
            else:
                #If we have samples, go to diagnosis
                print("GOTO DIAGNOSIS")
                continue
        #We explicitly split these groups into subgroups, but there must be an easier way
        #known_samples = [s for s in samples if s[3]!=-1]#those we own and are known
        #known_ownedsamples = [s for s in ownedsamples if s[3]!=-1]
        unknown_ownedsamples = [s for s in ownedsamples if s[4] == -1]
        if(robots[0][0] == "DIAGNOSIS"):
            #If we own samples which are unknown, identify them
            if(len(unknown_ownedsamples)>0):
                
                print("CONNECT",unknown_ownedsamples[0][0])
                continue
            else:
                print("GOTO MOLECULES")
                continue
                
            
        #eprint("ownedsamples",ownedsamples)
        if(robots[0][0] == "MOLECULES"):
            eprint("at molecules")
            #If we have something to turn in: go to laboratory:
            turnin = possible_turnin(robots,samples)
            eprint("we can turn in",turnin)
            if(turnin):
                print("GOTO LABORATORY")
                continue
            #If we do not, assemble a sample
            
            
            neededmatrix,possible = immediately_collectable(robots,ownedsamples)
            eprint("we can assemble", possible)
            #If any of these are possible, do them:
            if(any(possible)):    
                #Do the first one which is possible
                requestmol = None
                assemble_this = possible.index(True) #Returns the index of the first assemble-able
                for i,m in enumerate(neededmatrix[assemble_this]):
                    if(m>0): #fill out the molecules we need in order from A to E. Could be improved by grabbing the most critical first probably, or the ones with most overlap
                        requestmol = itm[i]
                        break
                print("CONNECT ", requestmol)
                continue
            
            #If none of them are possible, we should
            #1: turn in
            turnin = possible_turnin(robots,samples)
            if(turnin):
                print("GOTO LABORATORY")
                continue
            #2: get new samples
                
            
            
        if(robots[0][0] == "LABORATORY"):
            #for all owned samples, check if they are doable
            turnin = possible_turnin(robots,samples)
            if(turnin):
                print("CONNECT",turnin[0])
                continue
            #If we dont have anything, move on
            elif(not turnin):
                eprint("owned samples:",ownedsamples)
                #If we have samples we can finish, do those
                neededmatrix,possible = immediately_collectable(robots,ownedsamples)
                if(any(possible)):
                    eprint("at laboratory, going to molecules")
                    print("GOTO MOLECULES")
                    continue
                #If we dont have samples, go get more samples
                else:
                    print("GOTO SAMPLES")
                    continue
        '''
#input: robots and any list of samples
#Returns the list of possible sampleids we can turn in
#Accounts for discounts
#possible improvements:
#Return list of list of samples we can turn in simultaniously(accounting for future discounts.)
#(adjust to also return number of turns before this happens)
def possible_turnin(robots,samples): 
    #ownedsamples = [s for s in samples if s[1]==0]
    turnin = []   
    #for s in ownedsamples:
    for s in samples:    
        needed = np.maximum(s[5] - robots[0][3] - robots[0][4],0)
        if(all(n==0 for n in needed)):
            turnin.append(s[0])
    return turnin

#Returns
    #neededmatrix: list of numpy arrays: for each ownedsample: the number of each type needed
    #possible: list of bools: for each ownedsample: True if the molecules are able to be collected
    
#Does not account for molecules which can be stolen, or for molecules which are being returned.
#Only accounts for the current number of molecules in stock
def immediately_collectable(robots,ownedsamples):
    
    #Molecules needed for each sample
    neededmatrix = []
    for o in ownedsamples:
        needed = np.maximum(o[5] - robots[0][3] - robots[0][4],0)
        neededmatrix.append(needed)
    #neededmatrix: a row for each sample, describing what is needed
    #[eprint(n) for n in neededmatrix]
    stock = - robots[0][3] - robots[1][3] + 6 #Molecules left in stock(if there is a duplicate molecule, total will be 7, for -1 stock. special case handled)
    #eprint("stock:",stock)
    
    #Figure out which are possible to do atm:
    possible = [False]*len(neededmatrix)
    for j,n in enumerate(neededmatrix):
        if(all(stock[i] >= n[i] for i in range(len(n))) and np.sum(n)+np.sum(robots[0][3])<=10): #if there is enough in the stock and we can carry the mols, it is possible                    
            #eprint("there are enough molecules in stock for ",ownedsamples[j])
            possible[j] = True
    return neededmatrix, possible

#returns the order needed to turn in a sample
def getorder_turnin(robots,samples):
    
    
def availablemoves(robots,samples):
    moves = []
    if(robots[0][1] > 0):
        #cant do anything if we are moving
        moves.append("ETA: "+ str(robots[0][1]))
        return moves
    if(robots[0][0] == "START_POS"):
        #can only move to all other positions
        moves.append("GOTO SAMPLES")
        moves.append("GOTO DIAGNOSIS")
        moves.append("GOTO MOLECULES")
        moves.append("GOTO LABORATORY")
        return moves
        
    if(robots[0][0] == "SAMPLES"):
        #move to other locations
        moves.append("GOTO DIAGNOSIS")
        moves.append("GOTO MOLECULES")
        moves.append("GOTO LABORATORY")
        
        if(len([s for s in samples if s[1]==0]) < 3):
            moves.append("CONNECT 1")
            moves.append("CONNECT 2")
            moves.append("CONNECT 3")
        return moves
        
    if(robots[0][0] == "DIAGNOSIS"):
        moves.append("GOTO SAMPLES")
        moves.append("GOTO MOLECULES")
        moves.append("GOTO LABORATORY")
        
        #Add 'identify' for all unknown samples we own
        #Add 'discard' for all known samples we own
        [moves.append("CONNECT " + str(s[0])) for s in samples if s[1] == 0]
        
        #Add 'get from cloud' to all samples in the cloud, if we have space
        if(len([s for s in samples if s[1]==0]) < 3):
            [moves.append("CONNECT " + str(s[0])) for s in samples if s[1] == -1]
        return moves
        
    if(robots[0][0] == "MOLECULES"):
        moves.append("GOTO SAMPLES")
        moves.append("GOTO DIAGNOSIS")
        moves.append("GOTO LABORATORY")
        #Total unavailable molecules
        totalowned = robots[0][3] + robots[1][3]
        #If we have backpackspace, we can add molecules from those where totalowned<6
        if(sum(robots[0][3])<10):
            [moves.append("CONNECT " + str(k)) for k,v in mti.items() if totalowned[v]<6]
        
        return moves
        
    if(robots[0][0] == "LABORATORY"):
        moves.append("GOTO SAMPLES")
        moves.append("GOTO DIAGNOSIS")
        moves.append("GOTO MOLECULES")
        ownedsamples = [s for s in samples if s[1]==0 and s[4]!=-1]#owned and known
        mol = robots[0][3]
        exp = robots[0][4]
        
        for s in ownedsamples:
            cost = s[5]
            finalcost = np.maximum(cost-exp-mol,0) #is 0 for all entries if we can complete the sample
            if(all(v == 0 for v in finalcost)):
                moves.append("CONNECT " + str(s[0]))
        return moves
        
    
def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)
if(__name__) == "__main__":
    main()