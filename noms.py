# noms.py

import random

NOMS_PRENOMS = {
    "france": {
        "prenoms": ["Jean", "Pierre", "Marie", "Claire", "Sophie", "Luc", "Paul", "Julien"],
        "noms": ["Dupont", "Martin", "Bernard", "Petit", "Durand", "Moreau", "Laurent"]
    },
    "allemagne": {
        "prenoms": ["Hans", "Anna", "Peter", "Sophie", "Lukas", "Sabine"],
        "noms": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber"]
    },
    "italie": {
        "prenoms": ["Giuseppe", "Marco", "Francesca", "Giulia", "Luca", "Alessandro"],
        "noms": ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi"]
    },
    "espagne": {
        "prenoms": ["Juan", "Carlos", "Maria", "Isabel", "Antonio", "Lucia"],
        "noms": ["García", "Martínez", "López", "Sánchez", "Fernández"]
    },
    "portugal": {
        "prenoms": ["João", "Ana", "Miguel", "Inês", "Pedro", "Maria"],
        "noms": ["Silva", "Santos", "Ferreira", "Pereira", "Oliveira"]
    },
    "royaume-uni": {
        "prenoms": ["James", "William", "Emily", "Sophie", "Oliver", "George"],
        "noms": ["Smith", "Jones", "Taylor", "Williams", "Brown"]
    },
    "irlande": {
        "prenoms": ["Seán", "Patrick", "Aoife", "Ciara", "Liam", "Niamh"],
        "noms": ["Murphy", "Kelly", "O'Sullivan", "Walsh", "Byrne"]
    },
    "pays-bas": {
        "prenoms": ["Jan", "Anna", "Tom", "Lisa", "Pieter", "Sanne"],
        "noms": ["De Vries", "Jansen", "De Jong", "Bakker", "Van Dijk"]
    },
    "belgique": {
        "prenoms": ["Lucas", "Marie", "Louis", "Emma", "Noah", "Julie"],
        "noms": ["Peeters", "Janssens", "Maes", "Jacobs", "Mertens"]
    },
    "suisse": {
        "prenoms": ["Luca", "Laura", "Noah", "Lea", "Jan", "Sofia"],
        "noms": ["Müller", "Meier", "Schneider", "Weber", "Huber"]
    },
    "autriche": {
        "prenoms": ["Lukas", "Anna", "Paul", "Laura", "David", "Marie"],
        "noms": ["Gruber", "Huber", "Wagner", "Bauer", "Müller"]
    },
    "pologne": {
        "prenoms": ["Jan", "Anna", "Piotr", "Katarzyna", "Tomasz", "Agnieszka"],
        "noms": ["Nowak", "Kowalski", "Wiśniewski", "Dąbrowski", "Lewandowski"]
    },
    "hongrie": {
        "prenoms": ["László", "Gábor", "Eszter", "Katalin", "Zoltán", "Judit"],
        "noms": ["Nagy", "Kovács", "Tóth", "Szabó", "Horváth"]
    },
    "suède": {
        "prenoms": ["Erik", "Lars", "Anna", "Maria", "Johan", "Emma"],
        "noms": ["Johansson", "Andersson", "Karlsson", "Nilsson", "Larsson"]
    },
    "norvège": {
        "prenoms": ["Ole", "Lars", "Kari", "Anne", "Per", "Ingrid"],
        "noms": ["Hansen", "Johansen", "Olsen", "Larsen", "Andersen"]
    },
    "finlande": {
        "prenoms": ["Mikko", "Juhani", "Anna", "Maria", "Juha", "Sanna"],
        "noms": ["Korhonen", "Virtanen", "Mäkinen", "Nieminen", "Mäkelä"]
    },
    "danemark": {
        "prenoms": ["Lars", "Jens", "Anne", "Mette", "Søren", "Maria"],
        "noms": ["Jensen", "Nielsen", "Hansen", "Pedersen", "Andersen"]
    },
    "grèce": {
        "prenoms": ["Giorgos", "Nikos", "Maria", "Eleni", "Kostas", "Ioanna"],
        "noms": ["Papadopoulos", "Nikolaidis", "Pappas", "Georgiou", "Vasileiou"]
    },
    "turquie": {
        "prenoms": ["Mehmet", "Ahmet", "Ayşe", "Fatma", "Mustafa", "Emine"],
        "noms": ["Yılmaz", "Kaya", "Demir", "Şahin", "Çelik"]
    },
    "russie": {
        "prenoms": ["Ivan", "Anna", "Nikita", "Olga", "Sergei", "Tatiana"],
        "noms": ["Ivanov", "Petrov", "Smirnov", "Kuznetsov", "Volkov"]
    },
    "ukraine": {
        "prenoms": ["Oleksandr", "Andriy", "Olena", "Iryna", "Viktor", "Kateryna"],
        "noms": ["Shevchenko", "Kovalenko", "Boyko", "Bondarenko", "Tkachenko"]
    },
    "états-unis": {
        "prenoms": ["John", "Michael", "Sarah", "Emily", "Robert", "Jessica"],
        "noms": ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    },
    "canada": {
        "prenoms": ["Liam", "Emma", "Noah", "Olivia", "William", "Charlotte"],
        "noms": ["Smith", "Brown", "Tremblay", "Martin", "Roy"]
    },
    "mexique": {
        "prenoms": ["José", "Juan", "María", "Guadalupe", "Luis", "Carmen"],
        "noms": ["Hernández", "García", "Martínez", "López", "González"]
    },
    "brésil": {
        "prenoms": ["João", "Maria", "Pedro", "Ana", "Lucas", "Gabriela"],
        "noms": ["Silva", "Santos", "Oliveira", "Souza", "Lima"]
    },
    "argentine": {
        "prenoms": ["Juan", "María", "Carlos", "Ana", "Luis", "Lucía"],
        "noms": ["González", "Rodríguez", "Pérez", "Fernández", "Gómez"]
    },
    "colombie": {
        "prenoms": ["Juan", "Andrés", "María", "Camila", "Carlos", "Valentina"],
        "noms": ["García", "Rodríguez", "Martínez", "López", "González"]
    },
    "chine": {
        "prenoms": ["Wei", "Li", "Jing", "Hua", "Fang", "Wang"],
        "noms": ["Wang", "Li", "Zhang", "Liu", "Chen"]
    },
    "japon": {
        "prenoms": ["Haruto", "Yuki", "Sakura", "Hana", "Ren", "Aoi"],
        "noms": ["Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe"]
    },
    "corée du sud": {
        "prenoms": ["Min-jun", "Seo-yeon", "Ji-ho", "Soo-bin", "Jae-won", "Ha-yeon"],
        "noms": ["Kim", "Lee", "Park", "Jeong", "Choi"]
    },
    "inde": {
        "prenoms": ["Amit", "Priya", "Raj", "Anjali", "Vijay", "Sunita"],
        "noms": ["Singh", "Kumar", "Sharma", "Patel", "Gupta"]
    },
    "pakistan": {
        "prenoms": ["Ali", "Ayesha", "Ahmed", "Sana", "Imran", "Fatima"],
        "noms": ["Khan", "Ahmed", "Hussain", "Ali", "Malik"]
    },
    "iran": {
        "prenoms": ["Mohammad", "Ali", "Fatemeh", "Zahra", "Hossein", "Sara"],
        "noms": ["Mohammadi", "Hosseini", "Ahmadi", "Rezaei", "Karimi"]
    },
    "israël": {
        "prenoms": ["David", "Yael", "Daniel", "Noa", "Moshe", "Tal"],
        "noms": ["Cohen", "Levi", "Mizrahi", "Peretz", "Biton"]
    },
    "arabie saoudite": {
        "prenoms": ["Abdullah", "Faisal", "Aisha", "Fatimah", "Mohammed", "Noura"],
        "noms": ["Al Saud", "Al Harbi", "Al Qahtani", "Al Otaibi", "Al Shammari"]
    },
    "maroc": {
        "prenoms": ["Mohammed", "Fatima", "Youssef", "Khadija", "Omar", "Amina"],
        "noms": ["El Amrani", "Bennani", "Fassi", "Amrani", "Ouazzani"]
    },
    "algérie": {
        "prenoms": ["Ahmed", "Samir", "Karim", "Nadia", "Amina", "Yasmine"],
        "noms": ["Bouzid", "Benali", "Meziane", "Benkhelifa", "Guendouzi"]
    },
    "tunisie": {
        "prenoms": ["Mehdi", "Mouna", "Sami", "Nesrine", "Walid", "Ines"],
        "noms": ["Ben Salah", "Ayari", "Trabelsi", "Jaziri", "Bouazizi"]
    },
    "egypte": {
        "prenoms": ["Ahmed", "Mohamed", "Fatma", "Mona", "Omar", "Sara"],
        "noms": ["El-Sayed", "Hassan", "Mahmoud", "Ali", "Youssef"]
    },
    "afrique du sud": {
        "prenoms": ["Thabo", "Sipho", "Lerato", "Ayanda", "Nkosi", "Nomsa"],
        "noms": ["Nkosi", "Dlamini", "Botha", "Naidoo", "Mthembu"]
    },
    "nigeria": {
        "prenoms": ["Chinedu", "Ngozi", "Ifeanyi", "Aisha", "Emeka", "Blessing"],
        "noms": ["Okafor", "Adebayo", "Ogunleye", "Eze", "Abiola"]
    },
    "australie": {
        "prenoms": ["Jack", "Oliver", "Amelia", "Mia", "Lucas", "Emily"],
        "noms": ["Smith", "Williams", "Brown", "Wilson", "Taylor"]
    },
    "nouvelle-zélande": {
        "prenoms": ["Jack", "Charlotte", "Oliver", "Sophie", "James", "Isabella"],
        "noms": ["Smith", "Williams", "Brown", "Wilson", "Taylor"]
    },
    "indonésie": {
        "prenoms": ["Agus", "Dewi", "Budi", "Siti", "Andi", "Ratna"],
        "noms": ["Wijaya", "Sutanto", "Putra", "Saputra", "Gunawan"]
    },
    "malaisie": {
        "prenoms": ["Ahmad", "Nur", "Muhammad", "Siti", "Azlan", "Aisyah"],
        "noms": ["Ismail", "Abdullah", "Othman", "Yusof", "Rahman"]
    },
    "thailande": {
        "prenoms": ["Somchai", "Somsak", "Suthida", "Malee", "Kittipong", "Chalida"],
        "noms": ["Sukhum", "Srisai", "Pradchaphet", "Yongchaiyudh", "Chaiprasit"]
    },
    "viet nam": {
        "prenoms": ["Nguyen", "Thi", "Van", "Minh", "Huong", "Tuan"],
        "noms": ["Nguyen", "Tran", "Le", "Pham", "Hoang"]
    },
    "singapour": {
        "prenoms": ["Wei", "Xinyi", "Jia", "Yong", "Zhi", "Ting"],
        "noms": ["Tan", "Lim", "Lee", "Ng", "Wong"]
    },
    "kazakhstan": {
        "prenoms": ["Ayan", "Yerlan", "Aruzhan", "Dana", "Alikhan", "Aigerim"],
        "noms": ["Nursultan", "Tuleu", "Kenzhebek", "Nurmagambetov", "Abdikalykov"]
    },
    "islande": {
        "prenoms": ["Jón", "Guðrún", "Sigurður", "Anna", "Björn", "Kristín"],
        "noms": ["Jónsson", "Guðmundsdóttir", "Sigurðardóttir", "Einarsson", "Ólafsdóttir"]
    },
    "lettonie": {
        "prenoms": ["Jānis", "Anna", "Kristīne", "Mārtiņš", "Inese", "Artūrs"],
        "noms": ["Bērziņš", "Kalniņš", "Ozoliņš", "Jansons", "Vasiļjevs"]
    },
    "lituanie": {
        "prenoms": ["Jonas", "Dalia", "Mantas", "Ieva", "Vytautas", "Eglė"],
        "noms": ["Kazlauskas", "Jankauskas", "Petrauskas", "Balčiūnas", "Stankevičius"]
    },
    "estonie": {
        "prenoms": ["Kristjan", "Liis", "Jaan", "Mari", "Tanel", "Kadri"],
        "noms": ["Tamm", "Saar", "Kask", "Oja", "Mets"]
    },
    "slovaquie": {
        "prenoms": ["Martin", "Marek", "Katarína", "Jana", "Peter", "Lucia"],
        "noms": ["Horváth", "Kováč", "Varga", "Tóth", "Nagy"]
    },
    "bulgarie": {
        "prenoms": ["Georgi", "Ivan", "Maria", "Elena", "Dimitar", "Yana"],
        "noms": ["Ivanov", "Georgiev", "Dimitrov", "Petrov", "Nikolov"]
    },
    "roumanie": {
        "prenoms": ["Andrei", "Maria", "Alexandru", "Elena", "Vasile", "Ioana"],
        "noms": ["Popescu", "Ionescu", "Stan", "Dumitru", "Gheorghe"]
    },
    "croatie": {
        "prenoms": ["Ivan", "Ana", "Marko", "Marija", "Petar", "Ivana"],
        "noms": ["Horvat", "Kovačević", "Babić", "Marić", "Jurić"]
    },
    "serbie": {
        "prenoms": ["Nikola", "Jovan", "Ana", "Milica", "Marko", "Jelena"],
        "noms": ["Jovanović", "Petrović", "Nikolić", "Stojanović", "Marković"]
    },
    "bosnie": {
        "prenoms": ["Amir", "Jasmin", "Adnan", "Lejla", "Emina", "Dino"],
        "noms": ["Hadžić", "Hodžić", "Dedić", "Alić", "Mehić"]
    },
    "albanie": {
        "prenoms": ["Erion", "Arben", "Elira", "Luljeta", "Altin", "Anila"],
        "noms": ["Hoxha", "Shehu", "Krasniqi", "Gashi", "Shala"]
    },
    "monténégro": {
        "prenoms": ["Marko", "Jovan", "Ana", "Milica", "Petar", "Ivana"],
        "noms": ["Vuković", "Đukanović", "Jovanović", "Radović", "Nikolić"]
    },
    "géorgie": {
        "prenoms": ["Giorgi", "Nino", "Luka", "Ana", "Irakli", "Mariam"],
        "noms": ["Beridze", "Kapanadze", "Giorgadze", "Gogoladze", "Tsiklauri"]
    },
    "arménie": {
        "prenoms": ["Armen", "Ani", "Hayk", "Mariam", "Tigran", "Lilit"],
        "noms": ["Harutyunyan", "Grigoryan", "Hovhannisyan", "Khachatryan", "Sargsyan"]
    },
    "azerbaïdjan": {
        "prenoms": ["Ali", "Leyla", "Murad", "Aysel", "Elvin", "Gunel"],
        "noms": ["Aliyev", "Mammadov", "Huseynov", "Ismayilov", "Hasanov"]
    },
    "turkménistan": {
        "prenoms": ["Batyr", "Gulnara", "Myrat", "Ayna", "Sapar", "Maya"],
        "noms": ["Berdyev", "Atayev", "Saparov", "Annayev", "Rahimov"]
    },
    "ouzbékistan": {
        "prenoms": ["Aziz", "Dilnoza", "Shavkat", "Nigora", "Akmal", "Gulbahor"],
        "noms": ["Karimov", "Tursunov", "Rakhimov", "Yuldashev", "Nazarov"]
    },
    "kirghizistan": {
        "prenoms": ["Azamat", "Aigul", "Ermek", "Gulzat", "Nurzhan", "Altynai"],
        "noms": ["Bekbolotov", "Sadykov", "Abdyldaev", "Sydykov", "Mamatov"]
    },
    # ... (complète selon les pays)
}

def generer_nom_prenom(pays):
    pool = NOMS_PRENOMS.get(pays.lower(), NOMS_PRENOMS["france"])
    prenom = random.choice(pool["prenoms"])
    nom = random.choice(pool["noms"])
    return nom, prenom
