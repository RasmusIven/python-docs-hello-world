from dataclasses import dataclass, field
import DCR.structure as DCR

#------------------------------------- Matchers ---------------------------------------#

@dataclass
class Match:
    """ A match of two DCR Graph elements. """
    a: DCR.Element
    b: DCR.Element
    
    def contain(self, other):
        return (self.a == other) or (self.b == other)
    
    
@dataclass
class Matcher:
    """ Abstract class for matching DCR Graph elements. """
    source: DCR.Graph
    target: DCR.Graph  
    compare_types: list
    matches: list  = field(default_factory=list)
    
@dataclass 
class SpanMatcher(Matcher):
    """ Compare spans of highlights, to find matching elements. """
    def __post_init__(self):
        self.matches = self.compare_spans()
        
    def compare_spans(self):
        matches = []
        for type in self.compare_types:
            for a_element in self.source.get(type):
                for b_element in self.target.get(type):
                    for a_span in a_element.spans():
                        for b_span in b_element.spans():
                            if a_span == b_span:
                                matches.append(Match(a_element, b_element))
        
        return matches
 
@dataclass 
class LabelMatcher(Matcher):
    #Not implemented yet
    pass

@dataclass 
class RoleMatcher(Matcher):
    #Not implemented yet
    pass

@dataclass 
class RuleMatcher(Matcher):
    #Not implemented yet
    pass
 
 
#------------------------------------- Compare Handler ---------------------------------------#

@dataclass
class Compare:
    """ Given two DCR Graphs, compares them to get the intersection. Compare types and compare methods are given as parameters for the comparison. """
    source: DCR.Graph
    target: DCR.Graph
    compare_types: list
    compare_methods: list
    union: DCR.Graph = field(default_factory=DCR.Graph)
    remaining: DCR.Graph = field(default_factory=DCR.Graph)
    intersection: DCR.Graph  = field(default_factory=DCR.Graph)

    def update(self, matches):
        """ update remaining and intersection with list of matches. """
        for match in matches:
            for element in self.remaining.all():
                if match.contain(element):
                    self.remaining.remove(element)
                    
            if match.a not in self.intersection.all() or match.b not in self.intersection.all():
                self.intersection.add(match.a)
                self.intersection.add(match.b)

    def __post_init__(self):
        """ Creates the union and remaining. Depending on compare method, update remaining and intersection."""
        for type in self.compare_types:
            for element in self.source.get(type):
                self.union.add(element)
            for element in self.target.get(type):
                self.union.add(element)
        self.remaining = self.union
            
        for method in self.compare_methods:
            if method == 'spans':  
                spans = SpanMatcher(self.source, self.target, self.compare_types)
                self.update(spans.matches)
            
            elif method == 'labels':
                labels = LabelMatcher(self.source, self.target, self.compare_types)
                self.update(labels.matches)
                
            elif method == 'compositions':
                roles = RoleMatcher(self.source, self.target, self.compare_types)
                self.update(roles.matches)
                
                rules = RuleMatcher(self.source, self.target, self.compare_types)
                self.update(rules.matches)  
 
 
#------------------------------------- Evaluation ---------------------------------------#       

class Evaluator:
    """ Evaluate a comparison, getting a simularity score. Evaluation method is given as a parameter. """
    def __init__(self, comparison, evaluation_method):
        self.comparison = comparison
        self.method = evaluation_method
        self.simularity = self.evaluate()
    
    def percentage(part, whole):
        if part > 0 and whole > 0:
            return 100 * float(part)/float(whole)
        else:
            return 0
    
    def evaluate(self):
        """ Initialize the method chosen by the user, and gets the simularity. """
        evaluation = 0
        if self.method == 'union':
            evaluation = self.union_score()
        elif self.method == 'source_intersection':
            evaluation = self.intersection_score()
        else:
            raise ValueError(f'Comparison Method > {self.method} < not recognized.')
        return evaluation

    def union_score(self):
        """ Returns a percentage score of the intersection part of union. """
        whole = len(self.comparison.union.all())
        part = len(self.comparison.intersection.all())
        return self.percentage(part, whole)
    
    def source_intersection_score(self):
        """ Returns a percentage score of the intersection part of source. """
        left_side = DCR.Graph()
        for element in self.comparison.remaining.all():
            if element in self.comparison.source.all():
                left_side.add(element)
        whole = len(left_side.source.all())
        part = len(self.comparison.intersection.all())
        return self.percentage(part, whole)
