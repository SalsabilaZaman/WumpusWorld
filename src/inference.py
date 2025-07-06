class KnowledgeBase:
    def __init__(self):
        self.facts = set()

    def update(self, percepts):
        for p in percepts:
            self.facts.add(p)

    def query(self, proposition):
        return proposition in self.facts
