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

        each object has some descriptions attached (in the form 'description-type: descriptor')
            both these above are slipnet nodes
        a description is 'relevant' if its description-type-node is fully active

        at the start of a run, letter-cat + string-pos are clamped high 

        when a group is formed, it becomes a new object
            automatically given the default descriptions as a letter (where applicable)
            also probabilistically decided to add a 'length' description

        'codelets do almost no examination of the modified string' (cuz initial & modified differ by a single letter)
            no bonds / groups are built in modified string
            only analysis is the one-to-one letter correspondences w/ initial AND determining any potential relation b/w the changed letter & its replacement
            if relation present, a "description reflecting that relationship is added to the replacement letter's list of descriptions"
                (i found this lowk weird lmao)
            rule-codelet fills in the template "replace __<I>__ by __<II>__"
                <I>: some descriptor of changed letter; <II>: some descriptor of its replacement
                these descriptors chosen probabilistically (but biased 2wards conceptual depth)
                (but 3.5.2 talks more about the rule-preference function)

        stopping mechanism
            stops probabilistically when rule is translated
            formation of a rule triggers copycat to post rule-translator codelets each timestep 
                ...till one of 'em succeeds and (ofc) ends the run
            first, this codelet decides whether to 'fizzle' or not (a function of temperature + AMOUNT of structure)
                if temp low => likelIER 2run; 
                if temp high AND little structure is built, indicates lots of time has passed => also likelIER 2run
                if temp high AND much structure => let 'im cook
                (note: even in cases 1 & 2, probability of success is still pretty low)
            if it doesn't, it goes on to translate existing rule according to current slippages
                then, program stops running codelets & tries to create the answer w/ the translated rule (via a separate special-purpose function)

        
        workspace contains objects AND perceptual structures

        STRUCTURES:
        
        each structure has a time-varying strength (that measures its quality). 
            this influences codelets' probabilistic decisions. eg
                a) whether to continue evaluating that particular structures
                b) urgencies assigned to future codelets evaluating this structure
                c) whether it should win a fight against an existing, incompatible structure
            strength varies in response to
                new structures being built
                old structures being destroyed
                changing clipnet activations

        Strength of:
        Descriptions, is a function of
            conceptual depth of descriptor
            activation of description type
            local support of description (ie. number of other descriptions of the same type, in the same string)
        Bonds, depends on
            the type of bond (sameness bonds are intrinsically stronger than successor / predecessor)
            activation of associated slipnet node
            local support of bond (of same category AND same spatial direction)
        Groups, depends on
            the type of group (sameness stronger than successor / predecessor)
            activation of associated group category
            group's length - the longer, the stronger (size matters)
            local support! (category and spatial direction)
        Correspondence
            A correspondence (b/w two objects) is based on a set of concept mappings b/w their descriptors
            these "concept mappings" are either identities, or slippages
            not all descriptors have to be accounted for (cuz analogy doesn't hold across ALL axes)
            the STRENGTH of a correspondence has many factors:
                the number of concept mappings in the correspondence
                the proximity of the nodes in the concept-mappings (identity vs slippages - i think)
                conceptual depth of nodes in concept-mapping
                    tho deep similarities adds strength to correspondence, there is also a counterveiling pressure resisting these slippages in the first place
                    ie. it's hard to make, but when it happens, it adds significant strength
                the size of the objects in the correspondence
                    bias towards groups over letters
                    AND bias towards large groups over smaller ones
                internal coherence of correspondence 
                    ie. if the mappings are "conceptually parallel"
                "external coherence" of correspondence
                    (the strengths of) other correspondences that support this given one
                    "if a concept mapping in one is conceptually paralllel to a concept mapping in the other
        Rules
            conceptual depth of descriptors used in the rule
            how the *changed letter* in init-str is mapped onto tar-str (??)

        
        OBJECTS
        
        copycat itself determines what is important / salient in an analogy - and can dynamically modify this as it runs 
            (as opposed to a priori, fixed labels)
        each object has a time-varying "importance" and "happiness", which are combined to determine its overall "salience"
            salience ==  attractiveness to codelets

        importance is a function of
            how many relevant descriptions it has ("relevance" depending on description-type-activation)
            how active the *corresponding* descriptors are
            also! once the changed obj (letter?) in init-str is identified, its importance is raised
            +1 also! the importance of any object inside a group is lowered
        happiness measures an object's compatibility w/ existing structures. 
            it's a function of the (strengths of) attached structures (bonds, groups & correspondences)
        salience is the object's attractiveness to codelets
            function of the object's IMPORTANCE and UN-HAPPINESS
        
        
        the TEMPERATURE is a weighted average of the unhappiness of all objects
            unhappineses being weighted by, you guessed it, object importance
            
    """
    def __init__(self) -> None:
        self.descriptions_by_type = {
            'letter-category': [],
            'string-position': [],
            'object-type': [],
            'length': [],
            'direction': [],
            'alphabetic-position': [],
            'bond-category': [],
            'group-category': [],
        }
    
    def update_descriptions(self):
        # how am i managing state? do i want the nodes to communicate with me? do i want to query them directly?
            # okay ya, let's do it outside the update loop? slipnet directly communicates w/ this to set description relevance
        pass

    def add_description(self, description):
        array = self.descriptions_by_type[description.description_type]
        array.append(description)
    
    def remove_description(self, description):
        array = self.descriptions_by_type[description.description_type]
        array.remove(description)

    def set_description_relevance(self, description_type, relevance):
        """
        if this description_type node is fully active, the description will be relevant"""
        array = self.descriptions_by_type[description_type]
        for description in array:
            self.relevant = relevance


class Object():
    def __init__(self) -> None:
        self.importance = None
        self.happiness = None
        self.salience = None
        self.descriptions = []
    
    def add_description(self, description):
        self.descriptions.append(description)
    
    def calculate_importance(self):
        """
        calculates the importance-value for any particular object
        i copied this directly from the copycat implementation"""
        result = 0.0
        for description in self.descriptions:
            if description.descriptionType.fully_active():
                result += description.descriptor.activation
            else:
                result += description.descriptor.activation / 20.0
        if self.group:
            result *= 2.0 / 3.0
        if self.changed:
            result *= 2.0
        return result
    
    def calculate_happiness(self):
        pass

    def calculate_salience(self):
        pass


class Description():
    """
    these assigned to objects (either strings or groups)
        edit: or bonds too??
    
    these are of the format: "description-type: descriptor"
    they are RELEVANT iff their 'description-type'-node is fully activated
    imo these should NOT be included in an update loop. instead, you should toggle their relevance directly
        how? store 'em in a dict in workspace, by 'description-type'?
    """
    def __init__(self, description_type, descriptor, workspace) -> None:
        # TODO nah, okay, pass these in by NODE, not STRING
        self.description_type = description_type 
        self.descriptor = descriptor

        self.workspace = workspace
        self.relevant = False
        
        self.add_to_workspace()
    
    def add_to_workspace(self):
        self.workspace.add_description(self)
    
    def remove_from_workspace(self):
        self.workspace.remove_description(self)

    def is_relevant(self):
        """
        is this description relevant?"""
        return self.relevant


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
    """
    three types of groups - Predecessor Groups, Successor Groups, Sameness Groups

    can be a) an elt in a bond, b) part of larger group, c) in a correspondence

    when formed, automatically add following descriptions (where applicable)
        letter-cat + string-pos + obj-type
        add length-description probabilistically based on a) length of group (ie.
        longer is less likely), b) activation of 'length' node

    strength decay if turn out to not be useful
    """

    def __init__(self) -> None:
        pass