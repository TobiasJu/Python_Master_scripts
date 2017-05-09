
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

    def print_all(self):
        print self.__name
        print self.__type
        print self.__head
        print self.__chain
        print self.__resno
        print self.__res
        print self.__ss
        print self.__energy