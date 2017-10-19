import operator, os, sys, re, collections
import time
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
sendbuf = []
root = 0
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
                "yours", "yourself", "yourselves", "z", "zero"]

# Obtiene la suma del mínimo y del máximo de las ocurrncias de las palabras en dos documentos,
# luego hace una división entre el sumMin y el sumMax
def jaccard(x, y):
    sumMin=0
    sumMax=0
    for i in range(len(x)):
        sumMin+=min(x[i],y[i])
        sumMax+=max(x[i],y[i])
    return float(sumMin)/float(sumMax)

def getOcurrence(v):
    #leidos = []
    #finalwords = {}
    toSend = []
    for i in range(comm.rank, len(v), comm.size):
        #print("RANK: ", comm.rank, v[i])
        file = open(rootDir + v[i], 'r')
        ocurrenceWords = []
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word not in stopwordsman:
                    ocurrenceWords.append(word)
        file.close()
        sorted_ocurrenceWords = collections.Counter(ocurrenceWords).most_common(10)
        for i in range(10):
            toSend.append(sorted_ocurrenceWords[i][0])

    return toSend

# Se crea un diccionario el cual contendrá el nombre de los documentos con las ocurrencia de
# las palabras más frecuentes.
def ft(ocurrenceFile,v):
    dictionary = {}
    for i in range(comm.rank, len(v), comm.size):
        arrOcurrence = []
        for j in range(len(ocurrenceFile)):
            arrOcurrence.append(0)

        file = open(rootDir + v[i], 'r')
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word in ocurrenceFile:
                    arrOcurrence[ocurrenceFile.index(word)] += 1
        # Guarda el nombre del documento como la key y el array de las ocurrencias como el value.
        dictionary[v[i]] = arrOcurrence

    return dictionary

# Crea una matriz con el tamaño del diccionario de las ocurrencias de las palabras
# la cual va llenando con la resta entre 1.0 y el resultado que me arroja el jaccard
#
def preJaccard(x):
    sizeDict = len(x)
    matrixC = np.zeros((sizeDict, sizeDict))
    listFiles = list(x.keys())
    for i in range(comm.rank, len(x), comm.size):
        for j in range(sizeDict):
            matrixC[i][j] = 1.0 - (jaccard(x[listFiles[i]], x[listFiles[j]]))

    return matrixC

# Retorna un array con los centrosides dependiendo del K recibida,
# un array con los gurpos y otro con los nombres de los documentos
# en su respectivo grupo.
# Este código fue implementado gracias a ......
def Kmeans(matrizFinal,k,maxIters = 10,):
    C = []
    centroids = []
    if comm.rank == 0:
        centroids = matrizFinal[np.random.choice(np.arange(len(matrizFinal)), k), :]

    for i in range(maxIters):

        mJack = comm.bcast(matrizFinal,root)
        cent = comm.bcast(centroids, root)
        tam2 = len(mJack)
        argminList = np.zeros(tam2)

        for i in range(comm.rank, len(mJack), comm.size):
            dotList = []
            for y_k in cent:
                dotList.append(np.dot(mJack[i] - y_k, mJack[i] - y_k))
            #print("DOTLIST", dotList)
            argminList[i] = np.argmin(dotList)
        #print("ARGMING" , argminList)
        recibC = comm.gather(argminList, root)
        #print("RECIBC"+str(recibC[0]))
        cFinal = []
        if comm.rank == 0:
            cFinal = np.zeros(len(recibC[0]))
            for li in range(len(recibC)):
                cFinal += recibC[li]
            #print("CFINAL", cFinal)

        z = comm.bcast(cFinal,root)

        centroidesTemp = []
        for i in range(k):
            centroidesTemp.insert(i, [])

        #print("CENTMP", centroidesTemp)
        for i in range(comm.rank, k, comm.size):
            truefalseArr = z == i
            propiosKArr = mJack[truefalseArr]
            promedioArr = propiosKArr.mean(axis=0)
            #print("promedio: ", promedioArr, "RANK", comm.rank)
            centroidesTemp[i]=list(promedioArr)
        #print("CENTRO", centroidesTemp, "RANK",comm.rank)
        recibZ = comm.gather(centroidesTemp,root)
        centroidesFinales = []
        for j in range(k):
            centroidesFinales.append([])
        if comm.rank == 0:
            #print("FINAL", recibZ)
            for i in range(len(recibZ)):
                for j in range(len(recibZ[i])):
                    centroidesFinales[j] += recibZ[i][j]
            centroids = centroidesFinales
    return centroids,z

if __name__ == '__main__':
    timeini = time.time()
    k = 10
    rootDir = sys.argv[1]
    T = []
    Ttemp=[]
    fileListTemp = []
    fileList=[]
    mapFiles={}
    if comm.rank==0:
        fileListTemp = list(os.walk(rootDir))[0][2]
        for i in fileListTemp:
            mapFiles[os.stat(rootDir+i).st_size]=i
        sort = sorted(mapFiles.keys())[::-1]
        del fileListTemp [:]
        for i in sort:
            fileListTemp.append(mapFiles[i])
        #print("organizado: ",fileListTemp)

    fileList = comm.bcast(fileListTemp, root)


    Ttemp = comm.gather(getOcurrence(fileList),root)
    tFinal = []
    if comm.rank == 0:
        for i in range(len(Ttemp)):
            tFinal.extend([element for element in Ttemp[i] if element not in tFinal])
    T=comm.bcast(tFinal, root)
    #print(T)

    fdtTemp=comm.gather(ft(T,fileList),root)
    mapaFinal={}
    if comm.rank == 0:
        for i in range(len(fdtTemp)):
            mapaFinal.update(fdtTemp[i])
    fdt=comm.bcast(mapaFinal, root)
    #print(fdt)

    matriz=comm.gather(preJaccard(fdt), root)
    matrizFinalTemp=0
    if comm.rank==0:
        for matrix in matriz:
            matrizFinalTemp += matrix
    matrizFinal=comm.bcast(matrizFinalTemp, root)
    #print(matrizFinal)

    centroides,C= Kmeans(matrizFinal,k)
    group=[]
    if comm.rank==0:
        for i in range(k):
            group.insert(i,[])
        listaFiles=list(fdt.keys())
        #print(listaFiles[0])
        cont=0;
        for i in C:
            group[int(i)].append(listaFiles[cont])
            cont+=1
        #print(C)
        finalTime=time.time()-timeini
        cont=0
        for i in group:
            print("Closter numero ",cont,":")
            for j in i:
                print("Documento: ",j)
            print("--"*50)
            cont+=1
        #print(group)
        print("Tiempo final: ", finalTime)
