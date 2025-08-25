import sys
import os
import random
import folium
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QTabWidget, QHBoxLayout, QListWidget, QMessageBox, QInputDialog, QComboBox,
    QDialog, QRadioButton, QButtonGroup, QCheckBox, QListWidgetItem, QFrame, QDialogButtonBox, QFormLayout, QProgressBar,
    QGroupBox, QSpinBox
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
import villes
import services_francais
import fiches
import reseaux
import atlas
import logistique
import dossiers_suspects
import actions_crises
from gestionnaire_actions import gestionnaire_actions
import formations

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
        self.tabs.addTab(self._tab_formations(), "Formations")
        self.tabs.addTab(self._tab_cheat(), "Cheat")

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

        # Barre d'état en haut à gauche (argent et réputation)
        self.status_bar_left = QWidget()
        status_layout = QHBoxLayout(self.status_bar_left)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        # Affichage de la réputation (barre de progression colorée)
        self.reputation_bar = QProgressBar()
        self.reputation_bar.setRange(0, 100)
        self.reputation_bar.setFixedWidth(180)
        self.reputation_bar.setFormat("Réputation: %p%")
        self.reputation_bar.setTextVisible(True)
        status_layout.addWidget(self.reputation_bar)
        
        status_layout.addStretch(1)
        
        # Barre de temps en haut à droite
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
        
        # Positionner les deux barres
        self.tabs.setCornerWidget(self.status_bar_left, Qt.TopLeftCorner)
        self.tabs.setCornerWidget(self.time_btn_bar, Qt.TopRightCorner)
        self.set_time_speed(1)
        self.creation_reseaux_en_cours = []
        
        # Mise à jour initiale des labels de statut
        self.update_status_labels()

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
    
    def update_status_labels(self):
        """Met à jour l'affichage de la réputation"""
        try:
            # Mettre à jour la réputation
            reputation_actuelle = budget.get_reputation_service()
            self.reputation_bar.setValue(int(reputation_actuelle))
            # Couleur dynamique selon la valeur
            if reputation_actuelle <= 20:
                color = "#e53935"  # rouge
            elif reputation_actuelle <= 40:
                color = "#fdd835"  # jaune
            elif reputation_actuelle <= 70:
                color = "#1e88e5"  # bleu
            else:
                color = "#43a047"  # vert
            self.reputation_bar.setStyleSheet(
                f"QProgressBar {{ border: 1px solid #bbb; border-radius: 3px; text-align: center; }} "
                f"QProgressBar::chunk {{ background-color: {color}; }}"
            )
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la réputation: {e}")

    def advance_game_time(self):
        if not self.paused:
            minutes_to_add = self.speed_to_minutes.get(self.time_speed, 3)
            self.current_game_time += timedelta(minutes=minutes_to_add)
            self.update_time_label()
            # Nouveau système de budget (feature flag): applique la rente et les dépenses planifiées
            try:
                budget.tick_time(self.current_game_time)
                budget.executer_depenses_planifiees(self.current_game_time)
            except Exception:
                pass
            self.check_automatic_events()
            self.process_timed_events()
            for m in missions.MISSIONS:
                if hasattr(m, 'maj_etat'):
                    m.maj_etat(self.current_game_time)
            for c in crises.CRISES:
                if hasattr(c, 'maj_etat'):
                    # Appliquer la dégradation naturelle (quotidienne)
                    if hasattr(c, 'appliquer_degradation_naturelle'):
                        c.appliquer_degradation_naturelle(self.current_game_time)
                    # Mettre à jour l'état
                    c.maj_etat(self.current_game_time)
            
            # Vérifier les statuts temporaires des agents
            for agent in agents.AGENTS:
                if hasattr(agent, 'verifier_fin_statut'):
                    agent.verifier_fin_statut(self.current_game_time)
            
            # Rafraîchir l'interface des agents si elle est visible
            if hasattr(self, 'agentList') and self.agentList.isVisible():
                self.refresh_agents()
            
            # Rafraîchir l'interface des crises si elle est visible
            if hasattr(self, 'criseList') and self.criseList.isVisible():
                self.refresh_crises_onglet()
            for exf in logistique.lister_exfiltrations():
                if exf.get("date_fin") and exf["statut"] == "En attente" and self.current_game_time >= exf["date_fin"]:
                    exf["statut"] = "Terminée"
            
            # Avancer les actions sur les crises
            try:
                gestionnaire_actions.avancer_actions(self.current_game_time)
            except Exception as e:
                print(f"Erreur lors de l'avancement des actions: {e}")
            # Finaliser les formations arrivées à échéance
            try:
                formations.finaliser_formations(self.current_game_time)
            except Exception as e:
                print(f"Erreur finalisation des formations: {e}")
            
            self.process_reseaux_creation()
            
            # Mettre à jour l'affichage de la réputation
            self.update_status_labels()
            # Rafraîchir l'onglet budget si présent
            if hasattr(self, 'refresh_budget_tab'):
                self.refresh_budget_tab()
            # Rafraîchir l'onglet formations si présent
            if hasattr(self, 'refresh_formations_tab'):
                self.refresh_formations_tab()


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
        # Suppression du double-clic sur la liste des crises de l'accueil
        # self.liste_crises.itemDoubleClicked.connect(self.popup_crise)
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
            
            # Couleur du marqueur selon la gravité de la crise
            couleur_marqueur = self._get_couleur_gravite_crise(crise)
            
            folium.Marker(
                [lat, lon],
                popup=self._popup_crise(crise),
                icon=folium.Icon(color=couleur_marqueur, icon='exclamation-sign', prefix='glyphicon')
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
        """Popup simplifié pour la carte OSM : seulement nom et statut"""
        txt = f"<b>Crise :</b> {crise.nom}<br><b>Statut :</b> {crise.statut}"
        return txt

    def _popup_reseau(self, nom, r):
        txt = f"<b>Réseau clandestin :</b> {nom}<br>Pays : {r['pays']}"
        if r.get('ville'): txt += f"<br>Ville : {r['ville']}"
        txt += f"<br>Agents : {len(r['agents'])}, Sources : {len(r['sources'])}"
        return txt

    def _get_couleur_gravite_crise(self, crise):
        """Retourne la couleur du marqueur selon la gravité de la crise"""
        gravite = getattr(crise, 'gravite', 'Élevée').lower()
        
        couleurs = {
            'faible': 'green',      # Vert pour faible
            'modérée': 'yellow',    # Jaune pour modérée  
            'élevée': 'orange',     # Orange pour élevée
            'critique': 'red',      # Rouge pour critique
            'maximale': 'purple'    # Violet pour maximale
        }
        
        return couleurs.get(gravite, 'red')  # Rouge par défaut si gravité inconnue

    def refresh_agents(self):
        self.agentList.clear()
        for a in agents.AGENTS:
            nc = f" (Code: {a.nom_code})" if getattr(a, "nom_code", None) else ""
            statut = getattr(a, "statut", "Disponible")
            item_str = f"{a.nom} {a.prenom}{nc} ({a.bureau}) - {statut}"
            item = QListWidgetItem(item_str)
            
            # Couleur selon le statut
            if statut == "Disponible":
                item.setForeground(Qt.darkGreen)
            elif statut == "En mission":
                item.setForeground(Qt.darkBlue)
            elif statut == "En formation":
                item.setForeground(Qt.darkCyan)
            elif statut == "Blessé":
                item.setForeground(Qt.darkRed)
            elif statut == "Disparu":
                item.setForeground(Qt.darkMagenta)
            elif statut == "Mort":
                item.setForeground(Qt.black)
            elif statut == "En repos":
                item.setForeground(Qt.darkYellow)
            
            # Légende en surbrillance
            if getattr(a, "statut_legende", False):
                item.setBackground(Qt.yellow)
            
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
                metier = getattr(s, 'metier', 'N/A')
                item = QListWidgetItem(f"{s.nom} ({metier})")
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
            statut = getattr(a, "statut", "Disponible")
            item_str = f"{a.nom} {a.prenom}{nc} ({a.bureau}) - {statut}"
            item = QListWidgetItem(item_str)
            
            # Couleur selon le statut
            if statut == "Disponible":
                item.setForeground(Qt.darkGreen)
            elif statut == "En mission":
                item.setForeground(Qt.darkBlue)
            elif statut == "En formation":
                item.setForeground(Qt.darkCyan)
            elif statut == "Blessé":
                item.setForeground(Qt.darkRed)
            elif statut == "Disparu":
                item.setForeground(Qt.darkMagenta)
            elif statut == "Mort":
                item.setForeground(Qt.black)
            elif statut == "En repos":
                item.setForeground(Qt.darkYellow)
            
            # Légende en surbrillance
            if getattr(a, "statut_legende", False):
                item.setBackground(Qt.yellow)
            
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
                metier = getattr(s, 'metier', 'N/A')
                item = QListWidgetItem(f"{s.nom} ({metier})")
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
        
        # Ajout du double-clic pour ouvrir la fenêtre détaillée
        self.criseList.itemDoubleClicked.connect(self.popup_crise_onglet)
        
        for c in crises.CRISES:
            # Affichage enrichi avec origine, gravité, pays et progression
            info_crise = f"{c.nom} - {c.origine} ({c.gravite})"
            if hasattr(c, 'pays') and c.pays:
                info_crise += f" - {c.pays.title()}"
            # Ajouter la progression
            progression = getattr(c, 'progression', 100)
            info_crise += f" - {progression:.1f}%"
            info_crise += f" [{c.statut}]"
            self.criseList.addItem(info_crise)
        layout.addWidget(self.criseList)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        del_btn = QPushButton("Supprimer la crise sélectionnée")
        del_btn.clicked.connect(self.supprimer_crise)
        btn_layout.addWidget(del_btn)
        
        # Bouton pour rafraîchir la liste
        refresh_btn = QPushButton("Rafraîchir")
        refresh_btn.clicked.connect(self.refresh_crises_onglet)
        btn_layout.addWidget(refresh_btn)
        
        # Bouton pour voir les actions en cours
        actions_btn = QPushButton("Actions en cours")
        actions_btn.clicked.connect(self._voir_actions_en_cours)
        btn_layout.addWidget(actions_btn)
        
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget

    def supprimer_crise(self):
        idx = self.criseList.currentRow()
        if idx >= 0 and idx < len(crises.CRISES):
            crise = crises.CRISES[idx]
            confirm = QMessageBox.question(self, "Supprimer", f"Supprimer {crise.nom} ?")
            if confirm == QMessageBox.Yes:
                # Supprimer les dossiers suspects associés
                nb_dossiers_supprimes = dossiers_suspects.supprimer_dossiers_crise(crise.nom)
                if nb_dossiers_supprimes > 0:
                    QMessageBox.information(self, "Nettoyage", f"{nb_dossiers_supprimes} dossier(s) suspect(s) supprimé(s)")
                
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
        # Références pour rafraîchir dynamiquement
        self.budget_solde_label = QLabel()
        layout.addWidget(self.budget_solde_label)
        
        layout.addWidget(QLabel("Historique des transactions :"))
        self.budget_histo_list = QListWidget()
        layout.addWidget(self.budget_histo_list)
        
        self.budget_etat_label = QLabel("Nouveau système budget: ACTIVÉ" if getattr(budget, 'NEW_BUDGET_ENABLED', False) else "Nouveau système budget: DÉSACTIVÉ")
        self.budget_etat_label.setStyleSheet("color: green;" if getattr(budget, 'NEW_BUDGET_ENABLED', False) else "color: gray;")
        layout.addWidget(self.budget_etat_label)
        
        # Premier rafraîchissement
        self.refresh_budget_tab()
        widget.setLayout(layout)
        return widget

    def refresh_budget_tab(self):
        """Rafraîchit l'onglet budget (solde et historique)"""
        try:
            if hasattr(self, 'budget_solde_label'):
                solde_actuel = budget.solde()
                solde_fmt = "{:,}".format(solde_actuel).replace(",", " ")
                self.budget_solde_label.setText(f"Solde actuel : {solde_fmt} €")
            if hasattr(self, 'budget_histo_list'):
                self.budget_histo_list.clear()
                for motif, montant in budget.historique()[-50:][::-1]:
                    montant_fmt = "{:,}".format(montant).replace(",", " ")
                    prefix = "+" if montant > 0 else ""
                    self.budget_histo_list.addItem(f"{motif}: {prefix}{montant_fmt} €")
            if hasattr(self, 'budget_etat_label'):
                actif = getattr(budget, 'NEW_BUDGET_ENABLED', False)
                self.budget_etat_label.setText("Nouveau système budget: ACTIVÉ" if actif else "Nouveau système budget: DÉSACTIVÉ")
                self.budget_etat_label.setStyleSheet("color: green;" if actif else "color: gray;")
        except Exception as e:
            print(f"Erreur refresh_budget_tab: {e}")

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
    
    # ------------------ ONGLET FORMATIONS ------------------
    def _tab_formations(self):
        """Onglet des formations"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Titre
        layout.addWidget(QLabel("<h2>Formations</h2>"))
        
        # Section Formations de Compétences
        comp_group = QGroupBox("Formations de Compétences")
        comp_layout = QVBoxLayout(comp_group)
        
        # Liste des formations de compétences
        comp_list = QListWidget()
        comp_layout.addWidget(comp_list)
        
        # Bouton pour ouvrir la planification des formations de compétences
        btn_planifier_comp = QPushButton("Planifier une formation de compétence")
        btn_planifier_comp.clicked.connect(self._ouvrir_planification_competence)
        comp_layout.addWidget(btn_planifier_comp)
        
        layout.addWidget(comp_group)
        
        # Section Formations Linguistiques (NOUVEAU)
        lang_group = QGroupBox("Formations Linguistiques")
        lang_layout = QVBoxLayout(lang_group)
        
        # Liste des formations linguistiques
        lang_list = QListWidget()
        lang_layout.addWidget(lang_list)
        
        # Bouton pour ouvrir la planification des formations linguistiques
        btn_planifier_lang = QPushButton("Planifier une formation linguistique")
        btn_planifier_lang.clicked.connect(self._ouvrir_planification_langue)
        lang_layout.addWidget(btn_planifier_lang)
        
        layout.addWidget(lang_group)
        
        # Section Formations en cours
        en_cours_group = QGroupBox("Formations en cours")
        en_cours_layout = QVBoxLayout(en_cours_group)
        
        # Liste des formations en cours
        self.formations_list = QListWidget()
        en_cours_layout.addWidget(self.formations_list)
        
        # Boutons de gestion
        btn_refresh = QPushButton("Rafraîchir")
        btn_refresh.clicked.connect(lambda: self.refresh_formations_tab())
        en_cours_layout.addWidget(btn_refresh)
        
        layout.addWidget(en_cours_group)
        
        # Charger les données
        self.refresh_formations_tab()
        
        return tab

    def _ouvrir_planification_competence(self):
        """Ouvre la planification des formations de compétences"""
        try:
            from formations import lister_formations_catalogue
            
            dlg = QDialog(self)
            dlg.setWindowTitle("Planifier une formation de compétence")
            dlg.setGeometry(400, 500, 600, 500)
            
            layout = QVBoxLayout(dlg)
            
            # Sélection de l'agent
            layout.addWidget(QLabel("<b>Sélectionnez un agent :</b>"))
            agent_combo = QComboBox()
            agents_disponibles = [a for a in agents.AGENTS if a.est_disponible()]
            for agent in agents_disponibles:
                agent_combo.addItem(f"{agent.nom} {agent.prenom} ({agent.bureau})", agent)
            layout.addWidget(agent_combo)
            
            if not agents_disponibles:
                layout.addWidget(QLabel("Aucun agent disponible pour la formation"))
                btn_fermer = QPushButton("Fermer")
                btn_fermer.clicked.connect(dlg.accept)
                layout.addWidget(btn_fermer)
                dlg.setLayout(layout)
                dlg.exec_()
                return
            
            # Sélection de la formation
            layout.addWidget(QLabel("<b>Sélectionnez une formation :</b>"))
            formation_combo = QComboBox()
            formations = lister_formations_catalogue()
            for nom, config in formations.items():
                formation_combo.addItem(f"{nom} - {config['cout']}€ - {config['duree_jours']} jours", nom)
            layout.addWidget(formation_combo)
            
            # Informations sur la formation
            info_label = QLabel("Sélectionnez une formation pour voir les détails")
            info_label.setWordWrap(True)
            layout.addWidget(info_label)
            
            def update_info():
                nom_formation = formation_combo.currentData()
                if nom_formation and nom_formation in formations:
                    config = formations[nom_formation]
                    info = f"<b>Formation : {nom_formation}</b><br>"
                    info += f"• Coût : {config['cout']}€<br>"
                    info += f"• Durée : {config['duree_jours']} jours<br>"
                    info += f"• Compétence acquise : {', '.join(config['competences'])}"
                    info_label.setText(info)
                else:
                    info_label.setText("Sélectionnez une formation pour voir les détails")
            
            formation_combo.currentTextChanged.connect(update_info)
            update_info()
            
            # Boutons
            buttons_layout = QHBoxLayout()
            
            btn_planifier = QPushButton("Planifier la formation")
            btn_planifier.clicked.connect(lambda: self._planifier_formation_competence(
                agent_combo.currentData(),
                formation_combo.currentData(),
                dlg
            ))
            buttons_layout.addWidget(btn_planifier)
            
            btn_fermer = QPushButton("Fermer")
            btn_fermer.clicked.connect(dlg.accept)
            buttons_layout.addWidget(btn_fermer)
            
            layout.addLayout(buttons_layout)
            
            dlg.setLayout(layout)
            dlg.exec_()
            
        except ImportError:
            QMessageBox.warning(self, "Erreur", "Module formations non disponible")

    def _ouvrir_planification_langue(self):
        """Ouvre la planification des formations linguistiques"""
        try:
            from formations import lister_formations_langues_catalogue
            
            dlg = QDialog(self)
            dlg.setWindowTitle("Planifier une formation linguistique")
            dlg.setGeometry(400, 500, 600, 500)
            
            layout = QVBoxLayout(dlg)
            
            # Sélection de l'agent
            layout.addWidget(QLabel("<b>Sélectionnez un agent :</b>"))
            agent_combo = QComboBox()
            agents_disponibles = [a for a in agents.AGENTS if a.est_disponible()]
            for agent in agents_disponibles:
                # Afficher le nombre de langues actuelles
                nb_langues = len(getattr(agent, 'langues', []))
                agent_combo.addItem(f"{agent.nom} {agent.prenom} ({agent.bureau}) - {nb_langues}/5 langues", agent)
            layout.addWidget(agent_combo)
            
            if not agents_disponibles:
                layout.addWidget(QLabel("Aucun agent disponible pour la formation"))
                btn_fermer = QPushButton("Fermer")
                btn_fermer.clicked.connect(dlg.accept)
                layout.addWidget(btn_fermer)
                dlg.setLayout(layout)
                dlg.exec_()
                return
            
            # Sélection de la langue
            layout.addWidget(QLabel("<b>Sélectionnez une langue à apprendre :</b>"))
            langue_combo = QComboBox()
            formations_langues = lister_formations_langues_catalogue()
            
            # Filtrer les langues que l'agent ne maîtrise pas déjà
            agent_selectionne = agents_disponibles[0] if agents_disponibles else None
            langues_agent = getattr(agent_selectionne, 'langues', []) if agent_selectionne else []
            
            for nom, config in formations_langues.items():
                langue = config['langue']
                if langue.lower() not in [l.lower() for l in langues_agent]:
                    difficulte = config['difficulte']
                    couleur = "#2E8B57" if difficulte == "facile" else "#FF8C00" if difficulte == "moyenne" else "#DC143C"
                    langue_combo.addItem(f"{langue.title()} - {config['cout']}€ - {config['duree_jours']} jours - {difficulte}", nom)
                else:
                    langue_combo.addItem(f"{langue.title()} - DÉJÀ MAÎTRISÉE", nom)
                    # Désactiver cette option
                    langue_combo.setItemData(langue_combo.count() - 1, None, Qt.UserRole)
            
            layout.addWidget(langue_combo)
            
            # Mettre à jour la liste quand l'agent change
            def update_langues_agent():
                agent = agent_combo.currentData()
                if agent:
                    langues_agent = getattr(agent, 'langues', [])
                    langue_combo.clear()
                    
                    for nom, config in formations_langues.items():
                        langue = config['langue']
                        if langue.lower() not in [l.lower() for l in langues_agent]:
                            difficulte = config['difficulte']
                            couleur = "#2E8B57" if difficulte == "facile" else "#FF8C00" if difficulte == "moyenne" else "#DC143C"
                            langue_combo.addItem(f"{langue.title()} - {config['cout']}€ - {config['duree_jours']} jours - {difficulte}", nom)
                        else:
                            langue_combo.addItem(f"{langue.title()} - DÉJÀ MAÎTRISÉE", nom)
                            langue_combo.setItemData(langue_combo.count() - 1, None, Qt.UserRole)
            
            agent_combo.currentTextChanged.connect(update_langues_agent)
            
            # Informations sur la formation
            info_label = QLabel("Sélectionnez une langue pour voir les détails")
            info_label.setWordWrap(True)
            layout.addWidget(info_label)
            
            def update_info():
                nom_formation = langue_combo.currentData()
                if nom_formation and nom_formation in formations_langues:
                    config = formations_langues[nom_formation]
                    langue = config['langue']
                    difficulte = config['difficulte']
                    
                    info = f"<b>Formation linguistique : {langue.title()}</b><br>"
                    info += f"• Coût : {config['cout']}€<br>"
                    info += f"• Durée : {config['duree_jours']} jours<br>"
                    info += f"• Difficulté : {difficulte}<br>"
                    info += f"• Langue acquise : {langue.title()}"
                    
                    # Afficher la difficulté avec une couleur
                    if difficulte == "facile":
                        info += "<br><span style='color: #2E8B57;'>• Langue facile à apprendre</span>"
                    elif difficulte == "moyenne":
                        info += "<br><span style='color: #FF8C00;'>• Langue de difficulté moyenne</span>"
                    else:
                        info += "<br><span style='color: #DC143C;'>• Langue difficile à apprendre</span>"
                    
                    info_label.setText(info)
                else:
                    info_label.setText("Sélectionnez une langue pour voir les détails")
            
            langue_combo.currentTextChanged.connect(update_info)
            update_info()
            
            # Boutons
            buttons_layout = QHBoxLayout()
            
            btn_planifier = QPushButton("Planifier la formation")
            btn_planifier.clicked.connect(lambda: self._planifier_formation_langue(
                agent_combo.currentData(),
                langue_combo.currentData(),
                dlg
            ))
            buttons_layout.addWidget(btn_planifier)
            
            btn_fermer = QPushButton("Fermer")
            btn_fermer.clicked.connect(dlg.accept)
            buttons_layout.addWidget(btn_fermer)
            
            layout.addLayout(buttons_layout)
            
            dlg.setLayout(layout)
            dlg.exec_()
            
        except ImportError:
            QMessageBox.warning(self, "Erreur", "Module formations non disponible")

    def _planifier_formation_competence(self, agent, nom_formation, parent_dialog):
        """Planifie une formation de compétence"""
        try:
            from formations import planifier_formation
            
            if not agent or not nom_formation:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un agent et une formation")
                return
            
            succes, message = planifier_formation(agent, nom_formation, self.current_game_time)
            
            if succes:
                QMessageBox.information(self, "Formation planifiée", message)
                parent_dialog.accept()
                self.refresh_formations_tab()
            else:
                QMessageBox.warning(self, "Erreur", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la planification : {str(e)}")

    def _planifier_formation_langue(self, agent, nom_formation, parent_dialog):
        """Planifie une formation linguistique"""
        try:
            from formations import planifier_formation
            
            if not agent or not nom_formation:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un agent et une langue")
                return
            
            # Vérifier la limite de langues
            nb_langues = len(getattr(agent, 'langues', []))
            if nb_langues >= 5:
                QMessageBox.warning(self, "Limite atteinte", f"L'agent maîtrise déjà {nb_langues}/5 langues")
                return
            
            succes, message = planifier_formation(agent, nom_formation, self.current_game_time)
            
            if succes:
                QMessageBox.information(self, "Formation linguistique planifiée", message)
                parent_dialog.accept()
                self.refresh_formations_tab()
            else:
                QMessageBox.warning(self, "Erreur", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la planification : {str(e)}")

    def refresh_formations_tab(self):
        try:
            self.formations_list.clear()
            for f in formations.lister_formations_en_cours():
                ag = f.get('agent')
                nom = f.get('nom_formation')
                statut = f.get('statut')
                fin = f.get('date_fin')
                fin_txt = fin.strftime('%d/%m/%Y %H:%M') if fin else 'N/A'
                self.formations_list.addItem(
                    f"{nom} — {ag.nom} {ag.prenom} — {statut} — fin: {fin_txt}"
                )
        except Exception as e:
            print(f"Erreur refresh_formations_tab: {e}")
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
        # Mettre à jour dynamiquement les compétences et langues avant affichage
        try:
            fiches.ajouter_info_fiche(fiche_id, "Compétences", ", ".join(agent.competences))
            fiches.ajouter_info_fiche(fiche_id, "Langues", ", ".join(agent.langues))
        except Exception:
            pass
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
                vbox.addWidget(QLabel("Choisissez une ancienne légende à réassigner :"))
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
        """Ouvre l'assistant de recrutement en mode asynchrone"""
        dlg = QDialog(self)
        dlg.setWindowTitle("Assistant de Recrutement")
        dlg.setGeometry(400, 500, 600, 700)
        
        layout = QVBoxLayout(dlg)
        
        # Titre
        layout.addWidget(QLabel("<h2>Assistant de Recrutement</h2>"))
        
        # Section 1: Type de recrutement
        layout.addWidget(QLabel("<b>1. Type de recrutement</b>"))
        type_combo = QComboBox()
        type_combo.addItems(["Classique", "Ciblé"])
        layout.addWidget(type_combo)
        
        # Section 2: Ciblage
        ciblage_group = QGroupBox("2. Ciblage (optionnel)")
        ciblage_layout = QFormLayout(ciblage_group)
        
        # Bureau
        bureau_combo = QComboBox()
        bureau_combo.addItem("Aucun", None)
        for b in bureaux.BUREAUX:
            bureau_combo.addItem(f"{b['nom']} ({b['code']})", b['code'])
        ciblage_layout.addRow("Bureau:", bureau_combo)
        
        # Compétences
        competences_combo = QComboBox()
        competences_combo.addItem("Aucune", None)
        competences_liste = ["Infiltration", "Hacking", "Surveillance", "Combat rapproché", "Négociation", "Analyse", "Sécurité"]
        for comp in competences_liste:
            competences_combo.addItem(comp, comp)
        ciblage_layout.addRow("Compétence:", competences_combo)
        
        # Pays
        pays_combo = QComboBox()
        pays_combo.addItem("Aucun", None)
        for pays in sorted(villes.VILLES_PAR_PAYS.keys()):
            pays_combo.addItem(pays.title(), pays)
        ciblage_layout.addRow("Pays:", pays_combo)
        
        # Langue (NOUVEAU) - Import de la source unique
        from langues import obtenir_toutes_langues
        langue_combo = QComboBox()
        langue_combo.addItem("Aucune", None)
        langues_disponibles = obtenir_toutes_langues()
        for langue in langues_disponibles:
            langue_combo.addItem(langue.title(), langue)
        ciblage_layout.addRow("Langue:", langue_combo)
        
        layout.addWidget(ciblage_group)
        
        # Section 3: Informations de ciblage (nombre d'agents fixé à 1)
        info_label = QLabel("Sélectionnez des critères de ciblage pour voir les informations")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        layout.addWidget(info_label)
        
        def update_info():
            try:
                # Récupérer les critères sélectionnés
                bureau = bureau_combo.currentData()
                competence = competences_combo.currentData()
                pays = pays_combo.currentData()
                langue = langue_combo.currentData()
                
                # Construire le ciblage
                ciblage = {}
                if bureau:
                    ciblage["bureau"] = bureau
                if competence:
                    ciblage["competences"] = [competence]
                if pays:
                    ciblage["pays"] = pays
                if langue:
                    ciblage["langue"] = langue
                
                if ciblage:
                    # Afficher les informations de ciblage
                    info = "<b>Critères de ciblage sélectionnés :</b><br>"
                    if bureau:
                        info += f"• Bureau : {bureau}<br>"
                    if competence:
                        info += f"• Compétence : {competence}<br>"
                    if pays:
                        info += f"• Pays : {pays}<br>"
                    if langue:
                        info += f"• Langue : {langue}<br>"
                    
                    # Informations sur le coût
                    if type_combo.currentText() == "Ciblé":
                        info += "<br><b>Coût estimé :</b> 5000€ par agent (recrutement ciblé)"
                    else:
                        info += "<br><b>Coût estimé :</b> 2000€ par agent (recrutement classique)"
                    
                    info_label.setStyleSheet("QLabel { color: #2E8B57; font-weight: bold; }")
                else:
                    info = "Sélectionnez des critères de ciblage pour voir les informations"
                    info_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
                
                info_label.setText(info)
                
            except Exception as e:
                info_label.setText(f"Erreur lors de la mise à jour des informations : {str(e)}")
                info_label.setStyleSheet("QLabel { color: #DC143C; }")
        
        # Fonction pour activer/désactiver les options de ciblage
        def toggle_ciblage_options():
            if type_combo.currentText() == "Classique":
                ciblage_group.setEnabled(False)
                # Réinitialiser les sélections
                bureau_combo.setCurrentIndex(0)
                competences_combo.setCurrentIndex(0)
                pays_combo.setCurrentIndex(0)
                langue_combo.setCurrentIndex(0)
            else:
                ciblage_group.setEnabled(True)
            update_info()
        
        # Connecter les changements pour mettre à jour les informations
        type_combo.currentTextChanged.connect(toggle_ciblage_options)
        bureau_combo.currentTextChanged.connect(update_info)
        competences_combo.currentTextChanged.connect(update_info)
        pays_combo.currentTextChanged.connect(update_info)
        langue_combo.currentTextChanged.connect(update_info)
        
        # Initialiser l'état des options de ciblage
        toggle_ciblage_options()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        lancer_btn = QPushButton("Lancer le recrutement")
        lancer_btn.clicked.connect(lambda: self._lancer_recrutement_cible(
            type_combo.currentText(),
            bureau_combo.currentData(),
            competences_combo.currentData(),
            pays_combo.currentData(),
            langue_combo.currentData(),
            1,  # Nombre d'agents fixé à 1
            dlg
        ))
        buttons_layout.addWidget(lancer_btn)
        
        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(dlg.accept)
        buttons_layout.addWidget(btn_fermer)
        
        layout.addLayout(buttons_layout)
        
        dlg.setLayout(layout)
        dlg.exec_()

    def _lancer_recrutement_cible(self, type_recrutement, bureau, competence, pays, langue, nb_agents, parent_dialog):
        """Lance le recrutement avec les critères de ciblage"""
        try:
            # Construire le ciblage
            ciblage = {}
            if bureau:
                ciblage["bureau"] = bureau
            if competence:
                ciblage["competences"] = [competence]
            if pays:
                ciblage["pays"] = pays
            if langue:
                ciblage["langue"] = langue
            
            # Lancer le recrutement
            duree = random.randint(5, 15)
            date_debut = self.current_game_time
            date_fin = date_debut + timedelta(days=duree)
            
            # Déterminer le type de recrutement
            if type_recrutement == "Classique":
                type_final = "classique"
            else:
                type_final = "cible"
            
            # Ajouter à la liste des recrutements en cours
            RECRUTEMENTS_EN_COURS.append(RecrutementEnCours(
                type_final, ciblage, date_debut, date_fin
            ))
            
            # Message de confirmation
            message = f"Recrutement d'un agent lancé avec succès !<br><br>"
            if ciblage:
                message += "<b>Critères de ciblage :</b><br>"
                if bureau:
                    message += f"• Bureau : {bureau}<br>"
                if competence:
                    message += f"• Compétence : {competence}<br>"
                if pays:
                    message += f"• Pays : {pays}<br>"
                if langue:
                    message += f"• Langue : {langue}<br>"
                message += f"<br><b>Résultats attendus dans {duree} jours ingame.</b>"
            else:
                message += f"<b>Recrutement classique - Résultats attendus dans {duree} jours ingame.</b>"
            
            QMessageBox.information(self, "Recrutement lancé", message)
            parent_dialog.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du lancement du recrutement : {str(e)}")

    def popup_selection_profil(self, ciblage):
        # Générer 3 profils pour donner le choix
        profils = recrutement.generer_profils(3, ciblage)
        if not profils:
            QMessageBox.warning(self, "Erreur", "Aucun profil disponible.")
            return
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Sélection de l'agent recruté")
        dlg.setGeometry(300, 200, 800, 700)
        layout = QVBoxLayout(dlg)
        
        # Titre
        layout.addWidget(QLabel("<h3>Choisissez un agent à recruter</h3>"))
        
        # Groupe de boutons radio pour les profils
        choix_box = QButtonGroup(dlg)
        
        for i, profil in enumerate(profils):
            # Créer un frame pour chaque profil
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box)
            frame.setStyleSheet("QFrame { border: 2px solid #ddd; margin: 5px; padding: 10px; }")
            frame_layout = QVBoxLayout(frame)
            
            # Radio button
            radio = QRadioButton()
            if i == 0:  # Présélectionner le premier profil
                radio.setChecked(True)
            choix_box.addButton(radio, i)
            
            # Informations du profil
            info_text = f"<b>{profil['nom']} {profil['prenom']}</b> - {profil['pays'].title()}<br>"
            info_text += f"<b>Métier :</b> {profil['metier']} chez {profil['entreprise']}<br>"
            info_text += f"<b>Bureau idéal :</b> {profil['bureau_ideal']} - <b>Prix :</b> {profil['cout']}€<br>"
            
            # AFFICHAGE DES LANGUES
            if 'langues' in profil and profil['langues']:
                langues_str = ', '.join([l.title() for l in profil['langues']])
                info_text += f"<b>Langues :</b> {langues_str}<br>"
            
            # Compétences
            if profil['comp_univ']:
                info_text += f"<b>Compétences universelles :</b> {', '.join(profil['comp_univ'])}<br>"
            if profil['comp_metier']:
                info_text += f"<b>Compétences métiers :</b> {', '.join(profil['comp_metier'])}"
            
            # Layout horizontal pour radio + info
            profil_layout = QHBoxLayout()
            profil_layout.addWidget(radio)
            
            info_label = QLabel(info_text)
            info_label.setWordWrap(True)
            profil_layout.addWidget(info_label)
            
            frame_layout.addLayout(profil_layout)
            layout.addWidget(frame)
        
        # Affectation
        layout.addWidget(QLabel("<b>Affectation proposée (modifiable) :</b>"))
        aff_combo = QComboBox()
        bureaux_codes = [b['code'] for b in bureaux.BUREAUX]
        aff_combo.addItems(bureaux_codes)
        layout.addWidget(aff_combo)
        
        # Fonction pour mettre à jour le bureau recommandé
        def update_bureau_recommande():
            idx = choix_box.checkedId()
            if 0 <= idx < len(profils):
                profil_selectionne = profils[idx]
                if profil_selectionne['bureau_ideal'] in bureaux_codes:
                    aff_combo.setCurrentText(profil_selectionne['bureau_ideal'])
        
        # Connecter les changements de sélection
        for button in choix_box.buttons():
            button.toggled.connect(update_bureau_recommande)
        
        # Initialiser le bureau recommandé
        update_bureau_recommande()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        valider_btn = QPushButton("Recruter l'agent sélectionné")
        valider_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; }")
        
        annuler_btn = QPushButton("Annuler")
        annuler_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 10px; }")
        annuler_btn.clicked.connect(dlg.reject)
        
        buttons_layout.addWidget(annuler_btn)
        buttons_layout.addWidget(valider_btn)
        layout.addLayout(buttons_layout)
        
        def valider_final():
            idx = choix_box.checkedId()
            if idx < 0:
                QMessageBox.warning(self, "Aucun profil", "Veuillez sélectionner un profil.")
                return
            
            profil = profils[idx]
            bureau_choisi = aff_combo.currentText()
            forcer = bureau_choisi != profil['bureau_ideal']
            type_recrutement = 'cible' if ciblage else 'classique'
            agent, risque = recrutement.valider_recrutement(profil, bureau_choisi, legende_nom_choisi=None, forcer=forcer, type_recrutement=type_recrutement)
            if agent:
                self.refresh_agents()
                message = f"Agent {agent.nom} {agent.prenom} recruté avec succès !\n"
                message += f"Bureau : {agent.bureau}\n"
                if hasattr(agent, 'langues') and agent.langues:
                    message += f"Langues : {', '.join([l.title() for l in agent.langues])}\n"
                if risque:
                    message += "\n⚠️ Risque accru dû au forçage de bureau !"
                QMessageBox.information(self, "Recrutement réussi", message)
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
        langues_possibles = langues.obtenir_langues_pays(pays.lower())
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
            from sources import Source
            from dossiers import DossierSource
            
            # Créer l'objet Source pour la liste principale
            nouvelle_source = Source(
                nom=s["nom"],
                prenom=s["prenom"],
                metier=s["metier"],
                rattachement=reseau_nom
            )
            # Ajouter les informations supplémentaires dans le dossier
            nouvelle_source.dossier = {
                "pays": s["pays"],
                "ville": s["ville"],
                "competences": s["competences"],
                "langues": s["langues"],
                "agent_recruteur": agent.nom + " " + agent.prenom
            }
            sources.SOURCES.append(nouvelle_source)
            
            # Créer aussi un dossier source pour la compatibilité
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
            # Affichage enrichi avec origine, gravité, pays et progression
            info_crise = f"{c.nom} - {c.origine} ({c.gravite})"
            if hasattr(c, 'pays') and c.pays:
                info_crise += f" - {c.pays.title()}"
            # Ajouter la progression
            progression = getattr(c, 'progression', 100)
            info_crise += f" - {progression:.1f}%"
            info_crise += f" [{c.statut}]"
            self.criseList.addItem(info_crise)

    # Ancienne fonction popup_crise supprimée - remplacée par popup_crise_onglet

    def _lancer_action_crise(self, crise, dialog):
        """Lance une action sur la crise sélectionnée"""
        # Ouvrir le menu de sélection d'actions au lieu de fermer la fenêtre
        self._lancer_nouvelle_action(crise, dialog)

    def popup_crise_onglet(self, item):
        """Fenêtre détaillée de crise ouverte depuis l'onglet des crises"""
        idx = self.criseList.currentRow()
        if idx < 0 or idx >= len(crises.CRISES): return
        c = crises.CRISES[idx]
        
        # Si la crise est en attente, afficher d'abord le bouton "Gérer crise"
        if c.statut == "En attente":
            self.popup_crise_initiale(c)
            return
        
        # Sinon, afficher la fenêtre complète (crise déjà en cours)
        self.popup_crise_complete(c)
    
    def popup_crise_initiale(self, c):
        """Fenêtre initiale avec bouton 'Gérer crise' pour activer la crise"""
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Activation de la crise : {c.nom}")
        dlg.setGeometry(300, 200, 500, 300)
        
        layout = QVBoxLayout(dlg)
        
        # Titre
        titre = QLabel(f"<h2>Crise : {c.nom}</h2>")
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)
        
        # Informations de base
        info_label = QLabel(f"""
        <b>Statut :</b> {c.statut}<br>
        <b>Origine :</b> {getattr(c, 'origine', 'N/A')}<br>
        <b>Gravité :</b> {getattr(c, 'gravite', 'N/A')}<br>
        <b>Pays :</b> {getattr(c, 'pays', 'N/A').title() if getattr(c, 'pays', None) else 'N/A'}<br>
        <b>Progression :</b> {getattr(c, 'progression', 100):.1f}%
        """)
        info_label.setStyleSheet("padding: 20px; background-color: #f9f9f9; border-radius: 8px;")
        layout.addWidget(info_label)
        
        # Avertissement sur la dégradation
        warning_label = QLabel("⚠️ <b>Attention :</b> Une fois activée, cette crise commencera à se dégrader naturellement avec le temps.")
        warning_label.setStyleSheet("color: #d32f2f; padding: 15px; background-color: #ffebee; border-radius: 8px; border: 1px solid #f44336;")
        layout.addWidget(warning_label)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        btn_gerer = QPushButton("🚨 Gérer cette crise")
        btn_gerer.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        btn_gerer.clicked.connect(lambda: self.activer_crise(c, dlg))
        btn_layout.addWidget(btn_gerer)
        
        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(dlg.accept)
        btn_layout.addWidget(btn_fermer)
        
        layout.addLayout(btn_layout)
        
        dlg.setLayout(layout)
        dlg.exec_()
    
    def activer_crise(self, c, dialog):
        """Active une crise et ouvre la fenêtre de gestion complète"""
        from datetime import datetime, timedelta
        
        # Activer la crise
        c.statut = "En cours"
        c.actions_lancees = True
        
        # Réduire la progression à 98% pour permettre la dégradation
        c.progression = 98
        
        # Démarrer la crise si pas encore fait
        if not c.date_debut:
            c.demarrer(self.current_game_time, random.randint(600, 1440))  # 10-24h
        
        # Définir la date de dernière action au temps de jeu actuel
        # Cela permettra à la dégradation naturelle de fonctionner normalement
        c.derniere_action_date = self.current_game_time
        
        # Appliquer une dégradation immédiate symbolique (1% pour montrer que ça commence)
        c.progression = max(0, c.progression - 1)
        
        print(f"INFO: Crise {c.nom} activée et passée en statut 'En cours'")
        print(f"INFO: Progression réduite à 98% puis à 97% pour montrer la dégradation")
        print(f"INFO: Progression finale: {c.progression:.1f}%")
        print(f"INFO: La dégradation naturelle continue maintenant avec le temps de jeu")
        
        # Fermer la fenêtre d'activation
        dialog.accept()
        
        # Ouvrir la fenêtre de gestion complète
        self.popup_crise_complete(c)
    
    def popup_crise_complete(self, c):
        """Fenêtre complète de gestion de crise (après activation)"""
        # Création d'une fenêtre détaillée avec tableau
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Gestion de la crise : {c.nom}")
        dlg.setGeometry(400, 500, 700, 500)
        
        layout = QVBoxLayout(dlg)
        
        # Titre
        titre = QLabel(f"<h2>Crise : {c.nom}</h2>")
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)
        
        # Tableau des détails (en lecture seule)
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
        
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Propriété", "Valeur"])
        
        # Données de la crise
        donnees = [
            ("Statut", c.statut),
            ("Origine", getattr(c, 'origine', 'N/A')),
            ("Gravité", getattr(c, 'gravite', 'N/A')),
            ("Pays", getattr(c, 'pays', 'N/A').title() if getattr(c, 'pays', None) else 'N/A'),
            ("Progression", f"{getattr(c, 'progression', 100):.1f}%"),
            ("Latitude", f"{getattr(c, 'lat', 0):.4f}"),
            ("Longitude", f"{getattr(c, 'lon', 0):.4f}"),
            ("Date début", c.date_debut.strftime("%d/%m/%Y %H:%M") if c.date_debut else 'N/A'),
            ("Date fin", c.date_fin.strftime("%d/%m/%Y %H:%M") if c.date_fin else 'N/A')
        ]
        
        # Ajout des étapes
        etapes = getattr(c, 'etapes', [])
        if etapes:
            donnees.append(("Étapes", "; ".join(etapes)))
        else:
            donnees.append(("Étapes", "Aucune"))
        
        # Configuration du tableau
        table.setRowCount(len(donnees))
        for i, (propriete, valeur) in enumerate(donnees):
            table.setItem(i, 0, QTableWidgetItem(propriete))
            table.setItem(i, 1, QTableWidgetItem(str(valeur)))
        
        # Rendre le tableau en lecture seule
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Ajuster la largeur des colonnes
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        # Section des suspects avec une case par suspect (cliquable)
        layout.addWidget(QLabel("<b>Suspects :</b>"))
        suspects_layout = QVBoxLayout()
        
        suspects = getattr(c, 'suspects', [])
        if suspects:
            for i, suspect in enumerate(suspects, 1):
                # Créer un bouton cliquable pour chaque suspect
                suspect_btn = QPushButton(f"Suspect {i} : {suspect}")
                suspect_btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px;
                        margin: 2px;
                        border: 1px solid #ccc;
                        background-color: #f9f9f9;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                        border-color: #999;
                    }
                """)
                
                # Connecter le bouton à l'ouverture du dossier suspect
                suspect_btn.clicked.connect(lambda checked, s=suspect: self.ouvrir_dossier_suspect(s, c))
                suspects_layout.addWidget(suspect_btn)
        else:
            suspects_layout.addWidget(QLabel("Aucun suspect identifié"))
        
        layout.addLayout(suspects_layout)
        
        # Section des agents avec bonus réseau
        if hasattr(c, 'pays') and c.pays:
            layout.addWidget(QLabel("<b>Agents avec bonus réseau dans ce pays :</b>"))
            try:
                from gestionnaire_actions import gestionnaire_actions
                agents_bonus = gestionnaire_actions.lister_agents_avec_bonus_reseau(c.pays)
                
                # Filtrer seulement les agents avec bonus > 0
                agents_avec_bonus = [item for item in agents_bonus if item["bonus_info"]["bonus"] > 0]
                
                if agents_avec_bonus:
                    bonus_layout = QVBoxLayout()
                    for item in agents_avec_bonus:
                        agent = item["agent"]
                        bonus_info = item["bonus_info"]
                        nom_complet = f"{agent.nom} {agent.prenom}"
                        
                        # Agent avec bonus (on sait qu'il en a un car on a filtré)
                        bonus_text = f"🎯 {nom_complet} ({agent.bureau}) - +{bonus_info['bonus']}% - {bonus_info['description']}"
                        bonus_label = QLabel(bonus_text)
                        bonus_label.setStyleSheet("color: #2E8B57; font-weight: bold; padding: 5px; background-color: #f0fff0; border: 1px solid #90EE90; border-radius: 4px;")
                        bonus_layout.addWidget(bonus_label)
                    
                    layout.addLayout(bonus_layout)
                else:
                    layout.addWidget(QLabel("Aucun agent avec bonus réseau dans ce pays"))
            except ImportError:
                layout.addWidget(QLabel("Impossible de charger les informations de bonus réseau"))
        else:
            layout.addWidget(QLabel("Pays non spécifié - impossible de vérifier les bonus réseau"))
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        # Toujours afficher le bouton Lancer Action si la crise n'est pas finie
        if c.statut in ["En attente", "En cours"]:
            btn_action = QPushButton("Lancer Action")
            btn_action.clicked.connect(lambda: self._lancer_action_crise(c, dlg))
            btn_layout.addWidget(btn_action)
        
        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(dlg.accept)
        btn_layout.addWidget(btn_fermer)
        
        layout.addLayout(btn_layout)
        
        # Créer le widget d'onglets pour les actions
        tabs = QTabWidget()
        
        # Ajouter un onglet pour les actions
        actions_widget = QWidget()
        actions_layout = QVBoxLayout(actions_widget)
        
        # Titre des actions
        actions_layout.addWidget(QLabel("<b>Actions sur cette crise :</b>"))
        
        # Liste des actions
        actions_list = QListWidget()
        actions_layout.addWidget(actions_list)
        
        # Bouton pour lancer une nouvelle action
        btn_nouvelle_action = QPushButton("Lancer une nouvelle action")
        btn_nouvelle_action.clicked.connect(lambda: self._lancer_nouvelle_action(c, dlg))
        actions_layout.addWidget(btn_nouvelle_action)
        
        # Bouton pour rafraîchir manuellement
        btn_refresh = QPushButton("🔄 Actualiser")
        btn_refresh.clicked.connect(lambda: self._rafraichir_liste_actions(c, actions_list))
        actions_layout.addWidget(btn_refresh)
        
        # Rafraîchir la liste des actions
        self._rafraichir_liste_actions(c, actions_list)
        
        tabs.addTab(actions_widget, "Actions")
        
        # Ajouter les onglets au layout principal
        layout.addWidget(tabs)
        
        # Créer un timer pour rafraîchir automatiquement les actions toutes les 2 secondes
        from PyQt5.QtCore import QTimer
        refresh_timer = QTimer()
        refresh_timer.timeout.connect(lambda: self._rafraichir_liste_actions(c, actions_list))
        refresh_timer.start(2000)  # Rafraîchir toutes les 2 secondes
        
        # Connecter la fermeture de la fenêtre à l'arrêt du timer
        dlg.finished.connect(refresh_timer.stop)
        
        dlg.setLayout(layout)
        dlg.exec_()
        
        # Rafraîchir l'affichage après fermeture
        self.refresh_crises()
        self.refresh_crises_onglet()

    def ouvrir_dossier_suspect(self, nom_suspect, crise):
        """Ouvre le dossier détaillé d'un suspect"""
        # Vérifier d'abord si la crise est toujours active
        if crise.statut in ["Réussite", "Échec", "Clôturée"]:
            QMessageBox.information(self, "Crise terminée", f"Cette crise est terminée ({crise.statut}).\nLes dossiers suspects ont été archivés.")
            return
        
        # Extraire nom et prénom du suspect (format: "Prénom Nom")
        if ' ' in nom_suspect:
            prenom, nom = nom_suspect.split(' ', 1)
        else:
            prenom, nom = nom_suspect, ""
        
        # Rechercher le dossier suspect
        dossier_id = f"{nom}_{prenom}_{crise.nom}"
        dossier = dossiers_suspects.get_dossier_suspect(dossier_id)
        
        if not dossier:
            print(f"DEBUG: Recherche dossier suspect avec ID: {dossier_id}")
            print(f"DEBUG: Suspects dans la crise: {crise.suspects}")
            # Essayer de lister tous les dossiers pour debug
            tous_dossiers = dossiers_suspects.lister_tous_dossiers()
            print(f"DEBUG: Tous les dossiers disponibles: {[d.id for d in tous_dossiers]}")
            QMessageBox.warning(self, "Dossier introuvable", f"Dossier non trouvé pour {nom_suspect}\nID recherché: {dossier_id}\nCrise: {crise.nom} (Statut: {crise.statut})")
            return
        
        # Créer la fenêtre du dossier suspect
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Dossier suspect : {dossier.prenom} {dossier.nom}")
        dlg.setGeometry(400, 500, 800, 600)
        
        layout = QVBoxLayout(dlg)
        
        # Titre
        titre = QLabel(f"<h2>Dossier suspect : {dossier.prenom} {dossier.nom}</h2>")
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)
        
        # Informations de base
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
        
        info_table = QTableWidget()
        info_table.setColumnCount(2)
        info_table.setHorizontalHeaderLabels(["Propriété", "Valeur"])
        
        donnees_base = [
            ("Nom", dossier.nom),
            ("Prénom", dossier.prenom),
            ("Pays", dossier.pays),
            ("Nationalité", dossier.nationalite),
            ("Âge", str(dossier.age)),
            ("Métier", dossier.metier),
            ("Entreprise", dossier.entreprise),
            ("Adresse", dossier.adresse),
            ("Téléphone", dossier.telephone),
            ("Email", dossier.email),
            ("Date création", dossier.date_creation.strftime("%d/%m/%Y %H:%M")),
            ("Dernière mise à jour", dossier.derniere_mise_a_jour.strftime("%d/%m/%Y %H:%M"))
        ]
        
        info_table.setRowCount(len(donnees_base))
        for i, (propriete, valeur) in enumerate(donnees_base):
            info_table.setItem(i, 0, QTableWidgetItem(propriete))
            info_table.setItem(i, 1, QTableWidgetItem(str(valeur)))
        
        info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        info_table.resizeColumnsToContents()
        layout.addWidget(QLabel("<b>Informations de base :</b>"))
        layout.addWidget(info_table)
        
        # Onglets pour les informations détaillées
        from PyQt5.QtWidgets import QTabWidget
        
        tabs = QTabWidget()
        
        # Onglet Notes
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        if dossier.notes:
            for note in dossier.notes:
                note_text = f"[{note['date'].strftime('%d/%m/%Y %H:%M')}] {note['source']} : {note['texte']}"
                note_label = QLabel(note_text)
                note_label.setWordWrap(True)
                note_label.setFrameStyle(QFrame.Box)
                note_label.setStyleSheet("padding: 5px; margin: 2px; border: 1px solid #ddd; background-color: #f5f5f5;")
                notes_layout.addWidget(note_label)
        else:
            notes_layout.addWidget(QLabel("Aucune note"))
        tabs.addTab(notes_widget, "Notes")
        
        # Onglet Informations recueillies
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        if dossier.informations_recueillies:
            for info in dossier.informations_recueillies:
                info_text = f"[{info['date'].strftime('%d/%m/%Y %H:%M')}] {info['type']} - {info['source']} : {info['information']}"
                info_label = QLabel(info_text)
                info_label.setWordWrap(True)
                info_label.setFrameStyle(QFrame.Box)
                info_label.setStyleSheet("padding: 5px; margin: 2px; border: 1px solid #ddd; background-color: #e8f4f8;")
                info_layout.addWidget(info_label)
        else:
            info_layout.addWidget(QLabel("Aucune information recueillie"))
        tabs.addTab(info_widget, "Informations")
        
        # Onglet Surveillances
        surv_widget = QWidget()
        surv_layout = QVBoxLayout(surv_widget)
        if dossier.surveillances:
            for surv in dossier.surveillances:
                surv_text = f"[{surv['date'].strftime('%d/%m/%Y %H:%M')}] Lieu: {surv['lieu']}, Durée: {surv['duree']}, Agent: {surv['agent']}, Résultat: {surv['resultat']}"
                surv_label = QLabel(surv_text)
                surv_label.setWordWrap(True)
                surv_label.setFrameStyle(QFrame.Box)
                surv_label.setStyleSheet("padding: 5px; margin: 2px; border: 1px solid #ddd; background-color: #fff3cd;")
                surv_layout.addWidget(surv_label)
        else:
            surv_layout.addWidget(QLabel("Aucune surveillance effectuée"))
        tabs.addTab(surv_widget, "Surveillances")
        
        # Onglet Interceptions
        int_widget = QWidget()
        int_layout = QVBoxLayout(int_widget)
        if dossier.interceptions:
            for intc in dossier.interceptions:
                int_text = f"[{intc['date'].strftime('%d/%m/%Y %H:%M')}] {intc['type']} - {intc['source']} : {intc['contenu']}"
                int_label = QLabel(int_text)
                int_label.setWordWrap(True)
                int_label.setFrameStyle(QFrame.Box)
                int_label.setStyleSheet("padding: 5px; margin: 2px; border: 1px solid #ddd; background-color: #d1ecf1;")
                surv_layout.addWidget(int_label)
        else:
            int_layout.addWidget(QLabel("Aucune interception"))
        tabs.addTab(int_widget, "Interceptions")
        
        # Onglet Sources humaines
        src_widget = QWidget()
        src_layout = QVBoxLayout(src_widget)
        if dossier.sources_humaines:
            for src in dossier.sources_humaines:
                src_text = f"[{src['date'].strftime('%d/%m/%Y %H:%M')}] {src['nom']} (Fiabilité: {src['fiabilite']}) : {src['information']}"
                src_label = QLabel(src_text)
                src_label.setWordWrap(True)
                src_label.setFrameStyle(QFrame.Box)
                src_label.setStyleSheet("padding: 5px; margin: 2px; border: 1px solid #ddd; background-color: #d4edda;")
                src_layout.addWidget(src_label)
        else:
            src_layout.addWidget(QLabel("Aucune source humaine"))
        tabs.addTab(src_widget, "Sources humaines")
        
        layout.addWidget(tabs)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        # Bouton pour ajouter une note
        btn_note = QPushButton("Ajouter une note")
        btn_note.clicked.connect(lambda: self.ajouter_note_suspect(dossier, dlg))
        btn_layout.addWidget(btn_note)
        
        # Bouton pour ajouter une information
        btn_info = QPushButton("Ajouter information")
        btn_info.clicked.connect(lambda: self.ajouter_information_suspect(dossier, dlg))
        btn_layout.addWidget(btn_info)
        
        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(dlg.accept)
        btn_layout.addWidget(btn_fermer)
        
        layout.addLayout(btn_layout)
        
        dlg.setLayout(layout)
        dlg.exec_()

    def ajouter_note_suspect(self, dossier, dialog):
        """Ajoute une note au dossier suspect"""
        note, ok = QInputDialog.getText(self, "Ajouter une note", "Entrez votre note :")
        if ok and note:
            dossier.ajouter_note(note, "Agent")
            QMessageBox.information(self, "Note ajoutée", "Note ajoutée au dossier suspect")
            dialog.accept()
            # Rouvrir le dossier pour montrer la nouvelle note
            self.ouvrir_dossier_suspect(f"{dossier.prenom} {dossier.nom}", crises.CRISES[0])  # TODO: améliorer

    def ajouter_information_suspect(self, dossier, dialog):
        """Ajoute une information au dossier suspect"""
        info, ok = QInputDialog.getText(self, "Ajouter une information", "Entrez l'information recueillie :")
        if ok and info:
            type_info, ok2 = QInputDialog.getItem(self, "Type d'information", "Choisissez le type :", 
                                                ["Général", "Surveillance", "Interception", "Source humaine"], 0, False)
            if ok2:
                dossier.ajouter_information(info, type_info, "Agent")
                QMessageBox.information(self, "Information ajoutée", "Information ajoutée au dossier suspect")
                dialog.accept()
                # Rouvrir le dossier pour montrer la nouvelle information
                self.ouvrir_dossier_suspect(f"{dossier.prenom} {dossier.nom}", crises.CRISES[0])  # TODO: améliorer

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
            # Couleur selon le statut
            if c.statut == "En cours":
                couleur = "[🟡]"
            elif c.statut == "Réussite":
                couleur = "[🟢]"
            elif c.statut == "Échec":
                couleur = "[🔴]"
            elif c.statut == "En attente":
                couleur = "[⚪]"
            else:
                couleur = "[⚫]"
            
            # Affichage enrichi avec origine, pays et progression
            info_crise = f"{couleur} {c.nom} - {c.origine}"
            if hasattr(c, 'pays') and c.pays:
                info_crise += f" ({c.pays.title()})"
            # Ajouter la progression
            progression = getattr(c, 'progression', 100)
            info_crise += f" - {progression:.1f}%"
            self.liste_crises.addItem(info_crise)
        self.generate_osm_map()
        self.webView.load(QUrl.fromLocalFile(os.path.abspath(self.map_path)))

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
            # Compter seulement les crises actives (non clôturées)
            crises_actives = [c for c in crises.CRISES if c.statut != "Clôturée"]
            
            if len(crises_actives) < 3:  # Permettre jusqu'à 3 crises actives
                # Sélection aléatoire d'un pays et d'une ville
                pays = random.choice(list(missions.VILLES_PAR_PAYS.keys()))
                ville = random.choice(missions.VILLES_PAR_PAYS[pays])
                
                # Création de la crise avec génération automatique des origines et suspects
                c = crises.Crise(
                    lat=ville['lat'], 
                    lon=ville['lon'],
                    pays=pays  # Le pays sera utilisé pour générer les suspects
                )
                c.demarrer(self.current_game_time, random.randint(600, 1440))
                crises.ajouter_crise(c)
                self.refresh_crises()
                self.refresh_crises_onglet()
                print(f"INFO: Nouvelle crise créée : {c.nom} à {ville['ville']} ({pays})")
            
            self.prochaine_crise = self.current_game_time + timedelta(hours=random.randint(24, 72))
            
    def popup_creation_reseau(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Créer un réseau clandestin")
        layout = QFormLayout(dlg)

        agents_libres = [a for a in agents.AGENTS if not getattr(a, 'rattachement', None) and a.est_disponible()]
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

        # Affichage des bonus de langue
        info_langue_label = QLabel("Sélectionnez un agent et un pays pour voir les bonus de langue")
        info_langue_label.setWordWrap(True)
        info_langue_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        layout.addRow("", info_langue_label)

        def update_bonus_langue():
            try:
                agent_idx = agent_combo.currentIndex()
                if agent_idx >= 0 and agent_idx < len(agents_libres):
                    agent = agents_libres[agent_idx]
                    pays = pays_combo.currentText()
                    
                    # Calculer les bonus de langue
                    bonus = reseaux.calculer_bonus_langue_agent(agent, pays)
                    
                    # Construire le texte d'information
                    texte_info = f"<b>Langues de l'agent :</b> {', '.join(agent.langues) if agent.langues else 'Aucune'}<br>"
                    texte_info += f"<b>Langues du pays :</b> {', '.join(bonus['langues_pays'])}<br><br>"
                    
                    if bonus['langues_maitrisees']:
                        texte_info += f"<b>Langues communes :</b> {', '.join(bonus['langues_maitrisees'])}<br>"
                        texte_info += f"<b>Bonus chance de succès :</b> +{bonus['chance_succes']}%<br>"
                        texte_info += f"<b>Réduction de coût :</b> -{bonus['reduction_cout']}%<br>"
                        texte_info += f"<b>Réduction de durée :</b> -{bonus['reduction_duree']}%<br>"
                        texte_info += f"<b>Bonus de qualité :</b> +{bonus['bonus_qualite']}%<br>"
                        
                        info_langue_label.setStyleSheet("QLabel { color: #2E8B57; font-weight: bold; }")
                    else:
                        texte_info += "<b>Aucun bonus linguistique</b><br>"
                        texte_info += "L'agent ne parle aucune langue du pays cible"
                        info_langue_label.setStyleSheet("QLabel { color: #DC143C; font-weight: bold; }")
                    
                    info_langue_label.setText(texte_info)
                else:
                    info_langue_label.setText("Sélectionnez un agent et un pays pour voir les bonus de langue")
                    info_langue_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
            except Exception as e:
                info_langue_label.setText(f"Erreur lors du calcul des bonus : {str(e)}")
                info_langue_label.setStyleSheet("QLabel { color: #DC143C; }")

        # Connecter les changements pour mettre à jour les bonus
        agent_combo.currentTextChanged.connect(update_bonus_langue)
        pays_combo.currentTextChanged.connect(update_bonus_langue)
        
        # Mettre à jour une première fois
        update_bonus_langue()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)

        dlg.setLayout(layout)
        if dlg.exec_():
            agent = agents_libres[agent_combo.currentIndex()]
            pays = pays_combo.currentText()
            ville = ville_combo.currentText()
            
            # Calculer les bonus de langue pour ce réseau
            bonus_langue = reseaux.calculer_bonus_langue_agent(agent, pays)
            
            existants = list(reseaux.RESEAUX.keys()) + [r['id'] for r in CREATIONS_RESEAUX_EN_COURS]
            i = 1
            while True:
                id_reseau = f"Réseau {i:03}"
                if id_reseau not in existants:
                    break
                i += 1
            
            # Durée de base et réduction linguistique
            duree_base = random.randint(10, 60)
            reduction_duree = bonus_langue['reduction_duree']
            duree_finale = max(3, int(duree_base * (1 - reduction_duree / 100)))
            
            date_fin = self.current_game_time + timedelta(days=duree_finale)

            # Chance de succès avec bonus linguistique
            chance_base = 90  # Succès forcé simplifié
            chance_finale = min(100, chance_base + bonus_langue['chance_succes'])

            # Coût de création avec réduction linguistique
            cout_base = 15000  # Coût de base pour créer un réseau
            reduction_cout = bonus_langue['reduction_cout']
            cout_final = int(cout_base * (1 - reduction_cout / 100))

            CREATIONS_RESEAUX_EN_COURS.append({               
                "id": id_reseau,
                "agent": agent,
                "pays": pays,
                "ville": ville,
                "fin": date_fin,
                "chance": chance_finale,
                "cout": cout_final,
                "bonus_langue": bonus_langue
            })
            
            self.refresh_reseaux()
            
            # Message d'information avec les bonus
            message = f"{id_reseau} lancé à {ville} ({pays}) — résultat dans {duree_finale} jours ingame."
            if bonus_langue['langues_maitrisees']:
                message += f"\n\n<b>Bonus linguistiques appliqués :</b>"
                message += f"\n• Chance de succès : {chance_finale}% (+{bonus_langue['chance_succes']}%)"
                message += f"\n• Coût réduit : {cout_final}€ (-{reduction_cout}%)"
                message += f"\n• Durée réduite : {duree_finale} jours (-{reduction_duree}%)"
                message += f"\n• Qualité améliorée : +{bonus_langue['bonus_qualite']}%"
            
            QMessageBox.information(self, "Réseau en création", message)

    def refresh_reseaux(self):
        self.reseauList.clear()
        for k, v in reseaux.RESEAUX.items():
            self.reseauList.addItem(f"{k} ({v['pays']})")
        for r in CREATIONS_RESEAUX_EN_COURS:
            # Afficher les informations détaillées avec bonus linguistiques
            info_reseau = f"{r['id']} à {r['pays']} {r['ville']} — EN COURS DE CRÉATION"
            
            # Ajouter les informations de coût et de bonus si disponibles
            if 'cout' in r:
                info_reseau += f" | Coût: {r['cout']}€"
            
            if 'bonus_langue' in r and r['bonus_langue']['langues_maitrisees']:
                bonus = r['bonus_langue']
                langues_communes = ', '.join(bonus['langues_maitrisees'])
                info_reseau += f" | Langues: {langues_communes} (+{bonus['chance_succes']}% succès)"
            
            self.reseauList.addItem(info_reseau)

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

        # Affichage de la qualité du réseau
        if 'qualite' in r:
            qualite = r['qualite']
            bonus_qualite = r.get('bonus_qualite', 0)
            couleur_qualite = "#2E8B57" if qualite == "Excellente" else "#FF8C00" if qualite == "Bonne" else "#4169E1"
            layout.addWidget(QLabel(f"<b>Qualité :</b> <span style='color: {couleur_qualite};'>{qualite}</span> (+{bonus_qualite}%)"))
        else:
            layout.addWidget(QLabel(f"<b>Qualité :</b> Standard"))

        # Informations sur l'agent de création
        if 'agent_creation' in r:
            agent_creation = r['agent_creation']
            layout.addWidget(QLabel(f"<b>Agent créateur :</b> {agent_creation['nom']} ({agent_creation['bureau']})"))
            layout.addWidget(QLabel(f"<b>Langues de l'agent :</b> {', '.join(agent_creation['langues'])}"))
            
            # Afficher les bonus appliqués
            bonus = agent_creation['bonus_appliques']
            if bonus['langues_maitrisees']:
                layout.addWidget(QLabel(f"<b>Langues communes :</b> {', '.join(bonus['langues_maitrisees'])}"))
                layout.addWidget(QLabel(f"<b>Bonus appliqués :</b> +{bonus['chance_succes']}% succès, -{bonus['reduction_cout']}% coût, -{bonus['reduction_duree']}% durée"))

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
            layout.addWidget(QLabel("Aucun agent affecté"))

        # Sources
        layout.addWidget(QLabel("<b>Sources :</b>"))
        if r["sources"]:
            for s in r["sources"]:
                # Gérer les deux types d'objets : Source et DossierSource
                if hasattr(s, 'prenom') and hasattr(s, 'metier'):
                    # Objet Source
                    layout.addWidget(QLabel(f"- {s.nom} {s.prenom} — {s.metier}"))
                elif hasattr(s, 'infos') and 'metier' in s.infos:
                    # Objet DossierSource
                    metier = s.infos.get('metier', 'N/A')
                    layout.addWidget(QLabel(f"- {s.nom} — {metier}"))
                else:
                    # Fallback
                    layout.addWidget(QLabel(f"- {getattr(s, 'nom', 'Source inconnue')}"))
        else:
            layout.addWidget(QLabel("Aucune source"))

        # Événements du réseau
        if r.get("evenements"):
            layout.addWidget(QLabel("<b>Événements récents :</b>"))
            for evenement in r["evenements"][:5]:  # Afficher les 5 derniers
                layout.addWidget(QLabel(f"• {evenement}"))

        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        # Bouton pour assigner un responsable
        if not resp:
            assigner_btn = QPushButton("Assigner responsable")
            assigner_btn.clicked.connect(lambda: self._assigner_responsable_reseau(nom, dlg))
            buttons_layout.addWidget(assigner_btn)
        
        # Bouton pour ajouter/retirer des agents
        agents_btn = QPushButton("Gérer agents")
        agents_btn.clicked.connect(lambda: self._gerer_agents_reseau(nom, dlg))
        buttons_layout.addWidget(agents_btn)
        
        # Bouton pour rechercher des sources
        sources_btn = QPushButton("Rechercher sources")
        sources_btn.clicked.connect(lambda: self._rechercher_sources_reseau(nom, dlg))
        buttons_layout.addWidget(sources_btn)
        
        layout.addLayout(buttons_layout)

        dlg.setLayout(layout)
        dlg.exec_()

    def _voir_actions_en_cours(self):
        """Affiche toutes les actions en cours sur toutes les crises"""
        actions_dlg = QDialog(self)
        actions_dlg.setWindowTitle("Actions en cours sur toutes les crises")
        actions_dlg.setGeometry(400, 500, 800, 600)
        
        layout = QVBoxLayout(actions_dlg)
        
        # Titre
        layout.addWidget(QLabel("<h2>Actions en cours</h2>"))
        
        # Liste des actions
        actions_list = QListWidget()
        layout.addWidget(actions_list)
        
        # Bouton rafraîchir
        refresh_btn = QPushButton("Rafraîchir")
        refresh_btn.clicked.connect(lambda: self._rafraichir_actions_globales(actions_list))
        layout.addWidget(refresh_btn)
        
        # Bouton fermer
        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(actions_dlg.accept)
        layout.addWidget(btn_fermer)
        
        # Charger les actions
        self._rafraichir_actions_globales(actions_list)
        
        actions_dlg.setLayout(layout)
        actions_dlg.exec_()

    def _rafraichir_actions_globales(self, actions_list):
        """Rafraîchit la liste globale des actions"""
        actions_list.clear()
        
        try:
            # Obtenir toutes les actions en cours
            actions_en_cours = list(gestionnaire_actions.actions_en_cours.values())
            
            if not actions_en_cours:
                actions_list.addItem("Aucune action en cours")
                return
            
            # Grouper par crise
            actions_par_crise = {}
            for action in actions_en_cours:
                if action.crise_id not in actions_par_crise:
                    actions_par_crise[action.crise_id] = []
                actions_par_crise[action.crise_id].append(action)
            
            # Afficher par crise
            for crise_id, actions in actions_par_crise.items():
                actions_list.addItem(f"--- CRISE: {crise_id} ---")
                
                for action in actions:
                    # Calculer le temps restant
                    temps_restant = ""
                    if action.date_fin:
                        temps_restant = f" - Fin dans {int((action.date_fin - datetime.now()).total_seconds() / 60)} min"
                    
                    info_action = f"🟡 {action.type_action.value} - Agent: {action.agent_id}"
                    if action.cible:
                        info_action += f" - Cible: {action.cible}"
                    info_action += f" - {action.progression}%{temps_restant}"
                    
                    item = QListWidgetItem(info_action)
                    item.setData(Qt.UserRole, action)
                    actions_list.addItem(item)
                
                actions_list.addItem("")  # Ligne vide entre crises
            
        except Exception as e:
            actions_list.addItem(f"Erreur lors du chargement des actions: {e}")

    def _rafraichir_liste_actions(self, crise, actions_list):
        """Rafraîchit la liste des actions d'une crise"""
        actions_list.clear()
        
        try:
            actions = gestionnaire_actions.lister_actions_crise(crise.nom)
            
            if not actions:
                actions_list.addItem("Aucune action lancée sur cette crise")
                return
            
            for action in actions:
                # Déterminer la couleur selon le statut
                couleur = ""
                if action.statut.value == "En cours":
                    couleur = "[🟡]"
                elif action.statut.value == "Terminée":
                    couleur = "[🟢]"
                elif action.statut.value == "Échec":
                    couleur = "[🔴]"
                elif action.statut.value == "Annulée":
                    couleur = "[⚫]"
                
                # Afficher les informations de l'action
                info_action = f"{couleur} {action.type_action.value}"
                if action.agent_id:
                    info_action += f" - Agent: {action.agent_id}"
                if action.cible:
                    info_action += f" - Cible: {action.cible}"
                info_action += f" - {action.statut.value}"
                
                if action.statut.value == "En cours":
                    info_action += f" ({action.progression}%)"
                elif action.statut.value in ["Terminée", "Échec"]:
                    info_action += f" - {action.resultat}"
                
                item = QListWidgetItem(info_action)
                item.setData(Qt.UserRole, action)
                actions_list.addItem(item)
                
        except Exception as e:
            actions_list.addItem(f"Erreur lors du chargement des actions: {e}")

    def _lancer_nouvelle_action(self, crise, dialog):
        """Lance une nouvelle action sur une crise"""
        # Créer la fenêtre de sélection d'action
        action_dlg = QDialog(self)
        action_dlg.setWindowTitle(f"Lancer une action sur {crise.nom}")
        action_dlg.setGeometry(400, 500, 600, 400)
        
        layout = QVBoxLayout(action_dlg)
        
        # Sélection du type d'action
        layout.addWidget(QLabel("<b>Sélectionnez le type d'action :</b>"))
        
        from PyQt5.QtWidgets import QComboBox
        type_action_combo = QComboBox()
        for type_action in actions_crises.TypeAction:
            type_action_combo.addItem(type_action.value)
        layout.addWidget(type_action_combo)
        
        # Sélection de l'agent
        layout.addWidget(QLabel("<b>Sélectionnez l'agent :</b>"))
        agent_combo = QComboBox()
        
        # Variable pour stocker les agents filtrés
        agents_filtres = []
        
        def filtrer_agents_competents():
            type_selectionne = type_action_combo.currentText()
            for type_action in actions_crises.TypeAction:
                if type_action.value == type_selectionne:
                    config = actions_crises.ACTIONS_DISPONIBLES[type_action]
                    competences_requises = [p.replace("competence_", "") for p in config["prerequis"] if p.startswith("competence_")]
                    
                    # Filtrer les agents disponibles avec au moins une compétence requise
                    nonlocal agents_filtres
                    agents_filtres = []
                    for a in agents.AGENTS:
                        if not a.est_disponible():
                            continue
                        # Convertir les compétences requises pour la comparaison
                        comp_requises_normalisees = [c.replace("combat", "combat rapproché").replace("securite", "sécurité") for c in competences_requises]
                        # Vérifier si l'agent a au moins une des compétences requises
                        if any(c.lower() in [ac.lower() for ac in a.competences] for c in comp_requises_normalisees):
                            agents_filtres.append(a)
                    
                    agent_combo.clear()
                    for agent in agents_filtres:
                        competences_agent = ", ".join(c for c in agent.competences if c.lower() in [cr.replace("combat", "combat rapproché").replace("securite", "sécurité").lower() for cr in competences_requises])
                        
                        # Vérifier le bonus réseau de l'agent
                        bonus_reseau = ""
                        try:
                            from gestionnaire_actions import gestionnaire_actions
                            bonus_info = gestionnaire_actions.obtenir_bonus_reseau_agent(f"{agent.nom} {agent.prenom}", crise.pays)
                            if bonus_info["bonus"] > 0:
                                type_bonus = "responsable" if bonus_info["type"] == "responsable" else "membre"
                                bonus_reseau = f" | 🎯 Réseau: +{bonus_info['bonus']}% ({type_bonus})"
                        except:
                            pass
                        
                        agent_combo.addItem(f"{agent.nom} {agent.prenom} ({agent.bureau}) - {competences_agent}{bonus_reseau}")
                    break
        
        type_action_combo.currentTextChanged.connect(filtrer_agents_competents)
        filtrer_agents_competents()  # Appliquer le filtre initial
        layout.addWidget(agent_combo)
        
        # Sélection de la cible (suspect)
        layout.addWidget(QLabel("<b>Sélectionnez la cible (optionnel) :</b>"))
        cible_combo = QComboBox()
        cible_combo.addItem("Aucune cible spécifique")
        if hasattr(crise, 'suspects') and crise.suspects:
            for suspect in crise.suspects:
                cible_combo.addItem(suspect)
        layout.addWidget(cible_combo)
        
        # Informations sur l'action sélectionnée
        info_label = QLabel("Sélectionnez un type d'action pour voir les détails")
        info_label.setWordWrap(True)
        info_label.setFrameStyle(QFrame.Box)
        info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(info_label)
        
        def update_info():
            type_selectionne = type_action_combo.currentText()
            for type_action in actions_crises.TypeAction:
                if type_action.value == type_selectionne:
                    config = actions_crises.ACTIONS_DISPONIBLES[type_action]
                    info = f"<b>{type_action.value}</b><br>"
                    info += f"Coût: {config['cout']}€<br>"
                    info += f"Durée: {config['duree_minutes']} minutes<br>"
                    info += f"Description: {config['description']}<br>"
                    
                    # Afficher les prérequis de manière plus claire
                    prerequis = []
                    for p in config['prerequis']:
                        if p == "agent_disponible":
                            prerequis.append("Agent disponible")
                        elif p.startswith("competence_"):
                            comp = p.replace("competence_", "").capitalize()
                            prerequis.append(f"Compétence : {comp}")
                        elif p.startswith("equipement_"):
                            equip = p.replace("equipement_", "").capitalize()
                            prerequis.append(f"Équipement : {equip}")
                        else:
                            prerequis.append(p.capitalize())
                    
                    info += f"<br><b>Prérequis :</b><br>• " + "<br>• ".join(prerequis)
                    info += f"<br><br><b>Risques :</b><br>• " + "<br>• ".join(config['risques'])
                    info += f"<br><br><b>Récompenses :</b><br>• " + "<br>• ".join(config['recompenses'])
                    info_label.setText(info)
                    break
        
        type_action_combo.currentTextChanged.connect(update_info)
        update_info()  # Afficher les infos du premier type
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_lancer = QPushButton("Lancer l'action")
        btn_annuler = QPushButton("Annuler")
        btn_layout.addWidget(btn_lancer)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)
        
        def lancer_action():
            # Récupérer les sélections
            type_action_str = type_action_combo.currentText()
            agent_idx = agent_combo.currentIndex()
            cible_idx = cible_combo.currentIndex()
            
            if agent_idx < 0 or agent_idx >= len(agents_filtres):
                QMessageBox.warning(action_dlg, "Erreur", "Veuillez sélectionner un agent")
                return
            
            # Trouver le type d'action
            type_action = None
            for ta in actions_crises.TypeAction:
                if ta.value == type_action_str:
                    type_action = ta
                    break
            
            if not type_action:
                QMessageBox.warning(action_dlg, "Erreur", "Type d'action invalide")
                return
            
            # Récupérer l'agent et la cible
            agent = agents_filtres[agent_idx]
            cible = None
            if cible_idx > 0 and cible_idx <= len(crise.suspects):
                cible = crise.suspects[cible_idx - 1]
            
            # Lancer l'action avec le temps de jeu actuel
            success, message = gestionnaire_actions.lancer_action(
                type_action, crise.nom, f"{agent.nom} {agent.prenom}", cible, None, self.current_game_time
            )
            
            if success:
                QMessageBox.information(action_dlg, "Succès", message)
                action_dlg.accept()
                # NE PAS fermer la fenêtre principale - juste rafraîchir la liste des actions
                # Rafraîchir l'affichage des actions
                self.refresh_crises()
                self.refresh_crises_onglet()
            else:
                QMessageBox.warning(action_dlg, "Erreur", message)
        
        btn_lancer.clicked.connect(lancer_action)
        btn_annuler.clicked.connect(action_dlg.reject)
        
        action_dlg.setLayout(layout)
        action_dlg.exec_()

    # ------------------ ONGLET CHEAT ------------------
    def _tab_cheat(self):
        """Onglet pour les fonctions de test et de cheat"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Titre
        titre = QLabel("<h2>🔧 Menu Cheat - Tests et Développement</h2>")
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)
        
        # Section Argent
        argent_frame = QFrame()
        argent_frame.setFrameStyle(QFrame.Box)
        argent_layout = QVBoxLayout(argent_frame)
        argent_layout.addWidget(QLabel("<b>💰 Gestion de l'Argent</b>"))
        
        # Affichage du solde actuel
        self.solde_actuel_label = QLabel()
        argent_layout.addWidget(self.solde_actuel_label)
        
        # Boutons pour modifier l'argent
        argent_btn_layout = QHBoxLayout()
        
        btn_ajouter_argent = QPushButton("+ 10,000€")
        btn_ajouter_argent.clicked.connect(lambda: self.modifier_argent(10000))
        argent_btn_layout.addWidget(btn_ajouter_argent)
        
        btn_ajouter_gros_argent = QPushButton("+ 100,000€")
        btn_ajouter_gros_argent.clicked.connect(lambda: self.modifier_argent(100000))
        argent_btn_layout.addWidget(btn_ajouter_gros_argent)
        
        btn_retirer_argent = QPushButton("- 10,000€")
        btn_retirer_argent.clicked.connect(lambda: self.modifier_argent(-10000))
        argent_btn_layout.addWidget(btn_retirer_argent)
        
        argent_layout.addLayout(argent_btn_layout)
        
        # Saisie manuelle
        argent_input_layout = QHBoxLayout()
        argent_input_layout.addWidget(QLabel("Montant personnalisé:"))
        self.argent_input = QInputDialog()
        self.argent_input.setInputMode(QInputDialog.IntInput)
        self.argent_input.setIntRange(-1000000, 1000000)
        self.argent_input.setIntValue(0)
        
        btn_argent_perso = QPushButton("Appliquer")
        btn_argent_perso.clicked.connect(self.modifier_argent_personnalise)
        argent_input_layout.addWidget(btn_argent_perso)
        
        argent_layout.addLayout(argent_input_layout)
        layout.addWidget(argent_frame)
        
        # Section Réputation
        reputation_frame = QFrame()
        reputation_frame.setFrameStyle(QFrame.Box)
        reputation_layout = QVBoxLayout(reputation_frame)
        reputation_layout.addWidget(QLabel("<b>⭐ Gestion de la Réputation</b>"))
        
        # Affichage de la réputation actuelle
        self.reputation_actuelle_label = QLabel()
        reputation_layout.addWidget(self.reputation_actuelle_label)
        
        # Boutons pour modifier la réputation
        reputation_btn_layout = QHBoxLayout()
        
        btn_ajouter_reputation = QPushButton("+ 10 points")
        btn_ajouter_reputation.clicked.connect(lambda: self.modifier_reputation(10))
        reputation_btn_layout.addWidget(btn_ajouter_reputation)
        
        btn_ajouter_grosse_reputation = QPushButton("+ 25 points")
        btn_ajouter_grosse_reputation.clicked.connect(lambda: self.modifier_reputation(25))
        reputation_btn_layout.addWidget(btn_ajouter_grosse_reputation)
        
        btn_retirer_reputation = QPushButton("- 10 points")
        btn_retirer_reputation.clicked.connect(lambda: self.modifier_reputation(-10))
        reputation_btn_layout.addWidget(btn_retirer_reputation)
        
        reputation_layout.addLayout(reputation_btn_layout)
        
        # Saisie manuelle de la réputation
        reputation_input_layout = QHBoxLayout()
        reputation_input_layout.addWidget(QLabel("Réputation personnalisée:"))
        self.reputation_input = QInputDialog()
        self.reputation_input.setInputMode(QInputDialog.IntInput)
        self.reputation_input.setIntRange(0, 100)
        self.reputation_input.setIntValue(50)
        
        btn_reputation_perso = QPushButton("Appliquer")
        btn_reputation_perso.clicked.connect(self.modifier_reputation_personnalisee)
        reputation_input_layout.addWidget(btn_reputation_perso)
        
        reputation_layout.addLayout(reputation_input_layout)
        layout.addWidget(reputation_frame)
        
        # Section Actions rapides
        actions_frame = QFrame()
        actions_frame.setFrameStyle(QFrame.Box)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.addWidget(QLabel("<b>⚡ Actions Rapides</b>"))
        
        actions_btn_layout = QHBoxLayout()
        
        btn_reset_complet = QPushButton("Reset Complet")
        btn_reset_complet.clicked.connect(self.reset_complet)
        actions_btn_layout.addWidget(btn_reset_complet)
        
        btn_max_reputation = QPushButton("Max Réputation")
        btn_max_reputation.clicked.connect(lambda: self.modifier_reputation(100))
        actions_btn_layout.addWidget(btn_max_reputation)
        
        btn_max_argent = QPushButton("Max Argent")
        btn_max_argent.clicked.connect(lambda: self.modifier_argent(1000000))
        actions_btn_layout.addWidget(btn_max_argent)
        
        actions_layout.addLayout(actions_btn_layout)
        layout.addWidget(actions_frame)
        
        # Bouton rafraîchir
        btn_rafraichir = QPushButton("🔄 Rafraîchir l'affichage")
        btn_rafraichir.clicked.connect(self.rafraichir_cheat)
        layout.addWidget(btn_rafraichir)
        
        # Mise à jour initiale
        self.rafraichir_cheat()
        
        widget.setLayout(layout)
        return widget
    
    def modifier_argent(self, montant):
        """Modifie l'argent du service"""
        try:
            if montant > 0:
                budget.crediter(montant, f"Cheat: ajout de {montant}€")
            else:
                budget.debiter(abs(montant), f"Cheat: retrait de {abs(montant)}€")
            self.rafraichir_cheat()
            self.update_status_labels()
            QMessageBox.information(self, "Succès", f"Argent modifié de {montant:+d}€")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la modification: {e}")
    
    def modifier_argent_personnalise(self):
        """Modifie l'argent avec un montant personnalisé"""
        montant, ok = QInputDialog.getInt(self, "Modifier l'argent", 
                                         "Entrez le montant à ajouter/retirer:", 0, -1000000, 1000000)
        if ok:
            self.modifier_argent(montant)
    
    def modifier_reputation(self, points):
        """Modifie la réputation du service"""
        try:
            nouvelle_reputation = budget.ajouter_reputation_service(points)
            self.rafraichir_cheat()
            self.update_status_labels()
            QMessageBox.information(self, "Succès", f"Réputation modifiée de {points:+d} points\nNouvelle réputation: {nouvelle_reputation}/100")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la modification: {e}")
    
    def modifier_reputation_personnalisee(self):
        """Modifie la réputation avec une valeur personnalisée"""
        reputation, ok = QInputDialog.getInt(self, "Modifier la réputation", 
                                            "Entrez la nouvelle réputation:", 50, 0, 100)
        if ok:
            try:
                nouvelle_reputation = budget.modifier_reputation_service(reputation)
                self.rafraichir_cheat()
                self.update_status_labels()
                QMessageBox.information(self, "Succès", f"Réputation définie à {nouvelle_reputation}/100")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la modification: {e}")
    
    def reset_complet(self):
        """Reset complet de l'argent et de la réputation"""
        try:
            # Reset de l'argent
            solde_actuel = budget.solde()
            if solde_actuel != 200000:
                if solde_actuel > 200000:
                    budget.debiter(solde_actuel - 200000, "Cheat: reset argent")
                else:
                    budget.crediter(200000 - solde_actuel, "Cheat: reset argent")
            
            # Reset de la réputation
            budget.modifier_reputation_service(50)
            
            self.rafraichir_cheat()
            self.update_status_labels()
            QMessageBox.information(self, "Reset Complet", "Argent et réputation remis aux valeurs par défaut")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du reset: {e}")
    
    def rafraichir_cheat(self):
        """Rafraîchit l'affichage de l'onglet cheat"""
        try:
            # Mettre à jour l'affichage de l'argent
            solde_actuel = budget.solde()
            solde_fmt = "{:,}".format(solde_actuel).replace(",", " ")
            self.solde_actuel_label.setText(f"Solde actuel: {solde_fmt} €")
            
            # Mettre à jour l'affichage de la réputation
            reputation_actuelle = budget.get_reputation_service()
            self.reputation_actuelle_label.setText(f"Réputation actuelle: {reputation_actuelle}/100")
        except Exception as e:
            print(f"Erreur lors du rafraîchissement de l'onglet cheat: {e}")

    def _assigner_responsable_reseau(self, nom_reseau, parent_dialog):
        """Fonction pour assigner un responsable au réseau"""
        popup = QDialog(parent_dialog)
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
            reseaux.definir_responsable(nom_reseau, ag)
            reseaux.ajouter_evenement(nom_reseau, f"Responsable assigné : {ag.nom} {ag.prenom}")
            popup.accept()
            parent_dialog.accept()
            self.refresh_reseaux()
        
        bvalider.clicked.connect(confirmer)
        popup.setLayout(vbox)
        popup.exec_()

    def _gerer_agents_reseau(self, nom_reseau, parent_dialog):
        """Fonction pour gérer les agents du réseau"""
        popup = QDialog(parent_dialog)
        popup.setWindowTitle("Gérer les agents")
        vbox = QVBoxLayout(popup)
        
        # Boutons pour ajouter/retirer des agents
        btn_ajouter = QPushButton("Ajouter un agent")
        btn_retirer = QPushButton("Retirer un agent")
        vbox.addWidget(btn_ajouter)
        vbox.addWidget(btn_retirer)
        
        def ajouter_agent():
            popup_ajout = QDialog(popup)
            popup_ajout.setWindowTitle("Ajouter un agent")
            vbox_ajout = QVBoxLayout(popup_ajout)
            combo = QComboBox()
            reseau = reseaux.RESEAUX[nom_reseau]
            disponibles = [a for a in agents.AGENTS if a not in reseau["agents"] and a != reseau.get("responsable")]
            for a in disponibles:
                code = f" (Code: {a.nom_code})" if a.nom_code else ""
                combo.addItem(f"{a.nom} {a.prenom}{code} — {a.bureau}")
            if not disponibles:
                QMessageBox.information(popup_ajout, "Aucun agent", "Aucun agent disponible.")
                return
            vbox_ajout.addWidget(QLabel("Sélectionnez un agent à ajouter :"))
            vbox_ajout.addWidget(combo)
            btn_valider = QPushButton("Ajouter")
            vbox_ajout.addWidget(btn_valider)
            
            def valider_ajout():
                ag = disponibles[combo.currentIndex()]
                reseaux.rattacher_agent_reseau(nom_reseau, ag)
                reseaux.ajouter_evenement(nom_reseau, f"Agent ajouté : {ag.nom} {ag.prenom}")
                popup_ajout.accept()
                popup.accept()
                parent_dialog.accept()
                self.refresh_reseaux()
            
            btn_valider.clicked.connect(valider_ajout)
            popup_ajout.setLayout(vbox_ajout)
            popup_ajout.exec_()
        
        def retirer_agent():
            popup_retrait = QDialog(popup)
            popup_retrait.setWindowTitle("Retirer un agent")
            vbox_retrait = QVBoxLayout(popup_retrait)
            combo = QComboBox()
            reseau = reseaux.RESEAUX[nom_reseau]
            affectes = [a for a in reseau["agents"] if a != reseau.get("responsable")]
            for a in affectes:
                code = f" (Code: {a.nom_code})" if a.nom_code else ""
                combo.addItem(f"{a.nom} {a.prenom}{code} — {a.bureau}")
            if not affectes:
                QMessageBox.information(popup_retrait, "Aucun agent", "Aucun agent à retirer.")
                return
            vbox_retrait.addWidget(QLabel("Sélectionnez un agent à retirer :"))
            vbox_retrait.addWidget(combo)
            btn_valider = QPushButton("Retirer")
            vbox_retrait.addWidget(btn_valider)
            
            def valider_retrait():
                ag = affectes[combo.currentIndex()]
                reseau["agents"].remove(ag)
                reseaux.ajouter_evenement(nom_reseau, f"Agent retiré : {ag.nom} {ag.prenom}")
                popup_retrait.accept()
                popup.accept()
                parent_dialog.accept()
                self.refresh_reseaux()
            
            btn_valider.clicked.connect(valider_retrait)
            popup_retrait.setLayout(vbox_retrait)
            popup_retrait.exec_()
        
        btn_ajouter.clicked.connect(ajouter_agent)
        btn_retirer.clicked.connect(retirer_agent)
        
        popup.setLayout(vbox)
        popup.exec_()

    def _rechercher_sources_reseau(self, nom_reseau, parent_dialog):
        """Fonction pour rechercher des sources via le réseau"""
        popup = QDialog(parent_dialog)
        popup.setWindowTitle("Recherche de source")
        vbox = QVBoxLayout(popup)
        
        reseau = reseaux.RESEAUX[nom_reseau]
        agents_assignes = reseau["agents"]
        if not agents_assignes:
            QMessageBox.warning(popup, "Aucun agent", "Aucun agent n'est affecté à ce réseau.")
            return
        
        # Afficher la qualité du réseau et son impact sur la recherche de sources
        qualite_reseau = reseau.get("qualite", "Standard")
        bonus_qualite = reseau.get("bonus_qualite", 0)
        
        info_qualite = QLabel(f"<b>Qualité du réseau :</b> {qualite_reseau}")
        if bonus_qualite > 0:
            info_qualite.setStyleSheet("QLabel { color: #2E8B57; font-weight: bold; }")
        elif bonus_qualite < 0:
            info_qualite.setStyleSheet("QLabel { color: #DC143C; font-weight: bold; }")
        vbox.addWidget(info_qualite)
        
        # Impact de la qualité sur la recherche de sources
        impact_qualite = 0
        if qualite_reseau == "Excellente":
            impact_qualite = 25
        elif qualite_reseau == "Bonne":
            impact_qualite = 15
        elif qualite_reseau == "Améliorée":
            impact_qualite = 10
        elif qualite_reseau == "Faible":
            impact_qualite = -10
        
        if impact_qualite != 0:
            impact_label = QLabel(f"<b>Impact sur la recherche de sources :</b> {impact_qualite:+d}% de chance de succès")
            if impact_qualite > 0:
                impact_label.setStyleSheet("QLabel { color: #2E8B57; }")
            else:
                impact_label.setStyleSheet("QLabel { color: #DC143C; }")
            vbox.addWidget(impact_label)
        
        vbox.addWidget(QLabel(""))  # Ligne vide
        
        combo_agents = QComboBox()
        for a in agents_assignes:
            combo_agents.addItem(f"{a.nom} {a.prenom} ({a.bureau})")
        vbox.addWidget(QLabel("Sélectionnez l'agent qui lance la recherche :"))
        vbox.addWidget(combo_agents)
        
        try:
            from metiers import METIERS
            secteurs = sorted(set([v["secteur"] for v in METIERS.values()]))
            combo_secteurs = QComboBox()
            combo_secteurs.addItems(secteurs)
            vbox.addWidget(QLabel("Choisissez un secteur d'activité :"))
            vbox.addWidget(combo_secteurs)
            
            valider = QPushButton("Lancer la recherche")
            vbox.addWidget(valider)
            
            def valider_recherche():
                agent = agents_assignes[combo_agents.currentIndex()]
                secteur = combo_secteurs.currentText()
                
                # Calculer la durée et la chance de succès selon la qualité du réseau
                duree_base = random.randint(3, 10)
                duree_finale = max(1, int(duree_base * (1 - abs(impact_qualite) / 100)))
                
                # Chance de succès de base + bonus de qualité du réseau
                chance_base = 70  # 70% de base
                chance_finale = min(95, max(5, chance_base + impact_qualite))
                
                date_debut = self.current_game_time
                date_fin = date_debut + timedelta(days=duree_finale)
                
                # Ajouter à la liste des recrutements en cours
                RECRUTEMENTS_EN_COURS.append(RecrutementEnCours(
                    "source", {"agent": agent, "secteur": secteur, "reseau": nom_reseau}, date_debut, date_fin
                ))
                
                reseaux.ajouter_evenement(nom_reseau, f"Recherche de source lancée par {agent.nom} {agent.prenom} dans le secteur {secteur}")
                popup.accept()
                
                # Message de confirmation avec les bonus
                message = f"Recherche de source lancée !<br><br>"
                message += f"<b>Agent :</b> {agent.nom} {agent.prenom}<br>"
                message += f"<b>Secteur :</b> {secteur}<br>"
                message += f"<b>Durée estimée :</b> {duree_finale} jours<br>"
                message += f"<b>Chance de succès :</b> {chance_finale}%"
                
                if impact_qualite > 0:
                    message += f" (+{impact_qualite}% grâce à la qualité du réseau)"
                elif impact_qualite < 0:
                    message += f" ({impact_qualite}% à cause de la qualité du réseau)"
                
                QMessageBox.information(self, "Recherche lancée", message)
            
            valider.clicked.connect(valider_recherche)
            
        except ImportError:
            vbox.addWidget(QLabel("Module métiers non disponible"))
        
        popup.setLayout(vbox)
        popup.exec_()


def run_gui():
    app = QApplication(sys.argv)
    win = DGSESimGUI()
    win.show()
    sys.exit(app.exec_())




