from projet3 import *
import prenoms
from time import time

size = 100

doa = DictOpenAddressing(size)
dcl = DictChainingLinkedList(size)
dcs = DictChainingSkipList(size)

for d in (doa, dcl, dcs):
    print(d)
    insertion_survey_nb_at_size = {}
    insertion_time_at_size = {}
    insertion_error_at_size = {}

    search_survey_nb_at_size = {}
    search_time_at_size = {}
    search_error_at_size = {}

    deletion_survey_nb_at_size = {}
    deletion_time_at_size = {}
    deletion_error_at_size = {}

    insertion_survey_nb_at_size[size] = []
    insertion_time_at_size[size] = []
    insertion_error_at_size[size] = []
    insertionError = False

    search_survey_nb_at_size[size] = []
    search_time_at_size[size] = []
    search_error_at_size[size] = []
    searchError = False

    deletion_survey_nb_at_size[size] = []
    deletion_time_at_size[size] = []
    deletion_error_at_size[size] = []
    deletionError = False

    for insertion in range(size):
        prenom = prenoms.get_prenom()
        nom = prenoms.get_nom()
        d.insert(prenom, nom)

        if d.load_factor in (1/5, 2/5, 3/5, 4/5):
            prenom = prenoms.get_prenom()
            nom = prenoms.get_nom()
            print(prenom, nom)

            insertion_start = time()
            try:
                survey_nb = d.insert(prenom, nom)
                last_prenom_inserted = prenom
            except OverflowError:
                print('Overflowerror')
                insertionError = True
                survey_nb = 'error'

            insertion_time = time() - insertion_start
            if insertionError:
                insertion_error_at_size[size].append(insertion_time)
            else:
                insertion_error_at_size[size].append(None)

            insertion_survey_nb_at_size[size].append(survey_nb)
            insertion_time_at_size[size].append(insertion_time)

            search_start = time()
            try:
                survey_nb = d.search(last_prenom_inserted,
                                     survey_nb_check=True)
            except KeyError:
                searchError = True

            search_time = time() - search_start
            if searchError:
                search_error_at_size[size].append(search_time)

            else:
                search_error_at_size[size].append(None)
            search_survey_nb_at_size[size].append(survey_nb)
            search_time_at_size[size].append(search_time)

            deletion_start = time()
            try:
                survey_nb = d.delete(last_prenom_inserted)
            except KeyError:
                deletionError = True

            deletion_time = time() - deletion_start
            if deletionError:
                error = deletion_time
            else:
                error = None
            deletion_error_at_size[size].append(error)
            deletion_survey_nb_at_size[size].append(survey_nb)
            deletion_time_at_size[size].append(deletion_time)

    print("insertion_survey_nb_at_size:", insertion_survey_nb_at_size, "\n",
          "insertion_time_at_size:", insertion_time_at_size, "\n",
          "insertion_error_at_size:", insertion_error_at_size, "\n",

          "search_survey_nb_at_size:", search_survey_nb_at_size, "\n",
          "search_time_at_size:", search_time_at_size, "\n",
          "search_error_at_size:", search_error_at_size, "\n",

          "deletion_survey_nb_at_size:", deletion_survey_nb_at_size, "\n",
          "deletion_time_at_size:", deletion_time_at_size, "\n",
          "deletion_error_at_size:", deletion_error_at_size)
