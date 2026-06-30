class ImpactEngine:

    def __init__(self, graph):

        self.graph = graph
      

    def get_nodes(self, prefix):

    return [

        n

        for n in self.graph.nodes()

        if str(n).startswith(prefix)

    ]

  
    def requirements(self):

        return self.get_nodes("REQ-")


    def verifications(self):

        return self.get_nodes("VER-")


    def tests(self):

        return self.get_nodes("TEST-")


    def failures(self):

        return self.get_nodes("FAIL-")


    def summary(self):

        return {

            "requirements": len(
                self.requirements()
            ),

            "verifications": len(
                self.verifications()
            ),

            "tests": len(
                self.tests()
            ),

            "failures": len(
                self.failures()
            )

        }
