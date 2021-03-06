from qutip import *
from scipy import *
from numpy import *
import random
from math import log
from pygame import mixer
from random import randrange
from datetime import datetime
from tempfile import TemporaryFile


#********** Pauli Matrices Definition (useful for save the interaction matrices) *************#

class PAULI (object) :
    
    name = ''
    op = Qobj()
    
    def __init__(self, name, PauliMatrix) :
        self.name = name
        self.op = PauliMatrix
    
def make_pauli_matrix (name, PauliMatrix) :
    Pmatrix = PAULI (name, PauliMatrix)
    return Pmatrix

 
sx = make_pauli_matrix('X', sigmax())
sy = make_pauli_matrix('Y', sigmay())
sz = make_pauli_matrix('Z', sigmaz())
I = make_pauli_matrix('I', qeye(2))

j = complex(0,1)

pauliMatr = [[sz,sz],[sx,sx],[I,sx],[sz,I]] #types of interaction


######################################################
#GATE and DIMENSION
####################################################
N = 5        # n of qubits

G = toffoli()

interactions = [[0,1],[0,2],[1,2],[0,3],[1,3],[2,3],[0,4],[2,4],[1,4]] 	#interactions between qubits
									#the toffoli gate acts on 0-1-2

#######################################################################
#USEFUL DEFINITIONS
#######################################################################

dimG = G.shape[0]  
CareStateDim = int(log(dimG,2))

h = N-CareStateDim
if h > 1 :
    dontCareStates = [sin(0.847)*basis(2,1) + cos(0.847)*basis(2,0)]*(h)
    dontCareIdentity = [qeye(2)]*(h)
else :
    dontCareStates = [sin(0.847)*basis(2,1) + cos(0.847)*basis(2,0)]
    dontCareIdentity = [qeye(2)]


dCS = tensor(dontCareStates)
dCI = tensor(dontCareIdentity)

###########################################################################
#FUNCTIONS
###########################################################################

def Likelihood(J, rho_0) : #Likelihood function
    
    Ak = G*rho_0
    A = Ak*Ak.dag() #target state
    
    rho = tensor(rho_0, dCS) 	#initial state network
    H = Hamiltonian(J)
    U = (-j*H).expm()
    Btemp = U*rho		#unitary evolution
    Bk = Btemp*Btemp.dag()
    B = Bk.ptrace([0,1,2])	#trace off everything but 0-1-2
    
    out = (A*B).tr()		#inner product between target and evolved state

    return abs(out)


def Hamiltonian(x) : 	# The hamiltonian is simply the sum over all types of 2-body interactions 
    
    i = 0
    k = 0
    H = 0
    
    for p in interactions :
        
        temp = 0
        
        for S in pauliMatr :
        
            OpChain = [qeye(2)]*N
            OpChain[p[0]] = S[0].op
            OpChain[p[1]] = S[1].op
            
            temp += x[k]*tensor(OpChain)
            k += 1

        H += temp 
        
    
    return H

########################
#SGD
######################

step = 0.0008

t = open('ToffoliOK', 'w+')
startTime = datetime.now() 	#to measure the running time

Jopt = rand(len(interactions)*len(pauliMatr))	#random initialization	


delta = 0.0001 #for the derivative

check = 0
s = 0
time = step

for i in range(3): #we hit the walker 3 times during the optimization
    
    J = [x for x in Jopt]
    
    walk = step*500*i #strength of the punch
    
    while True :
        
        walk += step
        time += step
        
        rho_0 = rand_ket(N = 8, dims = [[2,2,2], [1,1,1]]) 	#random initialization of 0-1-2
        
	index = randrange(len(J))				#we optimize one direction (in J) at random
        JdJ = [x for x in J]
        JdJ[index] += delta
        grad = (Likelihood(JdJ, rho_0) - Likelihood(J, rho_0))/delta
        J[index] = J[index] + grad/sqrt(walk)
        s = Likelihood(J, rho_0) 
        
        
        
        t.write(str(time/step)+'    '+str(s)+'\n')        
        
        
        
        if abs(s) > 0.99 :					#check if we reached the maximum = 1
            check += 1    
            if check == 20:
                break
         
        if time/step % 100 < 1:					#track the evolution
            print(str(time/step)+ '   ' + str(s)+ '   ' + str(walk))
            
            
        if time/step > 1600*(i+1) :				#punch the walker every 1600 steps
            print('HIT')
            break
    
    Jopt = J

print(datetime.now()-startTime)#time
print(Jopt)
t.close()
alert.play()#alarm




