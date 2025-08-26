# geographie.py
# Fichier unifié contenant toutes les données géographiques, linguistiques et onomastiques
# Fusion des fichiers : noms.py, villes.py, langues.py
# GÉNÉRÉ AUTOMATIQUEMENT - NE PAS MODIFIER MANUELLEMENT

import random

# ============================================================================
# DONNÉES GÉOGRAPHIQUES UNIFIÉES
# ============================================================================

# Structure principale : PAYS -> {villes, langues, noms, coordonnées}
GEOGRAPHIE_UNIFIEE = {
    "afrique du sud": {
        "capitale": "Pretoria",
        "coordonnees": {"lat": -30.5595, "lon": 22.9375},
        "villes": [
            {"ville": "Pretoria", "lat": -25.7479, "lon": 28.2293},
            {"ville": "Johannesburg", "lat": -26.2041, "lon": 28.0473},
            {"ville": "Le Cap", "lat": -33.9249, "lon": 18.4241},
            {"ville": "Durban", "lat": -29.8587, "lon": 31.0218},
            {"ville": "Port Elizabeth", "lat": -33.7139, "lon": 25.5207},
            {"ville": "Bloemfontein", "lat": -29.0852, "lon": 26.1596},
            {"ville": "East London", "lat": -33.0292, "lon": 27.8546},
            {"ville": "Kimberley", "lat": -28.7282, "lon": 24.7499},
            {"ville": "Nelspruit", "lat": -25.4753, "lon": 30.9694},
            {"ville": "Polokwane", "lat": -23.9045, "lon": 29.4688},
        ],
        "langues": ["anglais", "afrikaans", "zoulou", "xhosa"],
        "noms": {
            "prenoms": ["Thabo", "Sipho", "Lerato", "Ayanda", "Nkosi", "Nomsa"],
            "noms": ["Nkosi", "Dlamini", "Botha", "Naidoo", "Mthembu"]
        }
    },

    "albanie": {
        "capitale": "Tirana",
        "coordonnees": {"lat": 41.1533, "lon": 20.1683},
        "villes": [
            {"ville": "Tirana", "lat": 41.3275, "lon": 19.8187},
            {"ville": "Durrës", "lat": 41.3245, "lon": 19.4511},
            {"ville": "Elbasan", "lat": 41.1136, "lon": 20.0822},
            {"ville": "Shkodër", "lat": 42.0683, "lon": 19.5119},
            {"ville": "Vlorë", "lat": 40.4667, "lon": 19.4833},
            {"ville": "Korçë", "lat": 40.6167, "lon": 20.7667},
            {"ville": "Fier", "lat": 40.7167, "lon": 19.5500},
            {"ville": "Berat", "lat": 40.7000, "lon": 19.9500},
            {"ville": "Lushnjë", "lat": 40.9333, "lon": 19.7000},
            {"ville": "Kavajë", "lat": 41.1833, "lon": 19.5500},
        ],
        "langues": ["albanais"],
        "noms": {
            "prenoms": ["Erion", "Arben", "Elira", "Luljeta", "Altin", "Anila"],
            "noms": ["Hoxha", "Shehu", "Krasniqi", "Gashi", "Shala"]
        }
    },

    "algérie": {
        "capitale": "Alger",
        "coordonnees": {"lat": 28.0339, "lon": 1.6596},
        "villes": [
            {"ville": "Alger", "lat": 36.7538, "lon": 3.0588},
            {"ville": "Oran", "lat": 35.6969, "lon": -0.6331},
            {"ville": "Constantine", "lat": 36.3650, "lon": 6.6147},
            {"ville": "Annaba", "lat": 36.9000, "lon": 7.7667},
            {"ville": "Batna", "lat": 35.5500, "lon": 6.1667},
            {"ville": "Blida", "lat": 36.4700, "lon": 2.8300},
            {"ville": "Sétif", "lat": 36.1900, "lon": 5.4100},
            {"ville": "Chlef", "lat": 36.1667, "lon": 1.3333},
            {"ville": "Djelfa", "lat": 34.6667, "lon": 3.2500},
            {"ville": "Tébessa", "lat": 35.4000, "lon": 8.1167},
        ],
        "langues": ["arabe", "berbère", "français"],
        "noms": {
            "prenoms": ["Ahmed", "Samir", "Karim", "Nadia", "Amina", "Yasmine"],
            "noms": ["Bouzid", "Benali", "Meziane", "Benkhelifa", "Guendouzi"]
        }
    },

    "allemagne": {
        "capitale": "Allemagne",
        "coordonnees": {"lat": 51.1657, "lon": 10.4515},
        "villes": [
            {"ville": "Berlin", "lat": 52.52, "lon": 13.405},
            {"ville": "Hambourg", "lat": 53.5511, "lon": 9.9937},
            {"ville": "Munich", "lat": 48.1351, "lon": 11.582},
            {"ville": "Cologne", "lat": 50.9375, "lon": 6.9603},
            {"ville": "Francfort", "lat": 50.1109, "lon": 8.6821},
            {"ville": "Stuttgart", "lat": 48.7758, "lon": 9.1829},
            {"ville": "Düsseldorf", "lat": 51.2277, "lon": 6.7735},
            {"ville": "Dortmund", "lat": 51.5136, "lon": 7.4653},
            {"ville": "Essen", "lat": 51.4556, "lon": 7.0116},
            {"ville": "Leipzig", "lat": 51.3397, "lon": 12.3731},
        ],
        "langues": ["allemand", "anglais", "turc", "français"],
        "noms": {
            "prenoms": ["Hans", "Anna", "Peter", "Sophie", "Lukas", "Sabine"],
            "noms": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber"]
        }
    },

    "arabie saoudite": {
        "capitale": "Riyad",
        "coordonnees": {"lat": 23.8859, "lon": 45.0792},
        "villes": [
            {"ville": "Riyad", "lat": 24.7136, "lon": 46.6753},
            {"ville": "Djeddah", "lat": 21.5433, "lon": 39.1678},
            {"ville": "La Mecque", "lat": 21.4225, "lon": 39.8262},
            {"ville": "Médine", "lat": 24.5247, "lon": 39.5692},
            {"ville": "Dammam", "lat": 26.4207, "lon": 50.0888},
            {"ville": "Taïf", "lat": 21.2703, "lon": 40.4158},
            {"ville": "Tabuk", "lat": 28.3835, "lon": 36.5664},
            {"ville": "Abha", "lat": 18.2164, "lon": 42.5053},
            {"ville": "Jizan", "lat": 16.8894, "lon": 42.5706},
            {"ville": "Najran", "lat": 17.5656, "lon": 44.2289},
        ],
        "langues": ["arabe", "anglais"],
        "noms": {
            "prenoms": ["Abdullah", "Faisal", "Aisha", "Fatimah", "Mohammed", "Noura"],
            "noms": ["Al Saud", "Al Harbi", "Al Qahtani", "Al Otaibi", "Al Shammari"]
        }
    },

    "argentine": {
        "capitale": "Buenos Aires",
        "coordonnees": {"lat": -38.4161, "lon": -63.6167},
        "villes": [
            {"ville": "Buenos Aires", "lat": -34.6118, "lon": -58.3960},
            {"ville": "Córdoba", "lat": -31.4167, "lon": -64.1833},
            {"ville": "Rosario", "lat": -32.9468, "lon": -60.6393},
            {"ville": "Mendoza", "lat": -32.8908, "lon": -68.8272},
            {"ville": "La Plata", "lat": -34.9215, "lon": -57.9546},
            {"ville": "San Miguel de Tucumán", "lat": -26.8083, "lon": -65.2176},
            {"ville": "Mar del Plata", "lat": -38.0000, "lon": -57.5500},
            {"ville": "Salta", "lat": -24.7833, "lon": -65.4167},
            {"ville": "Santa Fe", "lat": -31.6333, "lon": -60.7000},
            {"ville": "San Juan", "lat": -31.5375, "lon": -68.5364},
        ],
        "langues": ["espagnol", "anglais"],
        "noms": {
            "prenoms": ["Juan", "María", "Carlos", "Ana", "Luis", "Lucía"],
            "noms": ["González", "Rodríguez", "Pérez", "Fernández", "Gómez"]
        }
    },

    "arménie": {
        "capitale": "Erevan",
        "coordonnees": {"lat": 40.0691, "lon": 45.0382},
        "villes": [
            {"ville": "Erevan", "lat": 40.1872, "lon": 44.5152},
            {"ville": "Gyumri", "lat": 40.7894, "lon": 43.8475},
            {"ville": "Vanadzor", "lat": 40.8128, "lon": 44.4883},
            {"ville": "Vagharshapat", "lat": 40.1556, "lon": 44.0389},
            {"ville": "Abovyan", "lat": 40.2739, "lon": 44.6256},
            {"ville": "Kapan", "lat": 39.2011, "lon": 46.4150},
            {"ville": "Hrazdan", "lat": 40.5000, "lon": 44.7667},
            {"ville": "Ijevan", "lat": 40.8756, "lon": 45.1492},
            {"ville": "Gavar", "lat": 40.3589, "lon": 45.1267},
            {"ville": "Artashat", "lat": 39.9539, "lon": 44.5506},
        ],
        "langues": ["arménien", "russe"],
        "noms": {
            "prenoms": ["Armen", "Ani", "Hayk", "Mariam", "Tigran", "Lilit"],
            "noms": ["Harutyunyan", "Grigoryan", "Hovhannisyan", "Khachatryan", "Sargsyan"]
        }
    },

    "australie": {
        "capitale": "Canberra",
        "coordonnees": {"lat": -25.2744, "lon": 133.7751},
        "villes": [
            {"ville": "Canberra", "lat": -35.2809, "lon": 149.1300},
            {"ville": "Sydney", "lat": -33.8688, "lon": 151.2093},
            {"ville": "Melbourne", "lat": -37.8136, "lon": 144.9631},
            {"ville": "Brisbane", "lat": -27.4698, "lon": 153.0251},
            {"ville": "Perth", "lat": -31.9505, "lon": 115.8605},
            {"ville": "Adélaïde", "lat": -34.9285, "lon": 138.6007},
            {"ville": "Gold Coast", "lat": -28.0167, "lon": 153.4000},
            {"ville": "Newcastle", "lat": -32.9283, "lon": 151.7817},
            {"ville": "Wollongong", "lat": -34.4331, "lon": 150.8831},
            {"ville": "Hobart", "lat": -42.8821, "lon": 147.3272},
        ],
        "langues": ["anglais"],
        "noms": {
            "prenoms": ["Jack", "Oliver", "Amelia", "Mia", "Lucas", "Emily"],
            "noms": ["Smith", "Williams", "Brown", "Wilson", "Taylor"]
        }
    },

    "autriche": {
        "capitale": "Vienne",
        "coordonnees": {"lat": 47.5162, "lon": 14.5501},
        "villes": [
            {"ville": "Vienne", "lat": 48.2082, "lon": 16.3738},
            {"ville": "Graz", "lat": 47.0707, "lon": 15.4395},
            {"ville": "Linz", "lat": 48.3069, "lon": 14.2858},
            {"ville": "Salzbourg", "lat": 47.8095, "lon": 13.0550},
            {"ville": "Innsbruck", "lat": 47.2692, "lon": 11.4041},
            {"ville": "Klagenfurt", "lat": 46.6249, "lon": 14.3052},
            {"ville": "Villach", "lat": 46.6111, "lon": 13.8558},
            {"ville": "Wels", "lat": 48.1575, "lon": 14.0289},
            {"ville": "Sankt Pölten", "lat": 48.2084, "lon": 15.6261},
            {"ville": "Dornbirn", "lat": 47.4141, "lon": 9.7419},
        ],
        "langues": ["allemand", "anglais"],
        "noms": {
            "prenoms": ["Lukas", "Anna", "Paul", "Laura", "David", "Marie"],
            "noms": ["Gruber", "Huber", "Wagner", "Bauer", "Müller"]
        }
    },

    "azerbaïdjan": {
        "capitale": "Bakou",
        "coordonnees": {"lat": 40.1431, "lon": 47.5769},
        "villes": [
            {"ville": "Bakou", "lat": 40.3777, "lon": 49.8920},
            {"ville": "Ganja", "lat": 40.6828, "lon": 46.3606},
            {"ville": "Sumqayit", "lat": 40.5897, "lon": 49.6686},
            {"ville": "Mingachevir", "lat": 40.7703, "lon": 47.0486},
            {"ville": "Qaraçuxur", "lat": 40.3969, "lon": 49.9736},
            {"ville": "Şirvan", "lat": 39.9373, "lon": 48.9293},
            {"ville": "Nakhitchevan", "lat": 39.2089, "lon": 45.4122},
            {"ville": "Şamaxı", "lat": 40.6314, "lon": 48.6414},
            {"ville": "Lankaran", "lat": 38.7543, "lon": 48.8516},
            {"ville": "Quba", "lat": 41.3597, "lon": 48.5125},
        ],
        "langues": ["azéri", "russe"],
        "noms": {
            "prenoms": ["Ali", "Leyla", "Murad", "Aysel", "Elvin", "Gunel"],
            "noms": ["Aliyev", "Mammadov", "Huseynov", "Ismayilov", "Hasanov"]
        }
    },

    "belgique": {
        "capitale": "Bruxelles",
        "coordonnees": {"lat": 50.8503, "lon": 4.3517},
        "villes": [
            {"ville": "Bruxelles", "lat": 50.8503, "lon": 4.3517},
            {"ville": "Anvers", "lat": 51.2194, "lon": 4.4025},
            {"ville": "Gand", "lat": 51.0500, "lon": 3.7167},
            {"ville": "Charleroi", "lat": 50.4108, "lon": 4.4445},
            {"ville": "Liège", "lat": 50.6333, "lon": 5.5667},
            {"ville": "Bruges", "lat": 51.2093, "lon": 3.2247},
            {"ville": "Namur", "lat": 50.4667, "lon": 4.8667},
            {"ville": "Louvain", "lat": 50.8796, "lon": 4.7009},
            {"ville": "Mons", "lat": 50.4542, "lon": 3.9561},
            {"ville": "Tournai", "lat": 50.6067, "lon": 3.3883},
        ],
        "langues": ["français", "néerlandais", "allemand"],
        "noms": {
            "prenoms": ["Lucas", "Marie", "Louis", "Emma", "Noah", "Julie"],
            "noms": ["Peeters", "Janssens", "Maes", "Jacobs", "Mertens"]
        }
    },

    "bosnie": {
        "capitale": "Sarajevo",
        "coordonnees": {"lat": 43.9159, "lon": 17.6791},
        "villes": [
            {"ville": "Sarajevo", "lat": 43.8564, "lon": 18.4131},
            {"ville": "Banja Luka", "lat": 44.7722, "lon": 17.1914},
            {"ville": "Tuzla", "lat": 44.5384, "lon": 18.6671},
            {"ville": "Zenica", "lat": 44.2014, "lon": 17.9034},
            {"ville": "Mostar", "lat": 43.3433, "lon": 17.8081},
            {"ville": "Bijeljina", "lat": 44.7569, "lon": 19.2161},
            {"ville": "Prijedor", "lat": 44.9794, "lon": 16.7144},
            {"ville": "Brčko", "lat": 44.8667, "lon": 18.8000},
            {"ville": "Doboj", "lat": 44.7333, "lon": 18.0833},
            {"ville": "Zvornik", "lat": 44.3833, "lon": 19.1000},
        ],
        "langues": ["bosnien", "croate", "serbe"],
        "noms": {
            "prenoms": ["Amir", "Jasmin", "Adnan", "Lejla", "Emina", "Dino"],
            "noms": ["Hadžić", "Hodžić", "Dedić", "Alić", "Mehić"]
        }
    },

    "brésil": {
        "capitale": "Brasilia",
        "coordonnees": {"lat": -14.235, "lon": -51.9253},
        "villes": [
            {"ville": "Brasilia", "lat": -15.7942, "lon": -47.8822},
            {"ville": "São Paulo", "lat": -23.5505, "lon": -46.6333},
            {"ville": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
            {"ville": "Salvador", "lat": -12.9714, "lon": -38.5011},
            {"ville": "Fortaleza", "lat": -3.7319, "lon": -38.5267},
            {"ville": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345},
            {"ville": "Manaus", "lat": -3.1190, "lon": -60.0217},
            {"ville": "Curitiba", "lat": -25.4284, "lon": -49.2733},
            {"ville": "Recife", "lat": -8.0476, "lon": -34.8770},
            {"ville": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
        ],
        "langues": ["portugais", "espagnol", "anglais"],
        "noms": {
            "prenoms": ["João", "Maria", "Pedro", "Ana", "Lucas", "Gabriela"],
            "noms": ["Silva", "Santos", "Oliveira", "Souza", "Lima"]
        }
    },

    "bulgarie": {
        "capitale": "Sofia",
        "coordonnees": {"lat": 42.7339, "lon": 25.4858},
        "villes": [
            {"ville": "Sofia", "lat": 42.6977, "lon": 23.3219},
            {"ville": "Plovdiv", "lat": 42.1354, "lon": 24.7453},
            {"ville": "Varna", "lat": 43.2141, "lon": 27.9147},
            {"ville": "Bourgas", "lat": 42.4969, "lon": 27.4681},
            {"ville": "Roussé", "lat": 43.8564, "lon": 25.9709},
            {"ville": "Stara Zagora", "lat": 42.4328, "lon": 25.6419},
            {"ville": "Pleven", "lat": 43.4167, "lon": 24.6167},
            {"ville": "Sliven", "lat": 42.6856, "lon": 26.3292},
            {"ville": "Dobritch", "lat": 43.5667, "lon": 27.8333},
            {"ville": "Choumen", "lat": 43.2706, "lon": 26.9228},
        ],
        "langues": ["bulgare", "anglais"],
        "noms": {
            "prenoms": ["Georgi", "Ivan", "Maria", "Elena", "Dimitar", "Yana"],
            "noms": ["Ivanov", "Georgiev", "Dimitrov", "Petrov", "Nikolov"]
        }
    },

    "canada": {
        "capitale": "Ottawa",
        "coordonnees": {"lat": 56.1304, "lon": -106.3468},
        "villes": [
            {"ville": "Ottawa", "lat": 45.4215, "lon": -75.6972},
            {"ville": "Toronto", "lat": 43.6532, "lon": -79.3832},
            {"ville": "Montréal", "lat": 45.5017, "lon": -73.5673},
            {"ville": "Vancouver", "lat": 49.2827, "lon": -123.1207},
            {"ville": "Calgary", "lat": 51.0447, "lon": -114.0719},
            {"ville": "Edmonton", "lat": 53.5461, "lon": -113.4938},
            {"ville": "Québec", "lat": 46.8139, "lon": -71.2080},
            {"ville": "Winnipeg", "lat": 49.8951, "lon": -97.1384},
            {"ville": "Hamilton", "lat": 43.2557, "lon": -79.8711},
            {"ville": "Kitchener", "lat": 43.4516, "lon": -80.4925},
        ],
        "langues": ["anglais", "français"],
        "noms": {
            "prenoms": ["Liam", "Emma", "Noah", "Olivia", "William", "Charlotte"],
            "noms": ["Smith", "Brown", "Tremblay", "Martin", "Roy"]
        }
    },

    "chine": {
        "capitale": "Pékin",
        "coordonnees": {"lat": 35.8617, "lon": 104.1954},
        "villes": [
            {"ville": "Pékin", "lat": 39.9042, "lon": 116.4074},
            {"ville": "Shanghai", "lat": 31.2304, "lon": 121.4737},
            {"ville": "Guangzhou", "lat": 23.1291, "lon": 113.2644},
            {"ville": "Shenzhen", "lat": 22.3193, "lon": 114.1694},
            {"ville": "Tianjin", "lat": 39.3434, "lon": 117.3616},
            {"ville": "Chongqing", "lat": 29.4316, "lon": 106.9123},
            {"ville": "Chengdu", "lat": 30.5728, "lon": 104.0668},
            {"ville": "Nanjing", "lat": 32.0603, "lon": 118.7969},
            {"ville": "Wuhan", "lat": 30.5928, "lon": 114.3055},
            {"ville": "Xi'an", "lat": 34.3416, "lon": 108.9398},
        ],
        "langues": ["chinois", "anglais", "cantonais", "ouïghour"],
        "noms": {
            "prenoms": ["Wei", "Li", "Jing", "Hua", "Fang", "Wang"],
            "noms": ["Wang", "Li", "Zhang", "Liu", "Chen"]
        }
    },

    "colombie": {
        "capitale": "Bogota",
        "coordonnees": {"lat": 4.5709, "lon": -74.2973},
        "villes": [
            {"ville": "Bogota", "lat": 4.7110, "lon": -74.0721},
            {"ville": "Medellín", "lat": 6.2442, "lon": -75.5812},
            {"ville": "Cali", "lat": 3.4516, "lon": -76.5320},
            {"ville": "Barranquilla", "lat": 10.9685, "lon": -74.7813},
            {"ville": "Cartagena", "lat": 10.3932, "lon": -75.4792},
            {"ville": "Cúcuta", "lat": 7.8891, "lon": -72.4967},
            {"ville": "Bucaramanga", "lat": 7.1253, "lon": -73.1290},
            {"ville": "Pereira", "lat": 4.8143, "lon": -75.6946},
            {"ville": "Santa Marta", "lat": 11.2404, "lon": -74.2110},
            {"ville": "Ibagué", "lat": 4.4389, "lon": -75.2322},
        ],
        "langues": ["espagnol", "anglais"],
        "noms": {
            "prenoms": ["Juan", "Andrés", "María", "Camila", "Carlos", "Valentina"],
            "noms": ["García", "Rodríguez", "Martínez", "López", "González"]
        }
    },

    "corée du sud": {
        "capitale": "Séoul",
        "coordonnees": {"lat": 35.9078, "lon": 127.7669},
        "villes": [
            {"ville": "Séoul", "lat": 37.5665, "lon": 126.9780},
            {"ville": "Busan", "lat": 35.1796, "lon": 129.0756},
            {"ville": "Incheon", "lat": 37.4563, "lon": 126.7052},
            {"ville": "Daegu", "lat": 35.8714, "lon": 128.6014},
            {"ville": "Daejeon", "lat": 36.3504, "lon": 127.3845},
            {"ville": "Gwangju", "lat": 35.1595, "lon": 126.8526},
            {"ville": "Suwon", "lat": 37.2636, "lon": 127.0286},
            {"ville": "Ulsan", "lat": 35.5384, "lon": 129.3114},
            {"ville": "Changwon", "lat": 35.2278, "lon": 128.6817},
            {"ville": "Seongnam", "lat": 37.4449, "lon": 127.1389},
        ],
        "langues": ["coréen", "anglais"],
        "noms": {
            "prenoms": ["Min-jun", "Seo-yeon", "Ji-ho", "Soo-bin", "Jae-won", "Ha-yeon"],
            "noms": ["Kim", "Lee", "Park", "Jeong", "Choi"]
        }
    },

    "croatie": {
        "capitale": "Zagreb",
        "coordonnees": {"lat": 45.1, "lon": 15.2},
        "villes": [
            {"ville": "Zagreb", "lat": 45.8150, "lon": 15.9819},
            {"ville": "Split", "lat": 43.5081, "lon": 16.4402},
            {"ville": "Rijeka", "lat": 45.3271, "lon": 14.4422},
            {"ville": "Osijek", "lat": 45.5550, "lon": 18.6955},
            {"ville": "Zadar", "lat": 44.1194, "lon": 15.2314},
            {"ville": "Slavonski Brod", "lat": 45.1603, "lon": 18.0156},
            {"ville": "Pula", "lat": 44.8666, "lon": 13.8496},
            {"ville": "Karlovac", "lat": 45.4929, "lon": 15.5553},
            {"ville": "Varaždin", "lat": 46.3057, "lon": 16.3366},
            {"ville": "Šibenik", "lat": 43.7350, "lon": 15.8900},
        ],
        "langues": ["croate"],
        "noms": {
            "prenoms": ["Ivan", "Ana", "Marko", "Marija", "Petar", "Ivana"],
            "noms": ["Horvat", "Kovačević", "Babić", "Marić", "Jurić"]
        }
    },

    "danemark": {
        "capitale": "Copenhague",
        "coordonnees": {"lat": 56.2639, "lon": 9.5018},
        "villes": [
            {"ville": "Copenhague", "lat": 55.6761, "lon": 12.5683},
            {"ville": "Aarhus", "lat": 56.1629, "lon": 10.2039},
            {"ville": "Odense", "lat": 55.4038, "lon": 10.4024},
            {"ville": "Aalborg", "lat": 57.0488, "lon": 9.9217},
            {"ville": "Esbjerg", "lat": 55.4660, "lon": 8.4500},
            {"ville": "Randers", "lat": 56.4607, "lon": 10.0364},
            {"ville": "Kolding", "lat": 55.4904, "lon": 9.4721},
            {"ville": "Horsens", "lat": 55.8607, "lon": 9.8500},
            {"ville": "Vejle", "lat": 55.7094, "lon": 9.5347},
            {"ville": "Roskilde", "lat": 55.6415, "lon": 12.0808},
        ],
        "langues": ["danois", "anglais"],
        "noms": {
            "prenoms": ["Lars", "Jens", "Anne", "Mette", "Søren", "Maria"],
            "noms": ["Jensen", "Nielsen", "Hansen", "Pedersen", "Andersen"]
        }
    },

    "egypte": {
        "capitale": "Le Caire",
        "coordonnees": {"lat": 26.8206, "lon": 30.8025},
        "villes": [
            {"ville": "Le Caire", "lat": 30.0444, "lon": 31.2357},
            {"ville": "Alexandrie", "lat": 31.2001, "lon": 29.9187},
            {"ville": "Gizeh", "lat": 30.0131, "lon": 31.2089},
            {"ville": "Shubra El Kheima", "lat": 30.1286, "lon": 31.2422},
            {"ville": "Port-Saïd", "lat": 31.2667, "lon": 32.3000},
            {"ville": "Suez", "lat": 29.9668, "lon": 32.5498},
            {"ville": "Louxor", "lat": 25.6872, "lon": 32.6396},
            {"ville": "Mansourah", "lat": 31.0422, "lon": 31.3800},
            {"ville": "El-Mahalla El-Kubra", "lat": 30.9697, "lon": 31.1642},
            {"ville": "Assiout", "lat": 27.1828, "lon": 31.1828},
        ],
        "langues": ["arabe", "anglais", "français"],
        "noms": {
            "prenoms": ["Ahmed", "Mohamed", "Fatma", "Mona", "Omar", "Sara"],
            "noms": ["El-Sayed", "Hassan", "Mahmoud", "Ali", "Youssef"]
        }
    },

    "espagne": {
        "capitale": "Madrid",
        "coordonnees": {"lat": 40.4637, "lon": -3.7492},
        "villes": [
            {"ville": "Madrid", "lat": 40.4168, "lon": -3.7038},
            {"ville": "Barcelone", "lat": 41.3851, "lon": 2.1734},
            {"ville": "Valence", "lat": 39.4699, "lon": -0.3763},
            {"ville": "Séville", "lat": 37.3891, "lon": -5.9845},
            {"ville": "Saragosse", "lat": 41.6488, "lon": -0.8891},
            {"ville": "Malaga", "lat": 36.7213, "lon": -4.4217},
            {"ville": "Murcie", "lat": 37.9922, "lon": -1.1307},
            {"ville": "Palma", "lat": 39.5696, "lon": 2.6502},
            {"ville": "Las Palmas", "lat": 28.1235, "lon": -15.4366},
            {"ville": "Bilbao", "lat": 43.2627, "lon": -2.9253},
        ],
        "langues": ["espagnol", "catalan", "anglais", "français", "galicien", "basque"],
        "noms": {
            "prenoms": ["Juan", "Carlos", "Maria", "Isabel", "Antonio", "Lucia"],
            "noms": ["García", "Martínez", "López", "Sánchez", "Fernández"]
        }
    },

    "estonie": {
        "capitale": "Tallinn",
        "coordonnees": {"lat": 58.5953, "lon": 25.0136},
        "villes": [
            {"ville": "Tallinn", "lat": 59.4370, "lon": 24.7536},
            {"ville": "Tartu", "lat": 58.3776, "lon": 26.7290},
            {"ville": "Narva", "lat": 59.3770, "lon": 28.1900},
            {"ville": "Pärnu", "lat": 58.3859, "lon": 24.4966},
            {"ville": "Kohtla-Järve", "lat": 59.3986, "lon": 27.2733},
            {"ville": "Viljandi", "lat": 58.3639, "lon": 25.5900},
            {"ville": "Rakvere", "lat": 59.3464, "lon": 26.3558},
            {"ville": "Maardu", "lat": 59.4761, "lon": 25.0250},
            {"ville": "Kuressaare", "lat": 58.2529, "lon": 22.4851},
            {"ville": "Sillamäe", "lat": 59.3997, "lon": 27.7547},
        ],
        "langues": ["estonien", "russe"],
        "noms": {
            "prenoms": ["Kristjan", "Liis", "Jaan", "Mari", "Tanel", "Kadri"],
            "noms": ["Tamm", "Saar", "Kask", "Oja", "Mets"]
        }
    },

    "finlande": {
        "capitale": "Helsinki",
        "coordonnees": {"lat": 61.9241, "lon": 25.7482},
        "villes": [
            {"ville": "Helsinki", "lat": 60.1699, "lon": 24.9384},
            {"ville": "Espoo", "lat": 60.2055, "lon": 24.6559},
            {"ville": "Tampere", "lat": 61.4978, "lon": 23.7610},
            {"ville": "Vantaa", "lat": 60.2934, "lon": 25.0378},
            {"ville": "Oulu", "lat": 65.0121, "lon": 25.4651},
            {"ville": "Turku", "lat": 60.4518, "lon": 22.2666},
            {"ville": "Jyväskylä", "lat": 62.2415, "lon": 25.7209},
            {"ville": "Lahti", "lat": 60.9827, "lon": 25.6612},
            {"ville": "Kuopio", "lat": 62.8924, "lon": 27.6768},
            {"ville": "Pori", "lat": 61.4851, "lon": 21.7974},
        ],
        "langues": ["finnois", "suédois", "anglais"],
        "noms": {
            "prenoms": ["Mikko", "Juhani", "Anna", "Maria", "Juha", "Sanna"],
            "noms": ["Korhonen", "Virtanen", "Mäkinen", "Nieminen", "Mäkelä"]
        }
    },

    "france": {
        "capitale": "France",
        "coordonnees": {"lat": 46.2276, "lon": 2.2137},
        "villes": [
            {"ville": "Paris", "lat": 48.8566, "lon": 2.3522},
            {"ville": "Marseille", "lat": 43.2965, "lon": 5.3698},
            {"ville": "Lyon", "lat": 45.764, "lon": 4.8357},
            {"ville": "Toulouse", "lat": 43.6047, "lon": 1.4442},
            {"ville": "Nice", "lat": 43.7102, "lon": 7.262},
            {"ville": "Nantes", "lat": 47.2184, "lon": -1.5536},
            {"ville": "Strasbourg", "lat": 48.5734, "lon": 7.7521},
            {"ville": "Montpellier", "lat": 43.6108, "lon": 3.8767},
            {"ville": "Bordeaux", "lat": 44.8378, "lon": -0.5792},
            {"ville": "Lille", "lat": 50.6292, "lon": 3.0573},
        ],
        "langues": ["français", "anglais", "allemand", "espagnol", "arabe"],
        "noms": {
            "prenoms": ["Jean", "Pierre", "Marie", "Claire", "Sophie", "Luc", "Paul", "Julien"],
            "noms": ["Dupont", "Martin", "Bernard", "Petit", "Durand", "Moreau", "Laurent"]
        }
    },

    "grèce": {
        "capitale": "Athènes",
        "coordonnees": {"lat": 39.0742, "lon": 21.8243},
        "villes": [
            {"ville": "Athènes", "lat": 37.9838, "lon": 23.7275},
            {"ville": "Thessalonique", "lat": 40.6401, "lon": 22.9444},
            {"ville": "Patras", "lat": 38.2466, "lon": 21.7346},
            {"ville": "Piraeus", "lat": 37.9485, "lon": 23.6425},
            {"ville": "Larissa", "lat": 39.6390, "lon": 22.4191},
            {"ville": "Héraklion", "lat": 35.3387, "lon": 25.1442},
            {"ville": "Peristéri", "lat": 38.0154, "lon": 23.6918},
            {"ville": "Kallithea", "lat": 37.9550, "lon": 23.7020},
            {"ville": "Acharnes", "lat": 38.0833, "lon": 23.7333},
            {"ville": "Kalamaria", "lat": 40.5833, "lon": 22.9500},
        ],
        "langues": ["grec", "anglais"],
        "noms": {
            "prenoms": ["Giorgos", "Nikos", "Maria", "Eleni", "Kostas", "Ioanna"],
            "noms": ["Papadopoulos", "Nikolaidis", "Pappas", "Georgiou", "Vasileiou"]
        }
    },

    "géorgie": {
        "capitale": "Tbilissi",
        "coordonnees": {"lat": 42.3154, "lon": 43.3569},
        "villes": [
            {"ville": "Tbilissi", "lat": 41.7151, "lon": 44.8271},
            {"ville": "Koutaïssi", "lat": 42.2700, "lon": 42.7000},
            {"ville": "Batumi", "lat": 41.6168, "lon": 41.6367},
            {"ville": "Roustavi", "lat": 41.5475, "lon": 45.0156},
            {"ville": "Zougdidi", "lat": 42.5083, "lon": 41.8667},
            {"ville": "Gori", "lat": 41.9814, "lon": 44.1094},
            {"ville": "Poti", "lat": 42.1500, "lon": 41.6667},
            {"ville": "Khachouri", "lat": 41.9167, "lon": 43.4833},
            {"ville": "Samtredia", "lat": 42.1667, "lon": 42.3333},
            {"ville": "Sachkhere", "lat": 42.3333, "lon": 43.4000},
        ],
        "langues": ["géorgien", "russe"],
        "noms": {
            "prenoms": ["Giorgi", "Nino", "Luka", "Ana", "Irakli", "Mariam"],
            "noms": ["Beridze", "Kapanadze", "Giorgadze", "Gogoladze", "Tsiklauri"]
        }
    },

    "hongrie": {
        "capitale": "Budapest",
        "coordonnees": {"lat": 47.1625, "lon": 19.5033},
        "villes": [
            {"ville": "Budapest", "lat": 47.4979, "lon": 19.0402},
            {"ville": "Debrecen", "lat": 47.5299, "lon": 21.6394},
            {"ville": "Szeged", "lat": 46.2530, "lon": 20.1414},
            {"ville": "Miskolc", "lat": 48.1034, "lon": 20.7784},
            {"ville": "Pécs", "lat": 46.0755, "lon": 18.2282},
            {"ville": "Győr", "lat": 47.6875, "lon": 17.6504},
            {"ville": "Nyíregyháza", "lat": 47.9495, "lon": 21.7244},
            {"ville": "Kecskemét", "lat": 46.9061, "lon": 19.6897},
            {"ville": "Székesfehérvár", "lat": 47.1860, "lon": 18.4228},
            {"ville": "Szombathely", "lat": 47.2306, "lon": 16.6219},
        ],
        "langues": ["hongrois", "anglais"],
        "noms": {
            "prenoms": ["László", "Gábor", "Eszter", "Katalin", "Zoltán", "Judit"],
            "noms": ["Nagy", "Kovács", "Tóth", "Szabó", "Horváth"]
        }
    },

    "inde": {
        "capitale": "New Delhi",
        "coordonnees": {"lat": 20.5937, "lon": 78.9629},
        "villes": [
            {"ville": "New Delhi", "lat": 28.6139, "lon": 77.2090},
            {"ville": "Mumbai", "lat": 19.0760, "lon": 72.8777},
            {"ville": "Bangalore", "lat": 12.9716, "lon": 77.5946},
            {"ville": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
            {"ville": "Chennai", "lat": 13.0827, "lon": 80.2707},
            {"ville": "Kolkata", "lat": 22.5726, "lon": 88.3639},
            {"ville": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
            {"ville": "Pune", "lat": 18.5204, "lon": 73.8567},
            {"ville": "Jaipur", "lat": 26.9124, "lon": 75.7873},
            {"ville": "Surat", "lat": 21.1702, "lon": 72.8311},
        ],
        "langues": ["hindi", "anglais", "bengali", "tamoul", "télougou", "marathi", "gujarati", "kannada", "malayalam"],
        "noms": {
            "prenoms": ["Amit", "Priya", "Raj", "Anjali", "Vijay", "Sunita"],
            "noms": ["Singh", "Kumar", "Sharma", "Patel", "Gupta"]
        }
    },

    "indonésie": {
        "capitale": "Jakarta",
        "coordonnees": {"lat": -0.7893, "lon": 113.9213},
        "villes": [
            {"ville": "Jakarta", "lat": -6.2088, "lon": 106.8456},
            {"ville": "Surabaya", "lat": -7.2575, "lon": 112.7521},
            {"ville": "Bandung", "lat": -6.9175, "lon": 107.6191},
            {"ville": "Medan", "lat": 3.5952, "lon": 98.6722},
            {"ville": "Semarang", "lat": -6.9932, "lon": 110.4203},
            {"ville": "Palembang", "lat": -2.9761, "lon": 104.7754},
            {"ville": "Makassar", "lat": -5.1477, "lon": 119.4327},
            {"ville": "Tangerang", "lat": -6.1783, "lon": 106.6319},
            {"ville": "Depok", "lat": -6.3900, "lon": 106.8222},
            {"ville": "Bekasi", "lat": -6.2349, "lon": 106.9896},
        ],
        "langues": ["indonésien", "javanais", "anglais", "malais"],
        "noms": {
            "prenoms": ["Agus", "Dewi", "Budi", "Siti", "Andi", "Ratna"],
            "noms": ["Wijaya", "Sutanto", "Putra", "Saputra", "Gunawan"]
        }
    },

    "iran": {
        "capitale": "Téhéran",
        "coordonnees": {"lat": 32.4279, "lon": 53.688},
        "villes": [
            {"ville": "Téhéran", "lat": 35.6892, "lon": 51.3890},
            {"ville": "Mashhad", "lat": 36.2970, "lon": 59.6062},
            {"ville": "Ispahan", "lat": 32.6546, "lon": 51.6680},
            {"ville": "Tabriz", "lat": 38.0962, "lon": 46.2738},
            {"ville": "Chiraz", "lat": 29.5916, "lon": 52.5836},
            {"ville": "Kermanchah", "lat": 34.3277, "lon": 47.0778},
            {"ville": "Urmia", "lat": 37.5527, "lon": 45.0761},
            {"ville": "Qom", "lat": 34.6416, "lon": 50.8746},
            {"ville": "Kerman", "lat": 30.2839, "lon": 57.0834},
            {"ville": "Yazd", "lat": 31.8974, "lon": 54.3569},
        ],
        "langues": ["persan", "anglais", "azéri", "kurde"],
        "noms": {
            "prenoms": ["Mohammad", "Ali", "Fatemeh", "Zahra", "Hossein", "Sara"],
            "noms": ["Mohammadi", "Hosseini", "Ahmadi", "Rezaei", "Karimi"]
        }
    },

    "irlande": {
        "capitale": "Dublin",
        "coordonnees": {"lat": 53.4129, "lon": -8.2439},
        "villes": [
            {"ville": "Dublin", "lat": 53.3498, "lon": -6.2603},
            {"ville": "Cork", "lat": 51.8969, "lon": -8.4863},
            {"ville": "Limerick", "lat": 52.6638, "lon": -8.6267},
            {"ville": "Galway", "lat": 53.2707, "lon": -9.0568},
            {"ville": "Waterford", "lat": 52.2593, "lon": -7.1101},
            {"ville": "Drogheda", "lat": 53.7179, "lon": -6.3561},
            {"ville": "Dundalk", "lat": 54.0060, "lon": -6.4033},
            {"ville": "Swords", "lat": 53.4597, "lon": -6.2180},
            {"ville": "Bray", "lat": 53.2027, "lon": -6.1093},
            {"ville": "Navan", "lat": 53.6528, "lon": -6.6814},
        ],
        "langues": ["anglais", "irlandais"],
        "noms": {
            "prenoms": ["Seán", "Patrick", "Aoife", "Ciara", "Liam", "Niamh"],
            "noms": ["Murphy", "Kelly", "O'Sullivan", "Walsh", "Byrne"]
        }
    },

    "islande": {
        "capitale": "Reykjavik",
        "coordonnees": {"lat": 64.9631, "lon": -19.0208},
        "villes": [
            {"ville": "Reykjavik", "lat": 64.1466, "lon": -21.9426},
            {"ville": "Kópavogur", "lat": 64.1100, "lon": -21.9000},
            {"ville": "Hafnarfjörður", "lat": 64.0667, "lon": -21.9500},
            {"ville": "Reykjanesbær", "lat": 63.9833, "lon": -22.5667},
            {"ville": "Akureyri", "lat": 65.6833, "lon": -18.1000},
            {"ville": "Garðabær", "lat": 64.0833, "lon": -21.9833},
            {"ville": "Mosfellsbær", "lat": 64.1667, "lon": -21.7000},
            {"ville": "Árborg", "lat": 63.9333, "lon": -21.0000},
            {"ville": "Akranes", "lat": 64.3167, "lon": -22.1000},
            {"ville": "Fjallabyggð", "lat": 66.1500, "lon": -18.9167},
        ],
        "langues": ["islandais", "anglais"],
        "noms": {
            "prenoms": ["Jón", "Guðrún", "Sigurður", "Anna", "Björn", "Kristín"],
            "noms": ["Jónsson", "Guðmundsdóttir", "Sigurðardóttir", "Einarsson", "Ólafsdóttir"]
        }
    },

    "israël": {
        "capitale": "Jérusalem",
        "coordonnees": {"lat": 31.0461, "lon": 34.8516},
        "villes": [
            {"ville": "Jérusalem", "lat": 31.7683, "lon": 35.2137},
            {"ville": "Tel Aviv", "lat": 32.0853, "lon": 34.7818},
            {"ville": "Haïfa", "lat": 32.7940, "lon": 34.9896},
            {"ville": "Rishon LeZion", "lat": 31.9686, "lon": 34.7983},
            {"ville": "Petah Tikva", "lat": 32.0871, "lon": 34.8875},
            {"ville": "Ashdod", "lat": 31.8044, "lon": 34.6500},
            {"ville": "Netanya", "lat": 32.3328, "lon": 34.8600},
            {"ville": "Beer Sheva", "lat": 31.2518, "lon": 34.7913},
            {"ville": "Holon", "lat": 32.0167, "lon": 34.7833},
            {"ville": "Bnei Brak", "lat": 32.0833, "lon": 34.8333},
        ],
        "langues": ["hébreu", "arabe", "anglais", "russe"],
        "noms": {
            "prenoms": ["David", "Yael", "Daniel", "Noa", "Moshe", "Tal"],
            "noms": ["Cohen", "Levi", "Mizrahi", "Peretz", "Biton"]
        }
    },

    "italie": {
        "capitale": "Italie",
        "coordonnees": {"lat": 41.8719, "lon": 12.5674},
        "villes": [
            {"ville": "Rome", "lat": 41.9028, "lon": 12.4964},
            {"ville": "Milan", "lat": 45.4642, "lon": 9.19},
            {"ville": "Naples", "lat": 40.8518, "lon": 14.2681},
            {"ville": "Turin", "lat": 45.0703, "lon": 7.6869},
            {"ville": "Palerme", "lat": 38.1157, "lon": 13.3615},
            {"ville": "Gênes", "lat": 44.4056, "lon": 8.9463},
            {"ville": "Bologne", "lat": 44.4949, "lon": 11.3426},
            {"ville": "Florence", "lat": 43.7696, "lon": 11.2558},
            {"ville": "Bari", "lat": 41.1171, "lon": 16.8719},
            {"ville": "Catane", "lat": 37.5079, "lon": 15.0830},
        ],
        "langues": ["italien", "anglais", "français"],
        "noms": {
            "prenoms": ["Giuseppe", "Marco", "Francesca", "Giulia", "Luca", "Alessandro"],
            "noms": ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi"]
        }
    },

    "japon": {
        "capitale": "Tokyo",
        "coordonnees": {"lat": 36.2048, "lon": 138.2529},
        "villes": [
            {"ville": "Tokyo", "lat": 35.6762, "lon": 139.6503},
            {"ville": "Yokohama", "lat": 35.4437, "lon": 139.6380},
            {"ville": "Osaka", "lat": 34.6937, "lon": 135.5023},
            {"ville": "Nagoya", "lat": 35.1815, "lon": 136.9066},
            {"ville": "Sapporo", "lat": 43.0618, "lon": 141.3545},
            {"ville": "Kobe", "lat": 34.6901, "lon": 135.1955},
            {"ville": "Kyoto", "lat": 35.0116, "lon": 135.7681},
            {"ville": "Fukuoka", "lat": 33.5902, "lon": 130.4017},
            {"ville": "Kawasaki", "lat": 35.5206, "lon": 139.7172},
            {"ville": "Saitama", "lat": 35.8616, "lon": 139.6455},
        ],
        "langues": ["japonais", "anglais"],
        "noms": {
            "prenoms": ["Haruto", "Yuki", "Sakura", "Hana", "Ren", "Aoi"],
            "noms": ["Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe"]
        }
    },

    "kazakhstan": {
        "capitale": "Nour-Soultan",
        "coordonnees": {"lat": 48.0196, "lon": 66.9237},
        "villes": [
            {"ville": "Nour-Soultan", "lat": 51.1605, "lon": 71.4704},
            {"ville": "Almaty", "lat": 43.2220, "lon": 76.8512},
            {"ville": "Chymkent", "lat": 42.3000, "lon": 69.6000},
            {"ville": "Aktobe", "lat": 50.2833, "lon": 57.1667},
            {"ville": "Karaganda", "lat": 49.8333, "lon": 73.1667},
            {"ville": "Taraz", "lat": 42.9000, "lon": 71.3667},
            {"ville": "Pavlodar", "lat": 52.3000, "lon": 76.9500},
            {"ville": "Oskemen", "lat": 49.9500, "lon": 82.6167},
            {"ville": "Semey", "lat": 50.4000, "lon": 80.2500},
            {"ville": "Atyrau", "lat": 47.1167, "lon": 51.8833},
        ],
        "langues": ["kazakh", "russe", "anglais"],
        "noms": {
            "prenoms": ["Ayan", "Yerlan", "Aruzhan", "Dana", "Alikhan", "Aigerim"],
            "noms": ["Nursultan", "Tuleu", "Kenzhebek", "Nurmagambetov", "Abdikalykov"]
        }
    },

    "kirghizistan": {
        "capitale": "Bichkek",
        "coordonnees": {"lat": 41.2044, "lon": 74.7661},
        "villes": [
            {"ville": "Bichkek", "lat": 42.8746, "lon": 74.5698},
            {"ville": "Och", "lat": 40.5140, "lon": 72.8160},
            {"ville": "Jalal-Abad", "lat": 40.9333, "lon": 72.9833},
            {"ville": "Tokmok", "lat": 42.8333, "lon": 75.2833},
            {"ville": "Kara-Balta", "lat": 42.8167, "lon": 73.8500},
            {"ville": "Uzgen", "lat": 40.7667, "lon": 73.3000},
            {"ville": "Balykchy", "lat": 42.4667, "lon": 76.1833},
            {"ville": "Naryn", "lat": 41.4333, "lon": 75.9833},
            {"ville": "Karakol", "lat": 42.4833, "lon": 78.4000},
            {"ville": "Talas", "lat": 42.5167, "lon": 72.2333},
        ],
        "langues": ["kirghiz", "russe"],
        "noms": {
            "prenoms": ["Azamat", "Aigul", "Ermek", "Gulzat", "Nurzhan", "Altynai"],
            "noms": ["Bekbolotov", "Sadykov", "Abdyldaev", "Sydykov", "Mamatov"]
        }
    },

    "lettonie": {
        "capitale": "Riga",
        "coordonnees": {"lat": 56.8796, "lon": 24.6032},
        "villes": [
            {"ville": "Riga", "lat": 56.9496, "lon": 24.1052},
            {"ville": "Daugavpils", "lat": 55.8750, "lon": 26.5361},
            {"ville": "Liepāja", "lat": 56.5047, "lon": 21.0108},
            {"ville": "Jelgava", "lat": 56.6484, "lon": 23.7138},
            {"ville": "Jūrmala", "lat": 56.9680, "lon": 23.7703},
            {"ville": "Ventspils", "lat": 57.3937, "lon": 21.5647},
            {"ville": "Rēzekne", "lat": 56.5099, "lon": 27.3331},
            {"ville": "Valmiera", "lat": 57.5411, "lon": 25.4275},
            {"ville": "Jēkabpils", "lat": 56.4990, "lon": 25.8575},
            {"ville": "Ogre", "lat": 56.8167, "lon": 24.6000},
        ],
        "langues": ["letton", "russe"],
        "noms": {
            "prenoms": ["Jānis", "Anna", "Kristīne", "Mārtiņš", "Inese", "Artūrs"],
            "noms": ["Bērziņš", "Kalniņš", "Ozoliņš", "Jansons", "Vasiļjevs"]
        }
    },

    "lituanie": {
        "capitale": "Vilnius",
        "coordonnees": {"lat": 55.1694, "lon": 23.8813},
        "villes": [
            {"ville": "Vilnius", "lat": 54.6872, "lon": 25.2797},
            {"ville": "Kaunas", "lat": 54.8985, "lon": 23.9036},
            {"ville": "Klaipėda", "lat": 55.7033, "lon": 21.1443},
            {"ville": "Šiauliai", "lat": 55.9333, "lon": 23.3167},
            {"ville": "Panevėžys", "lat": 55.7333, "lon": 24.3500},
            {"ville": "Alytus", "lat": 54.4000, "lon": 24.0500},
            {"ville": "Marijampolė", "lat": 54.5667, "lon": 23.3500},
            {"ville": "Mažeikiai", "lat": 56.3167, "lon": 22.3333},
            {"ville": "Jonava", "lat": 55.0833, "lon": 24.2833},
            {"ville": "Utena", "lat": 55.5000, "lon": 25.6000},
        ],
        "langues": ["lituanien", "russe"],
        "noms": {
            "prenoms": ["Jonas", "Dalia", "Mantas", "Ieva", "Vytautas", "Eglė"],
            "noms": ["Kazlauskas", "Jankauskas", "Petrauskas", "Balčiūnas", "Stankevičius"]
        }
    },

    "malaisie": {
        "capitale": "Kuala Lumpur",
        "coordonnees": {"lat": 4.2105, "lon": 108.9758},
        "villes": [
            {"ville": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869},
            {"ville": "George Town", "lat": 5.4164, "lon": 100.3327},
            {"ville": "Ipoh", "lat": 4.5979, "lon": 101.0901},
            {"ville": "Shah Alam", "lat": 3.0738, "lon": 101.5183},
            {"ville": "Johor Bahru", "lat": 1.4927, "lon": 103.7414},
            {"ville": "Malacca", "lat": 2.1896, "lon": 102.2501},
            {"ville": "Alor Setar", "lat": 6.1184, "lon": 100.3688},
            {"ville": "Miri", "lat": 4.3995, "lon": 113.9915},
            {"ville": "Kuching", "lat": 1.5497, "lon": 110.3372},
            {"ville": "Kota Kinabalu", "lat": 5.9804, "lon": 116.0735},
        ],
        "langues": ["malais", "anglais", "tamoul", "mandarin"],
        "noms": {
            "prenoms": ["Ahmad", "Nur", "Muhammad", "Siti", "Azlan", "Aisyah"],
            "noms": ["Ismail", "Abdullah", "Othman", "Yusof", "Rahman"]
        }
    },

    "maroc": {
        "capitale": "Rabat",
        "coordonnees": {"lat": 31.7917, "lon": -7.0926},
        "villes": [
            {"ville": "Rabat", "lat": 34.0209, "lon": -6.8416},
            {"ville": "Casablanca", "lat": 33.5731, "lon": -7.5898},
            {"ville": "Fès", "lat": 34.0181, "lon": -5.0078},
            {"ville": "Marrakech", "lat": 31.6295, "lon": -7.9811},
            {"ville": "Agadir", "lat": 30.4278, "lon": -9.5981},
            {"ville": "Tanger", "lat": 35.7595, "lon": -5.8340},
            {"ville": "Meknès", "lat": 33.8935, "lon": -5.5473},
            {"ville": "Oujda", "lat": 34.6814, "lon": -1.9086},
            {"ville": "Kénitra", "lat": 34.2610, "lon": -6.5802},
            {"ville": "Tétouan", "lat": 35.5711, "lon": -5.3694},
        ],
        "langues": ["arabe", "berbère", "français", "espagnol"],
        "noms": {
            "prenoms": ["Mohammed", "Fatima", "Youssef", "Khadija", "Omar", "Amina"],
            "noms": ["El Amrani", "Bennani", "Fassi", "Amrani", "Ouazzani"]
        }
    },

    "mexique": {
        "capitale": "Mexico",
        "coordonnees": {"lat": 23.6345, "lon": -102.5528},
        "villes": [
            {"ville": "Mexico", "lat": 19.4326, "lon": -99.1332},
            {"ville": "Guadalajara", "lat": 20.6597, "lon": -103.3496},
            {"ville": "Monterrey", "lat": 25.6866, "lon": -100.3161},
            {"ville": "Puebla", "lat": 19.0413, "lon": -98.2062},
            {"ville": "Tijuana", "lat": 32.5149, "lon": -117.0382},
            {"ville": "Ciudad Juárez", "lat": 31.6904, "lon": -106.4225},
            {"ville": "León", "lat": 21.1250, "lon": -101.6860},
            {"ville": "Zapopan", "lat": 20.7236, "lon": -103.3848},
            {"ville": "Mérida", "lat": 20.9674, "lon": -89.5926},
            {"ville": "Aguascalientes", "lat": 21.8853, "lon": -102.2916},
        ],
        "langues": ["espagnol", "anglais"],
        "noms": {
            "prenoms": ["José", "Juan", "María", "Guadalupe", "Luis", "Carmen"],
            "noms": ["Hernández", "García", "Martínez", "López", "González"]
        }
    },

    "monténégro": {
        "capitale": "Podgorica",
        "coordonnees": {"lat": 42.7087, "lon": 19.3744},
        "villes": [
            {"ville": "Podgorica", "lat": 42.4304, "lon": 19.2594},
            {"ville": "Nikšić", "lat": 42.7787, "lon": 18.9564},
            {"ville": "Herceg Novi", "lat": 42.4531, "lon": 18.5375},
            {"ville": "Bar", "lat": 42.1000, "lon": 19.1000},
            {"ville": "Cetinje", "lat": 42.3833, "lon": 18.9167},
            {"ville": "Pljevlja", "lat": 43.3567, "lon": 19.3583},
            {"ville": "Bijelo Polje", "lat": 43.0333, "lon": 19.7500},
            {"ville": "Berane", "lat": 42.8500, "lon": 19.8833},
            {"ville": "Budva", "lat": 42.2778, "lon": 18.8369},
            {"ville": "Ulcinj", "lat": 41.9283, "lon": 19.2244},
        ],
        "langues": ["monténégrin"],
        "noms": {
            "prenoms": ["Marko", "Jovan", "Ana", "Milica", "Petar", "Ivana"],
            "noms": ["Vuković", "Đukanović", "Jovanović", "Radović", "Nikolić"]
        }
    },

    "nigeria": {
        "capitale": "Abuja",
        "coordonnees": {"lat": 9.082, "lon": 8.6753},
        "villes": [
            {"ville": "Abuja", "lat": 9.0765, "lon": 7.3986},
            {"ville": "Lagos", "lat": 6.5244, "lon": 3.3792},
            {"ville": "Kano", "lat": 11.9914, "lon": 8.5313},
            {"ville": "Ibadan", "lat": 7.3964, "lon": 3.8867},
            {"ville": "Kaduna", "lat": 10.5222, "lon": 7.4384},
            {"ville": "Port Harcourt", "lat": 4.8156, "lon": 7.0498},
            {"ville": "Maiduguri", "lat": 11.8333, "lon": 13.1500},
            {"ville": "Zaria", "lat": 11.1111, "lon": 7.7222},
            {"ville": "Jos", "lat": 9.8965, "lon": 8.8583},
            {"ville": "Ilorin", "lat": 8.5000, "lon": 4.5500},
        ],
        "langues": ["anglais", "haoussa", "yoruba", "igbo"],
        "noms": {
            "prenoms": ["Chinedu", "Ngozi", "Ifeanyi", "Aisha", "Emeka", "Blessing"],
            "noms": ["Okafor", "Adebayo", "Ogunleye", "Eze", "Abiola"]
        }
    },

    "norvège": {
        "capitale": "Oslo",
        "coordonnees": {"lat": 60.472, "lon": 8.4689},
        "villes": [
            {"ville": "Oslo", "lat": 59.9139, "lon": 10.7522},
            {"ville": "Bergen", "lat": 60.3913, "lon": 5.3221},
            {"ville": "Trondheim", "lat": 63.4305, "lon": 10.3951},
            {"ville": "Stavanger", "lat": 58.9700, "lon": 5.7331},
            {"ville": "Kristiansand", "lat": 58.1599, "lon": 8.0182},
            {"ville": "Tromsø", "lat": 69.6492, "lon": 18.9553},
            {"ville": "Drammen", "lat": 59.7439, "lon": 10.2045},
            {"ville": "Fredrikstad", "lat": 59.2181, "lon": 10.9298},
            {"ville": "Sandnes", "lat": 58.8516, "lon": 5.7392},
            {"ville": "Bodø", "lat": 67.2804, "lon": 14.4050},
        ],
        "langues": ["norvégien", "anglais"],
        "noms": {
            "prenoms": ["Ole", "Lars", "Kari", "Anne", "Per", "Ingrid"],
            "noms": ["Hansen", "Johansen", "Olsen", "Larsen", "Andersen"]
        }
    },

    "nouvelle-zélande": {
        "capitale": "Wellington",
        "coordonnees": {"lat": -40.9006, "lon": 174.886},
        "villes": [
            {"ville": "Wellington", "lat": -41.2866, "lon": 174.7756},
            {"ville": "Auckland", "lat": -36.8485, "lon": 174.7633},
            {"ville": "Christchurch", "lat": -43.5320, "lon": 172.6306},
            {"ville": "Hamilton", "lat": -37.7870, "lon": 175.2793},
            {"ville": "Tauranga", "lat": -37.6878, "lon": 176.1651},
            {"ville": "Napier", "lat": -39.4924, "lon": 176.9120},
            {"ville": "Palmerston North", "lat": -40.3523, "lon": 175.6082},
            {"ville": "Rotorua", "lat": -38.1368, "lon": 176.2497},
            {"ville": "New Plymouth", "lat": -39.0556, "lon": 174.0750},
            {"ville": "Whangarei", "lat": -35.7251, "lon": 174.3236},
        ],
        "langues": ["anglais", "maori"],
        "noms": {
            "prenoms": ["Jack", "Charlotte", "Oliver", "Sophie", "James", "Isabella"],
            "noms": ["Smith", "Williams", "Brown", "Wilson", "Taylor"]
        }
    },

    "ouzbekistan": {
        "capitale": "Tachkent",
        "coordonnees": {"lat": 41.3775, "lon": 64.5853},
        "villes": [
            {"ville": "Tachkent", "lat": 41.2995, "lon": 69.2401},
            {"ville": "Samarcande", "lat": 39.6273, "lon": 66.9747},
            {"ville": "Namangan", "lat": 40.9983, "lon": 71.6726},
            {"ville": "Andijan", "lat": 40.7833, "lon": 72.3500},
            {"ville": "Boukhara", "lat": 39.7684, "lon": 64.4556},
            {"ville": "Nukus", "lat": 42.4500, "lon": 59.6167},
            {"ville": "Karchi", "lat": 38.8667, "lon": 65.8000},
            {"ville": "Ferghana", "lat": 40.3833, "lon": 71.7833},
            {"ville": "Termez", "lat": 37.2167, "lon": 67.2833},
            {"ville": "Navoiy", "lat": 40.1000, "lon": 65.3667},
        ],
        "langues": ["ouzbek", "russe"],
        "noms": {
            "prenoms": ["Aziz", "Dilnoza", "Shavkat", "Nigora", "Akmal", "Gulbahor"],
            "noms": ["Karimov", "Tursunov", "Rakhimov", "Yuldashev", "Nazarov"]
        }
    },

    "pakistan": {
        "capitale": "Islamabad",
        "coordonnees": {"lat": 30.3753, "lon": 69.3451},
        "villes": [
            {"ville": "Islamabad", "lat": 33.7294, "lon": 73.0931},
            {"ville": "Karachi", "lat": 24.8607, "lon": 67.0011},
            {"ville": "Lahore", "lat": 31.5204, "lon": 74.3587},
            {"ville": "Faisalabad", "lat": 31.4167, "lon": 73.0833},
            {"ville": "Rawalpindi", "lat": 33.6007, "lon": 73.0679},
            {"ville": "Multan", "lat": 30.1978, "lon": 71.4697},
            {"ville": "Hyderabad", "lat": 25.3969, "lon": 68.3778},
            {"ville": "Gujranwala", "lat": 32.1617, "lon": 74.1883},
            {"ville": "Peshawar", "lat": 34.0080, "lon": 71.5785},
            {"ville": "Quetta", "lat": 30.1798, "lon": 66.9750},
        ],
        "langues": ["ourdou", "anglais", "pendjabi", "sindhi"],
        "noms": {
            "prenoms": ["Ali", "Ayesha", "Ahmed", "Sana", "Imran", "Fatima"],
            "noms": ["Khan", "Ahmed", "Hussain", "Ali", "Malik"]
        }
    },

    "pays-bas": {
        "capitale": "Amsterdam",
        "coordonnees": {"lat": 52.1326, "lon": 5.2913},
        "villes": [
            {"ville": "Amsterdam", "lat": 52.3676, "lon": 4.9041},
            {"ville": "Rotterdam", "lat": 51.9225, "lon": 4.4792},
            {"ville": "La Haye", "lat": 52.0705, "lon": 4.3007},
            {"ville": "Utrecht", "lat": 52.0907, "lon": 5.1214},
            {"ville": "Eindhoven", "lat": 51.4416, "lon": 5.4697},
            {"ville": "Tilbourg", "lat": 51.5719, "lon": 5.0672},
            {"ville": "Groningue", "lat": 53.2194, "lon": 6.5665},
            {"ville": "Almere", "lat": 52.3508, "lon": 5.2647},
            {"ville": "Breda", "lat": 51.5719, "lon": 4.7683},
            {"ville": "Nimègue", "lat": 51.8425, "lon": 5.8533},
        ],
        "langues": ["néerlandais", "anglais"],
        "noms": {
            "prenoms": ["Jan", "Anna", "Tom", "Lisa", "Pieter", "Sanne"],
            "noms": ["De Vries", "Jansen", "De Jong", "Bakker", "Van Dijk"]
        }
    },

    "pologne": {
        "capitale": "Varsovie",
        "coordonnees": {"lat": 51.9194, "lon": 19.1451},
        "villes": [
            {"ville": "Varsovie", "lat": 52.2297, "lon": 21.0122},
            {"ville": "Cracovie", "lat": 50.0647, "lon": 19.9450},
            {"ville": "Łódź", "lat": 51.7592, "lon": 19.4559},
            {"ville": "Wrocław", "lat": 51.1079, "lon": 17.0385},
            {"ville": "Poznań", "lat": 52.4064, "lon": 16.9252},
            {"ville": "Gdańsk", "lat": 54.3520, "lon": 18.6466},
            {"ville": "Szczecin", "lat": 53.4285, "lon": 14.5528},
            {"ville": "Bydgoszcz", "lat": 53.1235, "lon": 18.0084},
            {"ville": "Lublin", "lat": 51.2465, "lon": 22.5684},
            {"ville": "Katowice", "lat": 50.2613, "lon": 19.0239},
        ],
        "langues": ["polonais", "anglais", "allemand"],
        "noms": {
            "prenoms": ["Jan", "Anna", "Piotr", "Katarzyna", "Tomasz", "Agnieszka"],
            "noms": ["Nowak", "Kowalski", "Wiśniewski", "Dąbrowski", "Lewandowski"]
        }
    },

    "portugal": {
        "capitale": "Lisbonne",
        "coordonnees": {"lat": 39.3999, "lon": -8.2245},
        "villes": [
            {"ville": "Lisbonne", "lat": 38.7223, "lon": -9.1393},
            {"ville": "Porto", "lat": 41.1579, "lon": -8.6291},
            {"ville": "Braga", "lat": 41.5454, "lon": -8.4265},
            {"ville": "Setúbal", "lat": 38.5243, "lon": -8.8926},
            {"ville": "Coimbra", "lat": 40.2033, "lon": -8.4103},
            {"ville": "Faro", "lat": 37.0194, "lon": -7.9304},
            {"ville": "Évora", "lat": 38.5725, "lon": -7.9072},
            {"ville": "Aveiro", "lat": 40.6443, "lon": -8.6455},
            {"ville": "Leiria", "lat": 39.7477, "lon": -8.8070},
            {"ville": "Guarda", "lat": 40.5373, "lon": -7.2658},
        ],
        "langues": ["portugais", "anglais", "espagnol"],
        "noms": {
            "prenoms": ["João", "Ana", "Miguel", "Inês", "Pedro", "Maria"],
            "noms": ["Silva", "Santos", "Ferreira", "Pereira", "Oliveira"]
        }
    },

    "roumanie": {
        "capitale": "Bucarest",
        "coordonnees": {"lat": 45.9432, "lon": 24.9668},
        "villes": [
            {"ville": "Bucarest", "lat": 44.4268, "lon": 26.1025},
            {"ville": "Cluj-Napoca", "lat": 46.7712, "lon": 23.6236},
            {"ville": "Timișoara", "lat": 45.7607, "lon": 21.2263},
            {"ville": "Iași", "lat": 47.1585, "lon": 27.6014},
            {"ville": "Constanța", "lat": 44.1733, "lon": 28.6383},
            {"ville": "Craiova", "lat": 44.3195, "lon": 23.7967},
            {"ville": "Galați", "lat": 45.4353, "lon": 28.0076},
            {"ville": "Brașov", "lat": 45.6427, "lon": 25.5886},
            {"ville": "Ploiești", "lat": 44.9419, "lon": 26.0225},
            {"ville": "Brăila", "lat": 45.2667, "lon": 27.9833},
        ],
        "langues": ["roumain", "hongrois"],
        "noms": {
            "prenoms": ["Andrei", "Maria", "Alexandru", "Elena", "Vasile", "Ioana"],
            "noms": ["Popescu", "Ionescu", "Stan", "Dumitru", "Gheorghe"]
        }
    },

    "royaume-uni": {
        "capitale": "Londres",
        "coordonnees": {"lat": 55.3781, "lon": -3.436},
        "villes": [
            {"ville": "Londres", "lat": 51.5074, "lon": -0.1278},
            {"ville": "Birmingham", "lat": 52.4862, "lon": -1.8904},
            {"ville": "Manchester", "lat": 53.4808, "lon": -2.2426},
            {"ville": "Glasgow", "lat": 55.8642, "lon": -4.2518},
            {"ville": "Liverpool", "lat": 53.4084, "lon": -2.9916},
            {"ville": "Leeds", "lat": 53.8008, "lon": -1.5491},
            {"ville": "Sheffield", "lat": 53.3811, "lon": -1.4701},
            {"ville": "Edimbourg", "lat": 55.9533, "lon": -3.1883},
            {"ville": "Bristol", "lat": 51.4545, "lon": -2.5879},
            {"ville": "Cardiff", "lat": 51.4816, "lon": -3.1791},
        ],
        "langues": ["anglais", "français", "gallois", "écossais"],
        "noms": {
            "prenoms": ["James", "William", "Emily", "Sophie", "Oliver", "George"],
            "noms": ["Smith", "Jones", "Taylor", "Williams", "Brown"]
        }
    },

    "russie": {
        "capitale": "Moscou",
        "coordonnees": {"lat": 61.524, "lon": 105.3188},
        "villes": [
            {"ville": "Moscou", "lat": 55.7558, "lon": 37.6176},
            {"ville": "Saint-Pétersbourg", "lat": 59.9311, "lon": 30.3609},
            {"ville": "Novossibirsk", "lat": 55.0084, "lon": 82.9357},
            {"ville": "Iekaterinbourg", "lat": 56.8519, "lon": 60.6122},
            {"ville": "Kazan", "lat": 55.7887, "lon": 49.1221},
            {"ville": "Nijni Novgorod", "lat": 56.2965, "lon": 43.9361},
            {"ville": "Tcheliabinsk", "lat": 55.1644, "lon": 61.4368},
            {"ville": "Samara", "lat": 53.2001, "lon": 50.1500},
            {"ville": "Omsk", "lat": 54.9924, "lon": 73.3686},
            {"ville": "Rostov-sur-le-Don", "lat": 47.2357, "lon": 39.7015},
        ],
        "langues": ["russe", "anglais", "tatar", "ukrainien"],
        "noms": {
            "prenoms": ["Ivan", "Anna", "Nikita", "Olga", "Sergei", "Tatiana"],
            "noms": ["Ivanov", "Petrov", "Smirnov", "Kuznetsov", "Volkov"]
        }
    },

    "serbie": {
        "capitale": "Belgrade",
        "coordonnees": {"lat": 44.0165, "lon": 21.0059},
        "villes": [
            {"ville": "Belgrade", "lat": 44.7866, "lon": 20.4489},
            {"ville": "Novi Sad", "lat": 45.2551, "lon": 19.8452},
            {"ville": "Niš", "lat": 43.3247, "lon": 21.9033},
            {"ville": "Kragujevac", "lat": 44.0167, "lon": 20.9167},
            {"ville": "Subotica", "lat": 46.1000, "lon": 19.6667},
            {"ville": "Zrenjanin", "lat": 45.3833, "lon": 20.3833},
            {"ville": "Pančevo", "lat": 44.8667, "lon": 20.6333},
            {"ville": "Čačak", "lat": 43.8833, "lon": 20.3500},
            {"ville": "Kraljevo", "lat": 43.7167, "lon": 20.6833},
            {"ville": "Novi Pazar", "lat": 43.1500, "lon": 20.5167},
        ],
        "langues": ["serbe"],
        "noms": {
            "prenoms": ["Nikola", "Jovan", "Ana", "Milica", "Marko", "Jelena"],
            "noms": ["Jovanović", "Petrović", "Nikolić", "Stojanović", "Marković"]
        }
    },

    "singapour": {
        "capitale": "Singapour",
        "coordonnees": {"lat": 1.3521, "lon": 103.8198},
        "villes": [
            {"ville": "Singapour", "lat": 1.3521, "lon": 103.8198},
            {"ville": "Jurong West", "lat": 1.3404, "lon": 103.7054},
            {"ville": "Woodlands", "lat": 1.4360, "lon": 103.7860},
            {"ville": "Tampines", "lat": 1.3526, "lon": 103.9446},
            {"ville": "Sengkang", "lat": 1.3945, "lon": 103.9020},
            {"ville": "Hougang", "lat": 1.3612, "lon": 103.8866},
            {"ville": "Yishun", "lat": 1.4295, "lon": 103.8350},
            {"ville": "Ang Mo Kio", "lat": 1.3691, "lon": 103.8454},
            {"ville": "Bedok", "lat": 1.3508, "lon": 103.9280},
            {"ville": "Bukit Batok", "lat": 1.3483, "lon": 103.7461},
        ],
        "langues": ["anglais", "mandarin", "malais", "tamoul"],
        "noms": {
            "prenoms": ["Wei", "Xinyi", "Jia", "Yong", "Zhi", "Ting"],
            "noms": ["Tan", "Lim", "Lee", "Ng", "Wong"]
        }
    },

    "slovaquie": {
        "capitale": "Bratislava",
        "coordonnees": {"lat": 48.669, "lon": 19.699},
        "villes": [
            {"ville": "Bratislava", "lat": 48.1486, "lon": 17.1077},
            {"ville": "Košice", "lat": 48.7164, "lon": 21.2611},
            {"ville": "Prešov", "lat": 48.9984, "lon": 21.2339},
            {"ville": "Žilina", "lat": 49.2234, "lon": 18.7394},
            {"ville": "Banská Bystrica", "lat": 48.7353, "lon": 19.1455},
            {"ville": "Nitra", "lat": 48.3069, "lon": 18.0845},
            {"ville": "Trnava", "lat": 48.3774, "lon": 17.5870},
            {"ville": "Trenčín", "lat": 48.8945, "lon": 18.0444},
            {"ville": "Poprad", "lat": 49.0614, "lon": 20.2980},
            {"ville": "Martin", "lat": 49.0665, "lon": 18.9235},
        ],
        "langues": ["slovaque", "hongrois"],
        "noms": {
            "prenoms": ["Martin", "Marek", "Katarína", "Jana", "Peter", "Lucia"],
            "noms": ["Horváth", "Kováč", "Varga", "Tóth", "Nagy"]
        }
    },

    "suisse": {
        "capitale": "Berne",
        "coordonnees": {"lat": 46.8182, "lon": 8.2275},
        "villes": [
            {"ville": "Berne", "lat": 46.9479, "lon": 7.4474},
            {"ville": "Zurich", "lat": 47.3769, "lon": 8.5417},
            {"ville": "Genève", "lat": 46.2044, "lon": 6.1432},
            {"ville": "Bâle", "lat": 47.5596, "lon": 7.5886},
            {"ville": "Lausanne", "lat": 46.5197, "lon": 6.6323},
            {"ville": "Winterthour", "lat": 47.5000, "lon": 8.7500},
            {"ville": "Saint-Gall", "lat": 47.4245, "lon": 9.3767},
            {"ville": "Lucerne", "lat": 47.0502, "lon": 8.3093},
            {"ville": "Lugano", "lat": 46.0101, "lon": 8.9600},
            {"ville": "Bienne", "lat": 47.1371, "lon": 7.2464},
        ],
        "langues": ["allemand", "français", "italien", "romanche"],
        "noms": {
            "prenoms": ["Luca", "Laura", "Noah", "Lea", "Jan", "Sofia"],
            "noms": ["Müller", "Meier", "Schneider", "Weber", "Huber"]
        }
    },

    "suède": {
        "capitale": "Stockholm",
        "coordonnees": {"lat": 60.1282, "lon": 18.6435},
        "villes": [
            {"ville": "Stockholm", "lat": 59.3293, "lon": 18.0686},
            {"ville": "Göteborg", "lat": 57.7089, "lon": 11.9746},
            {"ville": "Malmö", "lat": 55.6050, "lon": 13.0038},
            {"ville": "Uppsala", "lat": 59.8586, "lon": 17.6389},
            {"ville": "Västerås", "lat": 59.6162, "lon": 16.5526},
            {"ville": "Örebro", "lat": 59.2753, "lon": 15.2134},
            {"ville": "Linköping", "lat": 58.4108, "lon": 15.6214},
            {"ville": "Helsingborg", "lat": 56.0465, "lon": 12.6945},
            {"ville": "Jönköping", "lat": 57.7826, "lon": 14.1618},
            {"ville": "Norrköping", "lat": 58.5877, "lon": 16.1924},
        ],
        "langues": ["suédois", "anglais"],
        "noms": {
            "prenoms": ["Erik", "Lars", "Anna", "Maria", "Johan", "Emma"],
            "noms": ["Johansson", "Andersson", "Karlsson", "Nilsson", "Larsson"]
        }
    },

    "thailande": {
        "capitale": "Bangkok",
        "coordonnees": {"lat": 15.87, "lon": 100.9925},
        "villes": [
            {"ville": "Bangkok", "lat": 13.7563, "lon": 100.5018},
            {"ville": "Chiang Mai", "lat": 18.7883, "lon": 98.9853},
            {"ville": "Pattaya", "lat": 12.9236, "lon": 100.8824},
            {"ville": "Phuket", "lat": 7.8804, "lon": 98.3923},
            {"ville": "Hat Yai", "lat": 7.0084, "lon": 100.4767},
            {"ville": "Udon Thani", "lat": 17.4074, "lon": 102.7942},
            {"ville": "Khon Kaen", "lat": 16.4326, "lon": 102.8236},
            {"ville": "Nakhon Ratchasima", "lat": 14.9730, "lon": 102.1013},
            {"ville": "Chiang Rai", "lat": 19.9061, "lon": 99.8305},
            {"ville": "Ubon Ratchathani", "lat": 15.2280, "lon": 104.8594},
        ],
        "langues": ["thaï", "anglais"],
        "noms": {
            "prenoms": ["Somchai", "Somsak", "Suthida", "Malee", "Kittipong", "Chalida"],
            "noms": ["Sukhum", "Srisai", "Pradchaphet", "Yongchaiyudh", "Chaiprasit"]
        }
    },

    "tunisie": {
        "capitale": "Tunis",
        "coordonnees": {"lat": 33.8869, "lon": 9.5375},
        "villes": [
            {"ville": "Tunis", "lat": 36.8065, "lon": 10.1815},
            {"ville": "Sfax", "lat": 34.7478, "lon": 10.7663},
            {"ville": "Sousse", "lat": 35.8333, "lon": 10.6333},
            {"ville": "Ettadhamen", "lat": 36.8333, "lon": 10.1167},
            {"ville": "Kairouan", "lat": 35.6781, "lon": 10.0963},
            {"ville": "Gabès", "lat": 33.8815, "lon": 10.0982},
            {"ville": "Bizerte", "lat": 37.2744, "lon": 9.8739},
            {"ville": "Ariana", "lat": 36.8667, "lon": 10.2000},
            {"ville": "Gafsa", "lat": 34.4167, "lon": 8.7833},
            {"ville": "Monastir", "lat": 35.7833, "lon": 10.8333},
        ],
        "langues": ["arabe", "français"],
        "noms": {
            "prenoms": ["Mehdi", "Mouna", "Sami", "Nesrine", "Walid", "Ines"],
            "noms": ["Ben Salah", "Ayari", "Trabelsi", "Jaziri", "Bouazizi"]
        }
    },

    "turkménistan": {
        "capitale": "Achgabat",
        "coordonnees": {"lat": 38.9697, "lon": 59.5563},
        "villes": [
            {"ville": "Achgabat", "lat": 37.9601, "lon": 58.3261},
            {"ville": "Türkmenabat", "lat": 39.0833, "lon": 63.5667},
            {"ville": "Dasoguz", "lat": 41.8333, "lon": 59.9667},
            {"ville": "Mary", "lat": 37.6000, "lon": 61.8333},
            {"ville": "Balkanabat", "lat": 39.5167, "lon": 54.3667},
            {"ville": "Bayramaly", "lat": 37.6167, "lon": 62.1500},
            {"ville": "Tejen", "lat": 37.3833, "lon": 60.5000},
            {"ville": "Gyzylarbat", "lat": 39.1167, "lon": 56.2833},
            {"ville": "Serdar", "lat": 38.9833, "lon": 56.2833},
            {"ville": "Kaka", "lat": 37.3500, "lon": 59.6167},
        ],
        "langues": ["turkmène", "russe"],
        "noms": {
            "prenoms": ["Batyr", "Gulnara", "Myrat", "Ayna", "Sapar", "Maya"],
            "noms": ["Berdyev", "Atayev", "Saparov", "Annayev", "Rahimov"]
        }
    },

    "turquie": {
        "capitale": "Ankara",
        "coordonnees": {"lat": 38.9637, "lon": 35.2433},
        "villes": [
            {"ville": "Ankara", "lat": 39.9334, "lon": 32.8597},
            {"ville": "Istanbul", "lat": 41.0082, "lon": 28.9784},
            {"ville": "Izmir", "lat": 38.4192, "lon": 27.1287},
            {"ville": "Bursa", "lat": 40.1885, "lon": 29.0610},
            {"ville": "Antalya", "lat": 36.8969, "lon": 30.7133},
            {"ville": "Adana", "lat": 37.0000, "lon": 35.3213},
            {"ville": "Konya", "lat": 37.8667, "lon": 32.4833},
            {"ville": "Gaziantep", "lat": 37.0662, "lon": 37.3833},
            {"ville": "Mersin", "lat": 36.8000, "lon": 34.6333},
            {"ville": "Diyarbakır", "lat": 37.9144, "lon": 40.2306},
        ],
        "langues": ["turc", "kurde", "anglais"],
        "noms": {
            "prenoms": ["Mehmet", "Ahmet", "Ayşe", "Fatma", "Mustafa", "Emine"],
            "noms": ["Yılmaz", "Kaya", "Demir", "Şahin", "Çelik"]
        }
    },

    "ukraine": {
        "capitale": "Kiev",
        "coordonnees": {"lat": 48.3794, "lon": 31.1656},
        "villes": [
            {"ville": "Kiev", "lat": 50.4501, "lon": 30.5234},
            {"ville": "Kharkiv", "lat": 49.9935, "lon": 36.2304},
            {"ville": "Odessa", "lat": 46.4825, "lon": 30.7233},
            {"ville": "Dnipro", "lat": 48.4647, "lon": 35.0172},
            {"ville": "Donetsk", "lat": 48.0159, "lon": 37.8028},
            {"ville": "Zaporijjia", "lat": 47.8388, "lon": 35.1396},
            {"ville": "Lviv", "lat": 49.8397, "lon": 24.0297},
            {"ville": "Kryvyï Rih", "lat": 47.9105, "lon": 33.3918},
            {"ville": "Mykolaïv", "lat": 46.9750, "lon": 31.9946},
            {"ville": "Marioupol", "lat": 47.0971, "lon": 37.5439},
        ],
        "langues": ["ukrainien", "russe", "anglais"],
        "noms": {
            "prenoms": ["Oleksandr", "Andriy", "Olena", "Iryna", "Viktor", "Kateryna"],
            "noms": ["Shevchenko", "Kovalenko", "Boyko", "Bondarenko", "Tkachenko"]
        }
    },

    "viet nam": {
        "capitale": "Hanoï",
        "coordonnees": {"lat": 16.0544, "lon": 108.2022},
        "villes": [
            {"ville": "Hanoï", "lat": 21.0285, "lon": 105.8542},
            {"ville": "Ho Chi Minh-Ville", "lat": 10.8231, "lon": 106.6297},
            {"ville": "Da Nang", "lat": 16.0544, "lon": 108.2022},
            {"ville": "Haïphong", "lat": 20.8449, "lon": 106.6881},
            {"ville": "Can Tho", "lat": 10.0452, "lon": 105.7469},
            {"ville": "Bien Hoa", "lat": 10.9574, "lon": 106.8426},
            {"ville": "Hue", "lat": 16.4637, "lon": 107.5909},
            {"ville": "Nha Trang", "lat": 12.2388, "lon": 109.1967},
            {"ville": "Buon Ma Thuot", "lat": 12.6667, "lon": 108.1667},
            {"ville": "Vung Tau", "lat": 10.3459, "lon": 107.0843},
        ],
        "langues": ["vietnamien", "anglais", "français"],
        "noms": {
            "prenoms": ["Nguyen", "Thi", "Van", "Minh", "Huong", "Tuan"],
            "noms": ["Nguyen", "Tran", "Le", "Pham", "Hoang"]
        }
    },

    "états-unis": {
        "capitale": "Washington",
        "coordonnees": {"lat": 39.8283, "lon": -98.5795},
        "villes": [
            {"ville": "Washington", "lat": 38.9072, "lon": -77.0369},
            {"ville": "New York", "lat": 40.7128, "lon": -74.0060},
            {"ville": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
            {"ville": "Chicago", "lat": 41.8781, "lon": -87.6298},
            {"ville": "Houston", "lat": 29.7604, "lon": -95.3698},
            {"ville": "Phoenix", "lat": 33.4484, "lon": -112.0740},
            {"ville": "Philadelphie", "lat": 39.9526, "lon": -75.1652},
            {"ville": "San Antonio", "lat": 29.4241, "lon": -98.4936},
            {"ville": "San Diego", "lat": 32.7157, "lon": -117.1611},
            {"ville": "Dallas", "lat": 32.7767, "lon": -96.7970},
        ],
        "langues": ["anglais", "espagnol"],
        "noms": {
            "prenoms": ["John", "Michael", "Sarah", "Emily", "Robert", "Jessica"],
            "noms": ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        }
    },

}

# ============================================================================
# FONCTIONS UNIFIÉES
# ============================================================================

def generer_nom_prenom(pays):
    """Génère un nom et prénom selon le pays"""
    if pays.lower() in GEOGRAPHIE_UNIFIEE:
        pays_data = GEOGRAPHIE_UNIFIEE[pays.lower()]
        prenom = random.choice(pays_data["noms"]["prenoms"])
        nom = random.choice(pays_data["noms"]["noms"])
        return nom, prenom
    else:
        # Fallback par défaut
        return "Smith", "John"

def obtenir_villes_pays(pays):
    """Retourne les villes d'un pays"""
    if pays.lower() in GEOGRAPHIE_UNIFIEE:
        return GEOGRAPHIE_UNIFIEE[pays.lower()]["villes"]
    return []

def obtenir_langues_pays(pays):
    """Retourne les langues d'un pays"""
    if pays.lower() in GEOGRAPHIE_UNIFIEE:
        return GEOGRAPHIE_UNIFIEE[pays.lower()]["langues"]
    return ["anglais"]

def obtenir_coordonnees_pays(pays):
    """Retourne les coordonnées d'un pays"""
    if pays.lower() in GEOGRAPHIE_UNIFIEE:
        return GEOGRAPHIE_UNIFIEE[pays.lower()]["coordonnees"]
    return {"lat": 0.0, "lon": 0.0}

def obtenir_capitale_pays(pays):
    """Retourne la capitale d'un pays"""
    if pays.lower() in GEOGRAPHIE_UNIFIEE:
        return GEOGRAPHIE_UNIFIEE[pays.lower()]["capitale"]
    return "Inconnue"

def lister_pays_disponibles():
    """Liste tous les pays disponibles"""
    return list(GEOGRAPHIE_UNIFIEE.keys())

def pays_existe(pays):
    """Vérifie si un pays existe dans la base"""
    return pays.lower() in GEOGRAPHIE_UNIFIEE

# ============================================================================
# COMPATIBILITÉ AVEC L'ANCIEN SYSTÈME
# ============================================================================

# Pour maintenir la compatibilité avec le code existant
NOMS_PRENOMS = {pays: data["noms"] for pays, data in GEOGRAPHIE_UNIFIEE.items()}
VILLES_PAR_PAYS = {pays: data["villes"] for pays, data in GEOGRAPHIE_UNIFIEE.items()}
LANGUES_PAR_PAYS = {pays: data["langues"] for pays, data in GEOGRAPHIE_UNIFIEE.items()}

def obtenir_toutes_langues():
    """Retourne la liste de toutes les langues uniques dans le système"""
    langues = set()
    for pays_langues in LANGUES_PAR_PAYS.values():
        langues.update(pays_langues)
    return sorted(list(langues))

def langue_existe(langue):
    """Vérifie si une langue existe dans le système"""
    return langue.lower() in [l.lower() for l in obtenir_toutes_langues()]

def obtenir_pays_langue(langue):
    """Retourne la liste des pays qui parlent une langue donnée"""
    pays_avec_langue = []
    for pays, langues in LANGUES_PAR_PAYS.items():
        if langue.lower() in [l.lower() for l in langues]:
            pays_avec_langue.append(pays)
    return pays_avec_langue
