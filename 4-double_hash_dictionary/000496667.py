"""
Nom : Bourgeois
Prénom : Noé
Matricule : 000496667
"""

import numpy


class Dict:
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
            if self.table[i] != []:
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
                self.keys.add(k)
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
                    self.keys.add(k)
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
        :return: value linked to k if k in dict else IndexError
        """

        if self.m == 1 and self.table[0][0] == k:
            return self.table[0][1]
        elif 1 < self.m:
            found = False
            i = 0
            while not found:
                j = self.double_h(k, i) % self.m
                if k == self.table[self.double_h(k, i) % self.m][0]:
                    # found = True
                    return self.table[self.double_h(k, i) % self.m][1]
                else:
                    i += 1
        else:
            raise IndexError

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        return self.search(k)


if __name__ == '__main__':
    d = Dict(100)
    keys = [
        'Leonhard',
        'Dénes',
        'Paul',
        'Graham',
        'László'
    ]
    values = [
        'Euler',
        'Kőnig',
        'Erdős',
        'Brightwell',
        'Babai'
    ]
    for k, v in zip(keys, values):
        d[k] = v
    assert len(d) == 5
    d['László'] = 'Lovász'
    assert len(d) == 5
    assert d.load_factor == .05

    d = Dict(1)
    d['Leonhard'] = 'Euler'
    # print(d.double_h('Leonhard', 0) % 1)
    # print(d.double_h('Paul', 0) % 1)
    try:
        name = d['Paul']
        # print("name: ", name)
    except Exception as e:
        assert isinstance(e, IndexError)
    else:
        assert False

    try:
        d['Paul'] = 'Graham'
    except Exception as e:
        assert isinstance(e, OverflowError)
    else:
        assert False
