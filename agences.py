# agences.py

import random

# Structure organisée par pays comme villes.py
AGENCES_PAR_PAYS = {
    "états-unis": [
        {"nom": "CIA", "domaines": ["SIGINT", "HUMINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Agence civile"},
        {"nom": "NSA", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": False, "type": "Agence militaire"},
        {"nom": "FBI", "domaines": ["HUMINT", "TECH"], "langues": ["anglais"], "coop": True, "type": "Police fédérale"},
        {"nom": "DIA", "domaines": ["HUMINT", "SIGINT"], "langues": ["anglais"], "coop": False, "type": "Agence militaire"},
        {"nom": "NRO", "domaines": ["SIGINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Agence spatiale"}
    ],
    
    "royaume-uni": [
        {"nom": "MI6", "domaines": ["HUMINT", "SIGINT"], "langues": ["anglais"], "coop": True, "type": "Agence extérieure"},
        {"nom": "MI5", "domaines": ["HUMINT", "SIGINT"], "langues": ["anglais"], "coop": True, "type": "Agence intérieure"},
        {"nom": "GCHQ", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": True, "type": "Agence SIGINT"},
        {"nom": "SIS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais"], "coop": True, "type": "Service secret"}
    ],
    
    "allemagne": [
        {"nom": "BND", "domaines": ["HUMINT", "SIGINT"], "langues": ["allemand", "anglais"], "coop": True, "type": "Agence fédérale"},
        {"nom": "BfV", "domaines": ["HUMINT", "TECH"], "langues": ["allemand"], "coop": True, "type": "Protection constitutionnelle"},
        {"nom": "BKA", "domaines": ["HUMINT", "TECH"], "langues": ["allemand"], "coop": True, "type": "Police criminelle"}
    ],
    
    "france": [
        # Exclu comme demandé
    ],
    
    "italie": [
        {"nom": "AISE", "domaines": ["HUMINT", "SIGINT"], "langues": ["italien", "anglais"], "coop": True, "type": "Agence extérieure"},
        {"nom": "AISI", "domaines": ["HUMINT", "TECH"], "langues": ["italien"], "coop": True, "type": "Agence intérieure"},
        {"nom": "ROS", "domaines": ["HUMINT", "TECH"], "langues": ["italien"], "coop": True, "type": "Carabiniers"}
    ],
    
    "espagne": [
        {"nom": "CNI", "domaines": ["HUMINT", "SIGINT"], "langues": ["espagnol", "anglais"], "coop": True, "type": "Agence nationale"},
        {"nom": "CESID", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": True, "type": "Service militaire"}
    ],
    
    "portugal": [
        {"nom": "SIED", "domaines": ["HUMINT", "SIGINT"], "langues": ["portugais", "anglais"], "coop": True, "type": "Service extérieur"},
        {"nom": "SIS", "domaines": ["HUMINT", "TECH"], "langues": ["portugais"], "coop": True, "type": "Service intérieur"}
    ],
    
    "pays-bas": [
        {"nom": "AIVD", "domaines": ["HUMINT", "CYBER"], "langues": ["néerlandais", "anglais"], "coop": True, "type": "Agence intérieure"},
        {"nom": "MIVD", "domaines": ["SIGINT", "TECH"], "langues": ["néerlandais"], "coop": True, "type": "Service militaire"}
    ],
    
    "belgique": [
        {"nom": "VSSE", "domaines": ["HUMINT", "SIGINT"], "langues": ["français", "néerlandais"], "coop": True, "type": "Agence d'État"},
        {"nom": "SGRS", "domaines": ["SIGINT", "TECH"], "langues": ["français", "néerlandais"], "coop": True, "type": "Service militaire"}
    ],
    
    "suisse": [
        {"nom": "NDB", "domaines": ["HUMINT", "SIGINT"], "langues": ["allemand", "français", "italien"], "coop": True, "type": "Service fédéral"},
        {"nom": "SRC", "domaines": ["SIGINT", "TECH"], "langues": ["allemand", "français"], "coop": True, "type": "Service militaire"}
    ],
    
    "autriche": [
        {"nom": "BVT", "domaines": ["HUMINT", "TECH"], "langues": ["allemand", "anglais"], "coop": True, "type": "Agence fédérale"},
        {"nom": "HNA", "domaines": ["SIGINT", "TECH"], "langues": ["allemand"], "coop": True, "type": "Service militaire"}
    ],
    
    "pologne": [
        {"nom": "ABW", "domaines": ["HUMINT", "TECH"], "langues": ["polonais", "anglais"], "coop": True, "type": "Agence intérieure"},
        {"nom": "SKW", "domaines": ["HUMINT", "SIGINT"], "langues": ["polonais"], "coop": True, "type": "Service militaire"},
        {"nom": "AW", "domaines": ["SIGINT", "TECH"], "langues": ["polonais"], "coop": True, "type": "Agence militaire"}
    ],
    
    "hongrie": [
        {"nom": "IH", "domaines": ["HUMINT", "TECH"], "langues": ["hongrois", "anglais"], "coop": True, "type": "Agence nationale"},
        {"nom": "KNBSZ", "domaines": ["SIGINT", "TECH"], "langues": ["hongrois"], "coop": True, "type": "Service militaire"}
    ],
    
    "suède": [
        {"nom": "SÄPO", "domaines": ["HUMINT", "TECH"], "langues": ["suédois", "anglais"], "coop": True, "type": "Agence de sécurité"},
        {"nom": "MUST", "domaines": ["SIGINT", "TECH"], "langues": ["suédois"], "coop": True, "type": "Service militaire"}
    ],
    
    "norvège": [
        {"nom": "PST", "domaines": ["HUMINT", "TECH"], "langues": ["norvégien", "anglais"], "coop": True, "type": "Agence de sécurité"},
        {"nom": "EOS", "domaines": ["SIGINT", "TECH"], "langues": ["norvégien"], "coop": True, "type": "Service militaire"}
    ],
    
    "finlande": [
        {"nom": "SUPO", "domaines": ["HUMINT", "TECH"], "langues": ["finnois", "suédois"], "coop": True, "type": "Agence de sécurité"},
        {"nom": "VK", "domaines": ["SIGINT", "TECH"], "langues": ["finnois"], "coop": True, "type": "Service militaire"}
    ],
    
    "danemark": [
        {"nom": "PET", "domaines": ["HUMINT", "TECH"], "langues": ["danois", "anglais"], "coop": True, "type": "Agence de sécurité"},
        {"nom": "FE", "domaines": ["SIGINT", "TECH"], "langues": ["danois"], "coop": True, "type": "Service militaire"}
    ],
    
    "grèce": [
        {"nom": "EYP", "domaines": ["HUMINT", "SIGINT"], "langues": ["grec", "anglais"], "coop": True, "type": "Agence nationale"},
        {"nom": "DIE", "domaines": ["SIGINT", "TECH"], "langues": ["grec"], "coop": True, "type": "Service militaire"}
    ],
    
    "turquie": [
        {"nom": "MIT", "domaines": ["HUMINT", "CYBER"], "langues": ["turc", "anglais"], "coop": False, "type": "Agence nationale"},
        {"nom": "JITEM", "domaines": ["HUMINT", "TECH"], "langues": ["turc"], "coop": False, "type": "Service militaire"}
    ],
    
    "russie": [
        {"nom": "FSB", "domaines": ["SIGINT", "HUMINT", "TECH"], "langues": ["russe"], "coop": False, "type": "Service fédéral"},
        {"nom": "SVR", "domaines": ["HUMINT", "SIGINT"], "langues": ["russe"], "coop": False, "type": "Service extérieur"},
        {"nom": "GRU", "domaines": ["SIGINT", "HUMINT"], "langues": ["russe"], "coop": False, "type": "Service militaire"},
        {"nom": "KGB", "domaines": ["HUMINT", "SIGINT", "TECH"], "langues": ["russe"], "coop": False, "type": "Service historique"}
    ],
    
    "ukraine": [
        {"nom": "SBU", "domaines": ["HUMINT", "CYBER"], "langues": ["ukrainien", "russe"], "coop": True, "type": "Service de sécurité"},
        {"nom": "GUR", "domaines": ["SIGINT", "TECH"], "langues": ["ukrainien"], "coop": True, "type": "Service militaire"}
    ],
    
    "canada": [
        {"nom": "CSIS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais", "français"], "coop": True, "type": "Service civil"},
        {"nom": "CSE", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais", "français"], "coop": True, "type": "Service SIGINT"}
    ],
    
    "mexique": [
        {"nom": "CISEN", "domaines": ["HUMINT", "SIGINT"], "langues": ["espagnol"], "coop": False, "type": "Agence nationale"},
        {"nom": "SEDENA", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ],
    
    "brésil": [
        {"nom": "ABIN", "domaines": ["HUMINT", "SIGINT"], "langues": ["portugais"], "coop": False, "type": "Agence nationale"},
        {"nom": "CIM", "domaines": ["SIGINT", "TECH"], "langues": ["portugais"], "coop": False, "type": "Service militaire"}
    ],
    
    "argentine": [
        {"nom": "SIDE", "domaines": ["HUMINT", "SIGINT"], "langues": ["espagnol"], "coop": False, "type": "Agence nationale"},
        {"nom": "SIE", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ],
    
    "colombie": [
        {"nom": "DAS", "domaines": ["HUMINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Agence de sécurité"},
        {"nom": "DIPOL", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ],
    
    "chine": [
        {"nom": "MSS", "domaines": ["HUMINT", "CYBER"], "langues": ["chinois", "anglais"], "coop": False, "type": "Ministère sécurité"},
        {"nom": "PLA", "domaines": ["SIGINT", "TECH"], "langues": ["chinois"], "coop": False, "type": "Armée populaire"},
        {"nom": "MPS", "domaines": ["HUMINT", "TECH"], "langues": ["chinois"], "coop": False, "type": "Ministère police"}
    ],
    
    "japon": [
        {"nom": "PSIA", "domaines": ["HUMINT", "CYBER"], "langues": ["japonais", "anglais"], "coop": True, "type": "Agence sécurité"},
        {"nom": "DIH", "domaines": ["SIGINT", "TECH"], "langues": ["japonais"], "coop": True, "type": "Service militaire"}
    ],
    
    "corée du sud": [
        {"nom": "NIS", "domaines": ["HUMINT", "CYBER"], "langues": ["coréen", "anglais"], "coop": True, "type": "Service national"},
        {"nom": "DIA", "domaines": ["SIGINT", "TECH"], "langues": ["coréen"], "coop": True, "type": "Service militaire"}
    ],
    
    "corée du nord": [
        {"nom": "RGB", "domaines": ["HUMINT", "SIGINT"], "langues": ["coréen"], "coop": False, "type": "Bureau renseignement"},
        {"nom": "MSS", "domaines": ["SIGINT", "TECH"], "langues": ["coréen"], "coop": False, "type": "Ministère sécurité"}
    ],
    
    "inde": [
        {"nom": "RAW", "domaines": ["HUMINT", "SIGINT"], "langues": ["hindi", "anglais"], "coop": False, "type": "Agence extérieure"},
        {"nom": "IB", "domaines": ["HUMINT", "TECH"], "langues": ["hindi", "anglais"], "coop": False, "type": "Bureau intérieur"},
        {"nom": "DIA", "domaines": ["SIGINT", "TECH"], "langues": ["hindi", "anglais"], "coop": False, "type": "Service militaire"}
    ],
    
    "pakistan": [
        {"nom": "ISI", "domaines": ["HUMINT", "SIGINT"], "langues": ["ourdou", "anglais"], "coop": False, "type": "Service inter-services"},
        {"nom": "IB", "domaines": ["HUMINT", "TECH"], "langues": ["ourdou"], "coop": False, "type": "Bureau intérieur"},
        {"nom": "MI", "domaines": ["SIGINT", "TECH"], "langues": ["ourdou"], "coop": False, "type": "Service militaire"}
    ],
    
    "iran": [
        {"nom": "MOIS", "domaines": ["HUMINT", "SIGINT"], "langues": ["persan", "anglais"], "coop": False, "type": "Ministère renseignement"},
        {"nom": "IRGC", "domaines": ["SIGINT", "TECH"], "langues": ["persan"], "coop": False, "type": "Garde révolutionnaire"},
        {"nom": "VEVAK", "domaines": ["HUMINT", "TECH"], "langues": ["persan"], "coop": False, "type": "Agence sécurité"}
    ],
    
    "israël": [
        {"nom": "Mossad", "domaines": ["HUMINT", "SIGINT"], "langues": ["hébreu", "anglais"], "coop": False, "type": "Agence extérieure"},
        {"nom": "Shin Bet", "domaines": ["HUMINT", "TECH"], "langues": ["hébreu", "arabe"], "coop": False, "type": "Agence intérieure"},
        {"nom": "AMAN", "domaines": ["SIGINT", "TECH"], "langues": ["hébreu"], "coop": False, "type": "Service militaire"}
    ],
    
    "arabie saoudite": [
        {"nom": "GIP", "domaines": ["HUMINT", "SIGINT"], "langues": ["arabe", "anglais"], "coop": False, "type": "Agence générale"},
        {"nom": "Mabahith", "domaines": ["HUMINT", "TECH"], "langues": ["arabe"], "coop": False, "type": "Agence intérieure"}
    ],
    
    "maroc": [
        {"nom": "DGST", "domaines": ["HUMINT", "TECH"], "langues": ["arabe", "français"], "coop": False, "type": "Direction sécurité"},
        {"nom": "DGED", "domaines": ["SIGINT", "TECH"], "langues": ["arabe", "français"], "coop": False, "type": "Direction études"}
    ],
    
    "australie": [
        {"nom": "ASIS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais"], "coop": True, "type": "Service extérieur"},
        {"nom": "ASD", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": True, "type": "Service SIGINT"},
        {"nom": "ASIO", "domaines": ["HUMINT", "TECH"], "langues": ["anglais"], "coop": True, "type": "Service intérieur"}
    ],
    
    "nouvelle-zélande": [
        {"nom": "NZSIS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais", "maori"], "coop": True, "type": "Service sécurité"},
        {"nom": "GCSB", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": True, "type": "Service SIGINT"}
    ],
    
    "indonésie": [
        {"nom": "BIN", "domaines": ["HUMINT", "TECH"], "langues": ["indonésien", "anglais"], "coop": False, "type": "Agence nationale"},
        {"nom": "BAIS", "domaines": ["SIGINT", "TECH"], "langues": ["indonésien"], "coop": False, "type": "Service militaire"}
    ],
    
    "malaisie": [
        {"nom": "MEIO", "domaines": ["HUMINT", "TECH"], "langues": ["malais", "anglais"], "coop": False, "type": "Agence extérieure"},
        {"nom": "JIO", "domaines": ["SIGINT", "TECH"], "langues": ["malais"], "coop": False, "type": "Service militaire"}
    ],
    
    "thailande": [
        {"nom": "NIA", "domaines": ["HUMINT", "TECH"], "langues": ["thaï", "anglais"], "coop": False, "type": "Agence nationale"},
        {"nom": "J2", "domaines": ["SIGINT", "TECH"], "langues": ["thaï"], "coop": False, "type": "Service militaire"}
    ],
    
    "viet nam": [
        {"nom": "TC2", "domaines": ["HUMINT", "TECH"], "langues": ["vietnamien", "français"], "coop": False, "type": "Service militaire"},
        {"nom": "A25", "domaines": ["SIGINT", "TECH"], "langues": ["vietnamien"], "coop": False, "type": "Agence sécurité"}
    ],
    
    "singapour": [
        {"nom": "SID", "domaines": ["HUMINT", "TECH"], "langues": ["anglais", "mandarin"], "coop": False, "type": "Service renseignement"},
        {"nom": "MIO", "domaines": ["SIGINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Service militaire"}
    ],
    
    "kazakhstan": [
        {"nom": "KNB", "domaines": ["HUMINT", "TECH"], "langues": ["kazakh", "russe"], "coop": False, "type": "Comité sécurité"},
        {"nom": "GRK", "domaines": ["SIGINT", "TECH"], "langues": ["kazakh"], "coop": False, "type": "Service militaire"}
    ],
    
    "islande": [
        {"nom": "RNS", "domaines": ["HUMINT", "TECH"], "langues": ["islandais", "anglais"], "coop": True, "type": "Service national"},
        {"nom": "VSK", "domaines": ["SIGINT", "TECH"], "langues": ["islandais"], "coop": True, "type": "Service militaire"}
    ],
    
    "lettonie": [
        {"nom": "SAB", "domaines": ["HUMINT", "TECH"], "langues": ["letton", "anglais"], "coop": True, "type": "Agence sécurité"},
        {"nom": "MID", "domaines": ["SIGINT", "TECH"], "langues": ["letton"], "coop": True, "type": "Service militaire"}
    ],
    
    "lituanie": [
        {"nom": "VSD", "domaines": ["HUMINT", "TECH"], "langues": ["lituanien", "anglais"], "coop": True, "type": "Service sécurité"},
        {"nom": "AOTD", "domaines": ["SIGINT", "TECH"], "langues": ["lituanien"], "coop": True, "type": "Service militaire"}
    ],
    
    "estonie": [
        {"nom": "KAPO", "domaines": ["HUMINT", "TECH"], "langues": ["estonien", "anglais"], "coop": True, "type": "Agence sécurité"},
        {"nom": "VTE", "domaines": ["SIGINT", "TECH"], "langues": ["estonien"], "coop": True, "type": "Service militaire"}
    ],
    
    "slovaquie": [
        {"nom": "SIS", "domaines": ["HUMINT", "TECH"], "langues": ["slovaque", "hongrois"], "coop": True, "type": "Service sécurité"},
        {"nom": "VSS", "domaines": ["SIGINT", "TECH"], "langues": ["slovaque"], "coop": True, "type": "Service militaire"}
    ],
    
    "bulgarie": [
        {"nom": "DANS", "domaines": ["HUMINT", "TECH"], "langues": ["bulgare", "anglais"], "coop": True, "type": "Agence sécurité"},
        {"nom": "RRS", "domaines": ["SIGINT", "TECH"], "langues": ["bulgare"], "coop": True, "type": "Service militaire"}
    ],
    
    "roumanie": [
        {"nom": "SRI", "domaines": ["HUMINT", "TECH"], "langues": ["roumain", "hongrois"], "coop": True, "type": "Service renseignement"},
        {"nom": "DGIA", "domaines": ["SIGINT", "TECH"], "langues": ["roumain"], "coop": True, "type": "Service militaire"}
    ],
    
    "croatie": [
        {"nom": "SOA", "domaines": ["HUMINT", "TECH"], "langues": ["croate", "anglais"], "coop": True, "type": "Agence sécurité"},
        {"nom": "VSOA", "domaines": ["SIGINT", "TECH"], "langues": ["croate"], "coop": True, "type": "Service militaire"}
    ],
    
    "serbie": [
        {"nom": "BIA", "domaines": ["HUMINT", "TECH"], "langues": ["serbe", "anglais"], "coop": False, "type": "Agence sécurité"},
        {"nom": "VBA", "domaines": ["SIGINT", "TECH"], "langues": ["serbe"], "coop": False, "type": "Service militaire"}
    ],
    
    "bosnie": [
        {"nom": "OSA", "domaines": ["HUMINT", "TECH"], "langues": ["bosnien", "croate", "serbe"], "coop": False, "type": "Agence sécurité"},
        {"nom": "VOS", "domaines": ["SIGINT", "TECH"], "langues": ["bosnien"], "coop": False, "type": "Service militaire"}
    ],
    
    "albanie": [
        {"nom": "SHISH", "domaines": ["HUMINT", "TECH"], "langues": ["albanais", "anglais"], "coop": False, "type": "Service renseignement"},
        {"nom": "KMSH", "domaines": ["SIGINT", "TECH"], "langues": ["albanais"], "coop": False, "type": "Service militaire"}
    ],
    
    "monténégro": [
        {"nom": "ANB", "domaines": ["HUMINT", "TECH"], "langues": ["monténégrin", "serbe"], "coop": False, "type": "Agence sécurité"},
        {"nom": "VOS", "domaines": ["SIGINT", "TECH"], "langues": ["monténégrin"], "coop": False, "type": "Service militaire"}
    ],
    
    "géorgie": [
        {"nom": "SSSG", "domaines": ["HUMINT", "TECH"], "langues": ["géorgien", "anglais"], "coop": False, "type": "Service sécurité"},
        {"nom": "J-2", "domaines": ["SIGINT", "TECH"], "langues": ["géorgien"], "coop": False, "type": "Service militaire"}
    ],
    
    "arménie": [
        {"nom": "NSS", "domaines": ["HUMINT", "TECH"], "langues": ["arménien", "russe"], "coop": False, "type": "Service sécurité"},
        {"nom": "GRU", "domaines": ["SIGINT", "TECH"], "langues": ["arménien"], "coop": False, "type": "Service militaire"}
    ],
    
    "azerbaïdjan": [
        {"nom": "MTN", "domaines": ["HUMINT", "TECH"], "langues": ["azéri", "russe"], "coop": False, "type": "Ministère sécurité"},
        {"nom": "XDM", "domaines": ["SIGINT", "TECH"], "langues": ["azéri"], "coop": False, "type": "Service militaire"}
    ],
    
    "turkménistan": [
        {"nom": "KNB", "domaines": ["HUMINT", "TECH"], "langues": ["turkmène", "russe"], "coop": False, "type": "Comité sécurité"},
        {"nom": "GRK", "domaines": ["SIGINT", "TECH"], "langues": ["turkmène"], "coop": False, "type": "Service militaire"}
    ],
    
    "ouzbekistan": [
        {"nom": "SNB", "domaines": ["HUMINT", "TECH"], "langues": ["ouzbek", "russe"], "coop": False, "type": "Service sécurité"},
        {"nom": "GRU", "domaines": ["SIGINT", "TECH"], "langues": ["ouzbek"], "coop": False, "type": "Service militaire"}
    ],
    
    "kirghizistan": [
        {"nom": "GKNB", "domaines": ["HUMINT", "TECH"], "langues": ["kirghiz", "russe"], "coop": False, "type": "Comité sécurité"},
        {"nom": "GRU", "domaines": ["SIGINT", "TECH"], "langues": ["kirghiz"], "coop": False, "type": "Service militaire"}
    ],
    
    "egypte": [
        {"nom": "GIS", "domaines": ["HUMINT", "SIGINT"], "langues": ["arabe", "anglais"], "coop": False, "type": "Service général"},
        {"nom": "SSI", "domaines": ["HUMINT", "TECH"], "langues": ["arabe"], "coop": False, "type": "Service sécurité"},
        {"nom": "MI", "domaines": ["SIGINT", "TECH"], "langues": ["arabe"], "coop": False, "type": "Service militaire"}
    ],
    
    "afrique du sud": [
        {"nom": "SASS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais", "afrikaans"], "coop": False, "type": "Service secret"},
        {"nom": "NIA", "domaines": ["HUMINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Agence nationale"},
        {"nom": "DSS", "domaines": ["SIGINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Service militaire"}
    ],
    
    "nigeria": [
        {"nom": "SSS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais", "haoussa"], "coop": False, "type": "Service sécurité"},
        {"nom": "DIA", "domaines": ["SIGINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Service militaire"}
    ],
    
    "sénégal": [
        {"nom": "DCRI", "domaines": ["HUMINT", "TECH"], "langues": ["français", "wolof"], "coop": False, "type": "Direction renseignement"},
        {"nom": "DSS", "domaines": ["SIGINT", "TECH"], "langues": ["français"], "coop": False, "type": "Service militaire"}
    ],
    
    "côte d'ivoire": [
        {"nom": "DCRI", "domaines": ["HUMINT", "TECH"], "langues": ["français"], "coop": False, "type": "Direction renseignement"},
        {"nom": "DSS", "domaines": ["SIGINT", "TECH"], "langues": ["français"], "coop": False, "type": "Service militaire"}
    ],
    
    "mali": [
        {"nom": "DCRI", "domaines": ["HUMINT", "TECH"], "langues": ["français", "bambara"], "coop": False, "type": "Direction renseignement"},
        {"nom": "DSS", "domaines": ["SIGINT", "TECH"], "langues": ["français"], "coop": False, "type": "Service militaire"}
    ],
    
    "rd congo": [
        {"nom": "ANR", "domaines": ["HUMINT", "TECH"], "langues": ["français", "lingala"], "coop": False, "type": "Agence nationale"},
        {"nom": "DSS", "domaines": ["SIGINT", "TECH"], "langues": ["français"], "coop": False, "type": "Service militaire"}
    ],
    
    "kenya": [
        {"nom": "NIS", "domaines": ["HUMINT", "TECH"], "langues": ["anglais", "swahili"], "coop": False, "type": "Service national"},
        {"nom": "DIA", "domaines": ["SIGINT", "TECH"], "langues": ["anglais"], "coop": False, "type": "Service militaire"}
    ],
    
    "éthiopie": [
        {"nom": "NISS", "domaines": ["HUMINT", "TECH"], "langues": ["amharique", "anglais"], "coop": False, "type": "Service national"},
        {"nom": "DIA", "domaines": ["SIGINT", "TECH"], "langues": ["amharique"], "coop": False, "type": "Service militaire"}
    ],
    
    "cuba": [
        {"nom": "DI", "domaines": ["HUMINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Direction renseignement"},
        {"nom": "DIM", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ],
    
    "vénézuela": [
        {"nom": "SEBIN", "domaines": ["HUMINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service renseignement"},
        {"nom": "DIM", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ],
    
    "chili": [
        {"nom": "ANI", "domaines": ["HUMINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Agence nationale"},
        {"nom": "DIM", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ],
    
    "pérou": [
        {"nom": "DINI", "domaines": ["HUMINT", "TECH"], "langues": ["espagnol", "quechua"], "coop": False, "type": "Direction renseignement"},
        {"nom": "DIM", "domaines": ["SIGINT", "TECH"], "langues": ["espagnol"], "coop": False, "type": "Service militaire"}
    ]
}

# Fonctions utilitaires
def choisir_agence():
    """Choisit une agence aléatoire parmi toutes les agences"""
    toutes_agences = []
    for pays, agences in AGENCES_PAR_PAYS.items():
        for agence in agences:
            agence_copy = agence.copy()
            agence_copy["pays"] = pays
            toutes_agences.append(agence_copy)
    return random.choice(toutes_agences)

def lister_agences(pays=None):
    """Liste les agences d'un pays spécifique ou toutes les agences"""
    if pays is None:
        toutes_agences = []
        for pays_nom, agences in AGENCES_PAR_PAYS.items():
            for agence in agences:
                agence_copy = agence.copy()
                agence_copy["pays"] = pays_nom
                toutes_agences.append(agence_copy)
        return toutes_agences
    else:
        pays_lower = pays.lower()
        if pays_lower in AGENCES_PAR_PAYS:
            agences = []
            for agence in AGENCES_PAR_PAYS[pays_lower]:
                agence_copy = agence.copy()
                agence_copy["pays"] = pays_lower
                agences.append(agence_copy)
            return agences
        return []

def lister_pays_agences():
    """Liste tous les pays qui ont des agences de renseignement"""
    return list(AGENCES_PAR_PAYS.keys())

def obtenir_agence_par_nom(nom_agence):
    """Recherche une agence par son nom exact"""
    for pays, agences in AGENCES_PAR_PAYS.items():
        for agence in agences:
            if agence["nom"] == nom_agence:
                agence_copy = agence.copy()
                agence_copy["pays"] = pays
                return agence_copy
    return None

def filtrer_agences_par_domaine(domaine):
    """Filtre les agences par domaine d'expertise"""
    resultats = []
    for pays, agences in AGENCES_PAR_PAYS.items():
        for agence in agences:
            if domaine in agence["domaines"]:
                agence_copy = agence.copy()
                agence_copy["pays"] = pays
                resultats.append(agence_copy)
    return resultats

def filtrer_agences_par_cooperation(coop=True):
    """Filtre les agences par niveau de coopération"""
    resultats = []
    for pays, agences in AGENCES_PAR_PAYS.items():
        for agence in agences:
            if agence["coop"] == coop:
                agence_copy = agence.copy()
                agence_copy["pays"] = pays
                resultats.append(agence_copy)
    return resultats

# Compatibilité avec l'ancien système
AGENCES = []
for pays, agences_pays in AGENCES_PAR_PAYS.items():
    for agence in agences_pays:
        agence_copy = agence.copy()
        agence_copy["pays"] = pays
        AGENCES.append(agence_copy)
