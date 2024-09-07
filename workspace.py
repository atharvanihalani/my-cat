# intra-string bonds
# inter-string bridges
# structures of a string
# rules? translated rules? descriptions?


class Workspace():
    """
    
    Features:
        contains various structures
            object descriptions + internal groups + intra-string bonds + inter-string bridges + rules
        how would i store strings?
    
    Properties:

    Methods:
            
    """
    pass


class Structure():
    """
    might make sense as a minimal superclass 'wrapper' OR maybe smtn to associate w/

    Properties:
        strength
        happiness??
    
    Methods:
        smtn to update strength over time?
        generate codelets to create / enhance these structures (based on what criteria?)
    
    """
    pass

class Description():
    """
    these assigned to objects (either strings or groups)
    not sure *how* they're attached to objects
    function of a) description-nodes and b) objects
    
    
    """
    pass


class Bond():
    """
    relations between objects (of the same type!)
    function of a) bond-nodes and b) objects

    again, a common concern is that *where are these structures attached*??
        how are they floating in this cytoplasm?? okay, diff question - what do they need to be VISIBLE to?
        cuz rn, that's just the main question w/ OOP lmao
        who cares about bonds?
        rn, i don't think we can perceive stuff as both-letter-and-group

    groups wanna perceive bonds 
    bonds wanna perceive descriptions
    bond wanna perceive objects (to make bonds 'of them')
    
    """

    # three types of bonds – Predecessor, Successor, Sameness

    pass


class Group():
    # three types of groups – Predecessor Groups, Successor Groups, Sameness Groups
    # can be a) an elt in a bond, b) part of larger group, c) in a correspondence

    def __init__(self) -> None:
        pass