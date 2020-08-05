
#spare code to explore KG
        # get predicates using ID
        #
        # predicatesForSubject = ep.getPredicatesForSubject(ent2, 10)
        # for p in predicatesForSubject:
        #     print('predicates for subject using ID', p)
        #
        # predicatesForObject = ep.getPredicatesForObject(ent2, 10)
        # for p in predicatesForObject:
        #     print('predicates for object using ID', p)
        #
        # print("Domain types")
        # types_domain = ep.getTopTypesUsingPredicatesForSubject(ent2, 3)
        # for t in types_domain:
        #     print('top types using predicates for subject', t)
        #
        # print("Range types")
        # types_range = ep.getTopTypesUsingPredicatesForObject(ent2, 3)
        # for t in types_range:
        #     print('top types using predicates for object', t)
        #
        # labels = []

        # get class siblings to create additional training data

        # for c in cls:  # for each class
        #     print('c', c)
        #     entities2 = ep.getEntitiesForType(c, 0, 5)
        #     print('entities for types from original entity', entities2)  # http://dbpedia.org/resource/Axel_Anderberg

            # entities_labels = ep.getEntitiesLabelsForType(c, 0, 5)
            # for e, label in entities_labels.items():
            #     print('ent', e, 'label', label)
            #     label = str(label)
            #     label = re.sub('}', '', label)
            #     label = re.sub('{', '', label)
            #     label = re.sub('\'', '\"', label)
            #     labels.append(label)

            # class_labels = ep.createSPARQLEntitiesLabelsForClass(c,0,5)
            # print('class labels', class_labels)
            # for lb in class_labels:
            #     print('class label', lb)
            #     print('test', onto_access.getClassByName(lb))
            #     print('test', onto_access.getClassByName(lb).descendants())
            #     print('test', onto_access.getClassByName(lb).ancestors())

    #         eq_class = ep.getEquivalentClasses(c)
    #         for cl in eq_class:
    #             print('equivalent classes', cl)
    #
    #         sup2dist = ep.getDistanceToAllSuperClasses(c)
    #         print('distance to sup', len(sup2dist), sup2dist)
    #
    #         sub2dist = ep.getDistanceToAllSubClasses(c)
    #         print('distance to sub', len(sub2dist), sub2dist)
    #
    # return







# wikidata

# look up in WD KG
# wikidata = WikidataAPI()
# entities = wikidata.getKGEntities(w, limit)
# print("Entities from Wikidata:")
# for ent in entities:
#     print(ent)
# print("\n")

# ep = WikidataEndpoint()
# types = ep.getAllTypesForEntity("http://www.wikidata.org/entity/Q22")
# print(len(types), types)

# equiv = ep.getEquivalentClasses(c)
# print(len(equiv), equiv)

# same = ep.getSameEntities(ent2)
# print(len(same), same)

# gt_cls = "http://www.wikidata.org/entity/Q5"
# sup2dist = ep.getDistanceToAllSuperClasses(gt_cls)
# print(len(sup2dist), sup2dist)
#
# sub2dist = ep.getDistanceToAllSubClasses(gt_cls, 2)
# print(len(sub2dist), sub2dist)