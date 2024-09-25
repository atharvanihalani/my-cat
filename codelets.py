from random import Random as rng
from workspace import Description
"""
okay so codelets themselves are methods

how are they stored in the coderack?

codelets that build groups / bonds / descriptions 
    send activation to associated slipnet nodes

urgency
    of top-down codelets depends on node activation
    of follow-up codelets depends on outcome of prior codelet
    of bottom-up codelets is fixed

"""


"""
common methods
    "choose an object in the Workspace, probabilistically as a function of salience"
        workspace has list of objects, sorted by salience?
        or 
"""

def accumulate(iterable):
    total = 0
    for v in iterable:
        total += v
        yield total

def bisect_left(a, x, lo=0, *, key=None):
    """
    Return the index where to insert item x in list a, assuming a is sorted."""

    hi = len(a)

    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
    return lo

def weighted_choice(mylist, myweights):
    """
    returns a probabilistically weighted choice from a list  
    if list is empty, it returns None

    mylist: list of items from which the choice is made  
    myweights: corresponding weights of each item in the list; these shouldn't be negative"""

    if len(mylist) == 0:
        return None

    cum_weights = list(accumulate(myweights))
    total = cum_weights[-1]
    index = bisect_left(cum_weights, rng.random() * total)

    return mylist[index]

def choose_salient_obj(ctx):
    """
    chooses an object as a probabilistic function of salience"""
    workspace = ctx.workspace
    objects = workspace.get_objects()
    weights = [obj.salience for obj in objects]

    return weighted_choice(objects, weights)

def try_choose_description(ctx, obj):
    """
    chooses a *relevant* description from a workspace object as a function 
    of activation (probablistic, of course)  

    obj: a workspace object with a list of descriptions attached  
    returns: an instance of a Description
    """
    descriptions = obj.get_descriptions()
    rel_descs = [desc for desc in descriptions if desc.is_relevant()]
    weights = [desc.get_activation() for desc in rel_descs]

    return weighted_choice(rel_descs, weights)

def try_choose_descriptor(ctx, descriptors):
    '''
    chooses a descriptor probablistically, weighted by its activation
    
    descriptors: a list of descriptor nodes  
    returns: a single descriptor node'''
    weights = [desc.activation for desc in descriptors]
    return weighted_choice(descriptors, weights)

def try_get_property(ctx, descriptor):
    '''
    probabilistically chooses a new descriptor node, that's connected to
    the current node by a property link
    
    descriptor: current descriptor Slipnode
    returns: new descriptor Slipnode, that's property-linked to the current one'''
    link = None #TODO get property link from descriptor
    probability = (100 - link.length) / 100

    if rng.random() > probability:
        return None
    else:
        return link.dest #ie. the corresponding property node (descriptor)
    
def create_new_description(ctx, descriptor):
    '''
    creates a new description from a descriptor node
    
    descriptor: a descriptor Slipnode  
    returns: a Description with this particular descriptor'''
    descriptor = descriptor
    description_type = descriptor.get_category()

    desc = Description(description_type, descriptor, ctx.workspace)
    return desc


def bottom_up_description_scout(ctx):
    # choose a workspace object (probabilistic fxn of salience)
    # choose a RELEVANT description from the list (probabilistic fxn of activation)
        # might be None!
    # does descriptor have property links? they short enough?
    # probabilistically pick a property, fxn of a) degree of association, b) activation
    # propose a description based on this property; post a strength-tester 
        # ...with urgency being fxn of activation of description-type
    
    obj = choose_salient_obj(ctx)
    desc = try_choose_description(ctx, obj)
    if desc is None:
        return
    
    new_descriptor = try_get_property(ctx, desc)
    if new_descriptor is None:
        return
    
    new_description = create_new_description(ctx, new_descriptor)
    urgency = new_descriptor.get_category().activation
    # post a description-strength-tester codelet

def try_apply_descriptor(ctx, d_type, obj):
    '''
    d_type: a description-type node (whose descriptors we're testing for)  
    obj: the object onto which the descriptions might be applicable  
    
    returns: list of valid description nodes'''
    descriptors = d_type.get_descriptors()
    valid_descriptors = []
    for descriptor in descriptors:
        # if descriptor applicable to object, add to list
        pass
    return valid_descriptors

def top_down_description_scout(ctx, d_type):
    '''
    d_type: a description-type node'''
    
    obj = choose_salient_obj(ctx)
    descriptors_list = try_apply_descriptor(ctx, d_type, obj)
    if len(descriptors_list) == 0:
        return
    
    descriptor = try_choose_descriptor(ctx, descriptors_list)
    if descriptor is None:
        return
    
    new_description = create_new_description(ctx, descriptor)
    urgency = descriptor.get_category().activation
    # post a strength-tester codelet


