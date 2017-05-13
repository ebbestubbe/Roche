import sys
import math
import numpy as np

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
def main():
    mti = {"A":0,"B":1,"C":2,"D":3,"E":4}
    itm = {v:k for k,v in mti.items()}
    eprint(itm)
    project_count = int(input())
    for i in range(project_count):
        a, b, c, d, e = [int(j) for j in input().split()]
    
    robots = []
    # game loop
    turn = -1
    while True:
        turn+=1
        robots = []
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
        [eprint(r) for r in robots]
        available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
        sample_count = int(input())
        samples = []
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
            samples.append([sample_id,carried_by,rank,health,cost])
        [eprint(s) for s in samples]
        
         
        #at the start, go get samples
        if(robots[0][0] == "START_POS"):
            print("GOTO DIAGNOSIS")
            continue
        ownedsamples = [s for s in samples if s[1]==0]
        ownedsamples.sort(key = lambda x: x[3]/sum(x[4]),reverse=True)

        if(robots[0][0] == "DIAGNOSIS"):
            #if we dont have enough samples, collect the ones with most value/molecule
            if(len(ownedsamples)<3):
                available = [s for s in samples if s[1] == -1]
                
                available.sort(key = lambda x: x[3]/sum(x[4]),reverse=True)
                [eprint(a) for a in available]
                print("CONNECT" ,available[0][0])
                continue
            else:
                eprint("at diagnosis, going to molecules")
                print("GOTO MOLECULES")
                continue
        eprint("ownedsamples",ownedsamples)
        if(robots[0][0] == "MOLECULES"):
            
            
            #get differences in the sample to robot storage
            diff = np.array(ownedsamples[0][4])-np.array(robots[0][3])
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
                diff = np.array(o[4])-np.array(robots[0][3])
                diff = list(diff)
                eprint("diff",diff)
                if(all(i<=0 for i in diff)):
                    eprint(diff)
                    turnin = o[0]
                    break
            if(turnin!=None):
                print("CONNECT",turnin)
                continue
            elif(turnin==None):
                eprint("owned samples:",ownedsamples)
                if(len(ownedsamples)>0):
                    eprint("at laboratory, going to molecules")
                    print("GOTO MOLECULES")
                    continue
                else:
                    print("GOTO DIAGNOSIS")
                    continue
def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)
if(__name__) == "__main__":
    main()