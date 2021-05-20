class TopologyBuilder:
    def __init__(self):
        pass
    
    def generate(self):
        return ""

class Machine:
    def __init__(self, name):
        self.name = name

class Switch(Machine):
    def __init__(self, name, p4_prog = None, p4_cli = None):
        super().__init__(name)
        self.p4_prog = p4_prog
        self.p4_cli = p4_cli
    
    def loadP4(self, p4_prog):
        self.p4_prog = p4_prog
    
    def setP4CLI(self, p4_cli):
        self.p4_cli = p4_cli
    
    def generate(self, dic):
        dic[self.name] = {}
        if self.p4_prog != None:
            dic[self.name]["program"] = self.p4_prog
        if self.p4_cli != None:
            dic[self.name]["cli_input"] = self.p4_cli

class Host(Machine):
    def __init__(self, name):
        super().__init__(name)
    
    def generate(self, dic):
        dic[self.name] = {}