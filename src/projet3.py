"""
Nom : Bourgeois
Prénom : Noé
Matricule : 000496667
"""

import numpy
from random import random
from math import log


class Dict:
    def __init__(self, m):
        self.m = m
        self.table = [[] for i in range(m)]
        self.keys = set()  # set element search faster

    def __len__(self):
        """
        :param self:
        :return: container keys quantity
        """
        return len(self.keys)

    @property
    def load_factor(self):
        """
        :return: load factor α ∈ [0,1]
        """
        return len(self) / self.m

    def kr(self, k):
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

    def djb2(self, k):
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

    def h(self, k):
        pass

    def double_h(self, k, survey_nb):
        pass

    def get_hk(self, k, survey_nb=None):
        if 1 == self.m:
            return 0
        else:
            if survey_nb is not None:
                return self.double_h(k, survey_nb) % self.m
            else:
                return self.h(k) % self.m

    def get_entry_for(self, k):
        return self.table[self.get_hk(k, survey_nb=None)]

    def insert(self, k, v):
        pass

    def search(self, k):
        pass

    def delete(self, k):
        pass

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        return self.search(k)

    def __delitem__(self, k):
        self.delete(k)


class DictOpenAddressing(Dict):
    def __init__(self, m):
        super().__init__(m)

    def double_h(self, k, i):
        """
        hashes k with combined use of kr & djb2
        :param k: str: key
        :param i: int: iter
        :return: int
        """
        return self.kr(k) + (i * self.djb2(k))

    def insert(self, k, v, survey_nb=False):
        """
        inserts [k, v] or v if k already in dict
        :param survey_nb:
        :param k: key
        :param v: value linked to key k
        :return: None or OverflowError exception if no free location was
        found
        """
        survey_nb = 0
        if 1 == self.m:
            if not self.table[0]:
                self.table[0] = [k, v]
                self.keys.add(k)
            elif self.table[0][0] == k:
                self.table[0][-1] = v
            else:
                raise OverflowError
            survey_nb = 1

        elif 1 < self.m:
            survey_nb = self.search(k, v, insert=True)

        return survey_nb

    def search(self, k, v=None,
               survey_nb=False,
               survey_nb_check=False,
               insert=False,
               delete=False):
        """
        :param v:
        :param insert:
        :param delete:
        :param survey_nb:
        :param k: key
        :return: value linked to k if k in dict else KeyError
        """
        survey_nb = 0
        if insert or k in self.keys:
            while survey_nb < self.m:
                hk = self.get_hk(k, survey_nb)

                if not self.table[hk] or self.table[hk] == "deleted":
                    if insert:
                        self.table[hk] = [k, v]
                        self.keys.add(k)
                        return survey_nb
                    else:
                        if self.table[hk] == "deleted":
                            survey_nb += 1

                elif self.table[hk][0] == k:
                    if insert:
                        self.table[hk][1] = v
                    elif delete:
                        self.table[hk] = "deleted"
                        self.keys.remove(k)
                    else:   # search
                        if survey_nb_check:
                            return survey_nb
                        else:
                            return self.table[hk][1]
                    return survey_nb
                else:
                    survey_nb += 1

            raise OverflowError

        else:
            raise KeyError

    def delete(self, k, survey_nb=False):
        """
        remplace la paire clé(k)-valeur si k est trouvé,
        leve une KeyError sinon
        :param k:
        :param survey_nb:
        :return:
        """
        survey_nb = self.search(k, delete=True)
        return survey_nb


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

    def setValue(self, newalue):
        self.value = newalue

    def setNext(self, newnext):
        self.next = newnext


class LinkedList:
    def __init__(self):
        self.head = None
        self.keys = set()

    def isEmpty(self):
        return self.head is None

    def length(self):
        return len(self.keys)

    def add(self, key, value):
        temp = Node(key, value)
        temp.setNext(self.head)
        self.head = temp
        self.keys.add(key)

    def get_value_of(self, key, survey_nb_check=False):
        current = self.head
        found = False
        survey_nb = 0
        while current is not None and not found:
            if current.getKey() == key:
                if survey_nb_check:
                    return survey_nb
                else:
                    return current.getValue()
            else:
                current = current.getNext()
                survey_nb +=1

    def remove(self, key, survey_nb_check=False):
        survey_nb = 0
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
                survey_nb += 1
        # if survey_nb_check:
        return survey_nb


class DictChaining(Dict):
    def __init__(self, m):
        super().__init__(m)

    def h(self, k):
        return self.djb2(k)


class DictChainingLinkedList(DictChaining):
    def __init__(self, m):
        super().__init__(m)
        self.table = [LinkedList() for _ in range(m)]

    def insert(self, k, v, survey_nb_check=False):
        """ l’insertion dans un liste chaˆın´ee se fait en d´ebut de
        chaˆıne"""
        survey_nb = 1
        entry = self.get_entry_for(k)

        if k in entry.keys:
            current = entry.head
            found = False
            while current is not None and not found:
                if current.getKey() == k:
                    found = True
                    current.setValue(v)
                else:
                    current = current.getNext()
                    survey_nb += 1
        else:
            entry.add(k, v)
            self.keys.add(k)

        return survey_nb

    def search(self, k, survey_nb_check=False):
        """
        :param k: key
        :return: value linked to k if k in dict else KeyError
        """
        if k in self.keys:
            return self.get_entry_for(k).get_value_of(k, survey_nb_check)
        else:
            raise KeyError

    def delete(self, k, survey_nb_check=False):
        entry = self.get_entry_for(k)
        survey_nb = entry.remove(k)
        self.keys.remove(k)
        return survey_nb


class End(object):
    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __gt__(self, other):
        return True


NIL = Node(End(), End(), next=[], width=[])


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

    def insert(self, key, value, survey_nb_check=False):
        survey_nb = 1   # search for entry
        chain = [None] * self.maxlevels
        steps_at_level = [0] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            level_next_key = node.next[level].key
            while level_next_key <= key:
                # print(level_next_key, key)

                steps_at_level[level] += node.width[level]
                node = node.next[level]
                level_next_key = node.next[level].key
                survey_nb += 1
            chain[level] = node
        d = 1
        while d < self.maxlevels and random() < 0.5:
            d += 1
        newnode = Node(key, value, [None] * d, [None] * d)
        steps = 0
        for level in range(d):
            prevnode = chain[level]
            newnode.next[level] = prevnode.getNext()[level]
            prevnode.next[level] = newnode
            newnode.width[level] = prevnode.width[level] - steps
            prevnode.width[level] = steps + 1
            steps += steps_at_level[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] += 1
        self.size += 1
        return survey_nb

    def remove(self, key, survey_nb_check=False):
        survey_nb = 1   # search for entry
        chain = [None] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].key < key:
                node = node.next[level]
                survey_nb += 1
            chain[level] = node
        if key != chain[0].next[0].key:
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

        return survey_nb

    def find(self, key, survey_nb_check=False):
        survey_nb = 1   # search for entry
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].getKey() < key:
                node = node.next[level]
        node = node.next[0]
        if node.getKey() == key:
            return survey_nb, node
        return None

    def find_value_of(self, key, survey_nb_check=False):
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].getKey() < key:
                node = node.next[level]
        node = node.next[0]
        if node.getKey() == key:
            return node.getValue()
        return None


class DictChainingSkipList(DictChaining):
    def __init__(self, m):
        super().__init__(m)
        self.table = [Skiplist() for i in range(m)]

    def insert(self, k, v, survey_nb_check=False):
        skiplist = self.get_entry_for(k)
        if k in self.keys:
            survey_nb, node = skiplist.find(k, survey_nb_check)
            node.setValue(v)
        else:
            survey_nb = skiplist.insert(k, v, survey_nb_check)
        self.keys.add(k)
        return survey_nb

    def search(self, k, survey_nb_check=False):
        """
        :param k: key
        :return: value linked to k if k in dict else KeyError
        """

        if k in self.keys:
            survey_nb, node = self.get_entry_for(k).find(k,
                                                        survey_nb_check)
            if survey_nb_check:
                return survey_nb
            else:
                return node.getValue()
        else:
            raise KeyError

    def delete(self, k, survey_nb_check=False):
        survey_nb = self.get_entry_for(k).remove(k, survey_nb_check)
        self.keys.remove(k)
        return survey_nb
