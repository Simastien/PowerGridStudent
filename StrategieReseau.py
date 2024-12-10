
from Terrain import Terrain, Case

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        # TODO
        noeuds ={}
        arcs = []
        num_noeud = 0
        print("configuration manuelle :")
        while True:
            print ("terrain actuel:")
            t.afficher()
            choix = input("ajouter un noeud? (yes/no)").strip().lower()
            if choix != 'no':
                break
            x,y = map(int, input("coordonées du noeud (x,y) :").split())
            noeuds[num_noeud] = (x,y)
            print(f"noeud{num_noeud} ajouté en position ({x},{y}) ")
            voisins = input("ajouter des arcs (liste d'IDs séparés par de espaces)").strip()
            for voisin_id in map(int,voisins.split()):
                arcs.append((num_noeud,voisin_id))
            num_noeud +=1
        noeud_entree = int( input("ID du noeud d'entrée :"))
        return noeud_entree, noeuds, arcs

class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        # TODO
        noeuds ={}
        arcs = []
        num_noeud = 0

        entree = t.get_entree()
        noeuds[num_noeud] =entree
        entree_id = num_noeud
        num_noeud +=1
        for client in t.get_clients():
            noeuds[num_noeud] = client
            arcs.append(entree_id, num_noeud)
            num_noeud+=1


        return entree_id, noeuds, arcs

