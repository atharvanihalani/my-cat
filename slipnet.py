import random

class Slipnode():
    """
    Features:
        activation should decay over time
        contain a list of outgoing links (to spread activation)
            do you spread activation across ALL types of links?
        if i recognize features, i want to be able to activate my node
        # clamp activation!

        *description/bond/group-nodes* should add top-down structure codelets if active

    Properties:
        # conceptual depth
        # present activation
        links (DS unknown? maybe categorize by type of link?)

        ONLY for some nodes - maybe instance-links? 
        
    Methods:
        update method
            check clamp
            maybe activation decays over time 

        activate_one() 
            some way for codelets to communicate with node when a structure is built
        activate_two()
            way for a node to spread activation to another node via links
        # method to maybe activate 100%
    
    """

    def __init__(self, depth, net) -> None:
        self.conceptual_depth = depth
        self.slipnet = net
        self.activation = 0
        self.clamp = (0, 0) # (time of clamping, duration of clamp)
        
        self.outgoing_links = []
    
    def try_fully_activate(self):
        """
        probabilistically tries to fully activate the node, only if current activation is greater than 50%
        """
        if self.activation < 50:
            return
        random_percent = random.random() * 100
        if random_percent < self.activation:
            self.activation = 100

    def is_fully_active(self):
        if self.activation == 100:
            return True

    def clamp_activation(self, duration):
        """
        duration: length of time for which to clamp node activation
        """
        current_time = self.slipnet.get_time()
        self.clamp = (current_time, duration)

    def is_clamped(self):
        return self.clamp[1] != 0

    def on_fully_active(self):
        # spread activation to all nodes i'm linked to
            # spr = ((100 - link_length) / 100) * self.activation
            # note – shrunk links only used to evaluate slippage, bonds, etc – NOT for spreading activation
        # IF has links, shrink links
        pass

    def spread_activation(self):
        pass

    def decay_activation(self):
        self.activation *= (self.conceptual_depth / 100)
    
    

class Link():
    """
    super-class for various types of links

    Features:
        # should be directional
        should be an intermediary to pass activation b/w nodes
        # should have a certain length (that influences activation-spreading)


        ___ links should be able to grow or shrink
        slip links should be able to SLIP

    
    
    """

    def __init__(self, source, length, dest) -> None:
        self.source = source
        self.length = length # the intrinsic length of the link
        self.destination = dest
    
    def spread_activation(self):
        """
        this is a function of the nodes length p much"""
        pass

    pass

class Slipnet():
    """

    Properties:
        centralized ticker to keep time

    Methods:
        update() - calls update method of all nodes
        reset all nodes and links!
    
    """
    def __init__(self) -> None:
        self.time = 0

    def reset(self):
        # delete all existing nodes/links (wipe current datastructures)
        # reinitialize everything from scratch
        
        pass

    def initialize_slipnet(self):

        pass

    def __init_nodes(self):
        pass

    def __init_links(self):
        pass

    def update(self):
        """
        called by the main copycat class to update the slipnet
        
        should update the time count
        iterate through and update all the slipnodes
            order matters?? do i want the updated nodes to display updated activations right away?
            if yes, i'd need to define some order on how nodes are updated (cuz i'd want the activation-receiving ones to go last)
            if no, then i can mediate it through the links (second update method)
            or heck, let's have it closer to idc?

        """




        pass

    def get_time(self):
        return self.time
    