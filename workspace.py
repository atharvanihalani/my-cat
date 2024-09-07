# intra-string bonds
# inter-string bridges
# structures of a string
# rules? translated rules? descriptions?


class Workspace():
    # contains various structures
    # also contains strings?
    pass


class Structure():
    def __init__(self) -> None:
        self.strength = 0

class Bond(Structure):
    # three types of bonds – Predecessor, Successor, Sameness

    def __init__(self) -> None:
        super().__init__()

class Description(Structure):
    def __init__(self) -> None:
        super().__init__()

class Group(Structure):
    # three types of groups – Predecessor Groups, Successor Groups, Sameness Groups
    # can be a) an elt in a bond, b) part of larger group, c) in a correspondence

    def __init__(self) -> None:
        super().__init__()

class Correspondence(Structure):
    def __init__(self) -> None:
        super().__init__()
