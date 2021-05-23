from p4util_builder.shared import Host, Switch, TopologyBuilder
import json
class FatTreeTopology(TopologyBuilder):
    def __init__(self, leaf=2, module_width=2, module_height=2,  out_modules=4, middle_modules=4):
        if(out_modules % module_width != 0):
            raise BaseException("非法参数")
        self.auto_arp_tables = True
        self.switches = []
        self.hosts = [Host("out")]
        self.links = []
        
        for i in range(middle_modules):
            for j in range(module_width):
                for k in range(leaf):
                    self.hosts.append(Host(f"host_{i}{j}{k}"))
        for i in range(out_modules):
            self.switches.append(Switch(f"sm_1{i}"))
            self.links.append([f"out", f"sm_1{i}"])
            tid = i // (out_modules // module_width)
            for j in range(middle_modules):
                self.links.append([f"sm_1{i}", f"sm_1{j}{0}{tid}"])
        for i in range(middle_modules):
            for j in range(module_height):
                for k in range(module_width):
                    self.switches.append(Switch(f"sm_1{i}{j}{k}"))
                    if j != module_height-1:
                        for t in range(module_width):
                            self.links.append([f"sm_1{i}{j}{k}", f"sm_1{i}{j+1}{t}"])
                    else:
                        for t in range(leaf):
                            self.links.append([f"sm_1{i}{j}{k}", f"host_{i}{k}{t}"])
        
    
    def populateP4(self, p4_prog):
        '''
        populate p4_prog to all switch
        '''
        for s in self.switches:
            s.loadP4(p4_prog)
    
    def populateP4_to(self, switch:Switch, p4_prog):
        '''
        populate p4_prog to a single switch
        '''
        switch.loadP4(p4_prog)
    
    def generate(self) -> str:
        if self.switches[0].p4_prog == None:
            raise BaseException("Failed to validate P4 Program")
        template = {
            "program": "default.p4",
            "switch": "simple_switch",
            "compiler": "p4c",
            "options": "--target bmv2 --arch v1model --std p4-16",
            "switch_cli": "simple_switch_CLI",
            "cli": True,
            "pcap_dump": True,
            "enable_log": True,
            "topo_module": {
                "file_path": "",
                "module_name": "p4utils.mininetlib.apptopo",
                "object_name": "AppTopoStrategies"
            },
            "controller_module": None,
            "topodb_module": {
                "file_path": "",
                "module_name": "p4utils.utils.topology",
                "object_name": "Topology"
            },
            "mininet_module": {
                "file_path": "",
                "module_name": "p4utils.mininetlib.p4net",
                "object_name": "P4Mininet"
            },
            "topology": {
                "assignment_strategy": "l2",
                "links": self.links,
                "hosts": {},
                "switches": {}
            }
        }
        for s in self.switches:
            s.generate(template["topology"]["switches"])
        for h in self.hosts:
            h.generate(template["topology"]["hosts"])
        return json.dumps(template, indent=4)