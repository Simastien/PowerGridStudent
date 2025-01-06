
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0:
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    def valider_reseau(self) -> bool:
        check=[]
        if(len(self.arcs)<len(self.noeuds)-1):
            return False
        for i in range(0, len(self.noeuds)-1):
            if(i==self.noeud_entree):
                check.append(True)
            else:
                if(self.arcs[i-1]==(self.noeud_entree,i)):
                    check.append(True)
                elif(check[self.arcs[i-1][0]]):
                    check.append(True)
                else:
                    return False           
        return True

    def valider_distribution(self, t: Terrain) -> bool:
        nb_client=-1
        coord_clients=[]
        for i in range(0, len(t.cases)-1):
            for j in range(0, len(t.cases[i])-1):
                if (t[i][j]==Case.CLIENT):
                    nb_client+=1
                    coord_clients.append((i,j))
        for k in range(0, nb_client):
            a=0
            co=-1
            for l in range(0, len(self.noeuds)-1):
                if (self.noeuds[l]==coord_clients[k]):
                    a=l
                    co+=1
            if(co!=nb_client):
                return False
            c=False
            for m in range(len(self.arcs)-1,0):
                if(self.arcs[m][1]==a):
                    if(self.arcs[m][0]==self.noeud_entree):
                        c=True
                    elif(m==0 and not c):
                        return False
                    else:
                        a=self.arcs[m][0]
        return True

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:

        pass

    def afficher_avec_terrain(self, t: Terrain) -> None:
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("~", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("+", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout

