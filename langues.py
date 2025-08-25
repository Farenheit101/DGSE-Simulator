# langues.py

# Source unique de vérité pour toutes les langues du système
# Cette liste est utilisée par : formations, recrutement, réseaux, sources
LANGUES_PAR_PAYS = {
    "france": ["français", "anglais", "allemand", "espagnol", "arabe"],
    "allemagne": ["allemand", "anglais", "turc", "français"],
    "italie": ["italien", "anglais", "français"],
    "espagne": ["espagnol", "catalan", "anglais", "français", "galicien", "basque"],
    "portugal": ["portugais", "anglais", "espagnol"],
    "royaume-uni": ["anglais", "français", "gallois", "écossais"],
    "irlande": ["anglais", "irlandais"],
    "pays-bas": ["néerlandais", "anglais"],
    "belgique": ["français", "néerlandais", "allemand"],
    "suisse": ["allemand", "français", "italien", "romanche"],
    "autriche": ["allemand", "anglais"],
    "pologne": ["polonais", "anglais", "allemand"],
    "hongrie": ["hongrois", "anglais"],
    "suède": ["suédois", "anglais"],
    "norvège": ["norvégien", "anglais"],
    "finlande": ["finnois", "suédois", "anglais"],
    "danemark": ["danois", "anglais"],
    "grèce": ["grec", "anglais"],
    "turquie": ["turc", "kurde", "anglais"],
    "russie": ["russe", "anglais", "tatar", "ukrainien"],
    "ukraine": ["ukrainien", "russe", "anglais"],
    "biélorusse": ["biélorusse", "russe"],
    "états-unis": ["anglais", "espagnol"],
    "canada": ["anglais", "français"],
    "mexique": ["espagnol", "anglais"],
    "brésil": ["portugais", "espagnol", "anglais"],
    "argentine": ["espagnol", "anglais"],
    "colombie": ["espagnol", "anglais"],
    "chine": ["chinois", "anglais", "cantonais", "ouïghour"],
    "japon": ["japonais", "anglais"],
    "corée du sud": ["coréen", "anglais"],
    "inde": ["hindi", "anglais", "bengali", "tamoul", "télougou", "marathi", "gujarati", "kannada", "malayalam"],
    "pakistan": ["ourdou", "anglais", "pendjabi", "sindhi"],
    "bangladesh": ["bengali", "anglais"],
    "sri lanka": ["singhalais", "tamoul", "anglais"],
    "népal": ["népalais", "hindi", "anglais"],
    "iran": ["persan", "anglais", "azéri", "kurde"],
    "israël": ["hébreu", "arabe", "anglais", "russe"],
    "arabie saoudite": ["arabe", "anglais"],
    "maroc": ["arabe", "berbère", "français", "espagnol"],
    "algérie": ["arabe", "berbère", "français"],
    "tunisie": ["arabe", "français"],
    "egypte": ["arabe", "anglais", "français"],
    "afrique du sud": ["anglais", "afrikaans", "zoulou", "xhosa"],
    "nigeria": ["anglais", "haoussa", "yoruba", "igbo"],
    "kenya": ["anglais", "swahili"],
    "éthiopie": ["amharique", "oromo", "anglais"],
    "sénégal": ["français", "wolof"],
    "côte d'ivoire": ["français"],
    "mali": ["français", "bambara"],
    "rd congo": ["français", "lingala", "swahili"],
    "australie": ["anglais"],
    "nouvelle-zélande": ["anglais", "maori"],
    "indonésie": ["indonésien", "javanais", "anglais", "malais"],
    "malaisie": ["malais", "anglais", "tamoul", "mandarin"],
    "thailand": ["thaï", "anglais"],
    "viet nam": ["vietnamien", "anglais", "français"],
    "singapour": ["anglais", "mandarin", "malais", "tamoul"],
    "kazakhstan": ["kazakh", "russe", "anglais"],
    "ouzbékistan": ["ouzbek", "russe"],
    "kirghizistan": ["kirghiz", "russe"],
    "tadjikistan": ["tadjik", "russe"],
    "turkménistan": ["turkmène", "russe"],
    "mongolie": ["mongol", "russe"],
    "cuba": ["espagnol"],
    "vénézuela": ["espagnol"],
    "chili": ["espagnol"],
    "pérou": ["espagnol", "quechua", "aymara"],
    "bolivie": ["espagnol", "quechua", "aymara"],
    "paraguay": ["espagnol", "guarani"],
    "islande": ["islandais", "anglais"],
    "lettonie": ["letton", "russe"],
    "lituanie": ["lituanien", "russe"],
    "estonie": ["estonien", "russe"],
    "slovaquie": ["slovaque", "hongrois"],
    "bulgarie": ["bulgare", "anglais"],
    "roumanie": ["roumain", "hongrois"],
    "croatie": ["croate"],
    "serbie": ["serbe"],
    "bosnie": ["bosnien", "croate", "serbe"],
    "albanie": ["albanais"],
    "monténégro": ["monténégrin"],
    "macédoine": ["macédonien"],
    "slovénie": ["slovène"],
    "géorgie": ["géorgien", "russe"],
    "arménie": ["arménien", "russe"],
    "azerbaïdjan": ["azéri", "russe"],
    "afghanistan": ["dari", "pashto", "anglais"],
    "irak": ["arabe", "kurde", "anglais"],
    "syrie": ["arabe", "kurde", "arménien"],
    "liban": ["arabe", "français", "anglais"],
    "jordanie": ["arabe", "anglais"],
    "tchéquie": ["tchèque", "allemand"],
    "maldives": ["divehi", "anglais"],
    "philippines": ["tagalog", "anglais"],
    "birmanie": ["birman", "anglais"],
    "laos": ["laotien", "français"],
    "cambodge": ["khmer", "français"],
    "malte": ["maltais", "anglais", "italien"],
}

# Fonction pour obtenir toutes les langues uniques du système
def obtenir_toutes_langues():
    """Retourne la liste de toutes les langues uniques dans le système"""
    langues = set()
    for pays_langues in LANGUES_PAR_PAYS.values():
        langues.update(pays_langues)
    return sorted(list(langues))

# Fonction pour obtenir les langues d'un pays
def obtenir_langues_pays(pays):
    """Retourne les langues d'un pays donné"""
    return LANGUES_PAR_PAYS.get(pays.lower(), ["français"])

# Fonction pour vérifier si une langue existe
def langue_existe(langue):
    """Vérifie si une langue existe dans le système"""
    return langue.lower() in [l.lower() for l in obtenir_toutes_langues()]

# Fonction pour obtenir les pays qui parlent une langue
def obtenir_pays_langue(langue):
    """Retourne la liste des pays qui parlent une langue donnée"""
    pays_avec_langue = []
    for pays, langues in LANGUES_PAR_PAYS.items():
        if langue.lower() in [l.lower() for l in langues]:
            pays_avec_langue.append(pays)
    return pays_avec_langue