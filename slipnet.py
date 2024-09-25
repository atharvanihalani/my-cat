import random
from enum import Enum

Link = Enum('Link', ['CATEGORY', 'INSTANCE', 'PROPERTY', 'SLIP', 'LATERAL'])

class Slipnode():
    """
    Features:
        activation should decay over time
        contain a list of outgoing links (to spread activation)
            do you spread activation across ALL types of links?
        if i recognize features, i want to be able to activate my node

        *description/bond/group-nodes* should add top-down structure codelets if active

    Properties:
        links (DS unknown? maybe categorize by type of link?)

        ONLY for some nodes - maybe instance-links? 
        
    Methods:
        activate_one() 
            some way for codelets to communicate with node when a structure is built
        activate_two()
            way for a node to spread activation to another node via links
    
        to 'get' a certain node, based on name (use dict)
            

    Spreading Activation - an overview

    i want activated nodes to spread some of their activation to neighbors! 
    this, however, is easier said than done. here are some questions / issues to think ab

    1) do i want activation to be spread recurrently? ie. bounce around lmao (while decaying, ofc).
        i think not!
    2) should it only be spread WHEN activation is increased? or should it be spread whenever activation is above a certain threshold?
    3) similarly, what about when a node is clamped? should it keep 'pumping out activation'?


    Description-type nodes, should have accessible a list of descriptor nodes


    """

    def __init__(self, depth, net) -> None:
        self.conceptual_depth = depth
        self.slipnet = net
        self.activation = 0
        self.clamp = (0, 0) # (time of clamping, duration of clamp)
        
        self.outgoing_links = []

    def get_category(self):
        cat_link = None #TODO get cat link
        return cat_link.dest

    def update(self):
        """
        check clamp, 
            if is, update clamp duration
            update if required
        decay activation 
            ...unless instances continue to be perceived???
        try decay activation
        
        """
        if self.is_clamped():
            self.try_unclamp()
        
        if not self.is_clamped():
            self.decay_activation()

    
    def try_fully_activate(self):
        """
        probabilistically tries to fully activate the node, only if current activation is greater than 50%
        """
        if self.activation < 50:
            return
        
        threshold = (self.activation / 100)**3
        random_percent = random.random() * 100
        if random_percent < threshold:
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

    def try_unclamp(self):
        """
        tries to unclamp this node, if it's been clamped for long enough
        
        returns:
            a boolean indicating whether this was successful
        """
        current_time = self.slipnet.get_time()
        start_time, clamp_duration = self.clamp

        if (current_time - start_time) >= clamp_duration:
            self.unclamp_activation()
            return True
        return False

    def unclamp_activation(self):
        self.clamp = (0, 0)

    def instance_perceived(self):
        """
        only called by codelets, if an instance of this structure has been perceived
        
        """


        pass

    def activate_node(self):
        """
        only to be used when structure is perceived by a CODELET


        """
        pass

    def on_fully_active(self):
        # spread activation to all nodes i'm linked to
            # spr = ((100 - link_length) / 100) * self.activation
            # note – shrunk links only used to evaluate slippage, bonds, etc – NOT for spreading activation
        # IF has links, shrink links
        # make descriptions relevant!

        # when NOT fully active, 
            # unshrink links
            # make descriptions not-relevant!
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

        # method to evaluate slippages / bonds 
        # method to spread activation
    
    """

    def __init__(self, source, length, dest, type) -> None:
        self.source = source
        self.length = length # the ('perceived') length of the link (as opposed to the 'intrinsic' length; only matters for labelled links)
        self.destination = dest
        self.type = type # enum noting the 'type' of link (eg. 'category link')

    
    def spread_activation(self):
        """
        this is a function of the nodes length p much"""
        pass

    pass

class LabeledLink(Link):
    def __init__(self, source, length, dest, type, label) -> None:
        super().__init__(source, length, dest, type)
        self.label = label 
        self.intrinsic_length = length # the intrinsic length of the link

        # shrunk link lengths are used to evaluate slippages / bonds / etc
        # regular link lengths used to spread activation
        # override spread activation ()
    
    def spread_activation(self):
        #  same method as super(); only use intrinsic_length for calculating it.
        pass

    def shrink_link(self):
        if self.is_shrunk():
            return
        self.length *= 0.4
    
    def unshrink_link(self):
        if not self.is_shrunk():
            return
        self.length *= 2.5

    def is_shrunk(self):
        return self.length != self.intrinsic_length

class Slipnet():
    """

    Properties:
        centralized ticker to keep time

    Methods:
        update() - calls update method of all nodes
        reset all nodes and links!
    
    """
    def __init__(self, ctx) -> None:
        self.coderack = ctx.coderack
        self.workspace = ctx.workspace
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
    