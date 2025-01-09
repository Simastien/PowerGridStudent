
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
        # Vérifie que le nombre d'arcs est suffisant pour relier tous les noeuds
        
        if len(self.arcs) < len(self.noeuds) - 1:
            return False

        # Initialisation d'un ensemble pour suivre les noeuds visités
        visited = set()
        to_visit = [self.noeud_entree]
        
        # Exploration des noeuds à partir de l'entrée
        while to_visit:
            
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)

                # Parcours des arcs pour trouver les noeuds connectés
                for n1, n2 in self.arcs:
                    if n1 == current and n2 not in visited:
                        to_visit.append(n2)
                    elif n2 == current and n1 not in visited:
                        to_visit.append(n1)

        # Vérifie que tous les noeuds ont été visités
        return len(visited) == len(self.noeuds)

    def valider_distribution(self, t: Terrain) -> bool:
        clients = t.get_clients()#on récupère la positions des clients
        noeuds_positions = set(self.noeuds.values())# on récupère la position de tout les noeuds de notre distribution
        return all(client in noeuds_positions for client in clients)#vérifie si la position de chaque client est dans la liste de position des noeuds
        #on vérifie juste la présence du noeud correspondant à la position du client et pas forcément si elle est relié 
        #car si l'algorithme pour relier les clients a pu arriver jusqu'à la position du client sachant qu'il part de l'entrée,
        #cela veut dire qu'il a trouvé un chemin pour arriver jusqu'au client.
        

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        print("Noeuds :")
        for key,coord in self.noeuds.items():
            print(f"{key}: {coord}")
        print("arcs :")
        for arc in self.arcs:
            print(f"{arc}")


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

