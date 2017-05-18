
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

    # creates a epros_file object
    @classmethod
    def create_energyprofile(self, energy_file):
        line_count = 0
        name = ""
        type = ""
        head = []
        chain = []
        resno = []
        res = []
        ss = []
        energy = []
        with open(energy_file, 'r') as energy_file_handle:  # with open(energy_dir + file, 'r') as energy_file:
            for line in energy_file_handle:
                line_array = line.split("\t")
                if not "REMK" in line_array:
                    if line_count == 0:
                        name = line_array[1].strip()
                    elif line_count == 1:
                        type = line_array[1]
                    elif line_count == 2:
                        header = line_array
                    else:
                        # just extract the A Chain
                        if line_array[1] == "B":
                            break
                        head.append(line_array[0])
                        chain.append(line_array[1])
                        resno.append(line_array[2])
                        res.append(line_array[3])
                        ss.append(line_array[4])
                        energy.append(line_array[5].rstrip())
                line_count += 1
        return epros_file(name, type, head, chain, resno, res, ss, energy)
