import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.Graph()


class Grafo:
    """
    Recebe um inteiro para gerar o grafo com determinada quantidade de vertices;

    Inicia uma matriz de adjacência onde todos os valores são vazios, sendo que os vértices são as colunas e as fileiras;

    Adição de arestas numa Matriz de Adjacencia, e um print logo apos para mostrar o 
    percurso de cada vertice e pesos, e a matriz;
    """

    def __init__(self, numeroDeVertices):
        self.numeroDeVertices = numeroDeVertices
        self.matrizDeAdj = [[0 for coluna in range(numeroDeVertices)]
                            for fileira in range(numeroDeVertices)]
        self.listaDeArestas = []

    def maisArestas(self, vertice1, vertice2, peso):
        self.matrizDeAdj[vertice1][vertice2] = peso
        self.matrizDeAdj[vertice2][vertice1] = peso
        self.listaDeArestas.append((vertice1, vertice2, peso))
        G.add_edge(vertice1, vertice2, weight=peso)

    def mostrarGrafo(self):
        print("Lista de arestas escolhidas:  ", self.listaDeArestas)
        peso = 0
        for i in self.listaDeArestas:
            peso += i[2]
        print("Peso total: ", peso)
        print('-------------------------------------------')
        return ''

    def printaMatriz(self):
        for i in range(self.numeroDeVertices):
            print(self.matrizDeAdj[i])

    def encontrandoPai(self, pai, i):
        """
        Método para encontrar o pai de 
        um vértice. Passa como parâmetro a lista auxiliar de pais para quando encontra o 
        vértice pai da subárvore e o retorna. De forma recursiva.
        """
        if pai[i] == i:
            return i
        return self.encontrandoPai(pai, pai[i])

    def conecSubArvore(self, pai, size_sub_arvore, x, y):
        """
        Método utilizado para conectar subárvores diferentes;

        A subárvore menor vira "filha" da maior;

        Caso ambas as subarvores tenham o mesmo tamanho, a primeira é escolhida automaticamente 
        como pai da segunda e o tamanho da subárvore aumenta;
        """
        xraiz = self.encontrandoPai(pai, x)
        yraiz = self.encontrandoPai(pai, y)
        if size_sub_arvore[xraiz] < size_sub_arvore[yraiz]:
            pai[xraiz] = yraiz
        elif size_sub_arvore[xraiz] > size_sub_arvore[yraiz]:
            pai[yraiz] = xraiz
        else:
            pai[yraiz] = xraiz
            size_sub_arvore[xraiz] += 1

    def kruskal(self):
        """
        Cria se a arvore minima inicial, com um contador para manter o controle do número de arestas
        da arvore minima;

        Ordena então as arestas do grafo de acordo com o peso (índice 2 de cada aresta);

        Para conseguir executar o método, são geradas duas listas auxiliares: 
        pai e tamSubArvore, ambas tem o tamanho igual ao número de vértices do grafo;

        A lista pai armazena dentro dos seus índices (um pra cada vértice) o vértice conectado 
        superiormente a ele (funciona como uma lista encadeada);

        A lista tamSubArvore mostra o tamanho das subarvores da qual cada vértice é pai;

        Se inicia as listas auxiliares, colocando o "pai" de cada vértice como ele próprio e o tamanho de suas subárvores como 0;

        A condicional necessária de restrição da árvore_mínima (num de arestas = num de vértices -1)

        Escolhe o vértice de menor peso (i começa olhando o primeiro índice da lista ordenada)

        Podemos então encontrar o vértice pai do vértice1;

        Caso não pertençam a mesma família (pais diferentes), aumenta o contador de arestas da árvore mínima,
        e insere a aresta na arvore mínima;

        No final do metodo fazemos a conexão das subárvores (trocando o pai da subárvore menor para o da subárvore maior)
        """
        arvoreMinima = Grafo(self.numeroDeVertices)

        i = 0
        j = 0

        self.listaDeArestas = sorted(
            self.listaDeArestas, key=lambda item: item[2])
        print("Lista de Arestas Completa Ordenada: ", self.listaDeArestas, '\n')

        pai = []
        size_sub_arvore = []

        for vertice in range(self.numeroDeVertices):
            pai.append(vertice)
            size_sub_arvore.append(0)

        while j < (self.numeroDeVertices - 1):
            vertice1, vertice2, peso = self.listaDeArestas[i]
            i = i + 1

            x = self.encontrandoPai(pai, vertice1)
            y = self.encontrandoPai(pai, vertice2)

            if x != y:
                j = j + 1
                arvoreMinima.maisArestas(vertice1, vertice2, peso)
                H.add_edge(
                    arvoreMinima.listaDeArestas[-1][0], arvoreMinima.listaDeArestas[-1][1], weight=peso)
                print(arvoreMinima.mostrarGrafo())
                self.conecSubArvore(pai, size_sub_arvore, x, y)

        plt.figure("Grafo Original")
        pos = nx.layout.planar_layout(G)
        nx.draw(G, pos=pos, with_labels=True)
        peso_aresta = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, peso_aresta)

        plt.figure("Arvore Geradora Minima - KRUSKAL")
        pos = nx.layout.planar_layout(H)
        nx.draw(H, pos=pos, with_labels=True)
        peso_aresta = nx.get_edge_attributes(H, "weight")
        nx.draw_networkx_edge_labels(H, pos, peso_aresta)

        plt.show()
        return arvoreMinima


grafo = Grafo(7)

grafo.maisArestas(0, 1, 3)
grafo.maisArestas(0, 6, 2)
grafo.maisArestas(0, 4, 7)
grafo.maisArestas(0, 3, 4)
grafo.maisArestas(1, 2, 5)
grafo.maisArestas(1, 4, 10)
grafo.maisArestas(2, 6, 4)
grafo.maisArestas(2, 3, 6)
grafo.maisArestas(3, 4, 1)
grafo.maisArestas(4, 5, 1)

arvoreMinima = grafo.kruskal()
arvoreMinima.mostrarGrafo()
# arvoreMinima.printMatriz()
