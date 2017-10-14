import operator, os, sys, re, time, collections
import numpy as np
patron = re.compile("[^a-zA-Z']")

stopwordsman = ["a", "able", "about", "above", "according", "accordingly", "across", "actually", "after",
                 "afterwards", "again", "against", "all", "allow", "allows", "almost", "alone", "along",
                 "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "another",
                 "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart",
                 "appear", "appreciate", "appropriate", "are", "around", "as", "aside", "ask", "asking",
                 "associated", "at", "available", "away", "awfully", "b", "be", "became", "because", "become",
                 "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below",
                 "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "c",
                 "came", "can", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes",
                 "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider",
                 "considering", "contain", "containing", "contains", "corresponding", "could", "course",
                 "currently", "d", "definitely", "described", "despite", "did", "different", "do", "does",
                 "doing", "done", "down", "downwards", "during", "e", "each", "edu", "eg", "eight", "either",
                 "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever", "every",
                 "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f",
                 "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former",
                 "formerly", "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting",
                 "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had",
                 "happens", "hardly", "has", "have", "having", "he", "hello", "help", "hence", "her", "here",
                 "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his",
                 "hither", "hopefully", "how", "howbeit", "however", "i", "ie", "if", "ignored", "immediate",
                 "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar",
                 "instead", "into", "inward", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps",
                 "kept", "know", "knows", "known", "l", "last", "lately", "later", "latter", "latterly",
                 "least", "less", "lest", "let", "like", "liked", "likely", "little", "ll", "look", "looking",
                 "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely",
                 "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name",
                 "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never",
                 "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor",
                 "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", "of", "off",
                 "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other",
                 "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over",
                 "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please",
                 "plus", "possible", "presumably", "probably", "provides", "q", "que", "quite", "qv", "r",
                 "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards",
                 "relatively", "respectively", "right", "s", "said", "same", "saw", "say", "saying", "says",
                 "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self",
                 "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "she",
                 "should", "since", "six", "so", "some", "somebody", "somehow", "someone", "something",
                 "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
                 "specifying", "still", "sub", "such", "sup", "sure", "t", "take", "taken", "tell", "tends",
                 "th", "than", "thank", "thanks", "thanx", "that", "thats", "the", "their", "theirs", "them",
                 "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein",
                 "theres", "thereupon", "these", "they", "think", "third", "this", "thorough", "thoroughly",
                 "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too",
                 "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "u",
                 "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us",
                 "use", "used", "useful", "uses", "using", "usually", "uucp", "v", "value", "various", "ve",
                 "very", "via", "viz", "vs", "w", "want", "wants", "was", "way", "we", "welcome", "well",
                 "went", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter",
                 "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while",
                 "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish",
                 "with", "within", "without", "wonder", "would", "would", "x", "y", "yes", "yet", "you", "your",
                 "yours", "yourself", "yourselves", "z", "zero","ii"]

def getT(rootDir):
    T = []
    mapFiles={}
    filesOrganized = []
    filesOrganized = list(os.walk(rootDir))[0][2]
    for i in filesOrganized:
        mapFiles[os.stat(rootDir+i).st_size]=i

    sort = sorted(mapFiles.keys())[::-1]
    for cont in range(len(sort)):

        file = open(rootDir + mapFiles[sort[cont]], 'r')

        mainwords = []

            # print(str(archivo))

        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word not in stopwordsman:
                    mainwords.append(word)
        file.close()
        sorted_mainwords = collections.Counter(mainwords).most_common(10)

        #finalwords = list(sorted_mainwords
        finalwords =[]
        for i in range(10):
            finalwords.append(sorted_mainwords[i][0])
        #Se hace la union entre todos los elementos para evitar repetir.
        T=list(set(T).union(set(finalwords)))
    return T


# Devuelve mapa con los resultados de ft(d,t)
def ft(T):
    mapa = {}
    mapFiles={}
    filesOrganized = []
    filesOrganized = list(os.walk(rootDir))[0][2]
    for i in filesOrganized:
        mapFiles[os.stat(rootDir+i).st_size]=i

    sort = sorted(mapFiles.keys())[::-1]
    for cont in range(len(sort)):
        result = []
        for i in range(len(T)):
            result.append(0)

        file = open(rootDir + mapFiles[sort[cont]], 'r')
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word in T:
                    result[T.index(word)] += 1

        mapa[mapFiles[sort[cont]]] = result

    return mapa


def preJaccard(fdt):
    tam = len(fdt)

    matrixC = np.empty((tam, tam))

    listaFiles = list(fdt.keys())

    for i in range(tam):
        for j in range(tam):
            matrixC[i][j] = 1.0 - (jaccard(fdt[listaFiles[i]], fdt[listaFiles[j]]))

    return matrixC


def jaccard(x, y):
    summin=0
    summax=0
    for i in range(len(x)):
        summin+=min(x[i],y[i])
        summax+=max(x[i],y[i])
    return summin/summax

def kMeans(fdt,X, K, maxIters=6, plot_progress=None):
    grupo = []
    centroids = X[np.random.choice(np.arange(len(X)), K), :]
    for i in range(maxIters):
        # Esta parte asigna el closter o el grupo al que pertenece cada socumento
        C = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in centroids]) for x_i in X])
        # Calcula los nuevos centroides, a partir de los agrupamientos de c
        # saca sus promedios
        centroids = [X[C == k].mean(axis=0) for k in range(K)]
    #inicializo un arreglo de arreglos con K arreglos.
    for i in range(K):
        grupo.insert(i,[])
    listaFiles=list(fdt.keys())
    cont=0
    #Añado el nombre del documento al grupo que le corresponde
    for i in C:
        grupo[i].append(listaFiles[cont])
        cont+=1
    return np.array(centroids), C, grupo


if __name__ == '__main__':
    timeini = time.time()
    k = 2
    rootDir = sys.argv[1]
    T = getT(rootDir)
    fdt = ft(T)
    #print("FDT: ", fdt)

    matrizJaccard = preJaccard(fdt)

    centroides, finalList, grupo = kMeans(fdt,matrizJaccard, k)
    finalTime= time.time() - timeini

    cont=0
    for i in grupo:
        print("Closter numero ",cont,":")
        for j in i:
            print("Documento: ",j)
        print("--"*50)
        cont+=1
    print("Tiempo final: ", finalTime)
