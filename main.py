from Simul_meta import*
from customtkinter import*
from tkinter import messagebox
from math import*


class UI:
    
    def __init__(self,screen):
        
        self.screen=screen
        self.screen.geometry("500x200+1100+300")
        self.screen.title("Mutation Simulation")

        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        # row 0 : Titre

        self.Texte=CTkLabel(self.screen, text="Mutation Simulation",font=("Times new roman",20))
        self.Texte.grid(row=0,column=1,columnspan=3)

        # row 1 : Sous-titre

        self.under_Texte=CTkLabel(self.screen, text="Les bases azotées : A, C, T, G",font=("Times new roman",10))
        self.under_Texte.grid(row=1,column=1,columnspan=3)

        # row 2 : Entrée de gen

        self.Entrée_gen=CTkEntry(self.screen, width=220, placeholder_text="Chaine initiale")
        self.Entrée_gen.grid(row=2, column=1,padx=20,pady=10)

        self.Vaal=CTkButton(self.screen, text="Valider", command=self.saisie_entrée)
        self.Vaal.grid(row=2,column=2)

        # row 3 : Entrée de proba

        self.Entrée_pro=CTkEntry(self.screen, width=220,placeholder_text="'Probabilitées'")
        self.Vaal_2=CTkButton(self.screen, text="Valider")
        
        self.conjecturer=CTkButton(self.screen, text="Conjecturer",command=self.conjectura)
        
        # Gen et proba user
        
        self.Gen_user=0
        self.Proba_user=0
        self.nmbre_data=0
        self.données=False
        self.chaine_base=None
        self.i=0
        self.limite=1000000
        self.distance_conj=1000
        
    def saisie_entrée(self):
        try:
            chaine=self.Entrée_gen.get().strip().replace(" ","")
            self.Entrée_gen.delete(0,"end")
            self.vérification_chaine(chaine)
        except Exception as i:
            messagebox.showerror("Erreur",f"Erreur: {i}")
            
    def vérification_chaine(self,chn):
        chne=chn.upper()
        try:
            norm="ACTG"
            oui=0
            for element in chne:
                if element not in norm:
                    messagebox.showwarning("Problème","Les bases azotées sont : A,C,T,G")
                    self.Entrée_gen.delete(0,"end")
                else:
                    oui+=1
            if oui == len(chne):
                self.start()
                self.chaine_base=list(chne)
                print(self.chaine_base)
                messagebox.showinfo("Confirmé","C'est bon !")        
        except Exception as e:
            try:
                return chne.split(",")
            except Exception as e2:
                messagebox.showerror("Erreur",f"Il y a eu : {e2}")
    
    def saisie_gen(self):
        try:
            self.Gen_user=int(self.Entrée_gen.get().strip().replace(" ",""))
            if self.Gen_user>=self.limite:
                messagebox.showwarning("Warning","Votre nombre est vraiment très grand ! (Risque de crash)")
                print(f"good {self.Gen_user}")
            elif self.Gen_user<=0:
                messagebox.showwarning("Warning","Vous avez entré 0 hein")
            else:
                self.Entrée_gen.configure(state=DISABLED)
                self.nmbre_data+=1
                print(f"good {self.Gen_user}")
            
            if self.nmbre_data==2:
                self.données=True
                self.sim()
            else:
                pass
        except Exception as sg:
            messagebox.showerror("Error",f"Erreur : {sg}")  
    
    def saisie_proba(self):
        try:
            if self.Gen_user>self.limite:
                messagebox.showwarning("Danger","êtes vous sûr du nombres de générations ?\n (Risque de crash)")
            else:
                self.Proba_user=int(self.Entrée_pro.get().strip().replace(" ",""))
                self.Entrée_pro.configure(state=DISABLED)
                self.nmbre_data+=1
                print(f"good {self.Proba_user}")
            if self.nmbre_data==2:
                self.données=True
                self.sim()
            else:
                pass
        except Exception as sp:
            messagebox.showerror("Error",f"Erreur : {sp}")  
            
    def start(self):
        self.Texte.configure(text="Entrez les données")
        self.under_Texte.configure(text="N'oubliez pas de cliquer sur 'valider'")
        self.Entrée_gen.configure(placeholder_text="'Generations'")
        self.Vaal.configure(command=self.saisie_gen)
        self.Vaal_2.configure(command=self.saisie_proba)
        
        self.Entrée_pro.grid(row=3, column=1)
        self.Vaal_2.grid(row=3,column=2)
    
    def sim(self):
        if self.données==True:
            self.under_Texte.configure(text="---Simulation effectuée---")
            self.Entrée_gen.grid_forget()
            self.Entrée_pro.grid_forget()
            self.Vaal.grid_forget()
            
            self.simulation=Gen(self.chaine_base,self.Gen_user,self.Proba_user)
            self.a=self.simulation.affi_simgen()
            self.b=self.simulation.analyse_muta()
            
            self.Texte.configure(text=self.b[0])
            self.Vaal_2.configure(text="retour",command=self.initia)
    
    def initia(self):
        
        self.i+=1
        if self.i>=2:
            self.screen.destroy()
        else:
            self.Texte.configure(text="Mutation simulation")
            self.conjecturer.grid(row=3,column=0)
            self.under_Texte.configure(text="Bye bye")
            self.Texte.grid(columnspan=10)
        
    def conjectura(self):
        somme=0
        for i in range(self.distance_conj):
            sim=Gen(self.chaine_base,self.Gen_user,self.Proba_user)
            sim.sim_gen()
            k=sim.analyse_muta()
            hamming=int(k[1])
            somme+=hamming
            
        moy=somme/self.distance_conj
        p = moy / len(self.chaine_base) # Ratio de mutations visibles, prochaine amélioration peut-être
        self.screen.geometry("700x200")

        self.under_Texte.configure(text=f"Les {self.Gen_user} générations\n ont été répétées {self.distance_conj} fois")
        conj=f"Conjecture de Motoo Kimura :\nPour une probabilité de {self.Proba_user}% avec une\nséquence de {len(self.chaine_base)} bases azotée\nla dérive génétique moyenne\nsur {self.Gen_user} générations converge vers {moy:.2f} bases mutées."
        self.Texte.configure(text=conj)
        self.conjecturer.grid_forget()
        return moy

        
             
            

if __name__=="__main__":
    screen=CTk()
    A=UI(screen)
    screen.mainloop()