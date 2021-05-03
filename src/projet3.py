"""
Nom : Bourgeois
Prénom : Noé
Matricule : 000496667
"""

import numpy
from random import random
from math import log


class DictOpenAddressing:
    def __init__(self, m):
        self.m = m
        self.table = [[] for i in range(m)]

    def __len__(self):
        """
        :param self:
        :return: container keys quantity
        """
        keys_quantity = 0
        for i in range(self.m):
            if self.table[i]:
                keys_quantity += 1
        return keys_quantity

    @property
    def load_factor(self):
        """
        :return: load factor α ∈ [0,1]
        """
        return len(self) / self.m

    def h1(self, k):
        """
        Kernighan & Ritchie Algorithm
        :param k: str: key
        :return: 32 bits int
        """
        hashkey = 0
        for char in k:
            hashkey = hashkey + ord(char)
        # print('kr', hashkey)
        return hashkey

    def h2(self, k):
        """
        Daniel J. Bernstein djb2 Algorithm
        :param k: str: key
        :return: int
        """
        hash = numpy.uint32(0x1505)
        for char in k:
            hash = 33 * hash + ord(char)
        # print('djb2', numpy.uint32(hash))
        return numpy.uint32(hash)

    def double_h(self, k, i):
        """
        hashes k with combined use of h1 & h2
        :param k: str: key
        :param i: int: iter
        :return: int
        """
        return self.h1(k) + (i * self.h2(k))

    def insert(self, k, v):
        """
        inserts [k, v] or v if k already in dict
        :param k: key
        :param v: value linked to key k
        :return: None or OverflowError exception if no free location was
        found
        """
        if 1 == self.m:
            if not self.table[0]:
                self.table[0] = [k, v]
            elif self.table[0][0] == k:
                self.table[0][-1] = v
            else:
                raise OverflowError

        elif 1 < self.m:
            inserted = False
            i = 0
            while not inserted:
                j = self.double_h(k, i) % self.m
                # print('hashtable index', j)
                if not self.table[j]:
                    self.table[j] = [k, v]
                    inserted = True
                elif self.table[j][0] == k:
                    self.table[j][-1] = v
                    inserted = True
                else:
                    i += 1
        else:
            raise OverflowError

    def search(self, k):
        """
        :param k: key
        :return: value linked to k if k in dict else KeyError
        """

        if self.m == 1 and self.table[0][0] == k:
            return self.table[0][1]
        elif 1 < self.m:
            found = False
            i = 0
            j = self.double_h(k, i) % self.m
            while not found and j:
                if k == self.table[j][0]:
                    # found = True
                    return self.table[j][1]
                else:
                    i += 1
                    j = self.double_h(k, i) % self.m
        else:
            raise KeyError

    def delete(self, k):
        """La suppression d’un ´el´ement dans une table de hachage `a adressage ouvert n’est pas triviale. En effet puisque
        l’adressage ouvert consiste en un sens a simuler le chaınage des elements dont la clef est hachee vers la meme
        valeur en utilisant des cellules libres de la table, mettre un ´el´ement quelconque `a None revient `a casser la
        liste chaˆın´ee en retirant un ´el´ement et tous les suivants. Il est donc important de maintenir la structure afin
        de pouvoir tout de mˆeme faire une recherche sur les ´el´ements qui suivent dans la table.
        Une solution est de marquer les cellules de la table qui ont contenu une entr´ee dans le pass´e
        mais qui ont ´et´e supprim´ees depuis. Ainsi, lors de l’ex´ecution de la m´ethode search, ces cellules ne forceront
        pas l’arrˆet de la boucle, mais la recherche continuera bien jusqu’`a trouver soit None soit une entr´ee de la clef
        recherch´ee."""
        if self.m == 1 and self.table[0][0] == k:
            return self.table[0][1]
        elif 1 < self.m:
            found = False
            i = 0
            j = self.double_h(k, i) % self.m
            while not found and j:
                if k == self.table[j][0]:
                    found = True
                    self.table[j][1] = "deleted"
                else:
                    i += 1
                    j = self.double_h(k, i) % self.m
        else:
            raise KeyError

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        return self.search(k)

    def __delitem__(self, k):
        self.delete(k)


class Node:
    def __init__(self, key, value, next=None, width=None):
        self.key = key
        self.value = value
        self.next = next
        self.width = width

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


class LinkedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head is None

    def length(self):
        current = self.head
        count = 0
        while current is not None:
            count = count + 1
            current = current.getNext()
        return count

    def add(self, key, value):
        temp = Node(key, value)
        temp.setNext(self.head)
        self.head = temp

    def addAfter(self, base, key, value):
        temp = Node(key, value)
        temp.setNext(base.getNext())
        base.setNext(temp)

    def search(self, key):
        current = self.head
        found = False
        while current is not None and not found:
            if current.getKey() == key:
                found = True
            else:
                current = current.getNext()
        return found

    def get_value_of(self, key):
        current = self.head
        found = False

        while current is not None and not found:
            if current.getKey() == key:
                return current.getValue()
            else:
                current = current.getNext()

    def remove(self, key):
        previous = None
        current = self.head
        found = False
        while current is not None and not found:
            if current.getKey == key:
                found = True
                if previous is not None:
                    previous.setNext(current.getNext())
                else:
                    self.head = current.getNext()
            else:
                previous = current
                current = current.getNext()


class DictChainingLinkedList:
    def __init__(self, m):
        self.m = m
        self.table = [LinkedList for i in range(m)]

    def __len__(self):
        """
        :param self:
        :return: container keys quantity
        """
        keys_quantity = 0
        for i in range(self.m):
            keys_quantity += self.table[i].length()
        return keys_quantity

    def h(self, k):
        """
        Daniel J. Bernstein djb2 Algorithm
        :param k: str: key
        :return: int
        """
        hash = numpy.uint32(0x1505)
        for char in k:
            hash = 33 * hash + ord(char)
        # print('djb2', numpy.uint32(hash))
        return numpy.uint32(hash)

    def insert(self, k, v):
        """ l’insertion dans un liste chaˆın´ee se fait en d´ebut de
        chaˆıne"""
        if 1 == self.m:
            hk = 0
        else:
            hk = self.h(k) % self.m
        entry = self.table[hk]
        current = entry().head
        found = False

        while current is not None and not found:
            if current.getKey() == k:
                found = True
                current.setValue(v)
            else:
                current = current.getNext()
        if not found:
            entry().add(k, v)

    def search(self, k):
        """
        :param k: key
        :return: value linked to k if k in dict else KeyError
        """
        if self.m == 1:
            return self.table[0].get_value_of(k)
        elif 1 < self.m:
            j = self.h(k) % self.m
            return self.table[j].get_value_of(k)
        else:
            raise KeyError

    def delete(self, k):
        if 1 == self.m:
            hk = 0
        else:
            hk = self.h(k) % self.m
        entry = self.table[hk]
        entry.remove(k)

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        return self.search(k)

    def __delitem__(self, k):
        self.delete(k)


class End(object):
    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __gt__(self, other):
        return True


NIL = Node(End(), [], [])


class Skiplist:
    def __init__(self, expected_size=100):
        self.size = 0
        self.maxlevels = int(1 + log(expected_size, 2))
        self.head = Node(key='HEAD',
                         value='HEAD',
                         next=[NIL] * self.maxlevels,
                         width=[1] * self.maxlevels)

    def __getitem__(self, i):
        node = self.head
        i += 1
        for level in reversed(range(self.maxlevels)):
            while node.width[level] <= i:
                i -= node.width[level]
                node = node.next[level]
        return node.value

    def insert(self, key, value):
        chain = [None] * self.maxlevels
        steps_at_level = [0] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value <= value:
                steps_at_level[level] += node.width[level]
                node = node.next[level]
            chain[level] = node
        d = 1
        while d < self.maxlevels and random() < 0.5:
            d += 1
        newnode = Node(key, value, [None] * d, [None] * d)
        steps = 0
        for level in range(d):
            prevnode = chain[level]
            newnode.next[level] = prevnode.next[level]
            prevnode.next[level] = newnode
            newnode.width[level] = prevnode.width[level] - steps
            prevnode.width[level] = steps + 1
            steps += steps_at_level[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] += 1
        self.size += 1

    def remove(self, value):
        chain = [None] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value < value:
                node = node.next[level]
            chain[level] = node
        if value != chain[0].next[0].value:
            raise KeyError('NotFound')
        d = len(chain[0].next[0].next)
        for level in range(d):
            prevnode = chain[level]
            prevnode.width[level] += prevnode.next[level].width[
                                         level] - 1
            prevnode.next[level] = prevnode.next[level].next[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] -= 1
        self.size -= 1

    def find(self, value):
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value < value:
                node = node.next[level]
        node = node.next[0]
        if node.value == value:
            return node
        return None


class DictChainingSkipList:
    def __init__(self, m):
        self.m = m
        self.table = [Skiplist for i in range(m)]

    def __len__(self):
        """
        :param self:
        :return: container keys quantity
        """
        keys_quantity = 0
        for i in range(self.m):
            keys_quantity += self.table[i].length()
        return keys_quantity

    def h(self, k):
        """
        Daniel J. Bernstein djb2 Algorithm
        :param k: str: key
        :return: int
        """
        hash = numpy.uint32(0x1505)
        for char in k:
            hash = 33 * hash + ord(char)
        # print('djb2', numpy.uint32(hash))
        return numpy.uint32(hash)

    def get_entry_for(self, k):
        if 1 == self.m:
            hk = 0
        else:
            hk = self.h(k) % self.m
        return self.table[hk]

    def insert(self, k, v):
        self.get_entry_for(k).insert(k, v)

    def search(self, k):
        """
        :param k: key
        :return: value linked to k if k in dict else KeyError
        """
        self.get_entry_for(k).find(k)

    def delete(self, k):
        self.get_entry_for(k).remove(k)

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        return self.search(k)

    def __delitem__(self, k):
        self.delete(self, k)
