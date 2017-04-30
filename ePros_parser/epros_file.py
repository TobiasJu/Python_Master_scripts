
class epros_file:
    __name = ""
    __type = ""
    __head = []
    __chain = []
    __resno = []
    __res = []
    __ss = []
    __energy = []

# constructor
    def __init__(self, name, type, head, chain, resno, res, ss, energy):
        self.__name = name
        self.__type = type
        self.__head = head
        self.__chain = chain
        self.__resno = resno
        self.__res = res
        self.__ss = ss
        self.__energy = energy

