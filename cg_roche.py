import sys
import math
import numpy as np
import random
from operator import add

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
mti = {"A":0,"B":1,"C":2,"D":3,"E":4}
itm = {v:k for k,v in mti.items()}
def main():

    projects = []
    project_count = int(input())
    for i in range(project_count):
        a, b, c, d, e = [int(j) for j in input().split()]
        projects.append([a,b,c,d,e])

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
            storage = [storage_a,storage_b,storage_c,storage_d,storage_e]
            expertise_a = int(expertise_a)
            expertise_b = int(expertise_b)
            expertise_c = int(expertise_c)
            expertise_d = int(expertise_d)
            expertise_e = int(expertise_e)
            expertise = [expertise_a,expertise_b,expertise_c,expertise_d,expertise_e]
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
            cost = [cost_a,cost_b,cost_c,cost_d,cost_e]
            samples.append([sample_id,carried_by,rank,expertise_gain,health,cost])
        eprint("TURN",turn)
        [eprint(r) for r in robots]
        eprint("All samples:")
        [eprint(s) for s in samples]
        
        moves = availablemoves(robots,samples)
        eprint("available moves:")
        [eprint(m) for m in moves]
            
        if(turn == 0):
            print("GOTO SAMPLES")
            continue
        elif(turn>=2 and turn<=4):
            print("CONNECT 1")
            continue
        
        elif(turn==5):
            print("GOTO DIAGNOSIS")
            continue
        elif(turn>=8 and turn <=10):
            print("CONNECT",turn-8)
            continue
        elif(turn==11):
            print("GOTO MOLECULES")
            continue
        else:
            print(random.choice(moves))
            continue
        '''
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
        
         
        #at the start, go get samples
        if(robots[0][0] == "START_POS"):
            print("GOTO SAMPLES")
            continue
        ownedsamples = [s for s in samples if s[1]==0]
        ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
        
        if(robots[0][0] == "SAMPLES"):
            #if we dont have enough samples, collect a sample
            if(len(ownedsamples)<1):
                print("CONNECT",2)
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
                print("CONNECT",ownedsamples[0][0])
                continue
            else:
                print("GOTO MOLECULES")
                continue
                
            
        eprint("ownedsamples",ownedsamples)
        if(robots[0][0] == "MOLECULES"):
            
            
            #get differences in the sample to robot storage
            diff = np.array(ownedsamples[0][5])-np.array(robots[0][3])
            eprint("pickup diff",diff)
            #if we need some molecules, get them
            if(any(_ > 0 for _ in diff)):
                eprint("inside if(any())")
                requesting = None
                for i in range(len(diff)):
                    if(diff[i]>0):
                        eprint("i,",i)
                        eprint("diff[i]",diff[i])
                        eprint(itm[i])
                        requesting = itm[i]
                        break
                print("CONNECT",requesting)
            #if we dont, go to laboratory
            else:
                print("GOTO LABORATORY")
                continue
        if(robots[0][0] == "LABORATORY"):
            #for all owned samples, check if they are doable
            turnin = None
            for o in ownedsamples:
                eprint("sample",o)
                eprint("owned",np.array(robots[0][3]))
                diff = np.array(o[5])-np.array(robots[0][3])
                diff = list(diff)
                eprint("diff",diff)
                if(all(i<=0 for i in diff)):
                    eprint(diff)
                    turnin = o[0]
                    break
            #if we found somehting to turn in, do it
            if(turnin!=None):
                print("CONNECT",turnin)
                continue
            #If we dont have anything, move on
            elif(turnin==None):
                eprint("owned samples:",ownedsamples)
                #If we have more samples, go to molecules and finish those
                if(len(ownedsamples)>0):
                    eprint("at laboratory, going to molecules")
                    print("GOTO MOLECULES")
                    continue
                #If we dont have samples, go get more samples
                else:
                    print("GOTO SAMPLES")
                    continue

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
        totalowned = np.array(robots[0][3]) + np.array(robots[1][3])
        #If we have backpackspace, we can add molecules from those where totalowned<6
        if(sum(robots[0][3])<10):
            [moves.append("CONNECT " + str(k)) for k,v in mti.items() if totalowned[v]<6]
        
        return moves
        
    if(robots[0][0] == "LABORATORY"):
        moves.append("GOTO SAMPLES")
        moves.append("GOTO DIAGNOSIS")
        moves.append("GOTO MOLECULES")
        ownedsamples = [s for s in samples if s[1]==0 and s[4]!=-1]#owned and known
        mol = np.array(robots[0][3])
        exp = np.array(robots[0][4])
        
        for s in ownedsamples:
            cost = np.array(s[5])
            finalcost = np.maximum(cost-exp-mol,0) #is 0 for all entries if we can complete the sample
            if(all(v == 0 for v in finalcost)):
                moves.append("CONNECT " + str(s[0]))
        return moves
        
    
def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)
if(__name__) == "__main__":
    main()