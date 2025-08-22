import sys
import os
import random
import folium
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QTabWidget, QHBoxLayout, QListWidget, QMessageBox, QInputDialog, QComboBox,
    QDialog, QRadioButton, QButtonGroup, QCheckBox, QListWidgetItem, QFrame, QDialogButtonBox, QFormLayout
)
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

import agents
from agents import est_disponible
import sources
import recrutement
import missions
import crises
import budget
import bureaux
import agences
import metiers
import noms
import langues
import services_francais
import fiches
import reseaux
import atlas
import logistique
import villes

RECRUTEMENTS_EN_COURS = []
ALERTES_EN_COURS = []
PROCHAINES_MISSIONS = []
PROCHAINES_ALERTES = []
PROCHAINES_CRISES = []
CREATIONS_RESEAUX_EN_COURS = []


class RecrutementEnCours:
    def __init__(self, type_recrutement, ciblage, date_debut, date_fin):
        self.type_recrutement = type_recrutement
        self.ciblage = ciblage
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.traite = False

class DGSESimGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulateur DGSE - PC")
        self.setGeometry(100, 100, 1400, 800)
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self._tab_accueil(), "Accueil")
        self.tabs.addTab(self._tab_agents(), "Agents")
        self.tabs.addTab(self._tab_sources(), "Sources")
        self.tabs.addTab(self._tab_missions(), "Missions")
        self.tabs.addTab(self._tab_crises(), "Crises")
        self.tabs.addTab(self._tab_reseaux(), "Réseaux")
        self.tabs.addTab(self._tab_budget(), "Budget")
        self.atlas_widget = atlas.LiveAtlasWidget()
        self.tabs.addTab(self.atlas_widget, "Atlas")
        self.tabs.addTab(self._tab_logistique(), "Logistique")

        self.init_time_system()

    def init_time_system(self):
        self.game_start_time = datetime(2025, 4, 7, 8, 0, 0)
        self.current_game_time = self.game_start_time
        self.time_speed = 1
        self.paused = False
        self.speed_to_minutes = {1: 3, 2: 6, 5: 30, 10: 1440}

        self.timer = QTimer()
        self.timer.timeout.connect(self.advance_game_time)
        self.timer.start(1000)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignRight)
        self.time_label.setFrameShape(QFrame.Box)
        self.time_label.setStyleSheet("padding: 5px; font-weight: bold; background: #f3f3f3; color: #3b3b3b;")
        self.update_time_label()

        self.time_btn_bar = QWidget()
        hbox = QHBoxLayout(self.time_btn_bar)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.speed_buttons = {}
        for label, spd in [("Pause", 0), ("x1", 1), ("x2", 2), ("x5", 5), ("x10", 10)]:
            btn = QPushButton(label)
            btn.setFixedWidth(50)
            btn.clicked.connect(lambda checked, s=spd: self.set_time_speed(s))
            hbox.addWidget(btn)
            self.speed_buttons[spd] = btn

        hbox.addWidget(self.time_label)
        hbox.addStretch(1)
        self.tabs.setCornerWidget(self.time_btn_bar, Qt.TopRightCorner)
        self.set_time_speed(1)
        self.creation_reseaux_en_cours = []

    def set_time_speed(self, spd):
        self.paused = (spd == 0)
        self.time_speed = spd if not self.paused else 1
        for s, btn in self.speed_buttons.items():
            if s == spd:
                btn.setStyleSheet("background-color: #2976e6; color: white; font-weight: bold;")
            else:
                btn.setStyleSheet("")

    def update_time_label(self):
        self.time_label.setText(self.current_game_time.strftime(" %d/%m/%Y  %H:%M:%S "))

    def advance_game_time(self):
        if not self.paused:
            minutes_to_add = self.speed_to_minutes.get(self.time_speed, 3)
            self.current_game_time += timedelta(minutes=minutes_to_add)
            self.update_time_label()
            self.check_automatic_events()
            self.process_timed_events()
            for m in missions.MISSIONS:
                if hasattr(m, 'maj_etat'):
                    m.maj_etat(self.current_game_time)
            for c in crises.CRISES:
                if hasattr(c, 'maj_etat'):
                    c.maj_etat(self.current_game_time)
            for exf in logistique.lister_exfiltrations():
                if exf.get("date_fin") and exf["statut"] == "En attente" and self.current_game_time >= exf["date_fin"]:
                    exf["statut"] = "Terminée"
            self.process_reseaux_creation()


    def process_reseaux_creation(self):
        for r in CREATIONS_RESEAUX_EN_COURS[:]:
            if self.current_game_time >= r["fin"]:
                CREATIONS_RESEAUX_EN_COURS.remove(r)
                chance = r["chance"]
                agent = r["agent"]
                success = random.randint(1, 100) <= chance
                if success:
                    villes_dispo = villes.VILLES_PAR_PAYS[r["pays"]]
                    v = next((v for v in villes_dispo if v["ville"] == r["ville"]), {})
                    reseaux.ajouter_reseau(r["id"], r["pays"], r["ville"], v.get("lat", 0), v.get("lon", 0))
                    reseaux.RESEAUX[r["id"]]["agents"].append(agent)
                    QMessageBox.information(self, "Succès", f"Le réseau {r['id']} a été créé à {r['ville']} ({r['pays']}).")
                    self.webView.load(QUrl.fromLocalFile(os.path.abspath(self.map_path)))
                else:
                    agent.rattachement = None
                    QMessageBox.warning(self, "Échec", f"La création du réseau {r['id']} a échoué.")
                self.refresh_reseaux()
                self.generate_osm_map()

    def process_timed_events(self):
        for r in RECRUTEMENTS_EN_COURS:
            if not r.traite and self.current_game_time >= r.date_fin:
                r.traite = True
                if r.type_recrutement in ["classique", "cible"]:
                    self.popup_selection_profil(r.ciblage)
                elif r.type_recrutement == "source":
                    self.popup_selection_source(r.ciblage)

    # --- ACCUEIL ---
    def _tab_accueil(self):
        widget = QWidget()
        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        self.map_path = "osm_map.html"
        self.generate_osm_map()
        self.webView = QWebEngineView()
        self.webView.load(QUrl.fromLocalFile(os.path.abspath(self.map_path)))
        self.liste_alertes = QListWidget()
        self.liste_crises = QListWidget()
        self.liste_missions = QListWidget()
        self.liste_alertes.itemDoubleClicked.connect(self.popup_alerte)
        self.liste_crises.itemDoubleClicked.connect(self.popup_crise)
        self.liste_missions.itemDoubleClicked.connect(self.popup_mission)
        side_layout = QVBoxLayout()
        side_layout.addWidget(QLabel("Alertes (France) :"))
        side_layout.addWidget(self.liste_alertes)
        side_layout.addWidget(QLabel("Crises en cours :"))
        side_layout.addWidget(self.liste_crises)
        side_layout.addWidget(QLabel("Missions en cours :"))
        side_layout.addWidget(self.liste_missions)
        hlayout.addLayout(side_layout, 1)

        hlayout.addWidget(self.webView, 4)
        action_layout = QVBoxLayout()
        action_layout.addStretch()
        hlayout.addLayout(action_layout, 1)
        layout.addLayout(hlayout)
        widget.setLayout(layout)
        return widget

    def generate_osm_map(self):
        m = folium.Map(location=[48.85, 2.35], zoom_start=4, tiles="OpenStreetMap")
        for agent in agents.AGENTS:
            folium.Marker(
                [getattr(agent, 'lat', 48.85), getattr(agent, 'lon', 2.35)],
                popup=self._popup_agent(agent),
                icon=folium.Icon(color='green', icon='user')
            ).add_to(m)
        for crise in crises.CRISES:
            lat, lon = getattr(crise, 'lat', 48.85), getattr(crise, 'lon', 2.35)
            folium.Marker(
                [lat, lon],
                popup=self._popup_crise(crise),
                icon=folium.Icon(color='red', icon='exclamation-sign', prefix='glyphicon')
            ).add_to(m)
        for nom, r in reseaux.RESEAUX.items():
            lat, lon = r.get('lat', 48.85), r.get('lon', 2.35)
            folium.Marker(
                [lat, lon],
                popup=self._popup_reseau(nom, r),
                icon=folium.Icon(color='black', icon='home', prefix='fa')
            ).add_to(m)
        m.save(self.map_path)

    def _popup_agent(self, agent):
        txt = f"<b>Agent :</b> {agent.nom} {agent.prenom}"
        if getattr(agent, "nom_code", None):
            txt += f" (Code: {agent.nom_code})"
        txt += f"<br>Bureau : {agent.bureau}<br>Niveau : {getattr(agent, 'niveau',1)}"
        if hasattr(agent, 'competences'):
            txt += "<br>Compétences : " + ", ".join(agent.competences)
        return txt

    def _popup_crise(self, crise):
        txt = f"<b>Crise :</b> {crise.nom}<br>Statut : {crise.statut}"
        if hasattr(crise, 'origine') and crise.origine:
            txt += f"<br>Origine : {crise.origine}"
        return txt

    def _popup_reseau(self, nom, r):
        txt = f"<b>Réseau clandestin :</b> {nom}<br>Pays : {r['pays']}"
        if r.get('ville'): txt += f"<br>Ville : {r['ville']}"
        txt += f"<br>Agents : {len(r['agents'])}, Sources : {len(r['sources'])}"
        return txt

    def refresh_agents(self):
        self.agentList.clear()
        for a in agents.AGENTS:
            nc = f" (Code: {a.nom_code})" if getattr(a, "nom_code", None) else ""
            item_str = f"{a.nom} {a.prenom}{nc} ({a.bureau})"
            item = QListWidgetItem(item_str)
            if getattr(a, "statut_legende", False):
                item.setForeground(Qt.darkYellow)
            self.agentList.addItem(item)
        self.generate_osm_map()
        self.webView.load(QUrl.fromLocalFile(os.path.abspath(self.map_path)))
        self.atlas_widget.update_atlas()
    def refresh_sources(self):
        self.sourceList.clear()
        par_reseau = {}
        for s in sources.SOURCES:
            try:
                reseau = s.rattachement or "Non rattachée"
            except AttributeError:
                reseau = "Non rattachée"
            par_reseau.setdefault(reseau, []).append(s)

        for reseau_nom, lst in par_reseau.items():
            self.sourceList.addItem(f"--- {reseau_nom} ---")
            for s in lst:
                metier = getattr(s, 'metier', getattr(s, 'infos', {}).get('metier', 'N/A'))
                item = QListWidgetItem(f"{s.nom} ({metier})")
                item.setData(Qt.UserRole, s)
                self.sourceList.addItem(item)

        self.sourceList.clear()
        par_reseau = {}
        for s in sources.SOURCES:
            try:
                reseau = s.rattachement or "Non rattachée"
            except AttributeError:
                reseau = "Non rattachée"
            par_reseau.setdefault(reseau, []).append(s)

        for reseau_nom, lst in par_reseau.items():
            self.sourceList.addItem(f"--- {reseau_nom} ---")
            for s in lst:
                item = QListWidgetItem(f"{s.nom} ({s.infos.get('metier', 'N/A')})")
                item.setData(Qt.UserRole, s)
                self.sourceList.addItem(item)

        self.agentList.clear()
        for a in agents.AGENTS:
            nc = f" (Code: {a.nom_code})" if getattr(a, "nom_code", None) else ""
            item_str = f"{a.nom} {a.prenom}{nc} ({a.bureau})"
            item = QListWidgetItem(item_str)
            if getattr(a, "statut_legende", False):
                item.setForeground(Qt.darkYellow)
            self.agentList.addItem(item)
        self.generate_osm_map()
        self.webView.load(QUrl.fromLocalFile(os.path.abspath(self.map_path)))
        self.atlas_widget.update_atlas()
    # ------------------ ONGLET AGENTS ------------------
    def _tab_agents(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Liste des agents :")
        layout.addWidget(label)
        self.agentList = QListWidget()
        for a in agents.AGENTS:
            nc = f" (Code: {a.nom_code})" if getattr(a, "nom_code", None) else ""
            item_str = f"{a.nom} {a.prenom}{nc} ({a.bureau})"
            item = QListWidgetItem(item_str)
            if getattr(a, "statut_legende", False):
                item.setForeground(Qt.darkYellow)
            self.agentList.addItem(item)
        layout.addWidget(self.agentList)
        self.agentList.itemDoubleClicked.connect(self.ouvrir_fiche_agent)
        btn_row = QHBoxLayout()
        recruter_btn = QPushButton("Recruter")
        recruter_btn.clicked.connect(self.open_recrutement_wizard_async)
        btn_row.addWidget(recruter_btn)
        modif_btn = QPushButton("Modifier l'agent sélectionné")
        btn_row.addWidget(modif_btn)
        del_btn = QPushButton("Supprimer l'agent sélectionné")
        del_btn.clicked.connect(self.supprimer_agent)
        btn_row.addWidget(del_btn)
        layout.addLayout(btn_row)
        widget.setLayout(layout)
        return widget

    def supprimer_agent(self):
        idx = self.agentList.currentRow()
        if idx >= 0 and idx < len(agents.AGENTS):
            agent = agents.AGENTS[idx]
            confirm = QMessageBox.question(self, "Supprimer", f"Supprimer {agent.nom} {agent.prenom} ?")
            if confirm == QMessageBox.Yes:
                agents.supprimer_agent(idx)
                self.refresh_agents()

    # ------------------ ONGLET SOURCES ------------------
    def _tab_sources(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Sources humaines :")
        layout.addWidget(label)
        self.sourceList = QListWidget()

        # Trie les sources par réseau
        par_reseau = {}
        for s in sources.SOURCES:
            try:
                reseau = s.rattachement or "Non rattachée"
            except AttributeError:
                reseau = "Non rattachée"
            par_reseau.setdefault(reseau, []).append(s)


        for reseau_nom, lst in par_reseau.items():
            self.sourceList.addItem(f"--- {reseau_nom} ---")
            for s in lst:
                item = QListWidgetItem(f"{s.nom} ({s.infos.get('metier', 'N/A')})")
                item.setData(Qt.UserRole, s)
                self.sourceList.addItem(item)

        layout.addWidget(self.sourceList)
        self.sourceList.itemDoubleClicked.connect(self.ouvrir_fiche_source)
        widget.setLayout(layout)
        return widget


    # ------------------ ONGLET MISSIONS ------------------
    def _tab_missions(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Missions en cours :")
        layout.addWidget(label)
        self.missionList = QListWidget()
        for m in missions.MISSIONS:
            self.missionList.addItem(f"{m.description} ({m.statut})")
        layout.addWidget(self.missionList)
        del_btn = QPushButton("Supprimer la mission sélectionnée")
        del_btn.clicked.connect(self.supprimer_mission)
        layout.addWidget(del_btn)
        widget.setLayout(layout)
        return widget

    def supprimer_mission(self):
        idx = self.missionList.currentRow()
        if idx >= 0 and idx < len(missions.MISSIONS):
            mission = missions.MISSIONS[idx]
            confirm = QMessageBox.question(self, "Supprimer", f"Supprimer {mission.description} ?")
            if confirm == QMessageBox.Yes:
                missions.supprimer_mission(idx)
                self.refresh_missions()

    # ------------------ ONGLET CRISES ------------------
    def _tab_crises(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Crises en cours :")
        layout.addWidget(label)
        self.criseList = QListWidget()
        for c in crises.CRISES:
            self.criseList.addItem(f"{c.nom} ({c.statut})")
        layout.addWidget(self.criseList)
        del_btn = QPushButton("Supprimer la crise sélectionnée")
        del_btn.clicked.connect(self.supprimer_crise)
        layout.addWidget(del_btn)
        widget.setLayout(layout)
        return widget

    def supprimer_crise(self):
        idx = self.criseList.currentRow()
        if idx >= 0 and idx < len(crises.CRISES):
            crise = crises.CRISES[idx]
            confirm = QMessageBox.question(self, "Supprimer", f"Supprimer {crise.nom} ?")
            if confirm == QMessageBox.Yes:
                crises.supprimer_crise(idx)
                self.refresh_crises()

    # ------------------ ONGLET RÉSEAUX ------------------
    def _tab_reseaux(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Réseaux et cellules :")
        layout.addWidget(label)
        self.reseauList = QListWidget()
        self.reseauList.itemDoubleClicked.connect(self.ouvrir_fiche_reseau)
        for k, v in reseaux.RESEAUX.items():
            self.reseauList.addItem(f"{k} ({v['pays']})")
        layout.addWidget(self.reseauList)
        del_btn = QPushButton("Supprimer le réseau sélectionné")
        del_btn.clicked.connect(self.supprimer_reseau)
        layout.addWidget(del_btn)
        widget.setLayout(layout)
        btn_creer = QPushButton("Créer un réseau")
        btn_creer.clicked.connect(self.popup_creation_reseau)
        layout.addWidget(btn_creer)
        return widget

    def supprimer_reseau(self):
        idx = self.reseauList.currentRow()
        noms = list(reseaux.RESEAUX.keys())
        if idx >= 0 and idx < len(noms):
            nom = noms[idx]
            confirm = QMessageBox.question(self, "Supprimer", f"Supprimer le réseau {nom} ?")
            if confirm == QMessageBox.Yes:
                reseaux.supprimer_reseau(nom)
                self.refresh_reseaux()

    # ------------------ ONGLET BUDGET ------------------
    def _tab_budget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Budget global :")
        layout.addWidget(label)
        solde = QLabel(f"Solde actuel : {budget.solde()} €")
        layout.addWidget(solde)
        histo = QListWidget()
        for motif, montant in budget.historique():
            histo.addItem(f"{motif}: {montant} €")
        layout.addWidget(QLabel("Historique des transactions :"))
        layout.addWidget(histo)
        widget.setLayout(layout)
        return widget

    # ------------------ ONGLET LOGISTIQUE ------------------
    def _tab_logistique(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Matériel disponible :"))
        matList = QListWidget()
        for m in logistique.lister_materiel():
            matList.addItem(f"{m['nom']} (x{m['quantite']}) - Affectation : {m['affectation']}")
        layout.addWidget(matList)
        layout.addWidget(QLabel("Plans d'urgence :"))
        planList = QListWidget()
        for p in logistique.lister_plans():
            planList.addItem(f"{p['nom']} : {p['description']}")
        layout.addWidget(planList)
        layout.addWidget(QLabel("Exfiltrations en cours :"))
        exfList = QListWidget()
        for e in logistique.lister_exfiltrations():
            exfList.addItem(f"Agent : {e['agent']}, Lieu : {e['lieu']}, Statut : {e['statut']}")
        layout.addWidget(exfList)
        layout.addWidget(QLabel("Moyens déployés :"))
        moyensList = QListWidget()
        for mo in logistique.lister_moyens():
            moyensList.addItem(f"{mo['type']} : {mo['details']}")
        layout.addWidget(moyensList)
        widget.setLayout(layout)
        return widget
    # --- Double clic agent : ouvre fiche (dossier complet) ---
    def ouvrir_fiche_agent(self, item):
        idx = self.agentList.row(item)
        if idx < 0 or idx >= len(agents.AGENTS):
            return
        agent = agents.AGENTS[idx]
        fiche_id = f"{agent.nom}_{agent.prenom}_{agent.bureau}"
        if fiches.get_fiche(fiche_id) is None:
            fiches.creer_fiche(fiche_id, "agent", {
                "Nom": agent.nom, "Prénom": agent.prenom,
                "Pays": agent.pays, "Bureau": agent.bureau,
                "Compétences": ", ".join(agent.competences),
                "Langues": ", ".join(agent.langues),
                "Niveau": agent.niveau, "XP": agent.exp,
                "Statut légende": "Oui" if agent.statut_legende else "Non",
                "Légende nom": agent.legende_nom or "Aucune",
                "Légende temporaire": str(agent.legende_temp) if agent.legende_temp else "Aucune"
            })
        fiche = fiches.get_fiche(fiche_id)
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Dossier agent {agent.nom} {agent.prenom}" + (f" (Code: {agent.nom_code})" if agent.nom_code else ""))
        layout = QVBoxLayout(dlg)
        infos = fiche["infos"]
        for k, v in infos.items():
            layout.addWidget(QLabel(f"<b>{k} :</b> {v}"))

        # --- Affichage légende actuelle ---
        if agent.legende_temp:
            leg = agent.legende_temp
            couv = leg.get("couverture", "Aucune")
            pays = leg.get("pays", "Aucun")
            nom = leg.get("nom", "Inconnu")
            prenom = leg.get("prenom", "Inconnu")
            layout.addWidget(QLabel(f"<b>Légende actuelle :</b> {nom} {prenom} - {pays} ({couv})"))

        # --- Affichage des 5 dernières légendes (hors légende actuelle) ---
        if agent.historique_legendes:
            layout.addWidget(QLabel("<b>5 dernières légendes utilisées :</b>"))
            for i, leg in enumerate(agent.historique_legendes[:5]):
                couv = leg.get("couverture", "Aucune")
                pays = leg.get("pays", "Aucun")
                nom = leg.get("nom", "Inconnu")
                prenom = leg.get("prenom", "Inconnu")
                layout.addWidget(QLabel(
                    f"{i+1}. {nom} {prenom} - {pays} ({couv})"
                ))

        # --- Bouton Reprendre légende ---
        if agent.historique_legendes:
            btn_reprendre = QPushButton("Reprendre légende")
            layout.addWidget(btn_reprendre)
            def ouvrir_menu_reprendre():
                menu_dlg = QDialog(self)
                menu_dlg.setWindowTitle("Reprendre une ancienne légende")
                vbox = QVBoxLayout(menu_dlg)
                choix_leg = QComboBox()
                for leg in agent.historique_legendes[:5]:
                    txt = f"{leg.get('nom', '')} {leg.get('prenom', '')} / {leg.get('pays', '')} / {leg.get('couverture', '')}"
                    choix_leg.addItem(txt)
                vbox.addWidget(QLabel("Choisissez une ancienne légende à réassigner :"))
                vbox.addWidget(choix_leg)
                valider_btn = QPushButton("Valider reprise")
                vbox.addWidget(valider_btn)
                def valider_reprise():
                    idx_sel = choix_leg.currentIndex()
                    agent.reprendre_legende(idx_sel)
                    QMessageBox.information(self, "Légende reprise", "Légende réassignée à l'agent.")
                    menu_dlg.accept()
                    dlg.accept()
                    self.refresh_agents()
                valider_btn.clicked.connect(valider_reprise)
                menu_dlg.setLayout(vbox)
                menu_dlg.exec_()
            btn_reprendre.clicked.connect(ouvrir_menu_reprendre)
        # --- Missions passées ---
        layout.addWidget(QLabel("<b>Missions passées :</b>"))
        missions_agent = [m for m in missions.MISSIONS if getattr(m, "assigned_agent", None) == agent]
        for m in missions_agent:
            layout.addWidget(QLabel(f"- {m.description} ({m.statut})"))
        historique = fiche.get("historique", [])
        if historique:
            layout.addWidget(QLabel("<b>Historique :</b>"))
            for evt in historique:
                layout.addWidget(QLabel(str(evt)))
        # --- Boutons légende temporaire ---
        btns = QHBoxLayout()
        btn_creer = QPushButton("Créer une légende")
        btn_suppr = QPushButton("Supprimer la légende")
        btns.addWidget(btn_creer)
        btns.addWidget(btn_suppr)
        btn_creer.setEnabled(agent.legende_temp is None)
        btn_suppr.setEnabled(agent.legende_temp is not None)
        layout.addLayout(btns)

        def creer_legende_direct():
            from noms import NOMS_PRENOMS
            pays_dlg = QDialog(self)
            pays_dlg.setWindowTitle("Sélectionner le pays du faux nom de la légende")
            playout = QVBoxLayout(pays_dlg)
            pays_combo = QComboBox()
            pays_combo.addItems(sorted(NOMS_PRENOMS.keys()))
            playout.addWidget(QLabel("Choisissez le pays cible pour le faux nom :"))
            playout.addWidget(pays_combo)
            valider_btn = QPushButton("Générer légende")
            playout.addWidget(valider_btn)
            def valider_legende():
                pays = pays_combo.currentText()
                couverture = metiers.choisir_metier_competence(agent.competences)
                if not couverture or not couverture.get("metier"):
                    QMessageBox.warning(self, "Aucun métier", "Aucun métier possible pour ces compétences.")
                    return
                nom_temp, prenom_temp = noms.generer_nom_prenom(pays)
                legende_temp = {
                    "nom": nom_temp,
                    "prenom": prenom_temp,
                    "pays": pays,
                    "couverture": couverture["metier"],
                    "entreprise": couverture["entreprise"]
                }
                agent.affecter_legende_temp(legende_temp)
                if not agent.nom_code:
                    nom_code, ok = QInputDialog.getText(self, "Nom de code", "Entrez un nom de code unique pour cet agent (définitif) :")
                    if not ok or not nom_code:
                        QMessageBox.warning(self, "Nom de code requis", "Aucun nom de code saisi. La légende est créée mais l'agent n'a pas de nom de code.")
                    else:
                        agent.nom_code = nom_code
                QMessageBox.information(self, "Légende temporaire", f"Légende temporaire générée pour l'agent : {nom_temp} {prenom_temp}, {couverture['metier']} chez {couverture['entreprise']}")
                pays_dlg.accept()
                dlg.accept()
                self.refresh_agents()
            valider_btn.clicked.connect(valider_legende)
            pays_dlg.setLayout(playout)
            pays_dlg.exec_()
        btn_creer.clicked.connect(creer_legende_direct)

        def supprimer_legende_direct():
            agent.supprimer_legende_temp()
            QMessageBox.information(self, "Légende supprimée", "Légende temporaire supprimée pour cet agent.")
            dlg.accept()
            self.refresh_agents()
        btn_suppr.clicked.connect(supprimer_legende_direct)
        dlg.setLayout(layout)
        dlg.exec_()

    def ouvrir_fiche_source(self, item):
        source = item.data(Qt.UserRole)
        if not source or not hasattr(source, "infos"):
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Dossier source : {source.nom}")
        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel(f"<b>Nom :</b> {source.nom}"))
        layout.addWidget(QLabel(f"<b>Pays :</b> {source.pays}"))
        layout.addWidget(QLabel(f"<b>Ville :</b> {source.ville}"))
        layout.addWidget(QLabel(f"<b>Réseau :</b> {source.rattachement}"))
        layout.addWidget(QLabel(f"<b>Métier :</b> {source.infos.get('metier', 'Non renseigné')}"))
        layout.addWidget(QLabel(f"<b>Compétences :</b> {', '.join(source.infos.get('competences', []))}"))
        layout.addWidget(QLabel(f"<b>Langues :</b> {', '.join(source.infos.get('langues', []))}"))
        layout.addWidget(QLabel(f"<b>Agent recruteur :</b> {getattr(source, 'agent_recruteur', 'Inconnu')}"))
        dlg.setLayout(layout)
        dlg.exec_()


    # --- RECRUTEMENT ASYNC AVEC DÉLAI INGAME ---
    def open_recrutement_wizard_async(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Recrutement d'agent - Sélectionnez le mode")
        layout = QVBoxLayout(dlg)
        radio_alea = QRadioButton("Recrutement aléatoire (rapide, peu exigeant)")
        radio_cible = QRadioButton("Recrutement ciblé (compétences/bureau)")
        radio_alea.setChecked(True)
        group = QButtonGroup(dlg)
        group.addButton(radio_alea)
        group.addButton(radio_cible)
        layout.addWidget(radio_alea)
        layout.addWidget(radio_cible)
        layout.addWidget(QLabel(" "))
        layout.addWidget(QLabel("Pour recrutement ciblé, choisissez vos critères :"))
        bureau_combo = QComboBox()
        bureau_combo.addItems([b['code'] for b in bureaux.BUREAUX])
        layout.addWidget(QLabel("Bureau (optionnel) :"))
        layout.addWidget(bureau_combo)
        comp_label = QLabel("Compétences (optionnelles) :")
        layout.addWidget(comp_label)
        comp_boxes = []
        for c in ["Infiltration", "Surveillance", "Hacking", "Langues étrangères", "Négociation", "Combat rapproché", "Crypto", "Conduite", "Déguisement"]:
            box = QCheckBox(c)
            comp_boxes.append(box)
            layout.addWidget(box)
        bureau_combo.setEnabled(False)
        comp_label.setEnabled(False)
        for box in comp_boxes: box.setEnabled(False)
        radio_cible.toggled.connect(lambda checked: [
            bureau_combo.setEnabled(checked),
            comp_label.setEnabled(checked),
            [box.setEnabled(checked) for box in comp_boxes]
        ])
        go_btn = QPushButton("Lancer recrutement")
        layout.addWidget(go_btn)
        result_lbl = QLabel("")
        layout.addWidget(result_lbl)
        def lancer_recrutement():
            result_lbl.setText("Recrutement en cours... (délai ingame)")
            dlg.accept()
            if radio_alea.isChecked():
                type_recrutement = "classique"
                duree_jours = 2
                ciblage = None
            else:
                type_recrutement = "cible"
                duree_jours = 5
                ciblage = {}
                if bureau_combo.currentText():
                    ciblage["bureau"] = bureau_combo.currentText()
                comp_select = [box.text() for box in comp_boxes if box.isChecked()]
                if comp_select: ciblage["competences"] = comp_select
            date_debut = self.current_game_time
            date_fin = date_debut + timedelta(days=duree_jours)
            RECRUTEMENTS_EN_COURS.append(RecrutementEnCours(type_recrutement, ciblage, date_debut, date_fin))
            QMessageBox.information(self, "Recrutement lancé", f"Recrutement {type_recrutement} en cours\nDisponible le {date_fin.strftime('%d/%m/%Y à %H:%M')}\nVous pouvez continuer à jouer ou lancer d'autres actions.")
        go_btn.clicked.connect(lancer_recrutement)
        dlg.exec_()

    def popup_selection_profil(self, ciblage):
        profils = recrutement.generer_profils(3, ciblage)
        dlg = QDialog(self)
        dlg.setWindowTitle("Sélection du profil recruté")
        layout = QVBoxLayout(dlg)
        choix_box = QButtonGroup(dlg)
        for i, profil in enumerate(profils):
            s = f"{profil['nom']} {profil['prenom']} - Pays: {profil['pays']}\n"
            s += f"Métier assigné : {profil['metier']} chez {profil['entreprise']}\n"
            s += f"Bureau idéal : {profil['bureau_ideal']} - Prix : {profil['cout']}€\n"
            s += f"Compétences universelles : {', '.join(profil['comp_univ'])}\n"
            s += f"Compétences métiers : {', '.join(profil['comp_metier'])}\n"
            radio = QRadioButton(s)
            choix_box.addButton(radio, i)
            layout.addWidget(radio)
        aff_combo = QComboBox()
        aff_combo.addItems([b['code'] for b in bureaux.BUREAUX])
        layout.addWidget(QLabel("Affectation proposée (modifiez à vos risques) :"))
        layout.addWidget(aff_combo)
        valider_btn = QPushButton("Valider recrutement")
        layout.addWidget(valider_btn)
        def valider_final():
            idx = choix_box.checkedId()
            if idx < 0:
                QMessageBox.warning(self, "Aucun profil", "Veuillez sélectionner un profil.")
                return
            profil = profils[idx]
            bureau_choisi = aff_combo.currentText()
            forcer = bureau_choisi != profil['bureau_ideal']
            agent, risque = recrutement.valider_recrutement(profil, bureau_choisi, legende_nom_choisi=None, forcer=forcer)
            if agent:
                self.refresh_agents()
                QMessageBox.information(self, "Recrutement", f"Agent {agent.nom} {agent.prenom} recruté ({agent.bureau})\n{'Risque accru !' if risque else ''}")
                dlg.accept()
            else:
                QMessageBox.warning(self, "Erreur recrutement", "Erreur lors du paiement ou ajout agent.")
        valider_btn.clicked.connect(valider_final)
        dlg.exec_()

    def popup_selection_source(self, ciblage):
        reseau_nom = ciblage["reseau"]
        agent = ciblage["agent"]
        secteur = ciblage["secteur"]
        pays = reseaux.RESEAUX[reseau_nom]["pays"]
        villes_possibles = villes.VILLES_PAR_PAYS.get(pays.lower(), [])
        langues_possibles = langues.LANGUES_PAR_PAYS.get(pays.lower(), [])
        if not villes_possibles:
            QMessageBox.warning(self, "Erreur", f"Aucune ville trouvée pour le pays : {pays}")
            return

        candidats = []
        for _ in range(random.randint(1, 3)):
            nom, prenom = noms.generer_nom_prenom(pays)
            ville = random.choice(villes_possibles)["ville"]
            metier = metiers.choisir_metier_secteur(secteur)
            langues_source = random.sample(langues_possibles, k=min(2, len(langues_possibles)))
            candidats.append({
                "nom": nom,
                "prenom": prenom,
                "pays": pays,
                "ville": ville,
                "metier": metier["metier"],
                "competences": metier["competences"],
                "langues": langues_source
            })

        dlg = QDialog(self)
        dlg.setWindowTitle("Résultats de la recherche de source")
        layout = QVBoxLayout(dlg)
        choix_box = QButtonGroup(dlg)

        for i, s in enumerate(candidats):
            txt = f"{s['nom']} {s['prenom']} ({s['ville']}, {s['pays']})\n"
            txt += f"Métier : {s['metier']}\nCompétences : {', '.join(s['competences'])}\nLangues : {', '.join(s['langues'])}"
            radio = QRadioButton(txt)
            choix_box.addButton(radio, i)
            layout.addWidget(radio)

        btn_valider = QPushButton("Recruter la source sélectionnée")
        layout.addWidget(btn_valider)

        def valider():
            idx = choix_box.checkedId()
            if idx < 0:
                QMessageBox.information(self, "Aucune sélection", "Aucune source ne sera recrutée.")
                dlg.accept()
                return
            s = candidats[idx]
            from dossiers import DossierSource
            dossier = DossierSource(
                nom=f"{s['nom']} {s['prenom']}",
                pays=s["pays"], ville=s["ville"],
                infos={
                    "metier": s["metier"],
                    "competences": s["competences"],
                    "langues": s["langues"]
                },
                agent_recruteur=agent.nom + " " + agent.prenom,
                rattachement=reseau_nom
            )
            sources.SOURCES.append(dossier)
            reseaux.rattacher_source_reseau(reseau_nom, dossier)
            reseaux.ajouter_evenement(reseau_nom, f"Source recrutée : {dossier.nom}")
            QMessageBox.information(self, "Source ajoutée", f"La source {dossier.nom} a été recrutée.")
            self.refresh_sources()
            dlg.accept()
            self.refresh_reseaux()

        btn_valider.clicked.connect(valider)
        dlg.setLayout(layout)
        dlg.exec_()

    def popup_alerte(self, item):
        idx = self.liste_alertes.row(item)
        if idx < 0 or idx >= len(ALERTES_EN_COURS): return
        al = ALERTES_EN_COURS[idx]
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alerte reçue")
        dlg.setText(f"{al['emetteur']}\n\n{al['message']}")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.Ignore | QMessageBox.Cancel)
        dlg.button(QMessageBox.Yes).setText("Action")
        dlg.button(QMessageBox.Cancel).setText("En attente")
        dlg.button(QMessageBox.Ignore).setText("Ignorer")
        res = dlg.exec_()
        if res == QMessageBox.Yes:
            m = missions.generer_mission_automatique()
            PROCHAINES_MISSIONS.append(m)
            self.refresh_missions_accueil()
        elif res == QMessageBox.Ignore:
            ALERTES_EN_COURS.pop(idx)
        self.refresh_alertes()

    def refresh_crises_onglet(self):
        self.criseList.clear()
        for c in crises.CRISES:
            self.criseList.addItem(f"{c.nom} ({c.statut})")

    def popup_crise(self, item):
        idx = self.liste_crises.row(item)
        if idx < 0 or idx >= len(crises.CRISES): return
        c = crises.CRISES[idx]
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Crise en cours")
        dlg.setText(f"{c.nom} - Origine : {c.origine or 'N/A'}")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        dlg.button(QMessageBox.Yes).setText("Action")
        dlg.button(QMessageBox.Cancel).setText("En attente")
        res = dlg.exec_()
        if res == QMessageBox.Yes:
            c.statut = "Action lancée"
            crises.modifier_crise(idx, statut="Action lancée")  # optionnel si tu veux maintenir la cohérence
        self.refresh_crises()
        self.refresh_crises_onglet()

    def popup_mission(self, item):
        idx = self.liste_missions.row(item)
        if idx < 0 or idx >= len(missions.MISSIONS): return
        m = missions.MISSIONS[idx]
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Mission")
        dlg.setText(f"{m.description}\nType : {m.type_mission}")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        dlg.button(QMessageBox.Yes).setText("Créer mission")
        dlg.button(QMessageBox.Cancel).setText("En attente")
        res = dlg.exec_()
        if res == QMessageBox.Yes:
            m.demarrer(self.current_game_time, random.randint(600, 2880))
        self.refresh_missions_accueil()
        self.missionList.addItem(f"{m.description} ({m.statut})")

    def refresh_alertes(self):
        self.liste_alertes.clear()
        for al in ALERTES_EN_COURS[-10:]:
            self.liste_alertes.addItem(f"{al['emetteur']} : {al['message']}")

    def refresh_crises(self):
        self.liste_crises.clear()
        for c in crises.lister_crises():
            couleur = "[VERT]" if c.statut == "Action lancée" else "[ROUGE]"
            self.liste_crises.addItem(f"{couleur} {c.nom}")
        self.generate_osm_map()
        self.webView.load(QUrl.fromLocalFile(os.path.abspath(self.map_path)))
        self.liste_crises.addItem(f"{couleur} {c.nom}")

    def refresh_missions_accueil(self):
        self.liste_missions.clear()
        for m in missions.get_missions()[-20:]:
            self.liste_missions.addItem(f"{m.description} ({m.statut})")
        
    def check_automatic_events(self):
        if not hasattr(self, "prochaine_alerte"):
            self.prochaine_alerte = self.current_game_time + timedelta(hours=random.randint(5, 20))
        if not hasattr(self, "prochaine_mission"):
            self.prochaine_mission = self.current_game_time + timedelta(hours=random.randint(1, 10))
        if not hasattr(self, "prochaine_crise"):
            self.prochaine_crise = self.current_game_time + timedelta(hours=random.randint(12, 48))

        if self.current_game_time >= self.prochaine_alerte:
            alerte = services_francais.generer_alerte()
            ALERTES_EN_COURS.append(alerte)
            self.refresh_alertes()
            self.prochaine_alerte = self.current_game_time + timedelta(hours=random.randint(5, 20))

        if self.current_game_time >= self.prochaine_mission:
            mission = missions.generer_mission_automatique()
            PROCHAINES_MISSIONS.append(mission)
            self.refresh_missions_accueil()
            self.prochaine_mission = self.current_game_time + timedelta(hours=random.randint(1, 10))

        if self.current_game_time >= self.prochaine_crise:
            if len(crises.CRISES) < 2:
                ville = random.choice(random.choice(list(missions.VILLES_PAR_PAYS.values())))
                c = crises.Crise(origine="Inconnue", gravite="Élevée", lat=ville['lat'], lon=ville['lon'])
                c.demarrer(self.current_game_time, random.randint(600, 1440))
                crises.ajouter_crise(c)
                self.refresh_crises()
                self.refresh_crises_onglet()
            self.prochaine_crise = self.current_game_time + timedelta(hours=random.randint(24, 72))
            
    def popup_creation_reseau(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Créer un réseau clandestin")
        layout = QFormLayout(dlg)

        agents_libres = [a for a in agents.AGENTS if not getattr(a, 'rattachement', None) and est_disponible(a)]
        agent_combo = QComboBox()
        agent_combo.addItems([f"{a.nom} {a.prenom}" for a in agents_libres])
        layout.addRow("Agent :", agent_combo)

        pays_combo = QComboBox()
        pays_combo.addItems(sorted(villes.VILLES_PAR_PAYS.keys()))
        layout.addRow("Pays :", pays_combo)

        ville_combo = QComboBox()
        def update_villes(p):
            ville_combo.clear()
            ville_combo.addItems([v["ville"] for v in villes.VILLES_PAR_PAYS[p]])
        pays_combo.currentTextChanged.connect(update_villes)
        update_villes(pays_combo.currentText())
        layout.addRow("Ville :", ville_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)

        dlg.setLayout(layout)
        if dlg.exec_():
            agent = agents_libres[agent_combo.currentIndex()]
            pays = pays_combo.currentText()
            ville = ville_combo.currentText()
            existants = list(reseaux.RESEAUX.keys()) + [r['id'] for r in CREATIONS_RESEAUX_EN_COURS]
            i = 1
            while True:
                id_reseau = f"Réseau {i:03}"
                if id_reseau not in existants:
                    break
                i += 1
            duree = random.randint(10, 60)
            date_fin = self.current_game_time + timedelta(days=duree)

            chance = 90  # Succès forcé simplifié


            CREATIONS_RESEAUX_EN_COURS.append({               
                "id": id_reseau,
                "agent": agent,
                "pays": pays,
                "ville": ville,
                "fin": date_fin,
                "chance": chance
            })
            self.refresh_reseaux()
            QMessageBox.information(self, "Réseau en création", f"{id_reseau} lancé à {ville} ({pays}) — résultat dans {duree} jours ingame.")
            
    def refresh_reseaux(self):
        self.reseauList.clear()
        for k, v in reseaux.RESEAUX.items():
            self.reseauList.addItem(f"{k} ({v['pays']})")
        for r in CREATIONS_RESEAUX_EN_COURS:
            self.reseauList.addItem(f"{r['id']} à {r['pays']} {r['ville']} — EN COURS DE CRÉATION")
            
    def ouvrir_fiche_reseau(self, item):
        texte = item.text()
        if "à" in texte:
            nom = texte.split(" à ")[0].strip()
        else:
            nom = texte.split(" (")[0].strip()
        r = reseaux.RESEAUX.get(nom)
        if not r:
            QMessageBox.warning(self, "Erreur", f"Réseau {nom} introuvable.")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Dossier réseau : {nom}")
        layout = QVBoxLayout(dlg)

        layout.addWidget(QLabel(f"<b>Nom :</b> {nom}"))
        layout.addWidget(QLabel(f"<b>Date de création :</b> {r.get('date_creation', 'Inconnue')}"))
        layout.addWidget(QLabel(f"<b>Pays :</b> {r['pays']}"))
        layout.addWidget(QLabel(f"<b>Ville :</b> {r['ville']}"))
        layout.addWidget(QLabel(f"<b>Coordonnées :</b> {r['lat']} / {r['lon']}"))

        resp = r.get("responsable")
        if resp:
            info = f"{resp.nom} {resp.prenom}"
            if resp.nom_code:
                info += f" (Code: {resp.nom_code})"
            info += f" — {resp.bureau}"
            layout.addWidget(QLabel(f"<b>Responsable :</b> {info}"))
        else:
            layout.addWidget(QLabel(f"<b>Responsable :</b> Aucun"))

        # Agents
        layout.addWidget(QLabel("<b>Agents affectés :</b>"))
        if r["agents"]:
            for a in r["agents"]:
                code = f" (Code: {a.nom_code})" if a.nom_code else ""
                layout.addWidget(QLabel(f"- {a.nom} {a.prenom}{code} — {a.bureau}"))
        else:
            layout.addWidget(QLabel("Aucun agent"))

        # Sources
        layout.addWidget(QLabel("<b>Sources rattachées :</b>"))
        if r["sources"]:
            for s in r["sources"]:
                layout.addWidget(QLabel(f"- {s.nom} — {s.infos.get('metier', 'Inconnu')}"))
        else:
            layout.addWidget(QLabel("Aucune source"))

        # Missions
        layout.addWidget(QLabel("<b>Missions liées :</b>"))
        if r["missions"]:
            for m in r["missions"]:
                layout.addWidget(QLabel(f"- {m.description} ({m.statut})"))
        else:
            layout.addWidget(QLabel("Aucune mission"))

        # Historique des événements
        layout.addWidget(QLabel("<b>Historique du réseau :</b>"))
        histo = r.get("evenements", [])
        if histo:
            for evt in histo[:5]:
                layout.addWidget(QLabel(f"• {evt}"))
        else:
            layout.addWidget(QLabel("Aucun événement enregistré"))

        # Gestion responsable
        btns = QHBoxLayout()
        btn_assigner = QPushButton("Assigner agent")
        btn_suppr = QPushButton("Supprimer responsable")
        btns.addWidget(btn_assigner)
        btns.addWidget(btn_suppr)
        layout.addLayout(btns)

        btn_assigner.setEnabled(resp is None)
        btn_suppr.setEnabled(resp is not None)

        def assigner():
            popup = QDialog(dlg)
            popup.setWindowTitle("Assigner responsable")
            vbox = QVBoxLayout(popup)
            combo = QComboBox()
            all_agents = agents.AGENTS
            for a in all_agents:
                code = f" (Code: {a.nom_code})" if a.nom_code else ""
                combo.addItem(f"{a.nom} {a.prenom}{code} — {a.bureau}")
            vbox.addWidget(QLabel("Sélectionnez un agent :"))
            vbox.addWidget(combo)
            bvalider = QPushButton("Valider")
            vbox.addWidget(bvalider)
            def confirmer():
                ag = all_agents[combo.currentIndex()]
                reseaux.definir_responsable(nom, ag)
                reseaux.ajouter_evenement(nom, f"Responsable assigné : {ag.nom} {ag.prenom}")
                popup.accept()
                dlg.accept()
                self.refresh_reseaux()
            bvalider.clicked.connect(confirmer)
            popup.setLayout(vbox)
            popup.exec_()

        def retirer():
            reseaux.supprimer_responsable(nom)
            reseaux.ajouter_evenement(nom, "Responsable supprimé.")
            dlg.accept()
            self.refresh_reseaux()

        btn_assigner.clicked.connect(assigner)
        btn_suppr.clicked.connect(retirer)
        # --- Boutons ajouter / retirer agent (hors responsable) ---
        gestion_layout = QHBoxLayout()
        btn_ajouter_agent = QPushButton("Ajouter un agent")
        btn_retirer_agent = QPushButton("Supprimer un agent")
        btn_retirer_agent.setEnabled(len(r["agents"]) > 0)
        gestion_layout.addWidget(btn_ajouter_agent)
        gestion_layout.addWidget(btn_retirer_agent)
        layout.addLayout(gestion_layout)

        def ajouter_agent():
            popup = QDialog(dlg)
            popup.setWindowTitle("Ajouter un agent")
            vbox = QVBoxLayout(popup)
            combo = QComboBox()
            disponibles = [a for a in agents.AGENTS if a not in r["agents"] and a != resp]
            for a in disponibles:
                code = f" (Code: {a.nom_code})" if a.nom_code else ""
                combo.addItem(f"{a.nom} {a.prenom}{code} — {a.bureau}")
            if not disponibles:
                QMessageBox.information(dlg, "Aucun agent", "Aucun agent disponible.")
                return
            vbox.addWidget(QLabel("Sélectionnez un agent à ajouter :"))
            vbox.addWidget(combo)
            btn_valider = QPushButton("Ajouter")
            vbox.addWidget(btn_valider)

            def valider_ajout():
                ag = disponibles[combo.currentIndex()]
                reseaux.rattacher_agent_reseau(nom, ag)
                reseaux.ajouter_evenement(nom, f"Agent ajouté : {ag.nom} {ag.prenom}")
                popup.accept()
                dlg.accept()
                self.refresh_reseaux()

            btn_valider.clicked.connect(valider_ajout)
            popup.setLayout(vbox)
            popup.exec_()

        def retirer_agent():
            popup = QDialog(dlg)
            popup.setWindowTitle("Supprimer un agent")
            vbox = QVBoxLayout(popup)
            combo = QComboBox()
            affectes = r["agents"]
            for a in affectes:
                code = f" (Code: {a.nom_code})" if a.nom_code else ""
                combo.addItem(f"{a.nom} {a.prenom}{code} — {a.bureau}")
            if not affectes:
                QMessageBox.information(dlg, "Aucun agent", "Aucun agent à retirer.")
                return
            vbox.addWidget(QLabel("Sélectionnez un agent à retirer :"))
            vbox.addWidget(combo)
            btn_valider = QPushButton("Retirer")
            vbox.addWidget(btn_valider)

            def valider_retrait():
                ag = affectes[combo.currentIndex()]
                r["agents"].remove(ag)
                reseaux.ajouter_evenement(nom, f"Agent retiré : {ag.nom} {ag.prenom}")
                popup.accept()
                dlg.accept()
                self.refresh_reseaux()

            btn_valider.clicked.connect(valider_retrait)
            popup.setLayout(vbox)
            popup.exec_()

        btn_ajouter_agent.clicked.connect(ajouter_agent)
        btn_retirer_agent.clicked.connect(retirer_agent)
        btn_recherche = QPushButton("Rechercher une source")
        layout.addWidget(btn_recherche)

        def lancer_recherche_source():
            popup = QDialog(dlg)
            popup.setWindowTitle("Recherche de source")
            vbox = QVBoxLayout(popup)
            agents_assignes = r["agents"]
            if not agents_assignes:
                QMessageBox.warning(popup, "Aucun agent", "Aucun agent n'est affecté à ce réseau.")
                return
            combo_agents = QComboBox()
            for a in agents_assignes:
                combo_agents.addItem(f"{a.nom} {a.prenom} ({a.bureau})")
            vbox.addWidget(QLabel("Sélectionnez l'agent qui lance la recherche :"))
            vbox.addWidget(combo_agents)

            secteurs = sorted(set([v["secteur"] for v in metiers.METIERS.values()]))
            combo_secteurs = QComboBox()
            combo_secteurs.addItems(secteurs)
            vbox.addWidget(QLabel("Choisissez un secteur d’activité :"))
            vbox.addWidget(combo_secteurs)

            valider = QPushButton("Lancer la recherche")
            vbox.addWidget(valider)

            def valider_recherche():
                agent = agents_assignes[combo_agents.currentIndex()]
                secteur = combo_secteurs.currentText()
                duree = random.randint(3, 10)
                date_debut = self.current_game_time
                date_fin = date_debut + timedelta(days=duree)
                RECRUTEMENTS_EN_COURS.append(RecrutementEnCours(
                    "source", {"agent": agent, "secteur": secteur, "reseau": nom}, date_debut, date_fin
                ))
                reseaux.ajouter_evenement(nom, f"Recherche de source lancée par {agent.nom} {agent.prenom} dans le secteur {secteur}")
                popup.accept()
                QMessageBox.information(self, "Recherche lancée", f"Résultats attendus dans {duree} jours ingame.")

            valider.clicked.connect(valider_recherche)
            popup.setLayout(vbox)
            popup.exec_()

        btn_recherche.clicked.connect(lancer_recherche_source)


        dlg.setLayout(layout)
        dlg.exec_()



def run_gui():
    app = QApplication(sys.argv)
    win = DGSESimGUI()
    win.show()
    sys.exit(app.exec_())




