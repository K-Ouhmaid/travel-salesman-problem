
# coding: utf-8

# In[48]:
#Implemented by Khalid Ouhmaid
#Sorry for the frensh you can translate the comments into english

import math
import random

# Class City il est considérer dans ce cas comme des sommets d'un graphe
# alors chaque sommet a sa propre X et Y comme dans un repére
class City:
    #Constructeur de la glasse . les getters & les stters
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y
    #fonction distanceTo : permet de calculer la distance entre la ville courant et la ville donné en paramétre
    def distanceTo(self, city):
        xDistance = math.fabs(self.x - city.x)
        yDistance = math.fabs(self.y - city.y)
        distance = math.sqrt((xDistance * xDistance) + (yDistance * yDistance))
        return distance
    #representation de la ville courante
    def __repr__(self):
        return str(self.x) + ", " + str(self.y)

# Class TourManager : ce class permet d'ajouter l'ensemble des villes dans une liste. dont laquellee on va effectuer l'étude
class TourManager:
    #constructeur permet de définir une liste s'appelle destinationCites
    def __init__(self):
        self.destinationCities = []
#pour ajouter une ville
    def addCity(self, city):
        self.destinationCities.append(city)
#pour prndre une ville spécifique
    def getCity(self, index):
        return self.destinationCities[index]
#return le nombre total des villes
    def numberOfCities(self):
        return len(self.destinationCities)

# Class Tour : ce classe est capable á chaque fois de générer un possible tour chaque tour a sa propre distance
class Tour:
    #constructeur qui prend en paramétre une instance de la classe TourMnager et il initialise une liste tour dont laquelle on va mettre les ville
    #alors la position des ville dans la liste est différent d'un tour a l' autre
    def __init__(self, tourmanager, tour=None):
        self.tourmanager = tourmanager
        self.tour = []
        self.fitness = 0.0
        self.distance = 0
        if tour is not None:
            self.tour = tour
        else:
            for i in range(0, self.tourmanager.numberOfCities()):
                self.tour.append(None)

    def __len__(self):
        return len(self.tour)

    def __getitem__(self, index):
        return self.tour[index]

    def __setitem__(self, key, value):
        self.tour[key] = value

    def __repr__(self):
        geneString = "|"
        for i in range(0, self.tourSize()):
            geneString += str(self.getCity(i)) + "|"
        return geneString
#a fonction generateIndividual est capable de générer un possible tour en mélangant les villes dans la liste aléatoirement
    def generateIndividual(self):
        for cityIndex in range(0, self.tourmanager.numberOfCities()):
            self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
        random.shuffle(self.tour)

    def getCity(self, tourPosition):
        return self.tour[tourPosition]
#peremet de mettre une ville dans une position donnée dans la liste
    def setCity(self, tourPosition, city):
        self.tour[tourPosition] = city
        self.fitness = 0.0
        self.distance = 0
#fitness est égale 1 sur la distance du tour
    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.getDistance())
        return self.fitness
#la fonction getDistance est capable de calculer la distance de ou le tour en passant sur tous les villes
    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for cityIndex in range(0, self.tourSize()):
                fromCity = self.getCity(cityIndex)
                destinationCity = None
                if cityIndex + 1 < self.tourSize():
                    destinationCity = self.getCity(cityIndex + 1)
                else:
                    destinationCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(destinationCity)
            self.distance = tourDistance
        return self.distance
#retourne la taille du tour
    def tourSize(self):
        return len(self.tour)
# test si  une ville est dans la liste tour
    def containsCity(self, city):
        return city in self.tour

# Classe Population c'est la classe qui est cpable de doné la tour optimal dans l'ensemble des tours possible
class Population:
    #constructeur prend en paramétre instnce de la class TourManager et populationSize qui est la taille des tours sur lequel on va travaillé
    #et la variable booléan parceque nous avons deux cas diff´rents
    def __init__(self, tourmanager, populationSize, initialise):
        self.tours = []
        for i in range(0, populationSize):
            self.tours.append(None)
#si initialise est vrai alors on va stockek dans la liste Tours les possible tour et ce dernier liste a une taille de populationSize
        if initialise:
            for i in range(0, populationSize):
                newTour = Tour(tourmanager)
                newTour.generateIndividual()
                self.saveTour(i, newTour)

    def __setitem__(self, key, value):
        self.tours[key] = value

    def __getitem__(self, index):
        return self.tours[index]
#permet de stocker un tour dans la liste Tours
    def saveTour(self, index, tour):
        self.tours[index] = tour
#retourne un tour donné en paramétre
    def getTour(self, index):
        return self.tours[index]
#getFiitest : c'est la fonction qui est capable de retourner le tour optimal dans lènsemble des tours
    def getFittest(self, start=0):
        fittest = self.tours[0]
        for i in range(start, self.populationSize()):
            if fittest.getFitness() <= self.getTour(i).getFitness():
                fittest = self.getTour(i)
        return fittest

    def drawFittestTour(self,color,width):
        fittest = self.getFittest()
        fittest.takeTour(color,width)

    def drawFirstTour(self,color,width):
        first = self.tours[0]
        first.takeTour(color,width)
#retourne la taille ce la liste Tours
    def populationSize(self):
        return len(self.tours)

# La classe GA permet d' Améliorer les résultats de recherche gráce a des fonctions efficace
class GA:

    def __init__(self, tourmanager, mutationRate=0.015, tournamentSize=5, elitism=1):
        self.tourmanager = tourmanager
        self.mutationRate = mutationRate
        self.tournamentSize = tournamentSize
        self.elitism = elitism
#c'est la fonction qui est capable d'amèliore les résultats en prenant en paramétre une instance de la classe Population
    def evolvePopulation(self, pop):
        #on a initialisé un nouvelle instance de la classe de Population mais cette fois si avec un booléan false
        #alors l'instance de la classe ne doit pas initialiser des tours
        newPopulation = Population(self.tourmanager, pop.populationSize(), False)
        #elitism est égale a 1
        elitismOffset = self.elitism
        #on a sauvegarder juste une tour dans la liste qui est la plus optimal dans l'indice 1
        for i in range(elitismOffset):
            newPopulation.saveTour(i, pop.getFittest(i))
#on va boucler de 1 jusqu'a la fin pour stocker des tours
#voire la commentaire en haut de chaque fonction utilisé ci desous
        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            child = self.crossover(parent1, parent2)
            #sauvegarder l'ensemble des optimal ours pour choisir le plus optimal entre elle aprés
            newPopulation.saveTour(i, child)

        for i in range(elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getTour(i))

        return newPopulation
#c`est une fonction a un principe de croissement il prend deux parents(deux instance de la classe Pppulation optimal ) et il donne un enfant Résltat(child)
    def crossover(self, parent1, parent2):
        #Initialisation d'un Tour
        child = Tour(self.tourmanager)
#srartPos et endPos prend des valeux aléatoire entre 0 et paren1.tourSize
        startPos = int(random.random() * parent1.tourSize())
        endPos = int(random.random() * parent1.tourSize())
#Lá on va stocker les villes dans une liste tour (child)selon certain condition
        for i in range(0, child.tourSize()):
            if startPos < endPos and i > startPos and i < endPos:
                child.setCity(i, parent1.getCity(i))
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
                    child.setCity(i, parent1.getCity(i))

        for i in range(0, parent2.tourSize()):
            if not child.containsCity(parent2.getCity(i)):
                for ii in range(0, child.tourSize()):
                    if child.getCity(ii) == None:
                        child.setCity(ii, parent2.getCity(i))
                        break

        return child
#fonction mutate prend en paramétre un Tour il permet de changere la place des villes selon certain condition
   #mutationRate égale 0.015 on peut toujours changer les valeurs pour tester lesr resultats
    def mutate(self, tour):
        for tourPos1 in range(0, tour.tourSize()):
            if random.random() < self.mutationRate:
                tourPos2 = int(tour.tourSize() * random.random())

                city1 = tour.getCity(tourPos1)
                city2 = tour.getCity(tourPos2)

                tour.setCity(tourPos2, city1)
                tour.setCity(tourPos1, city2)
#cette fonction prend en paramétre instance de la classe Population
#il  permet de stocker 5 (TournamentSize)tours qui sont pris aléatoirement dans la liste Tours
#et de choisir la plus opimal enre les 5 en retournant ce qu' on applle la parent
    def tournamentSelection(self, pop):
        tournament = Population(self.tourmanager, self.tournamentSize, False)
        for i in range(0, self.tournamentSize):
            randomId = int(random.random() * pop.populationSize())
            tournament.saveTour(i, pop.getTour(randomId))
        fittest = tournament.getFittest()
        return fittest


# initialisation des villes
tm = TourManager()
city = City(224, 179)
tm.addCity(city)
city2 = City(226, 7)
tm.addCity(city2)
city3 = City(319, 180)
tm.addCity(city3)
city4 = City(508, 265)
tm.addCity(city4)
city5 = City(320, 354)
tm.addCity(city5)
city6 = City(238, 535)
tm.addCity(city6)
city7 = City(125, 358)
tm.addCity(city7)
city8 = City(155, 218)
tm.addCity(city8)
city9 = City(105, 210)
tm.addCity(city9)
city10 = City(105, 220)
tm.addCity(city10)




pop = Population(tm, 50, True)
print('la distance Iniiale : ' + str(pop.getFittest().getDistance()))

# Evolve population for 50 generations
ga = GA(tm)
pop = ga.evolvePopulation(pop)
for i in range(0, 100):
    pop = ga.evolvePopulation(pop)

# Print final results
print("la distance Finale: " + str(pop.getFittest().getDistance()))
print("Le chemin Opimal:")
print(pop.getFittest())
