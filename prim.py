from cProfile import label
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.Graph()

class Grafo:
    """
    O metodo adicionaAresta() adiciona as arestas recebendo o vertice 1 e o vertice 2, 
    e como terceiro parametro o seu peso, as arestas são adicionadas na matriz duas vezes, 
    para que ela seja simétrica, já que o grafo é não-direcionado.

    Metodo mostrarGrafo() imprime o grafo, com lista de arestas e peso de cada uma, e depois peso total.

    Metodo printMatriz() imprime a matriz de adjacencia.

    No metodo principal prim() recebe como parametro o vertice arbitrario, e um numero 
    infinito é definido para ser o teto dos pesos das arestas. Lista de Vertices selecionados ja inicia com os vertices 
    como falso,, que já percencem a nossa lista de arvore minima.
    Uma matriz de adjacencia é gerada como resultado.

    Enquanto existirem vertices qque não estão na arvore minima, o loop while continuara ativo.
    O número infinito definido anteriormente é resetado no começo de cada execução do comando de repetição,
    é guardado o vértice escolhido no início da aplicação do algoritmo e último vértice adicionado na nossa árvore mínima.

    O segundo loop, vai percorrer todas as colunas da matriz de adjacência, verificando 
    se aquele vértice está na lista de vértices já incluídos.

    O terceiro loop, vai percorrer todas as fileiras da matriz de adjacência, verificando se o vértice 
    da fileira não esta na lista de vértices do grafo definida anteriormente, ele checa se o cruzamento 
    do vértice da coluna e da fileira tem valor > 0. 
    Se o peso do cruzamento analisado (aresta) for menor que o valor mínimo setado, ele vai receber 
    o peso dele como novo mínimo e mudar os valores de comeco e fim.

    O vértice novo adicionado (retirado da fileira da matriz) é verificado na lista de vértices falseados,
    preenchendo o valor do cruzamento dos vértices na matriz resultante da aplicação do algoritmo.

    Se o valor mínimo for infinito (ocorre na primeira repetição), é setado o cruzamento 
    entre os dois vértices como 0 (vértice inicial do algoritmo).

    É adicionado a arvore minima a aresta escolhida, apos a pimeira interação, pois antes disso ela se 
    encontra vazia, e transforma a matriz em simetrica no final, e por fim retornando a listas de arestas escolhidas.
    """
    def __init__(self, numeroDeVertices):                                                   
        self.numeroDeVertices = numeroDeVertices                                                  
        self.matrizDeAdj = [[0 for coluna in range(numeroDeVertices)]                        
                    for fileira in range(numeroDeVertices)]
        self.listaDeArestas = []                                                 

    def adicionaAresta(self, vertice1, vertice2, peso):                                    
        self.matrizDeAdj[vertice1][vertice2] = peso                                      
        self.matrizDeAdj[vertice2][vertice1] = peso
        self.listaDeArestas.append((vertice1, vertice2, peso))   
        G.add_edge(vertice1, vertice2, weight = peso)          

    def mostrarGrafo(self):                                                               
        print("\nLista de arestas completa: ", self.listaDeArestas)
        peso = 0
        for i in self.listaDeArestas:
            peso+= i[2]
        print("Peso total: ", peso, "\n")

        plt.figure("Grafo Original")
        pos = nx.layout.planar_layout(G)
        nx.draw(G, pos = pos, with_labels= True)
        peso_aresta = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, peso_aresta)
            

    def printMatriz(self):                                                              
        for i in range(self.numeroDeVertices):
            print(self.matrizDeAdj[i])

    def prim(self, inicio):                                                             
        infinito = float('inf')                                                         
        arvoreMinima = Grafo(self.numeroDeVertices)                                         
        verticesSelecionados = [False for vertice in range(self.numeroDeVertices)]           

        resultado = [[0 for coluna in range(self.numeroDeVertices)]                          
                    for fileira in range(self.numeroDeVertices)]
        
        index = 0                                                               
        
        while(False in verticesSelecionados):                                           
            pesoMinimo = infinito                                                     
            comeco = inicio                                                     
            fim = inicio                                                              

            for i in range(self.numeroDeVertices):                                           
                if verticesSelecionados[i]:                                             
                    for j in range(self.numeroDeVertices):                                   
                        if (not verticesSelecionados[j] and self.matrizDeAdj[i][j]>0):   
                            if self.matrizDeAdj[i][j] < pesoMinimo:                     
                                pesoMinimo = self.matrizDeAdj[i][j]
                                comeco, fim = i, j
            
            verticesSelecionados[fim] = True                                           
            resultado[comeco][fim] = pesoMinimo                                       
            
            if pesoMinimo == infinito:                                                 
                resultado[comeco][fim] = 0                                              

            if(index >= 1):                                                              
                arvoreMinima.adicionaAresta(comeco, fim, pesoMinimo)     
                print(index, ' interacao - aresta percorrida: ', arvoreMinima.listaDeArestas[-1]) 
                H.add_edge(arvoreMinima.listaDeArestas[-1][0], arvoreMinima.listaDeArestas[-1][1], weight = pesoMinimo)           
            
            index += 1
            resultado[fim][comeco] = resultado[comeco][fim]                             
        
        plt.figure("Arvore Geradora Minima - PRIM")
        pos = nx.layout.planar_layout(H)
        nx.draw(H, pos = pos, with_labels= True)
        peso_aresta = nx.get_edge_attributes(H, "weight")
        nx.draw_networkx_edge_labels(H, pos, peso_aresta)

        return arvoreMinima          


grafo = Grafo(5) #Especifica a quantidade vertices

#E indica suas arestas sendo os parametros 1 e 2, e o 3 o peso dessa aresta
grafo.adicionaAresta(0, 1, 4)
grafo.adicionaAresta(0, 2, 2)
grafo.adicionaAresta(1, 2, 3)
grafo.adicionaAresta(1, 3, 3)
grafo.adicionaAresta(1, 4, 5)
grafo.adicionaAresta(2, 4, 2)
grafo.adicionaAresta(3, 4, 2)

arvoreMinima = grafo.prim(2)
arvoreMinima.mostrarGrafo()
# arvoreMinima.printMatriz()

plt.show()