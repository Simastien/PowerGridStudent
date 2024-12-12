
from Terrain import Terrain, Case
from heapq import heappop, heappush

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
            voisins = input("ajouter des arcs (liste d'IDs séparés par des espaces)").strip()
            for voisin_id in map(int,voisins.split()):
                arcs.append((num_noeud,voisin_id))
            num_noeud +=1
        noeud_entree = int( input("ID du noeud d'entrée :"))
        return noeud_entree, noeuds, arcs

class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        # TODO
        entree = t.get_entree()
        clients = t.get_clients()

        if entree == (-1, -1) or not clients:
            return -1, {}, []

        noeuds = {}
        arcs = []
        id_counter = 0

        # Map des positions aux IDs des noeuds
        position_to_id = {}

        # Ajouter le noeud d'entrée
        position_to_id[entree] = id_counter
        noeuds[id_counter] = entree
        id_counter += 1

        # Ajouter les noeuds des clients
        for client in clients:
            position_to_id[client] = id_counter
            noeuds[id_counter] = client
            id_counter += 1

        # Construire un graphe et trouver les chemins les plus courts(on ne prend pas en compte les cases où il y a des obstacles pour éviter de passer dessus)
        # on fait une reconnaissance du terrain
        def voisins(pos):
            i, j = pos
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < t.hauteur and 0 <= nj < t.largeur and t[ni][nj] != Case.OBSTACLE:
                    yield (ni, nj)

        #méthode de dijkstra: trouver le chemin le plus court entre deux postitions (ici l'entrée et les clients) 
        #on essaie d'éviter les obstacles (avec la fonction voisins)
        #on ne visite qu'une seule fois les cases
        def dijkstra(debut):
            dist = {debut: 0}
            prev = {}
            pile = [(0, debut)]
            visited = set()

            #parcours du terrain
            while pile:
                dist_courant, pos_courant = heappop(pile)
                if pos_courant in visited:
                    continue
                visited.add(pos_courant)

                for voisin in voisins(pos_courant):
                    cost = 1 if t[voisin[0]][voisin[1]] == Case.VIDE else 2
                    new_dist = dist_courant + cost
                    if voisin not in dist or new_dist < dist[voisin]:
                        dist[voisin] = new_dist
                        prev[voisin] = pos_courant
                        heappush(pile, (new_dist, voisin))

            return dist, prev

        # Connecter l'entrée à chaque client et faire les arcs entre chaque noeud
        for client in clients:
            dist, prev = dijkstra(entree)
            chemin = []
            current = client

        # Tant que le noeud actuel n'est pas l'entrée et qu'il existe dans le dictionnaire 'prev' (qui stocke les prédecesseurs)
        while current != entree and current in prev:
        # Ajouter le noeud actuel au chemin
            chemin.append(current)
            # Passer au prédecesseur du noeud actuel
            current = prev[current]

        # Si on atteint l'entrée après avoir parcouru les prédecesseurs
        if current == entree:
        # Inverser l'ordre du chemin pour qu'il soit dans la bonne direction (de l'entrée au client)
            chemin.reverse()

        # Initialiser le dernier noeud traité avec l'ID correspondant à la position de l'entrée
            last_node = position_to_id[entree]

        # Parcourir chaque étape dans le chemin calculé
            for step in chemin:
        # Si l'étape actuelle (coordonnées) n'a pas encore de noeud assigné
                if step not in position_to_id:
                # Associer un nouvel ID à cette étape
                    position_to_id[step] = id_counter
                # Ajouter ce noeud aux noeuds connus avec son ID et ses coordonnées
                    noeuds[id_counter] = step
                # Incrémenter le compteur d'ID pour le prochain noeud
                    id_counter += 1
        
                # Récupérer l'ID du noeud correspondant à cette étape
                next_node = position_to_id[step]

                # Ajouter un arc entre le dernier noeud traité et le noeud actuel
                arcs.append((last_node, next_node))

                # Mettre à jour le dernier noeud traité pour continuer à connecter les noeuds
                last_node = next_node


        return position_to_id[entree], noeuds, arcs

