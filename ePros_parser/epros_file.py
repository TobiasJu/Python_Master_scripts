
class epros_file:
    __name = ""
    __prot_prot_type = ""
    __head = []
    __chain = []
    __resno = []
    __res = []
    __ss = []
    __energy = []
    __pdb_pos = ""

# constructor
    def __init__(self, name, prot_type, head, chain, resno, res, ss, energy, pdb_pos):
        self.__name = name
        self.__prot_type = prot_type
        self.__head = head
        self.__chain = chain
        self.__resno = resno
        self.__res = res
        self.__ss = ss
        self.__energy = energy
        self.__pdb_pos = pdb_pos

    def print_all(self):
        print self.__name
        print self.__prot_type
        print self.__head
        print self.__chain
        print self.__resno
        print self.__res
        print self.__ss
        print self.__energy
        print self.__pdb_pos

    # creates a epros_file object
    @classmethod
    def create_energyprofile(self, energy_file, pdb_pos):
        line_count = 0
        name = ""
        prot_type = ""
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
                        prot_type = line_array[1]
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
                        energy_str = line_array[5].rstrip()
                        #energy_float = energy_str.round(2)
                        energy.append(float(energy_str))
                line_count += 1
        return epros_file(name, prot_type, head, chain, resno, res, ss, energy, pdb_pos)
