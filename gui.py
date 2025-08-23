import sys
import os
import random
import folium
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QTabWidget, QHBoxLayout, QListWidget, QMessageBox, QInputDialog, QComboBox,
    QDialog, QRadioButton, QButtonGroup, QCheckBox, QListWidgetItem, QFrame, QDialogButtonBox, QFormLayout, QProgressBar
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
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Formations en cours :"))
        self.formations_list = QListWidget()
        layout.addWidget(self.formations_list)

        # Actions
        btn_row = QHBoxLayout()
        btn_planifier = QPushButton("Planifier une formation")
        btn_annuler = QPushButton("Annuler la formation sélectionnée")
        btn_refresh = QPushButton("Rafraîchir")
        btn_row.addWidget(btn_planifier)
        btn_row.addWidget(btn_annuler)
        btn_row.addWidget(btn_refresh)
        layout.addLayout(btn_row)

        def open_planification():
            dlg = QDialog(self)
            dlg.setWindowTitle("Planifier une formation")
            v = QVBoxLayout(dlg)
            # Choix agent
            v.addWidget(QLabel("Sélectionnez l'agent :"))
            agent_combo = QComboBox()
            agents_dispos = [a for a in agents.AGENTS if getattr(a, 'est_disponible', lambda: True)()]
            for a in agents_dispos:
                agent_combo.addItem(f"{a.nom} {a.prenom} ({a.bureau})")
            v.addWidget(agent_combo)
            # Choix formation (filtrée: uniquement compétences universelles/prérequis et NON possédées)
            v.addWidget(QLabel("Sélectionnez la formation :"))
            formation_combo = QComboBox()
            catalogue = formations.lister_formations_catalogue()
            noms_form = []
            if agents_dispos:
                ag0 = agents_dispos[0]
                owned_lower = {c.lower() for c in getattr(ag0, 'competences', [])}
                for nom, cfg in catalogue.items():
                    comp = cfg.get('competences', [])
                    if not comp:
                        continue
                    # Une seule compétence par formation
                    skill = comp[0]
                    if skill.lower() not in owned_lower:
                        noms_form.append(nom)
            for nom in noms_form:
                cfg = catalogue[nom]
                formation_combo.addItem(f"{nom} — {cfg['cout']}€ — {cfg['duree_jours']} j")
            v.addWidget(formation_combo)
            # Valider
            btn_ok = QPushButton("Lancer")
            v.addWidget(btn_ok)

            def do_launch():
                if not agents_dispos:
                    QMessageBox.warning(dlg, "Aucun agent", "Aucun agent disponible.")
                    return
                ag = agents_dispos[agent_combo.currentIndex()]
                # Filtrer en fonction de l'agent réellement choisi (pour éviter d'offrir une compétence déjà acquise)
                owned_lower = {c.lower() for c in getattr(ag, 'competences', [])}
                valid_names = [n for n in catalogue.keys() if catalogue[n]['competences'] and catalogue[n]['competences'][0].lower() not in owned_lower]
                if not valid_names:
                    QMessageBox.information(dlg, "Aucune formation", "Cet agent possède déjà toutes les compétences proposées.")
                    return
                # Reconstruction de noms_form pour l'agent sélectionné
                noms_form_agent = [n for n in noms_form if n in valid_names]
                if not noms_form_agent:
                    # Si l'UI n'est plus synchronisée, retomber sur valid_names
                    noms_form_agent = valid_names
                idx_form = max(0, min(formation_combo.currentIndex(), len(noms_form_agent)-1))
                nom = noms_form_agent[idx_form]
                ok, msg = formations.planifier_formation(ag, nom, self.current_game_time)
                if ok:
                    QMessageBox.information(dlg, "Formation", msg)
                    dlg.accept()
                    self.refresh_formations_tab()
                    # Mettre à jour budget
                    if hasattr(self, 'refresh_budget_tab'):
                        self.refresh_budget_tab()
                    # Rafraîchir agents
                    if hasattr(self, 'agentList'):
                        self.refresh_agents()
                else:
                    QMessageBox.warning(dlg, "Erreur", msg)

            btn_ok.clicked.connect(do_launch)
            dlg.setLayout(v)
            dlg.exec_()

        def do_cancel():
            idx = self.formations_list.currentRow()
            if idx < 0:
                return
            ok, msg = formations.annuler_formation(idx)
            if ok:
                QMessageBox.information(self, "Formation", msg)
                self.refresh_formations_tab()
                if hasattr(self, 'refresh_budget_tab'):
                    self.refresh_budget_tab()
                if hasattr(self, 'agentList'):
                    self.refresh_agents()
            else:
                QMessageBox.warning(self, "Erreur", msg)

        def do_refresh():
            self.refresh_formations_tab()

        btn_planifier.clicked.connect(open_planification)
        btn_annuler.clicked.connect(do_cancel)
        btn_refresh.clicked.connect(do_refresh)

        # Premier chargement
        self.refresh_formations_tab()
        widget.setLayout(layout)
        return widget

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
        # Mettre à jour dynamiquement les compétences avant affichage
        try:
            fiches.ajouter_info_fiche(fiche_id, "Compétences", ", ".join(agent.competences))
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
        dlg = QDialog(self)
        dlg.setWindowTitle("Recrutement d'agent - Sélectionnez le mode")
        layout = QVBoxLayout(dlg)
        radio_alea = QRadioButton("Recrutement aléatoire (rapide, peu exigeant) — 2000 €")
        radio_cible = QRadioButton("Recrutement ciblé — 5000 €")
        radio_alea.setChecked(True)
        group = QButtonGroup(dlg)
        group.addButton(radio_alea)
        group.addButton(radio_cible)
        layout.addWidget(radio_alea)
        layout.addWidget(radio_cible)
        layout.addWidget(QLabel(" "))
        
        # Critères de ciblage
        criteres_frame = QWidget()
        criteres_layout = QVBoxLayout(criteres_frame)
        
        # Options de ciblage
        criteres_layout.addWidget(QLabel("<b>Type de ciblage :</b>"))
        radio_bureau = QRadioButton("Par bureau uniquement")
        radio_competences = QRadioButton("Par compétences uniquement")
        radio_mixte = QRadioButton("Par bureau ET compétences")
        radio_bureau.setChecked(True)
        
        group_ciblage = QButtonGroup(criteres_frame)
        group_ciblage.addButton(radio_bureau)
        group_ciblage.addButton(radio_competences)
        group_ciblage.addButton(radio_mixte)
        
        criteres_layout.addWidget(radio_bureau)
        criteres_layout.addWidget(radio_competences)
        criteres_layout.addWidget(radio_mixte)
        criteres_layout.addWidget(QLabel(" "))
        
        # Sélection du bureau
        bureau_frame = QWidget()
        bureau_layout = QVBoxLayout(bureau_frame)
        bureau_layout.addWidget(QLabel("<b>Bureau souhaité :</b>"))
        bureau_combo = QComboBox()
        bureau_combo.addItems([b['code'] for b in bureaux.BUREAUX])
        bureau_layout.addWidget(bureau_combo)
        criteres_layout.addWidget(bureau_frame)
        
        # Sélection des compétences
        comp_frame = QWidget()
        comp_layout = QVBoxLayout(comp_frame)
        comp_layout.addWidget(QLabel("<b>Compétences souhaitées :</b>"))
        comp_boxes = []
        for c in ["Infiltration", "Surveillance", "Hacking", "Langues étrangères", 
                 "Négociation", "Combat rapproché", "Crypto", "Conduite", "Déguisement",
                 "Analyse", "Technique", "Sécurité", "Gestion", "Recherche"]:
            box = QCheckBox(c)
            comp_boxes.append(box)
            comp_layout.addWidget(box)
        criteres_layout.addWidget(comp_frame)
        
        layout.addWidget(criteres_frame)
        
        # Activer/désactiver les sections selon le type de recrutement
        def update_sections():
            is_cible = radio_cible.isChecked()
            criteres_frame.setEnabled(is_cible)
            
            # Activer/désactiver selon le type de ciblage
            if is_cible:
                bureau_frame.setEnabled(radio_bureau.isChecked() or radio_mixte.isChecked())
                comp_frame.setEnabled(radio_competences.isChecked() or radio_mixte.isChecked())
            else:
                bureau_frame.setEnabled(False)
                comp_frame.setEnabled(False)
        
        radio_cible.toggled.connect(update_sections)
        radio_bureau.toggled.connect(update_sections)
        radio_competences.toggled.connect(update_sections)
        radio_mixte.toggled.connect(update_sections)
        update_sections()
        go_btn = QPushButton("Lancer recrutement")
        layout.addWidget(go_btn)
        result_lbl = QLabel("")
        layout.addWidget(result_lbl)
        def lancer_recrutement():
            result_lbl.setText("Recrutement en cours... (délai ingame)")
            
            if radio_alea.isChecked():
                type_recrutement = "classique"
                duree_jours = 2
                ciblage = None
            else:
                type_recrutement = "cible"
                duree_jours = 5
                ciblage = {}
                
                # Vérifier le type de ciblage
                if radio_bureau.isChecked():
                    # Ciblage par bureau uniquement
                    if bureau_combo.currentText():
                        ciblage["bureau"] = bureau_combo.currentText()
                    else:
                        QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bureau.")
                        return
                
                elif radio_competences.isChecked():
                    # Ciblage par compétences uniquement
                    comp_select = [box.text() for box in comp_boxes if box.isChecked()]
                    if comp_select:
                        ciblage["competences"] = comp_select
                    else:
                        QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une compétence.")
                        return
                
                elif radio_mixte.isChecked():
                    # Ciblage mixte (bureau + compétences)
                    if not bureau_combo.currentText():
                        QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bureau.")
                        return
                    comp_select = [box.text() for box in comp_boxes if box.isChecked()]
                    if not comp_select:
                        QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une compétence.")
                        return
                    ciblage["bureau"] = bureau_combo.currentText()
                    ciblage["competences"] = comp_select
            
            dlg.accept()
            date_debut = self.current_game_time
            date_fin = date_debut + timedelta(days=duree_jours)
            # Débiter le coût au lancement selon le système actif
            try:
                cout = budget.cout_recrutement_mode(type_recrutement)
                if not budget.debiter(cout, f"Recrutement {type_recrutement} lancé"):
                    QMessageBox.warning(self, "Budget insuffisant", f"Solde insuffisant pour payer {cout} €")
                    return
            except Exception as e:
                print(f"Erreur débit recrutement: {e}")
            # Rafraîchir affichages budget
            self.update_status_labels()
            if hasattr(self, 'refresh_budget_tab'):
                self.refresh_budget_tab()
            RECRUTEMENTS_EN_COURS.append(RecrutementEnCours(type_recrutement, ciblage, date_debut, date_fin))
            
            # Message de confirmation avec détails du ciblage
            message = f"Recrutement {type_recrutement} en cours\n"
            if ciblage:
                if "bureau" in ciblage:
                    message += f"Bureau ciblé : {ciblage['bureau']}\n"
                if "competences" in ciblage:
                    message += f"Compétences ciblées : {', '.join(ciblage['competences'])}\n"
            message += f"\nDisponible le {date_fin.strftime('%d/%m/%Y à %H:%M')}\n"
            message += "Vous pouvez continuer à jouer ou lancer d'autres actions."
            QMessageBox.information(self, "Recrutement lancé", message)
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
        layout.addWidget(QLabel("Affectation proposée (modifiez à vos risques) :"))
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
            type_recrutement = 'cible' if ciblage else 'classique'
            agent, risque = recrutement.valider_recrutement(profil, bureau_choisi, legende_nom_choisi=None, forcer=forcer, type_recrutement=type_recrutement)
            if agent:
                self.refresh_agents()
                QMessageBox.information(self, "Recrutement", f"Agent {agent.nom} {agent.prenom} recruté ({agent.bureau})\n{'Risque accru\u00a0!' if risque else ''}")
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
            vbox.addWidget(QLabel("Choisissez un secteur d'activité :"))
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


def run_gui():
    app = QApplication(sys.argv)
    win = DGSESimGUI()
    win.show()
    sys.exit(app.exec_())




