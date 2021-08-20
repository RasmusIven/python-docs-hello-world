from dataclasses import dataclass, field

#------------------------------------- Highlight ---------------------------------------#

@dataclass
class Highlight:
    """ Highlight class, representing a text span, associated to a DCR element. """
    start: int
    end: int
    text: str = field(default_factory=str)
    
    def span(self) -> list:
        return [self.start, self.end]

    def __eq__(self, o: object):
        """ Compares two Highlights by checking if the ranges overlap."""
        return (self.end >= o.start) and (o.end >= self.start)
 
 
#------------------------------------- DCR Elements ---------------------------------------#   

@dataclass
class Element:
    """Base class for handeling an edge or node element of a DCR graph. """
    ID: str 
    type: str
    highlights: list = field(default_factory=list)
   
    def spans(self):
        return [H.span() for H in self.highlights]

    def __eq__(self, o: object):
        return self.ID == o.ID

@dataclass
class Activity(Element):
    """ DCR Activity """
    ID: str
    type: str = 'ACTIVITY'
    #Needs implementation: is_subprocess?
    #Needs implementation: role_of_activity

@dataclass
class Role(Element):
    """ DCR Role """
    ID: str
    type: str = 'ROLE'

@dataclass
class Rule(Element):
    """ DCR Rule """
    ID: str
    type: str = 'RULE'
    #Needs implementation: rule_type
    #Needs implementation: target
    #Needs implementation: source


#------------------------------------- DCR Graph ---------------------------------------#

@dataclass
class Graph:
    """ Handles a DCR Graph. """
    activities: list = field(default_factory=list)
    roles: list = field(default_factory=list)
    rules: list = field(default_factory=list)

    def add(self, e):
        """ Add an element to the DCR Graph. """
        if e.type == 'ACTIVITY' or 'activity':
            self.activities.append(e)
        elif e.type == 'ROLE' or 'role':
            self.roles.append(e)
        elif e.type == 'RULE' or 'rule':
            self.rules.append(e)
        else:
            raise ValueError(f"{e.type} type not parsed correctly. Only accepts 'ACTIVITY', 'ROLE' and 'RULE'")
            
    def remove(self, e):
        """ Remove an element from the DCR Graph. """
        if e.type == 'ACTIVITY' or 'activity':
            if e in self.activities:
                self.activities.remove(e)
        elif e.type == 'ROLE' or 'role':
            if e in self.roles:
                self.roles.remove(e)
        elif e.type == 'RULE' or 'rule':
            if e in self.rules:
                self.rules.remove(e)
        else:
            raise ValueError(f"{e.type} type not parsed correctly. Only accepts 'ACTIVITY', 'ROLE' and 'RULE'")
    
    def get(self, type):
        """ Returns a list of elements of a specific type. """
        if type == 'ACTIVITY' or 'activity':
            return self.activities
        elif type == 'ROLE' or 'role':
            return self.roles
        elif type == 'RULE' or 'rule':
            return self.rules
        else:
            raise ValueError(f"{type} type not parsed correctly. Only accepts 'ACTIVITY', 'ROLE' and 'RULE'")
        
    def all(self):
        """ Returns a list of all elements of the DCR Graph. """
        elements = []
        elements.append(self.activities)
        elements.append(self.roles)
        elements.append(self.rules)
        return elements
            