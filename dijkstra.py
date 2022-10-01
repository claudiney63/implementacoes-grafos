from queue import PriorityQueue                                                                     #primeira mudança desse código pros outros: finalmente temos que importar uma classe de um módulo. Brabo. É uma fila de prioridade
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.Graph()

class Grafo:
    def __init__(self, numeroDeVertices):                                                                #método construtor, recebe número de vértices
        self.numeroDeVertices = numeroDeVertices
        self.matrizDeAdj = [[-1 for i in range(numeroDeVertices)] for j in range(numeroDeVertices)]            #ele exibe as arestas como uma matriz de adj, importante notar que ele inicializa os valores como -1
        self.visitado = []                                                                           #essa lista vai armazenar os vértices que já visitamos

    def addAresta(self, vertice1, vertice2, weight):                                                #função básica de adição de aresta
        self.matrizDeAdj[vertice1][vertice2] = weight                                                #como a matriz de adj é simétrica, ele passa o mesmo peso pros índices espelhados
        self.matrizDeAdj[vertice2][vertice1] = weight 
        G.add_edge(vertice1, vertice2)   

    def dijkstra(self, origem):                                                                     #método de dijkstra não gera uma árvore mínima, é um método de cálculo de caminhos mínimos. Passamos como parâmetro o vértice de origem dos nossos caminhos
        D = {vertice:float('inf') for vertice in range(self.numeroDeVertices)}                           #D é a lista de caminhos para todos os vértices(que aqui são os índices) do grafo. Começamos definindo a distância para todos os vértices como infinito
        D[origem] = 0                                                                               #definimos a distância para o vértice inicial como 0 (porque partimos dele)
        P = [[] for indice in range(self.numeroDeVertices)]                                              #lista de percursos (teste)---------------
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
                                                                  

grafo = Grafo(5)

grafo.addAresta(0, 1, 4)
grafo.addAresta(0, 2, 2)
grafo.addAresta(1, 2, 3)
grafo.addAresta(1, 3, 3)
grafo.addAresta(1, 4, 5)
grafo.addAresta(2, 4, 2)
grafo.addAresta(3, 4, 2)
#grafo.addAresta(5, 4, 10)
grafo.dijkstra(0)

plt.figure("Grafo Original")
nx.draw_networkx(G, pos = nx.spring_layout(G), with_labels = True)

# plt.figure("Arvore Geradora Minima")
# nx.draw_networkx(H, pos = nx.spring_layout(H), with_labels = True)

plt.show()