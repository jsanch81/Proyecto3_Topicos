# Proyecto 3

## Autores
  *Jose David Sánchez Castrillón*   _jsach81@eafit.edu.co_

  *Mayerli Andrea López Galeano*    _mlopez12@eafit.edu.co_

## Créditos

K-menas fue  un código reutilizado de internet, el cual pueden encontrar en el siguiente link, [k-means](https://gist.github.com/bistaumanga/6023692 "k-me") y jaccard fue implementado gracias a el algoritmo encontrado en el siquiente link [jaccard](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.332.4480&rep=rep1&type=pdf).

## Instalaciones

  Para la implementación de este proyecto fue necesaria la intalación de mpi4py, numpy y slurm

  ### Open MPI
  ```
  $ sudo apt-get install openmpi-bin
  ```
  ### mpi4py
  Es esencial para la implementación en paralelo.
  ```
  $ sudo apt-get install pip
  $ sudo pip install mpi4py
  ```

  ### numpy
  Es una extensión de python que nos ayuda a implementar con matrices y vectores.
  ```
  $ sudo apt-get install python-numpy
  ```
  ```
  $ sudo apt-get install python3-numpy
  ```
  ### slurm
  Es un sitema de gestion de recursos.
  ```
  $ sudo apt-get install slurm
  ```



## Ejecución
### Serial
Para la ejecución del programa serial es necesario tener instalado la versión de python 3, y
sus correspondientes dependencias, además de tener instaladas todas las bibliotecas utilizadas
en el proyecto. La ejecución se realiza de la siguiente manera.

`python3 serial.py Datasets/`

Donde Datasets puede ser cualquier directorio, el cual va a contener los archivos
que serán analizados, que en este caso son .txt

### Paralelo
Para la ejecución del paralelo es necesario tener instalado la versión de python 3, además debe
de tener instalado openmpi en su computadora como también la biblioteca mpi4py, y las demás bibliotecas
que se estén utilizando. Para el paralelo existen dos maneras de ejecución:
#### Ejecución por línea de comandos:

`mpiexec -n 4 python3 paralelo.py Datasets/`

En este caso su ejecución es diferente al serial, ya que se está ejecutando
con `mpiexec`, el cual me va a ejecutar el programa en paralelo con el número de nucleas
que se le indique en frente de la instrucción `-n`. En este caso se correrá con cuatro nucleas,
pero se podrá poner el número de núcleos con la cual cuente su máquina, o menos.

#### Ejecución con slurm:

Para esta ejecución es necesario tener instalado slurm en la
 computadora, y configurar un script con los siguientes
datos:

```[bash]
#!/bin/bash

#SBATCH --time=00:00:20
#SBATCH --nodes=4
# Memory per node specification is in MB. It is optional.
# The default limit is 3000MB per core.
#SBATCH --job-name="hello_test"
#SBATCH --output=test-srun.out

mpiexec -np 2 python ./paralelo.py folder/
```
Donde configuras el tiempo promedio que podría tardar la
ejecución del programa, el número de nodos, el nombre del
programa, y su salida.

Después de esto se pone el mismo comando de mpiexce, este archivo debe de guardarse en un archivo con extensión `.sh`.
Y al final se ejecuta el siguiente comando en la terminal.

`sbatch ./name_script.sh`

## Funcionalidad del codigo

La principal funcionalidad de este código consiste en minería de textos,
lo cual es relacionar un documento con otros que sean parecidos, o hablen del
mismo tema, esto se está haciendo con una métrica de similaridad, la cual es sacada de un algoritmo de similardad valga su redundancia. En nuestro caso es el jaccard, al cual se le están entregando dos arreglos los cuales son de documentos distintos, donde cada posición de los arreglos representa el número de veces que tiene una palabra ese documento. En nuestro caso son varias palabras, y son las mismas palabras para todos los archivos, por lo cual estos arreglos tienen un tamaño similar. Ya el jaccard a partir de estos datos saca la similaridad de estos documentos.

Esta es la formula correspondiente al jaccard utilizado.

`J(x,y)=(∑i min(Xi,Yi))/(∑i max(Xi,Yi))`

Después de tener la similardad es necesario agrupar los documentos. para hacer esto estamos utilizando el algoritmo de agrupamiento kmeans, el cual trabaja con centroides, y relaciona cada dato a el centroide más cercano y así sucesivamente. En nuestro caso el centroide se toma de la matriz que tiene los resultados de similaridad de todos los documentos. ya con estos datos el kmeans recorre esta matriz y va comprobando cada documento con cada centroide, al final agrupa este documento con el centroide que tenga la menor distancia. Después se realizara un promedio con cada dato que tenga cada grupo y salen los nuevos centroides, y así hasta cierto número de iteraciones. al final este me devolverá un n de grupos, donde en cada grupo hay n documentos que tienden a hablar del mismo tema.

Con esta respuesta que genera el kmeans, ya se podría dar recomendaciones de libros que tienden a hablar del mismo tema
