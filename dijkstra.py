from queue import PriorityQueue                                                             
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.DiGraph()

class Grafo:
    def __init__(self, numeroDeVertices):                                                                #método construtor, recebe número de vértices
        self.numeroDeVertices = numeroDeVertices
        self.matrizDeAdj = [[-1 for i in range(numeroDeVertices)] for j in range(numeroDeVertices)]            #ele exibe as arestas como uma matriz de adj, importante notar que ele inicializa os valores como -1
        self.visitado = []                                                                           #essa lista vai armazenar os vértices que já visitamos

    def addAresta(self, vertice1, vertice2, weight):                                                #função básica de adição de aresta
        self.matrizDeAdj[vertice1][vertice2] = weight                                                #como a matriz de adj é simétrica, ele passa o mesmo peso pros índices espelhados
        self.matrizDeAdj[vertice2][vertice1] = weight 
        G.add_edge(vertice1, vertice2, weight = weight)   

    def dijkstra(self, origem, destino):  
        """
        Método de dijkstra não gera uma árvore mínima, é um método de cálculo de caminhos mínimos. 
        Passamos como parâmetro o vértice de origem dos nossos caminhos.
        
        D é a lista de caminhos para 
        todos os vértices(que aqui são os índices) do grafo. Começamos definindo a distância para todos os vértices como infinito
        definimos a distância para o vértice inicial como 0 (porque partimos dele).

        O vértice inicial é colocado na frente da fila (prioridade 0),
        limitador da repetição é a fila de prioridades não estar vazia,
        retiramos da fila o vértice que está sendo analisado atualmente e sua distância do ponto de origem.

        Adicionamos o vértice que está sendo analisado na lista de vértices visitados,
        vemos todos os possíveis vizinhos do nosso vértice atual (todos os vértices),
        se tiver uma aresta entre eles, o valor na matriz será diferente de -1,
        definimos a distância para esse vizinho como o valor da interseção na matriz (peso da aresta).

        Se esse vizinho ainda não estivar na lista de vértices já visitados, nós verificamos a distância,
        se obeserva o custo antigo guardado para esse vizinho (inicializado como infinito quando se declara D).

        Um novo custo é a distância do vértice origem até o atual + a distância desse atual até o vizinho,
        se o custo for menor, atualizamos o valor em D e colocamos a prioridade e o vértice na fila.
        """                                                                  
        D = {vertice:float('inf') for vertice in range(self.numeroDeVertices)}                           
        D[origem] = 0                                                                               
        P = [[] for indice in range(self.numeroDeVertices)]                                           
        P[origem] = [origem]

        pq = PriorityQueue()                                                                        #pq é a fila de prioridade que vamos usar nessa função
        pq.put((0, origem))                                                                         #o vértice inicial é colocado na frente da fila (prioridade 0)

        i = 0
        while not pq.empty():                                                                      #limitador da repetição é a fila de prioridades não estar vazia
            (dist, verticeAtual) = pq.get()                                                         #retiramos da fila o vértice que está sendo analisado atualmente e sua distância do ponto de origem
            self.visitado.append(verticeAtual)
            print(i+1, " - interacao:")
            print("vertice atual: ", verticeAtual)    
            print("Distancia: ", D)
            print('-'*45)                                                   #adicionamos o vértice que está sendo analisado na lista de vértices visitados

            for vizinho in range(self.numeroDeVertices):                                                 #vemos todos os possíveis vizinhos do nosso vértice atual (todos os vértices)
                if self.matrizDeAdj[verticeAtual][vizinho] != -1:                                    #se tiver uma aresta entre eles, o valor na matriz será diferente de -1
                    distancia = self.matrizDeAdj[verticeAtual][vizinho]            #definimos a distância para esse vizinho como o valor da interseção na matriz (peso da aresta)
                    
                    if vizinho not in self.visitado:                                                                       #se esse vizinho ainda não estivar na lista de vértices já visitados, nós verificamos a distância
                        distanciaAnterior = D[vizinho]                                              #vemos o custo antigo guardado para esse vizinho (inicializado como infinito ali quando declaramos D)
                        distanciaNova = D[verticeAtual] + distancia                                 #novo custo é a distância do vértice origem até o atual + a distância desse atual até o vizinho
                        
                        if distanciaNova < distanciaAnterior:                                    #se o custo for menor, atualizamos o valor em D e colocamos a prioridade e o vértice na fila
                            pq.put((distanciaNova, vizinho))
                            P[vizinho] = P[verticeAtual].copy()
                            P[vizinho].append(vizinho)
                            D[vizinho] = distanciaNova
            i += 1

        j = 0
        for vertice in range(len(D)):                                                               #impressão das distâncias contidas em D (retorno da função de dijkstra)
            cont = 0
            print("\nDistancia do vertice", origem, "para o vertice", vertice, "eh", D.get(j))
            j += 1
            print("Percurso: ", P[vertice])

            if vertice == destino:
                peso_ant = 0
                for i in range(len(P[vertice])-1):
                    H.add_edge(P[vertice][i], P[vertice][i+1], weight = (D.get(P[vertice][i+1])-peso_ant))
                    peso_ant = D.get(P[vertice][i+1])

        plt.figure("Arvore Geradora Minima - DIJKSTRA")
        pos = nx.layout.planar_layout(H)
        nx.draw(H, pos = pos, with_labels= True)
        peso_aresta = nx.get_edge_attributes(H, "weight")
        nx.draw_networkx_edge_labels(H, pos, peso_aresta)

        plt.figure("Grafo Original")
        pos = nx.layout.planar_layout(G)
        nx.draw(G, pos = pos, with_labels= True)
        peso_aresta = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, peso_aresta)

        plt.show()
                                                                  

grafo = Grafo(6)

grafo.addAresta(0, 1, 4)
grafo.addAresta(0, 2, 2)
grafo.addAresta(1, 2, 3)
grafo.addAresta(1, 3, 3)
grafo.addAresta(1, 4, 5)
grafo.addAresta(2, 4, 2)
grafo.addAresta(3, 4, 2)
grafo.addAresta(5, 4, 10)
grafo.dijkstra(3, 5)
