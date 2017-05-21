import sys
import numpy as np
from collections import Counter
import itertools
#Notes:
    #If the enemy moves to laboratory, he has enough to turn in his samples

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
mti = {"A":0,"B":1,"C":2,"D":3,"E":4}
itm = {v:k for k,v in mti.items()}
dist_mat = np.array([[1000,2,2,2,2],[1000,0,3,3,3],[1000,3,0,3,4],[1000,3,3,0,3],[1000,3,4,3,0]])
pos_dict = {"START_POS": 0,"SAMPLES":1,"DIAGNOSIS":2,"MOLECULES":3,"LABORATORY":4}

def main():
    
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
        samples = [] #[0:id, 1:carriedby, 2:rank, 3:exp gain, 4:health,5:cost,6:needed for robot1,7:needed for robot2,8:timetofinish1, 9:timetofinish2]
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
            needed1 = np.maximum(cost - robots[0][3] - robots[0][4],0)
            needed2 = np.maximum(cost - robots[1][3] - robots[1][4],0)
            timetofinish1 = np.sum(needed1) + getdist(robots[0][0],'MOLECULES') + robots[0][1]
            timetofinish2 = np.sum(needed2) + getdist(robots[1][0],'MOLECULES') + robots[1][1]
            #eprint(expertise_gain)
            samples.append([sample_id,carried_by,rank,expertise_gain,health,cost,needed1,needed2,timetofinish1,timetofinish2])

        eprint("TURN",turn)
        [eprint(r) for r in robots]
        eprint("All samples:")
        [eprint(s) for s in samples]        
        #moves = availablemoves(robots,samples)
        #eprint("available moves:")
        #[eprint(m) for m in moves]
        #order = naivegreedystrategy(robots,samples)
        order = sequencestrategy(projects,robots,samples)
        print(order)
        continue

def sequencestrategy(projects,robots,samples):
    ownedsamples = [s for s in samples if s[1]==0]
    ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    ownedunknownsamples = [s for s in ownedsamples if s[4]==-1]
    
    cloudsamples = [s for s in samples if s[1]==-1]
    cloudsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    enemysamples = [s for s in samples if s[1]==1]
    enemysamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    turnin = possible_turnin(robots,samples,ownedsamples)
    ownedknownsamples = [s for s in ownedsamples if s[4]!=-1]

    #eprint("STARTING LOGIC")
    #if(len(ownedknownsamples)>0):
    #    seq_info = try_all_sequences(projects,robots,samples,ownedknownsamples)
    #    [eprint(seq) for seq in seq_info]
    if(robots[0][0] == 'LABORATORY'):
        if(turnin):
            seq_info = try_all_sequences(projects,robots,samples,ownedknownsamples)
            seq_info.sort(key= lambda x: (-x[3],sum(x[1])))
            
            to_turnin_ind = [s[0] for s in seq_info].index(True)
            order = "CONNECT " + str(seq_info[to_turnin_ind][6][0][0])
            return(order)
        elif(len(ownedsamples)<2):
            order = "GOTO SAMPLES"
            return(order)
    if(robots[0][0] == 'DIAGNOSIS' and len(ownedunknownsamples)>0):
        #eprint("unknown:",ownedunknownsamples)
        order = getorder_diagnoseall(robots,samples)
        return(order)
    if(robots[0][0] == "SAMPLES"):
        if(len(ownedsamples)==3 and len(ownedunknownsamples)>0):
            order = getorder_diagnoseall(robots,samples)
            return(order)
        if(len(ownedsamples)<3):
            order = getorder_newsamples_conservative(robots,samples)
            return(order)
    #eprint("SEQ INFO LOGIC")
    if(len(ownedknownsamples)>0):
        seq_info = try_all_sequences(projects,robots,samples,ownedknownsamples)
        #[eprint(seq) for seq in seq_info]
        #eprint("seq info:")
        #[eprint(s) for s in seq_info]
        if(any([s[0] for s in seq_info])):
            #eprint("SOME OF THEM ARE POSSIBLE")
            if(robots[0][0] != "MOLECULES"):
                order = "GOTO MOLECULES"
                return(order)
            if(robots[0][0] == "MOLECULES" and np.sum(robots[0][3])<10):
                seq_info.sort(key= lambda x: (-x[3],x[5]))
                #eprint("sorted seq info:")
                #[eprint(s) for s in seq_info]
                to_assemble_ind = [s[0] for s in seq_info].index(True)
                
                eprint("to_assemble",seq_info[to_assemble_ind])
                #priority = seq_info[to_assemble_ind].argsort()[::-1]
                priority = seq_info[to_assemble_ind][2].argsort()[::-1]

                #eprint("priority",priority)
                order = getorder_getmolecule_bypriority(robots,samples,priority)   
                #eprint(order)
                return(order)
        else:
            if(robots[0][0] == "MOLECULES" and np.sum(robots[0][3])<10):
                #eprint("none of them are possible")
                seq_info.sort(key= lambda x: (-x[3],x[5]))
                #eprint("sorted seq info:")
                #[eprint(s) for s in seq_info]

                #priority = seq_info[to_assemble_ind].argsort()[::-1]
                priority = seq_info[0][2].argsort()[::-1]

                #eprint("priority",priority)
                order = getorder_getmolecule_bypriority(robots,samples,priority)   
                #eprint(order)
                return(order)
    #eprint("AFTER SEQ LOGIC")   

    if(turnin):
        eprint(turnin)
        order = getorder_turnin(robots,turnin[0])
        return(order)

    '''
    neededmatrix,possible_assemble_cloud = immediately_collectable(robots,samples,cloudsamples)
    if(any(possible_assemble_cloud)):
        if(robots[0][0] != "DIAGNOSIS"):
            order = "GOTO DIAGNOSIS"
            return(order)
        #first discard
        if(len(ownedsamples)==3):
            order = "CONNECT " + str(ownedsamples[-1][0])
            return(order)
        else:
            to_pickup = cloudsamples[possible_assemble_cloud.index(True)]
            order = "CONNECT " + str(to_pickup[0])
            return(order)
    '''
    if(robots[0][0] == "DIAGNOSIS"):
        if(len(ownedsamples)>0):
            order = "CONNECT " + str(ownedsamples[-1][0]) #dump worst sample
            return(order)
        else:
            order = "GOTO SAMPLES"
            return(order)

    if(len(ownedsamples)<3):
        order = getorder_newsamples_conservative(robots,samples)
        return(order)
    else:
        order = "GOTO DIAGNOSIS"
        return(order)

#stockupstrategy:
#Turn in anything
#Stock up on samples
#Assemble samples and block enemy
#Discard worst samples
#Get new samples

#Does not account for multiple turn ins
#Does not account for expertise
#Does not account for science projects 
def stockupstrategy(robots,samples):
    ownedsamples = [s for s in samples if s[1]==0]
    ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    ownedunknownsamples = [s for s in ownedsamples if s[4]==-1]
    
    cloudsamples = [s for s in samples if s[1]==-1]
    cloudsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    enemysamples = [s for s in samples if s[1]==1]
    enemysamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    turnin = possible_turnin(robots,samples,ownedsamples)
    ownedknownsamples = [s for s in ownedsamples if s[4]!=-1]


    
    if(robots[0][0] == 'LABORATORY' and turnin):
        eprint(turnin)
        order = getorder_turnin(robots,turnin[0])
        return(order)
    if(robots[0][0] == 'DIAGNOSIS' and len(ownedunknownsamples)>0):
        #eprint("unknown:",ownedunknownsamples)
        order = getorder_diagnoseall(robots,samples)
        return(order)
    if(robots[0][0] == "SAMPLES"):
        if(len(ownedsamples)==3 and len(ownedunknownsamples)>0):
            order = getorder_diagnoseall(robots,samples)
            return(order)
        if(len(ownedsamples)<3):
            order = getorder_newsamples(robots,samples)
            return(order)
    neededmatrix, possible_assemble_owned = immediately_collectable(robots,samples,ownedsamples)
    if(any(possible_assemble_owned) and robots[0][0] != "MOLECULES" and np.sum(robots[0][3])<10):
        eprint("We are going to molecules")
        order = "GOTO MOLECULES"
        return(order)
    if(robots[0][0] == "MOLECULES" and np.sum(robots[0][3])<10):
        order = getorder_stockup(robots,samples)
        return order
    if(turnin):
        eprint(turnin)
        order = getorder_turnin(robots,turnin[0])
        return(order)
        
    
    neededmatrix,possible_assemble_cloud = immediately_collectable(robots,samples,cloudsamples)
    if(any(possible_assemble_cloud)):
        if(robots[0][0] != "DIAGNOSIS"):
            order = "GOTO DIAGNOSIS"
            return(order)
        #first discard
        if(len(ownedsamples)==3):
            order = "CONNECT " + str(ownedsamples[-1][0])
            return(order)
        else:
            to_pickup = cloudsamples[possible_assemble_cloud.index(True)]
            order = "CONNECT " + str(to_pickup[0])
            return(order)
    if(robots[0][0] == "DIAGNOSIS"):
        if(len(ownedsamples)>0):
            order = "CONNECT " + str(ownedsamples[-1][0]) #dump worst sample
            return(order)
        else:
            order = "GOTO SAMPLES"
            return(order)
        
    if(len(ownedsamples)<3):
        order = getorder_newsamples(robots,samples)
        return(order)

#naivegreedystrategy:
#Turn in anything
#Stock up on samples
#Assemble samples if the molecules are available right now
#Get samples from cloud we can assemble right now
#Discard worst samples
#Get new samples

#Does not block enemy
#Does not account for multiple turn ins
#Does not account for expertise
#Does not account for science projects
def naivegreedystrategy(robots,samples):
    ownedsamples = [s for s in samples if s[1]==0]
    ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    ownedunknownsamples = [s for s in ownedsamples if s[4]==-1]
    
    cloudsamples = [s for s in samples if s[1]==-1]
    cloudsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    
    turnin = possible_turnin(robots,samples,ownedsamples)
    
    #If we can turn anything in, turn in the first possible one
    if(turnin):
        eprint(turnin)
        order = getorder_turnin(robots,turnin[0])
        return(order)
    if(robots[0][0] == 'DIAGNOSIS' and len(ownedunknownsamples)>0):
        #eprint("unknown:",ownedunknownsamples)
        order = getorder_diagnoseall(robots,samples)
        return(order)
    if(robots[0][0] == "SAMPLES"):
        if(len(ownedsamples)==3 and len(ownedunknownsamples)>0):
            order = getorder_diagnoseall(robots,samples)
            return(order)
        if(len(ownedsamples)<3):
            order = getorder_newsamples(robots,samples)
            return(order)
    #If we can assemble a sample we own, do it
    neededmatrix, possible_assemble_owned = immediately_collectable(robots,samples,ownedsamples)
    if(any(possible_assemble_owned)):
        to_assemble = ownedsamples[possible_assemble_owned.index(True)]
        order = getorder_assemble(robots,samples,to_assemble)
        return(order)
    neededmatrix,possible_assemble_cloud = immediately_collectable(robots,samples,cloudsamples)
    if(any(possible_assemble_cloud)):
        if(robots[0][0] != "DIAGNOSIS"):
            order = "GOTO DIAGNOSIS"
            return(order)
        #first discard
        if(len(ownedsamples)==3):
            order = "CONNECT " + str(ownedsamples[-1][0])
            return(order)
        else:
            to_pickup = cloudsamples[possible_assemble_cloud.index(True)]
            order = "CONNECT " + str(to_pickup[0])
            return(order)
    eprint("nothing worth assembling")
    #if we have undiagnosed samples, diagnose them
    #getorder_diagnosenew(robots,samples)
    
    #If neither of these work, discard diagnose new samples
    #order = getorder_diagnosenew(robots,samples)
    
    if(robots[0][0] == "DIAGNOSIS"):
        if(len(ownedsamples)>0):
            order = "CONNECT " + str(ownedsamples[-1][0]) #dump worst sample
            return(order)
        else:
            order = "GOTO SAMPLES"
            return(order)
        
    if(len(ownedsamples)<3):
        order = getorder_newsamples(robots,samples)
        return(order)
        
'''
#input: robots and samples. to_assemble: The sample to assemble
#Returns the molecule to get, which has the most molecules in common with the other molecules
def getorder_assembleown_mostoverlap(robots,samples,to_assemble):
    ownedsamples = [s for s in samples if s[1] == 0]
    ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    othersamples = ownedsamples.copy()
    othersamples.remove(to_assemble)
    eprint("ownedsamples",ownedsamples)
    eprint("othersamples",othersamples)
    
    needed = np.maximum(to_assemble[5] - robots[0][3] - robots[0][4],0)

    #If any of these are possible, do them:
    #Do the first one which is possible
    requestmol = None
    for i,n in enumerate(needed):
         #fill out the molecules we need in order from A to E. Could be improved by grabbing the most critical first probably, or the ones with most overlap
         if(n>0):
             requestmol = itm[i]
             break
    order = "CONNECT " + str(requestmol)
    
    eprint("")
    return 
'''        
#input: robots and samples. candidate_samples are the samples we wish to check for
#Returns the list of possible sampleids we can turn in
#Accounts for discounts
#possible improvements:
#Return list of list of samples we can turn in simultaniously(accounting for future discounts.)
#(adjust to also return number of turns before this happens)
def possible_turnin(robots,samples,candidate_samples): 
    diagnosed = [s for s in candidate_samples if s[4]!=-1]

    turnin = []   
    for s in diagnosed:
        if(all(n==0 for n in s[6])):
            turnin.append(s)
    
    return turnin

#needs: robots, samples, a list of samples to search in
#robots and samples: are always given, to make it possible to do more finely tuned decision making
#candidate_samples: the list of samples we would like to know if we can collect immediately
#Returns
    #neededmatrix: list of numpy arrays: for each ownedsample: the number of each type needed
    #possible: list of bools: for each ownedsample: True if the molecules are able to be collected
    
#Does not account for molecules which can be stolen, or for molecules which are being returned.
#Only accounts for the current number of molecules in stock
def immediately_collectable(robots,samples,candidate_samples):
    #diagnosed = [s for s in candidate_samples if s[4] !=-1]
    #Molecules needed for each sample
    neededmatrix = []
    for o in candidate_samples:
        neededmatrix.append(o[6])
    #neededmatrix: a row for each sample, describing what is needed
    #[eprint(n) for n in neededmatrix]
    stock = getstock(robots)
    
    #eprint("stock:",stock)
    
    #Figure out which are possible to do atm:
    possible = [False]*len(neededmatrix)
    for j,n in enumerate(neededmatrix):
        if(all(stock[i] >= n[i] for i in range(len(n))) and np.sum(n)+np.sum(robots[0][3])<=10 and candidate_samples[j][4]!=-1): #if there is enough in the stock and we can carry the mols, it is possible                    
            #eprint("there are enough molecules in stock for ",ownedsamples[j])
            possible[j] = True
            
    return neededmatrix, possible

#For a list of blocksamples, figure out which of these we can block.
#If the enemy wants to pick up molecules for the sample, the category which there are fewest if after potential pickup, are the ones we can block.
#returns: 
    #priority: list for each sample, the ordered priority of what molecules to block.
    #remainder: list for each sample, the needed amount of molecules to block
    #possible_block: bool for each sample, if it is possible to block it in time, assuming enemy goes straight for it.
'''
def blockable(robots,samples,enemysamples):
    stock = getstock(robots)
    eprint("stock:",stock)
    priorities = []
    remainders = []
    possible_blocks = []
    for i in range(len(enemysamples)):
        remainder = stock-enemysamples[i][7]
        eprint("sample",enemysamples[i])
        eprint("remainder before nan",remainder)
        for j in range(len(remainder)):
            if(enemysamples[i][7][j] == 0):
                remainder[j] = np.nan
        eprint("remainder after nan",remainder)
        priority = np.argsort(remainder)
        eprint("priority",priority)
        turns_to_block = remainder[priority[0]] + dist(robots[1][0],"MOLECULES") + robots[1][1] #After this many turns, the last molecule has been picked up.
        turns_available = 
        priorities.append(priority)
        remainders.append(possible_blocks)
'''     
#returns the order needed to turn in a sample
def getorder_turnin(robots,sample):
    if(robots[0][0] != "LABORATORY"):
        order = "GOTO LABORATORY"
    else:
        order = "CONNECT " + str(sample[0])
    return order        
            
def getorder_assemble(robots,samples,to_assemble):
    
    if(robots[0][0] != "MOLECULES"):
        order = "GOTO MOLECULES"
    
    else:
        #eprint("we can assemble", to_assemble)

        #If any of these are possible, do them:
        #Do the first one which is possible
        requestmol = None
        for i,n in enumerate(to_assemble[6]):
             #fill out the molecules we need in order from A to E. Could be improved by grabbing the most critical first probably, or the ones with most overlap
             if(n>0):
                 requestmol = itm[i]
                 break
        order = "CONNECT " + str(requestmol)
    return order

#Assumes we are at molecules, gives order to stock up on the right molecules
def getorder_stockup(robots,samples):
    eprint("STOCKING UP")
    #Go through the storage(unused molecules) and samples, to determine which are already able to be assembled
    unused_mol = np.copy(robots[0][3])#The cargo we can use to solve samples
    
    
    ownedsamples = [s for s in samples if s[1] == 0]
    #eprint("ownedsamples:")
    [eprint(s) for s in ownedsamples]
    can_turnin = [False]*len(ownedsamples)
    #eprint("TURN IN")
    for i,s in enumerate(ownedsamples):
        needed = np.maximum(s[5]-robots[0][4],0)
        #eprint("sample",s)
        #eprint("needed",needed)
        if(s[4] == -1):
            continue
        if(all(needed<=unused_mol)):
            #we can assemble 's'
            unused_mol -= needed
            can_turnin[i] = True
        #else: break

    #eprint("can turn in",can_turnin)
    #eprint("storage",robots[0][3])
    freespace = 10 - np.sum(robots[0][3])  
    #eprint("freespace",freespace)
    can_assemble = [False]*len(ownedsamples)
    tentative_stock = getstock(robots)
    
    #eprint("tentativestock",tentative_stock)
    #eprint("POSSIBLE ASSEMBLY")
    neededmatrix = []
    for i,s in enumerate(ownedsamples):
        if(can_turnin[i]):
            neededmatrix.append(np.array([0,0,0,0,0]))
            continue
        discountcost = np.maximum(s[5]-robots[0][4],0)
        needed = np.maximum(discountcost-unused_mol,0)
        neededmatrix.append(needed)
        #eprint("sample",s)
        #eprint("needed",needed)
        #eprint("tentstock",tentative_stock)
        #eprint("tentstorage",unused_mol)
        #eprint("freespace",freespace)
        room = freespace-np.sum(needed)>=0
        #eprint("do we have room",room)
        available = all(tentative_stock>=needed)
        #eprint("are the molecules available",available)
        diagnosed = (s[4] != -1)
        #eprint("diagnosed",diagnosed)
        if(room and diagnosed and available):
            freespace-=np.sum(needed)
            tentative_stock-=needed
            can_assemble[i] = True
    #eprint("can assemble",can_assemble)
    #eprint(neededmatrix)
    if(any(can_assemble)):
            
        to_assemble = can_assemble.index(True)
        #eprint("we can assemble",ownedsamples[to_assemble])
        priority = neededmatrix[to_assemble].argsort()[::-1]
        order = getorder_getmolecule_bypriority(robots,samples,priority)        
        #order = getorder_assemble(robots,samples,ownedsamples[to_assemble])
        return order
    else:
        #eprint("we cant assemble")
        priority = np.array([1,2,0,3,4])
        order = getorder_getmolecule_bypriority(robots,samples,priority)
        return order
#
def getorder_getmolecule_bypriority(robots,samples,priority):
    stock = getstock(robots)
    for i,p in enumerate(priority):
        #eprint("checking molecule",p)
        if(stock[p]>0):
            #eprint("we can get molecule",p)
            order = "CONNECT " + str(itm[p])
            return order
'''
def getbest_turnin(robots,samples,candidate_samples):
    eprint("CALCULATING TURN IN")
    #Go through the storage(unused molecules) and samples, to determine which are already able to be assembled
    
    tentative_exp = np.copy(robots[0][4])
    #ownedsamples = [s for s in samples if s[1] == 0]
    eprint("candidates")
    [eprint(s) for s in candidate_samples]
    total_needed = np.array([0,0,0,0,0])
    eprint("calc needed")
    for i,s in enumerate(ownedsamples):
        expgain = itm[s[3]]
        needed = np.maximum(s[5]-tentative_exp,0)
        eprint("sample",s)
        eprint("needed",needed)
        if(s[4] == -1):
            continue
        if(all(needed<=unused_mol)):
            #we can assemble 's'
            unused_mol -= needed
            can_turnin[i] = True
        #else: break
    return needed,score,exp
'''


    
#assumes the samples are diagnosed
def needed_for_sequence(robots,samplesequence):
    tentative_exp = np.copy(robots[0][4])
    needed = np.array([0,0,0,0,0])
    #eprint("sequnece")
    #[eprint(s) for s in samplesequence]
    for i,s in enumerate(samplesequence):
        needed += np.maximum(s[5]-tentative_exp,0)
        expgained = mti[s[3]] #molecule to int
        tentative_exp[expgained]+=1
    #eprint("tentexp",tentative_exp)    
    #eprint("needed",needed)
    return needed

#assumes the samples are diagnosed
#Only callthis on a non-empty list of diagnosed samples.
def try_all_sequences(projects,robots,samples,candidate_samples):
    all_sequences = []
    seqlength = min(len(candidate_samples),3)
    while(seqlength>0):
        all_sequences.extend(list(itertools.permutations(candidate_samples,seqlength)))
        seqlength-=1

    seq_info = []
    for i,seq in enumerate(all_sequences):

        total_needed = needed_for_sequence(robots,seq)
        
        mol_still_needed = np.maximum(total_needed-robots[0][3],0)
        turns_to_complete = np.sum(mol_still_needed) + getdist(robots[0][0],'MOLECULES') + robots[0][1]
        stock = getstock(robots)

        room = np.sum(mol_still_needed)<=10-np.sum(robots[0][3])
        available = all(mol_still_needed<=stock)
        
        if(room and available):
            possible = True
        else:
            possible = False
        seq_exp = np.copy(robots[0][4])
        seq_score = robots[0][2]
        for s in seq:
            
            
            seq_exp[mti[s[3]]] += 1 #for each sample, convert mol to int, add to that index
            seq_score += s[4]
        for p in projects:
            if(all(robots[0][4] < p) and all(seq_exp)>=p):
                seq_score+=50
            
        seq_i = [possible, total_needed, mol_still_needed,seq_score,seq_exp,turns_to_complete,seq]
        seq_info.append(seq_i)
   
    return seq_info
            
def getorder_diagnosenew(robots,samples):
    ownedsamples = [s for s in samples if s[1] == 0]
    #ownedsamples.sort(key = lambda x: x[4]/sum(x[5]),reverse=True)
    ownedunknownsamples = [s for s in ownedsamples if s[4] == -1]
    #Depending on the number of samples we own, go to the different stations,
    #If we are at either of those stations, they will be overwritten
    if(len(ownedunknownsamples)>0):
        order = "GOTO DIAGNOSIS" #identify
    elif(len(ownedsamples)==3):
        order = "GOTO DIAGNOSIS" #discard
    else:
        order = "GOTO SAMPLES"  
    
    if(robots[0][0] == "DIAGNOSIS"):
        if(len(ownedunknownsamples)>0):
            #Diagnose if we can
            order = "CONNECT " + str(ownedunknownsamples[0][0])
        elif(len(ownedsamples) > 0):
            #Discard all
            order = "CONNECT " + str(ownedsamples[0][0])
        else:
            order = "GOTO SAMPLES"
    elif(robots[0][0] == "SAMPLES"):
        if(len(ownedsamples)<3):
            order = "CONNECT 1"
            if(np.sum(robots[0][4])>3):
                order = "CONNECT 2"
            if(np.sum(robots[0][4])>5):
                order = "CONNECT 3"
        else:
            order = "GOTO DIAGNOSIS"
          
    return order

def getorder_diagnoseall(robots,samples):
    ownedunknownsamples = [s for s in samples if s[4] == -1 and s[1] == 0]
    if(robots[0][0] != "DIAGNOSIS"):
        order = "GOTO DIAGNOSIS" #identify
    if(robots[0][0] == "DIAGNOSIS"):
        order = "CONNECT " + str(ownedunknownsamples[0][0])
    return order
    
def getorder_newsamples(robots,samples):
    if (robots[0][0] != "SAMPLES"):
        order = "GOTO SAMPLES"
    else:
        if(len([s for s in samples if s[1] == 0]) < 3):
            #desired: the desired ranks 
            currentranks = Counter([s[2] for s in samples if s[1] == 0])
            if(np.sum(robots[0][4])<2):
                desired = [1,1,1]
            elif(np.sum(robots[0][4])<4 and np.sum(robots[0][4])>=2):
                desired = [1,1,2]
            elif(np.sum(robots[0][4])<6 and np.sum(robots[0][4])>=4):
                desired = [1,2,2]
            elif(np.sum(robots[0][4])<8 and np.sum(robots[0][4])>=6):
                desired = [2,2,2]
            elif(np.sum(robots[0][4])<9 and np.sum(robots[0][4])>=8):
                desired = [2,2,3]
            else:#(np.sum(robots[0][4])>=8):
                desired = [3,3,3]
            desired = Counter(desired)
            to_order = list((desired-currentranks).elements())
            
            order = "CONNECT " + str(to_order[-1])
    return order
def getorder_newsamples_conservative(robots,samples):
    if (robots[0][0] != "SAMPLES"):
        order = "GOTO SAMPLES"
    else:
        if(len([s for s in samples if s[1] == 0]) < 3):
            #desired: the desired ranks 
            currentranks = Counter([s[2] for s in samples if s[1] == 0])
            if(np.sum(robots[0][4])<3):
                desired = [1,1,1]
            elif(np.sum(robots[0][4])<4 and np.sum(robots[0][4])>=3):
                desired = [1,1,2]
            elif(np.sum(robots[0][4])<6 and np.sum(robots[0][4])>=4):
                desired = [1,1,2]
            elif(np.sum(robots[0][4])<8 and np.sum(robots[0][4])>=6):
                desired = [1,2,2]
            elif(np.sum(robots[0][4])<9 and np.sum(robots[0][4])>=8):
                desired = [2,2,2]
            elif(np.sum(robots[0][4])<11 and np.sum(robots[0][4])>=9):
                desired = [2,2,3]
            else:#(np.sum(robots[0][4])>=8):
                
                desired = [3,3,3]
            desired = Counter(desired)
            to_order = list((desired-currentranks).elements())
            
            order = "CONNECT " + str(to_order[-1])
    return order

'''
def getorder_cyclesamples(robots,samples):
    ownedsamples = [s for s in samples if s[1] == 0]
    ownedunknownsamples = [s for s in samples if s[4] == -1 and s[1] == 0]
    if(robots[0][0] == "SAMPLES"):
        if(len(ownedsamples) < 3):
            order = getorder_newsamples(robots,samples)
    if(robots[])
    return order
'''
    
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
        #If we have backpackspace, we can add molecules from those where totalowned<5
        if(sum(robots[0][3])<10):
            [moves.append("CONNECT " + str(k)) for k,v in mti.items() if totalowned[v]<5]
        
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

def getdist(pos1,pos2):
    pos1 = pos_dict[pos1]
    pos2 = pos_dict[pos2]
    dist = dist_mat[pos1,pos2]
    return dist

def getstock(robots):
    stock = np.maximum(- robots[0][3] - robots[1][3] + 5,0) #Molecules left in stock(if there is a duplicate molecule, total will be 6, for -1 stock. special case handled by np.maximum
    return stock
                       
def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)
if(__name__) == "__main__":
    main()