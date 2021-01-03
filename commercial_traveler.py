# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:14:17 2020

@author: ld
"""

from __future__ import division

import numpy as np
import pytest

np.random.seed(123)
TAILLE = 50

class Ville(object):

    """
    Ville, contient une liste (non-ordonnée) de destinations.
    """

    def __init__(self):
        """Initialisation d'une ville sans destination."""

        self.destinations = np.array([])

    def aleatoire(self, n=20):
        """Création de *n* destinations aléatoires."""
        self.destinations = np.random.randint(0,50,[n,2])

    def lecture(self, nomfichier="ville.dat"):
        """
        Lecture d'un fichier ASCII donnant les coordonnÃ©es des destinations.
        """
        file = open("ville.dat")
        file = file.read()
        file = file.split("\n")
        self.destinations = list(map(lambda elem: [int(x) for x in elem.split(" ")],file))
        
    def ecriture(self, nomfichier="ville.dat"):
        """
        Ã‰criture d'un fichier ASCII avec les coordonnÃ©es des destinations.
        """
        file = open("ville.dat")
        for i in self.destinations:
            file = file.writeLine( i[0] + " " + i[1])
            
            
    def nb_trajets(self):
        """Retourne le nombre total (entier) de trajets: (n-1)!/2."""     
        nbRoads = len(self.destinations)
        return np.math.factorial(nbRoads - 1)/2
        
    def distance(self, i, j):
        """
        Retourne la distance Manhattan-L1 entre les destinations numero
        *i* et *j*.
        """       
        return np.math.abs(self.destinations[j][1] - self.destinations[i][1]) + np.math.abs(self.destinations[j][0] - self.destinations[i][0])       

    def plus_proche(self, i, exclus=[]):
        """
        Retourne la destination la plus proche de la destination *i*, hors les
        destinations de la liste `exclus`.
        """
        distanceList = np.zeros(len(self.destinations))
        for j in range(len(self.destinations)):
            if j not in exclus:
                distanceList[j] = Ville.distance(self, i, j)
        
        """second way to implement the calculation of distance
        distanceList2 = np.array([ Ville.distance(self, i, j) for j in range(len(self.destinations)) ])
        """
        
        closest = np.sort(distanceList, axis=None, kind='mergesort')[0]

        return closest

    def trajet_voisins(self, depart=0):
        """
        Retourne un `Trajet` dÃ©terminÃ© selon l'heuristique des plus proches
        voisins (i.e. l'Ã©tape suivante est la destination la plus proche hors
        les destinations dÃ©jÃ  visitÃ©es) en partant de l'Ã©tape initiale
        `depart`.
        """
        frm = depart
        exclude = []
        trajet = [depart]
        item = 0
        while len(exclude) != len(self.destinations):
            item = Ville.plus_proche(self, frm, exclude)       
            frm = item
            trajet.append(item)
            exclude.append(item)
            
        return trajet

    def optimisation_trajet(self, trajet):
        """
        Retourne le trajet le plus court de tous les trajets Â« voisins Â» Ã 
        `trajet` (i.e. rÃ©sultant d'une simple interversion de 2 Ã©tapes).
        """
        currentLength = 0
        testedLength = 0
        for i in range(len(trajet.etapes)):
            for j in range(i + 2,len(trajet.etapes)):
                currentLength = ville.distance(i, i + 1)
                testedLength = ville.distance(i, j)
                if currentLength > testedLength:
                    trajet.intervension(i,j)
        return trajet                      

    def trajet_opt2(self, trajet=None, maxiter=100):
        """
        Ã€ partir d'un `trajet` initial (par dÃ©faut le trajet des plus proches
        voisins), retourne un `Trajet` optimisÃ© de faÃ§on itÃ©rative par
        interversion successive de 2 Ã©tapes.  Le nombre maximum d'itÃ©ration est
        `maxiter`.
        """
        if trajet == None:
            trajet = ville.trajet_voisins()
        nbIter = 0
        for i in range(len(trajet.etapes)):
            for j in range(i + 2,len(trajet.etapes)):
                if nbIter == maxiter:
                    break
                currentLength = ville.distance(i, i + 1)
                testedLength = ville.distance(i, j)
                if currentLength > testedLength:
                    trajet.intervension(i,j)
                nbIter = nbIter + 1               
            nbIter = nbIter + 1
        return trajet

class Trajet(object):

    """
    Trajet, contient une liste ordonnÃ©e des destinations (Ã©tapes) d'une
    Ville.
    """

    def __init__(self, ville, etapes=None):
        """
        Initialisation sur une `ville`.  Si `etapes` n'est pas spÃ©cifiÃ©, le
        trajet par dÃ©faut est celui suivant les destinations de `ville`.
        """
        if etapes != None:
            self.etapes = etapes
        else:
            self.etapes = ville.destinations
        

    def longueur(self, ville):
        """
        Retourne la longueur totale du trajet *bouclÃ©* (i.e. revenant Ã  son
        point de dÃ©part).
        """
        
        length = ville.distance(self.etapes[0],self.etapes[len(self.etapes)] - 1)
        for i in range(len(self.etapes) - 1):
            length = length + ville.distance(i,i+1)
        return length

    def interversion(self, i, j):
        """
        Retourne un nouveau `Trajet` rÃ©sultant de l'interversion des 2 Ã©tapes
        *i* et *j*.
        """
        newPath = self.etapes
        step1 = self.etapes[i]
        step2 = self.etapes[j]
        newPath[i] = step2
        newPath[j] = step1
        self.etapes = newPath

# TESTS ==============================

def test_ville_aleatoire():

    ville = Ville()
    ville.aleatoire(10)
    assert ville.destinations.shape == (10, 2)
    assert np.issubdtype(ville.destinations.dtype, int)

def test_ville_lecture():

    ville = Ville()
    ville.lecture("ville.dat")
    assert ville.destinations.shape == (20, 2)
    assert (ville.destinations[:3] == [[45, 2], [28, 34], [38, 17]]).all()

@pytest.fixture
def ville_test():

    ville = Ville()
    ville.destinations = np.array([[0, 0], [1, 1], [3, 0], [2, 2]])
    return ville

def test_ville_ecriture(ville_test):

    ville_test.ecriture("test_ecriture.dat")
    ville = Ville()
    ville.lecture("test_ecriture.dat")
    assert (ville_test.destinations == ville.destinations).all()

def test_ville_trajets(ville_test):

    assert ville_test.nb_trajets() == 3

def test_ville_distance(ville_test):

    assert ville_test.distance(0, 1) == 2
    assert ville_test.distance(1, 2) == 3
    assert ville_test.distance(2, 0) == 3

def test_trajet_init(ville_test):

    trajet = Trajet(ville_test)
    assert (trajet.etapes == range(4)).all()

@pytest.fixture
def trajet_test(ville_test):

    return Trajet(ville_test)

def test_trajet_longueur(trajet_test):

    assert trajet_test.longueur() == 12

def test_ville_plus_proche(ville_test):

    assert ville_test.plus_proche(0) == 1
    assert ville_test.plus_proche(0, [1, 2]) == 3

def test_ville_trajet_voisins(ville_test):

    assert (ville_test.trajet_voisins(depart=0).etapes == [0, 1, 3, 2]).all()

def test_trajet_interversion(trajet_test):

    assert (trajet_test.interversion(0, 1).etapes == [1, 0, 2, 3]).all()

def test_ville_optimisation_trajet(ville_test, trajet_test):

    assert (ville_test.optimisation_trajet(trajet_test).etapes ==
            [1, 0, 2, 3]).all()
    
    
if __name__=="__main__":
    NewYork = Ville()
    NewYork.aleatoire()
    
    test_ville_aleatoire()