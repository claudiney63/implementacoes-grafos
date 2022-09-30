import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.Graph()

class Grafo:
    def __init__(self, numeroDeVertices):                                                #para gerar um novo grafo tem de passar um inteiro de parâmetro, e o inteiro vai dizer o número de vértices
        self.numeroDeVertices = numeroDeVertices                                              #atributo do número de vértices
        self.matrizDeAdj = [[0 for coluna in range(numeroDeVertices)]                     #inicia uma matriz de adjacência onde todos os valores são vazios, sendo que os vértices são as colunas e as fileiras
                    for fileira in range(numeroDeVertices)]
        self.listaDeArestas = []                                                      #ele inicia uma lista de arestas básica

    def addAresta(self, vertice1, vertice2, peso):                                  #para adicionar uma nova aresta no grafo, tem de passar os dois vértices e o peso da ligação deles
        self.matrizDeAdj[vertice1][vertice2] = peso                                  #o comando passa a aresta duas vezes para a matriz de adjacência para que ela seja simétrica, já que o grafo é não-direcionado
        self.matrizDeAdj[vertice2][vertice1] = peso
        self.listaDeArestas.append((vertice1, vertice2, peso))
        G.add_edge(vertice1, vertice2)

    def mostrarGrafo(self):                                                           #eh, resolvi adicionar um comando de impressão do grafo, ele imprime a lista de arestas (com o peso de cada uma) e depois o peso total -----------
        print("Lista de arestas escolhidas:  ", self.listaDeArestas)
        peso = 0
        for i in self.listaDeArestas:
            peso+= i[2]
        print("Peso total: ", peso)
        print('-------------------------------------------')
        return ''

    def printMatriz(self):                                                          #impressão da matriz de adjacência
        for i in range(self.numeroDeVertices):
            print(self.matrizDeAdj[i])

    def encontPai(self, pai, i):                                                    #método para encontrar o pai(explicação dentre os comentários do método kruskal) de um vértice. Passa como parâmetro a lista auxiliar de pais
        if pai[i] == i:                                                             #para quando encontra o vértice pai da subárvore e o retorna(explicação mais abaixo (dentre os comentários do método kruskal))
            return i
        return self.encontPai(pai, pai[i])                                          #a função é recursiva

    def conecSubArvore(self, pai, tamSubArvore, x, y):                              #método utilizado para conectar subárvores diferentes (explicação mais abaixo (dentre os comentários do método kruskal))
        xraiz = self.encontPai(pai, x)
        yraiz = self.encontPai(pai, y)
        if tamSubArvore[xraiz] < tamSubArvore[yraiz]:                               #a subárvore menor vira "filha" da maior
            pai[xraiz] = yraiz
        elif tamSubArvore[xraiz] > tamSubArvore[yraiz]:
            pai[yraiz] = xraiz
        else:                                                                       #caso ambas as subarvores tenham o mesmo tamanho, a primeira é escolhida automaticamente como pai da segunda e o tamanho da subárvore aumenta
            pai[yraiz] = xraiz
            tamSubArvore[xraiz] += 1

    def kruskal(self):
        arvoreMinima = Grafo(self.numeroDeVertices)                                     #arvoreMinima que será retornada pelo método
        
        i = 0                                                                       #contador
        e = 0                                                                       #utilizado pra manter o controle do número de arestas da árvore mínima (tem de ter valor final = número de vértices -1)

        self.listaDeArestas = sorted(self.listaDeArestas, key=lambda item: item[2])     #ordenação das arestas do grafo de acordo com o peso (índice 2 de cada aresta)
        print("Lista de Arestas Completa Ordenada: ", self.listaDeArestas, '\n')
                                                                                    #esse é o grande ponto do método kruskal, o que faltava no nosso código original
                                                                                    #para conseguir executar o método, são geradas duas listas auxiliares: pai e tamSubArvore, ambas tem o tamanho = número de vértices do grafo
        pai = []                                                                    #a lista pai armazena dentro dos seus índices (um pra cada vértice) o vértice conectado superiormente a ele (funciona meio que como uma lista encadeada)
        tamSubArvore = []                                                           #a lista tamSubArvore mostra o tamanho das subarvores da qual cada vértice é pai

        for vertice in range(self.numeroDeVertices):                                     #inicialização das listas auxiliares, botando o "pai" de cada vértice como ele próprio e o tamanho de suas subárvores como 0
            pai.append(vertice)
            tamSubArvore.append(0)

        while e < (self.numeroDeVertices - 1):                                           #a condicional necessária lá de restrição da árvore_mínima (num de arestas = num de vértices -1)
            vertice1, vertice2, peso = self.listaDeArestas[i]                         #escolhe o vértice de menor peso (i começa olhando o primeiro índice da lista ordenada)
            i = i + 1                                                               #aumenta o contador lá do i

            x = self.encontPai(pai, vertice1)                                       #encontra o vértice pai do vértice1
            y = self.encontPai(pai, vertice2)

            if x != y:                                                              #caso não pertençam a mesma família(pais diferentes)
                e = e + 1                                                           #aumenta o contador de arestas da árvore mínima
                arvoreMinima.addAresta(vertice1, vertice2, peso)                   #insere a aresta na arvore mínima
                H.add_edge(arvoreMinima.listaDeArestas[-1][0], arvoreMinima.listaDeArestas[-1][1])
                print(arvoreMinima.mostrarGrafo())
                self.conecSubArvore(pai, tamSubArvore, x, y)                        #faz a conexão das subárvores (trocando o pai da subárvore menor para o da subárvore maior)
                #print(i, " interacao - aresta adicionada: ", arvoreMinima.listaDeArestas[-1])

        return arvoreMinima


grafo = Grafo(7)

grafo.addAresta(0, 1, 3)
grafo.addAresta(0, 6, 2)
grafo.addAresta(0, 4, 7)
grafo.addAresta(0, 3, 4)
grafo.addAresta(1, 2, 5)
grafo.addAresta(1, 4, 10)
grafo.addAresta(2, 6, 4)
grafo.addAresta(2, 3, 6)
grafo.addAresta(3, 4, 1)
grafo.addAresta(4, 5, 1)

arvoreMinima = grafo.kruskal()
arvoreMinima.mostrarGrafo()
#arvoreMinima.printMatriz()

plt.figure("Grafo Original")
nx.draw_networkx(G, pos = nx.spring_layout(G), with_labels = True)

plt.figure("Arvore Geradora Minima")
nx.draw_networkx(H, pos = nx.spring_layout(H), with_labels = True)

plt.show()