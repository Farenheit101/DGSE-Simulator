# atlas.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
import bureaux
import agents
import missions

class LiveAtlasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Atlas des Bureaux/Directions DGSE")
        self.layout.addWidget(self.label)
        self.bureauList = QListWidget()
        self.layout.addWidget(self.bureauList)
        self.setLayout(self.layout)
        self.update_atlas()

    def update_atlas(self):
        self.bureauList.clear()
        for b in bureaux.BUREAUX:
            nb_agents = len([a for a in agents.AGENTS if a.bureau == b["code"]])
            nb_missions = len([m for m in missions.MISSIONS if getattr(m, "bureau", None) == b["code"]])
            self.bureauList.addItem(
                f"{b['nom']} ({b['code']}) - Agents: {nb_agents}, Missions: {nb_missions}"
            )
