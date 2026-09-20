from random import*

class Gen:
    def __init__(self,sequence,gen,proba):
        self.BaseA=["A","T","C","G"]
        self.sequence=sequence.copy()
        self.gen=gen
        self.proba=proba
        self.sequence_n={0:sequence}
        self.simulated=False
        
    def sim_gen(self):
        liste_tempo_BaseA=self.sequence.copy()
        for i in range(1,self.gen+1):
            if randint(1,100)<=self.proba:
                liste_tempo_BaseA[randint(0,len(liste_tempo_BaseA)-1)]=choice(self.BaseA)
                self.sequence_n[i]=liste_tempo_BaseA.copy()
            else:
                self.sequence_n[i]=liste_tempo_BaseA.copy()
                
        self.simulated=True
    
    def affi_simgen(self):
        if self.simulated==True:
            print(self.sequence_n)
        else:
            self.sim_gen()
            print("Simulation en cours :\n")
            print(self.sequence_n)
            return(self.sequence_n)
    
    def analyse_muta(self):
        
        if self.sequence_n[0]==self.sequence_n[self.gen]:
            print(f"Au final, après les {self.gen} générations passées, On ne remarque pas de différence...")
            Ben="Rien"
            return Ben
        else:
            first_gen=self.sequence_n[0]
            last_gen=self.sequence_n[self.gen]
            Hamming=0
            no_Hamming=0
            
            for k in range(len(first_gen)):
                if first_gen[k] != last_gen[k]:
                    Hamming+=1
                else:
                    no_Hamming+=1
            Ben=f"À l'issue des {self.gen} générations simulées,\nle nombre de mutations observées (distance de Hamming)\nest de {Hamming}"            
            print(Ben)
            return Ben,Hamming


Test=False
if Test==True:
    seq=["A","C","T","G"]
    A=Gen(seq,100,10)            
    A.affi_simgen()
    A.analyse_muta()
else:
    pass
