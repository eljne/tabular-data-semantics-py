'''
Created on 2 Jan 2019

@author: ejimenez-ruiz
'''
from owlready2 import *


class OntologyAccess(object):
    '''
    classdocs
    '''


    def __init__(self, urionto):
        
        self.urionto = urionto
        
        #List from owlready2
        #onto_path.append(pathontos) #For local ontologies
        
    
    
    def loadOntology(self, classify):   
        
        self.onto = get_ontology(self.urionto)
        self.onto.load()
        
        #self.classifiedOnto = get_ontology(self.urionto + '_classified')        
        if classify:
            with self.onto:
                sync_reasoner()  #it does add inferences to ontology
            
        #report problem with unsat (Nothing not declared....)
        #print(list(self.onto.inconsistent_classes()))
        
    
    
    def getOntology(self):
        return self.onto
    
    
    #Does not seem to be a better way (or working way) according to the documentation...
    def getClassByURI(self, uri):
        
        for cls in list(self.getOntology().classes()):
            if (cls.iri==uri):
                return cls
            
        return None
            
    
    def getClassByName(self, name):
        
        for cls in list(self.getOntology().classes()):
            if (cls.name.lower()==name.lower()):
                return cls
            
        return None
    
    
    def getClassObjectsContainingName(self, name):
        
        classes = []
        
        for cls in list(self.getOntology().classes()):
            if (name.lower() in cls.name.lower()):
                classes.append(cls)
            
        return classes
    
    
    def getClassIRIsContainingName(self, name):
        
        classes = []
        
        for cls in list(self.getOntology().classes()):
            if (name.lower() in cls.name.lower()):
                classes.append(cls.iri)
            
        return classes

    def getClassIRIsContainingNameLimit(self, name, limit):

        classes = []

        for cls in list(self.getOntology().classes()):
            if (name.lower() in cls.name.lower()):
                classes.append(cls.iri)

        classes = classes[0:limit-1]
        return classes

    def getAncestorsURIsMinusClass(self,cls):
        ancestors_str = self.getAncestorsURIs(cls)
        
        ancestors_str.remove(cls.iri)
        
        return ancestors_str

    def getAncestorsURIs(self,cls):
        ancestors_str = set()
        
        for anc_cls in cls.ancestors():
            ancestors_str.add(anc_cls.iri)
        
        return ancestors_str    

    def getDescendantURIs(self,cls):
        descendants_str = set()
        
        for desc_cls in cls.descendants():
            descendants_str.add(desc_cls.iri)
        
        return descendants_str    

    def getDescendantNames(self,cls):
        descendants_str = set()
        
        for desc_cls in cls.descendants():
            descendants_str.add(desc_cls.name)
    
        return descendants_str

    def getDescendantNamesForClassName(self, cls_name):
        
        cls = self.getClassByName(cls_name)
        
        descendants_str = set()
        
        for desc_cls in cls.descendants():
            descendants_str.add(desc_cls.name)
    
        return descendants_str

    def isSubClassOf(self, sub_cls1, sup_cls2):
        
        if sup_cls2 in sub_cls1.ancestors():
            return True
        return False

    def isSuperClassOf(self, sup_cls1, sub_cls2):
        
        if sup_cls1 in sub_cls2.ancestors():
            return True
        return False
    
    
    
    
        

class DBpediaOntology(OntologyAccess):
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getOntologyIRI())
        
        
    def getOntologyIRI(self):
        return "http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
    
    
    def getAncestorsURIs(self,cls):
        ancestors_str = set()
        
        for anc_cls in cls.ancestors():
            ancestors_str.add(anc_cls.iri)
        
        agent = "http://dbpedia.org/ontology/Agent"
        if agent in ancestors_str:
            ancestors_str.remove(agent)
        
        return ancestors_str
    
    
class SchemaOrgOntology(OntologyAccess):
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getOntologyIRI())
        
        
    def getOntologyIRI(self):
        return "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
        
    

if __name__ == '__main__':

    #folder_ontos="/home/ejimenez-ruiz/eclipse-python/TabularSemantics/ontologies/"
    uri_onto="http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
    uri_onto="http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
    #uri_onto="file:///home/ejimenez-ruiz/eclipse-python/TabularSemantics/ontologies/dbpedia.owl"
    #uri_onto="file:///home/ejimenez-ruiz/eclipse-python/TabularSemantics/ontologies/schema.org.owl"
    
    #onto_access = OntologyAccess(uri_onto)
    
    
    onto_access = DBpediaOntology()
    #onto_access = SchemaOrgOntology()
    
    onto_access.loadOntology(True)

    onto_access.getAncestorsURIs(onto_access.getClassByName("gymnast")) #ancestors

    
    print(onto_access.getClassIRIsContainingName("player"))
    print(onto_access.getClassIRIsContainingName("actor"))


    
    #
    # print('1', onto_access.getClassByName("gymnast"))
    # print('2', onto_access.getClassByName("gymnast").descendants())
    # print('3', onto_access.getClassByName("gymnast").ancestors())
    # print('4', onto_access.getDescendantURIs(onto_access.getClassByName("gymnast")))

    t = "gymnast"
    print('ancestors', onto_access.getAncestorsURIs(onto_access.getClassByName(t)))
    test = onto_access.getAncestorsURIs(onto_access.getClassByName(t))
    test2 = test.pop()
    print('ancestor', test2)
    test3 = onto_access.getClassByURI(test2)
    print(test3)

    try:
        siblings2 = onto_access.getDescendantNames(test3)
        print('siblings2', siblings2)
        sibling2 = siblings2.pop()
        print('sibling2', sibling2)
    except:
        print(";)")

'''
    ancestors
    {'http://schema.org/Person', 'http://www.wikidata.org/entity/Q215627', 'http://www.w3.org/2002/07/owl#Thing',
     'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#Agent', 'http://dbpedia.org/ontology/Athlete',
     'http://www.wikidata.org/entity/Q24229398', 'http://dbpedia.org/ontology/Person',
     'http://www.wikidata.org/entity/Q5', 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#NaturalPerson',
     'http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/ontology/Gymnast'}
    ancestor
    http: // schema.org / Person
    schema.org.Person
    siblings2
    {'Q2526255', 'SongWriter', 'Lieutenant', 'FormulaOneRacer', 'NaturalPerson', 'Q3055126', 'HorseTrainer',
     'RallyDriver', 'Q488111', 'Q214917', 'Q901', 'PokerPlayer', 'Q1930187', 'ComicsCharacter', 'Q2566598',
     'Politician', 'HighDiver', 'Dancer', 'HandballPlayer', 'GridironFootballPlayer', 'PlayWright',
     'MemberResistanceMovement', 'AthleticsPlayer', 'Q42178', 'Canoeist', 'BasketballPlayer', 'Ski_jumper', 'Q1028181',
     'ChessPlayer', 'AustralianRulesFootballPlayer', 'Q3501317', 'Governor', 'Farmer', 'Deputy', 'TelevisionDirector',
     'Producer', 'Q131512', 'VolleyballPlayer', 'Q15117302', 'Q14467526', 'Q28389', 'Cleric', 'SnookerPlayer', 'Q40348',
     'Boxer', 'Curler', 'Sculptor', 'AmateurBoxer', 'Priest', 'SumoWrestler', 'Q14128148', 'President', 'NascarDriver',
     'ChristianPatriarch', 'Biologist', 'Q15410431', 'Chef', 'Q4270517', 'Humorist', 'RugbyPlayer', 'Murderer',
     'Q486839', 'Historian', 'ComicsCreator', 'Q753110', 'Poet', 'Engineer', 'Q4964182', 'Q16266334', 'Host', 'Q937857',
     'Q33231', 'Q10871364', 'Q49757', 'TeamMember', 'Q3621491', 'Scientist', 'SpeedwayRider', 'Q378622', 'BeautyQueen',
     'Artist', 'Comedian', 'Q132050', 'Person', 'Swimmer', 'FashionDesigner', 'AmericanFootballCoach', 'Painter',
     'Skater', 'Q628099', 'Q13219587', 'MilitaryPerson', 'Q177220', 'Criminal', 'Coach', 'Ambassador', 'Singer',
     'MartialArtist', 'Writer', 'Linguist', 'RadioHost', 'Aristocrat', 'MotorcycleRider', 'PrimeMinister',
     'Archeologist', 'Q188094', 'Q16533', 'BeachVolleyballPlayer', 'Cricketer', 'DartsPlayer', 'Surfer', 'Astronaut',
     'SoccerPlayer', 'Q4610556', 'TelevisionHost', 'NordicCombined', 'VoiceActor', 'RomanEmperor', 'TableTennisPlayer',
     'Q842606', 'PoliticianSpouse', 'Entomologist', 'Skier', 'IceHockeyPlayer', 'Monarch', 'GaelicGamesPlayer',
     'NationalCollegiateAthleticAssociationAthlete', 'Q121998', 'Q13156709', 'Q95074', 'Egyptologist', 'Senator',
     'Q42603', 'VolleyballCoach', 'Q215627', 'Psychologist', 'Chancellor', 'Royalty', 'Gymnast', 'Q33999',
     'AnimangaCharacter', 'PlayboyPlaymate', 'BusinessPerson', 'Q2159907', 'AdultActor', 'HorseRider', 'Q10833314',
     'Actor', 'Q3282637', 'GolfPlayer', 'DTMRacer', 'Q483501', 'Referee', 'Q30461', 'Q1350189', 'BadmintonPlayer', 'Q5',
     'NarutoCharacter', 'ArcherPlayer', 'Jockey', 'Noble', 'VicePresident', 'Q82955', 'CrossCountrySkier', 'Q10842936',
     'Lawyer', 'BaseballPlayer', 'Q212980', 'ChristianBishop', 'Religious', 'Cyclist', 'Q13365117', 'Q211236',
     'Q13415036', 'Q13382519', 'Baronet', 'Saint', 'SportsTeamMember', 'TheatreDirector', 'BullFighter', 'Medician',
     'Q13414980', 'Biathlete', 'NetballPlayer', 'LacrossePlayer', 'Q43115', 'Q19546', 'SoccerManager', 'Guitarist',
     'CanadianFootballPlayer', 'Athlete', 'MemberOfParliament', 'Model', 'OfficeHolder', 'Congressman', 'SpeedSkater',
     'RacingDriver', 'Journalist', 'Fencer', 'DisneyCharacter', 'SerialKiller', 'Q1198887', 'Celebrity',
     'SoapCharacter', 'MotocycleRacer', 'Q3665646', 'Q36180', 'Mayor', 'Q116', 'Q11631', 'ClassicalMusicArtist',
     'Judge', 'Q855091', 'CollegeCoach', 'Q11774891', 'Presenter', 'Vicar', 'Q3387717', 'FictionalCharacter',
     'ScreenWriter', 'Q484188', 'Pope', 'BritishRoyalty', 'MusicComposer', 'OrganisationMember', 'MotorsportRacer',
     'Q737498Q13381863', 'SnookerChamp', 'MovieDirector', 'Bodybuilder', 'AmericanFootballPlayer', 'Rower',
     'Photographer', 'WaterPoloPlayer', 'SportsManager', 'Q947873', 'Q847400', 'MusicDirector', 'SquashPlayer',
     'Q2722764', 'Q13590141', 'TennisPlayer', 'Instrumentalist', 'Q373085', 'Q10843402', 'MythologicalFigure',
     'VicePrimeMinister', 'Orphan', 'Q15982795', 'TelevisionPersonality', 'Q13382576', 'BackScene', 'Economist',
     'Wrestler', 'Q13561328', 'BobsleighAthlete', 'Cardinal', 'Q81096', 'WinterSportPlayer', 'Architect',
     'MusicalArtist', 'FigureSkater', 'Q30185', 'Professor', 'Q13474373', 'Philosopher', 'Q16278103'}
    sibling2
    Q2526255

'''