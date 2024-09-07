# TODO work out sliplinks of certain node-types
    # maybe have activation change a link by a 'multiple', while the 'opposite'-node changes the link's underlying numerical value?
# TODO visualize slipnet as graph??

# TODO debug and annotate code
# TODO smtn to prevent / check for duplicate links?
# okay, chalo, make creative decisions. 
# first, the activation of a node type REDUCES the length of the link ('base length'??)
# this is different from the 'perceived length' of the link – ie. the one that influences slippage
# second, this perceived length is a function of the activation of the two end nodes. 
    # or am i making this too complicated? can i skip activation for now? yeah let's do that.
    # but let's still do double-ended links! as default? as default.
        # potentially new category – 'instance of'. something todo for later mega-cat.

import random

class Slipnode():
    def __init__(self, name, depth, activation=0) -> None:
        self.name = name
        self.depth = depth
        self.activation = activation
        self.out_links = [] #list of outgoing links
        self.instance_links = [] #list of instance links – where this node is used to 'label' a link
        self.clamp_count = 0
    
    def add_out_links(self, new_links):
        self.out_links.extend(new_links)

    def add_instance_links(self, new_links):
        self.instance_links.extend(new_links)
    
    def update(self):
        # every 15 time steps (ie. one update loop), the activation of the node reduces a little
        # if increase, increase. else, decay
        decay_rate = 100-self.depth

        if self.clamp_count != 0: #TODO – this is gonna be fucky if i'm clamping before the update loop
            if self.clamp_count > 3:
                self.unclamp()
            else:
                self.clamp_count += 1
        else:
            self.activation *= decay_rate
            

    # gotta add activation somehow
        # not sure if this will *add activation* or *set* it to smtn
        # bumps up activation of surrounding nodes
        # if above 50, potential to be fully activated! – and then shrink instance links
    
    def activate(self):
        for link in self.out_links:
            link.spread()
            pass
        pass
    
    def spread_activation(self, incoming):
        # incoming: the incoming activation amount (positive integer ≤ 90)
        # again, lot of choices i'm making here – eg. no second degree activations being passed (also computationally expensive ASF)
        self.activation = min(self.activation + incoming, 100)
        if self.activation >= 50 and random.random() > 0.5:
            self.clamp_activation()
            pass

    def clamp_activation(self):
        # activation is clamped for 30 time steps
        self.clamp_count = 1
        self.activation = 100
        for link in self.instance_links:
            link.shrink()

    def unclamp(self):
        self.clamp_count = 0
        for link in self.instance_links:
            link.unshrink()
        
    
    def set_activation(self, amount):
        if amount<0 or amount>100:
            raise ValueError("enter an activation between 0-100, please")
        self.activation = amount
        self.update_sliplinks()

    def update_sliplinks(self):
        pass
    pass

class Sliplink():
    def __init__(self, to, net, length=80, type=None) -> None:
        self.to = to
        self.net = net
        self.length = length
        self.type = type #whether the link is a slipnode

        if self.type:
            self.net.add_instance_link(self.type, self)

    def spread(self, activation):
        # activation: incoming activation that will be spread
        # say, proximity (ie. link length) varies from 10-90. 
        out = (100 - self.length) * activation
        self.to.spread_activation(out)
        
    def shrink(self):
        self.length *= 0.4
    
    def unshrink(self):
        self.length *= 2.5

class Slipnet():
    def __init__(self) -> None:
        self.nodes = {}
        self.initialize_slipnet()

    def initialize_slipnet(self):
        self.__initnodes()
        self.__initlinks()
        print('allset')


    def add_instance_link(self, node, link):
        # meant to be called by Sliplink 
        node.add_instance_links([link])
    
    def __add_out_link(self, node, to, length=80, type=None):
        # meant to be called within Slipnet
        mytype = self.nodes[type] if type else None
        self.add_out_link(self.nodes[node], self.nodes[to], length, mytype)
    
    def __add_double_link(self, node_a, node_b, length=80, type=None):
        mytype = self.nodes[type] if type else None
        self.add_out_link(self.nodes[node_a], self.nodes[node_b], length, mytype)
        self.add_out_link(self.nodes[node_b], self.nodes[node_a], length, mytype)
        pass

    def add_out_link(self, node, to, length=80, type=None):
        link = Sliplink(to, self, length, type)
        node.add_out_links([link])
    
    def __initlinks(self):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        numbers = ['one', 'two', 'three', 'four', 'five']
        
        for index in range(24):
            self.__add_out_link(alphabet[1+index], alphabet[2+index], type='Successor')
            self.__add_out_link(alphabet[1+index], alphabet[index], type='Predecessor')
            self.__add_double_link('LetterCategory', alphabet[1+index])
        self.__add_out_link('a', 'b', type='Successor')
        self.__add_out_link('z', 'y', type='Predecessor')
        self.__add_double_link('LetterCategory', 'a')
        self.__add_double_link('LetterCategory', 'z')
        self.__add_double_link('a', 'First')
        self.__add_double_link('z', 'Last')

        for index in range(3):
            self.__add_out_link(numbers[1+index], numbers[2+index], type='Successor')
            self.__add_out_link(numbers[1+index], numbers[index], type='Predecessor')
            self.__add_double_link(numbers[1+index], 'Length')
        self.__add_out_link('one', 'two', type='Successor')
        self.__add_out_link('five', 'four', type='Predecessor')
        self.__add_double_link('Length', 'one')
        self.__add_double_link('Length', 'five')

        self.__add_double_link('LetterCategory', 'BondFacet')
        self.__add_double_link('LetterCategory', 'SamenessGroup')
        self.__add_double_link('LetterCategory', 'Length')

        self.__add_double_link('Length', 'SamenessGroup')
        self.__add_double_link('Length', 'SuccessorGroup')
        self.__add_double_link('Length', 'PredecessorGroup')

        self.__add_double_link('First', 'Last', type='Opposite')
        self.__add_double_link('AlphabeticPosition', 'First')
        self.__add_double_link('AlphabeticPosition', 'Last')
        self.__add_double_link('First', 'Rightmost')
        self.__add_double_link('First', 'Leftmost')
        self.__add_double_link('Last', 'Rightmost')
        self.__add_double_link('Last', 'Leftmost')

        self.__add_double_link('Rightmost', 'Leftmost', type='Opposite')
        self.__add_double_link('Rightmost', 'Right')
        self.__add_double_link('Rightmost', 'Left')
        self.__add_double_link('Leftmost', 'Right')
        self.__add_double_link('Leftmost', 'Left')

        self.__add_double_link('Right', 'Left', type='Opposite')
        self.__add_double_link('Right', 'Direction')
        self.__add_double_link('Left', 'Direction')

        self.__add_double_link('StringPosition', 'Leftmost')
        self.__add_double_link('StringPosition', 'Rightmost')
        self.__add_double_link('StringPosition', 'Middle')
        self.__add_double_link('StringPosition', 'Single')
        self.__add_double_link('StringPosition', 'Whole')
        self.__add_double_link('Single', 'Whole')

        self.__add_double_link('Letter', 'Group')
        self.__add_double_link('Letter', 'ObjectCategory')
        self.__add_double_link('Group', 'ObjectCategory')

        self.__add_double_link('PredecessorGroup', 'GroupCategory')
        self.__add_double_link('PredecessorGroup', 'Predecessor')
        self.__add_double_link('PredecessorGroup', 'SuccessorGroup', type='Opposite')
        self.__add_double_link('SuccessorGroup', 'GroupCategory')
        self.__add_double_link('SuccessorGroup', 'Successor')

        self.__add_double_link('Predecessor', 'Successor', type='Opposite')
        self.__add_double_link('Predecessor', 'BondCategory')
        self.__add_double_link('Successor', 'BondCategory')

        self.__add_double_link('BondCategory', 'Sameness')
        self.__add_double_link('Sameness', 'SamenessGroup')
        self.__add_double_link('SamenessGroup', 'GroupCategory')
    
    def __initnodes(self):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for letter in alphabet:
            self.nodes[letter] = Slipnode(letter, 10)
        self.nodes['Letter'] = Slipnode('Letter', 15)
        self.nodes['LetterCategory'] = Slipnode('LetterCategory', 20)

        numbers = ['one', 'two', 'three', 'four', 'five']
        for number in numbers:
            self.nodes[number] = Slipnode(number, 25)

        self.nodes['Leftmost'] = Slipnode('Leftmost', 30)
        self.nodes['Rightmost'] = Slipnode('Rightmost', 30)
        self.nodes['Left'] = Slipnode('Left', 30)
        self.nodes['Middle'] = Slipnode('Middle', 30)
        self.nodes['Right'] = Slipnode('Right', 30)
        self.nodes['Single'] = Slipnode('Single', 30)
        self.nodes['Whole'] = Slipnode('Whole', 30)

        self.nodes['Successor'] = Slipnode('Successor', 40)
        self.nodes['Predecessor'] = Slipnode('Predecessor', 40)
        self.nodes['SuccessorGroup'] = Slipnode('SuccessorGroup', 40)
        self.nodes['PredecessorGroup'] = Slipnode('PredecessorGroup', 40)

        self.nodes['Group'] = Slipnode('Group', 50)
        self.nodes['BondFacet'] = Slipnode('BondFacet', 50)
        self.nodes['First'] = Slipnode('First', 50)
        self.nodes['Last'] = Slipnode('Last', 50)

        self.nodes['Length'] = Slipnode('Length', 55)

        self.nodes['Direction'] = Slipnode('Direction', 60)
        self.nodes['StringPosition'] = Slipnode('StringPosition', 60)

        self.nodes['AlphabeticPosition'] = Slipnode('AlphabeticPosition', 70)
        self.nodes['BondCategory'] = Slipnode('BondCategory', 70)
        self.nodes['GroupCategory'] = Slipnode('GroupCategory', 70)

        self.nodes['Sameness'] = Slipnode('Sameness', 80)
        self.nodes['SamenessGroup'] = Slipnode('SamenessGroup', 80)

        self.nodes['ObjectCategory'] = Slipnode('ObjectCategory', 90)
        self.nodes['Identity'] = Slipnode('Identity', 90)
        self.nodes['Opposite'] = Slipnode('Opposite', 90)

    
    pass

mynet = Slipnet()