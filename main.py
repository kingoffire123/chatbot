import re
from collections import defaultdict
from collections import Counter

mots_communs = set([
    'de', 'la', '', 'et', 'le', 'est', 'du', 'les', 'des', 'plus', 'par', 'a', 'à', 'sa', 'dans',
    'un', 'après', 'en', 'une', 'sur', 'fois', 'grand', 'avec', 'même', 'qui', 'entre', 'elle', 'mais',
    'son', 'que','celle', 'cette', 'fait', 'ou', 'il', "c'est", 'lui', 'donc', 'celle-ci', "d'une",
    "quel", "quelle"
])

def decoupe_phrase(phrase):
    # on retire les espaces au debut et a la fin
    phrase = phrase.strip(" \n\t.?")
    # on retire les characteres pas interessants
    phrase = phrase.replace("\n", "")
    # si la phrase est vide, on passe a la suivante
    if len(phrase) == 0:
        return None
    # on retire les majuscules
    phrase = phrase.lower()
    # pour chaque phrase, on decoupe en mots
    mots = re.split("[ ,;:'()]", phrase)
    # on retire les mots trop communs
    return set(mots) - mots_communs

# cette fonction charge les articles les uns apres les autres
# et extrait les mots-cles.
def charger_et_preparer(fichiers):
    phrases = [] 
    index_phrase = 0
    phrases_par_mot = defaultdict(set)
    for fichier in fichiers:
        # 1. charger un article en memoire
        with open(fichier) as f:
            texte = f.read()
            # 2. decouper l'article en phrases
            texte_phrases = re.split("[.\n]", texte)
            # 3. pour chaque phrase, decoupe en mots
            tous_les_mots = Counter()
            for phrase in texte_phrases:
                mots = decoupe_phrase(phrase)
                if not mots: continue
                phrases.append(phrase)
                for mot in mots:
                    # pour chaque mot, on garde la liste des phrases
                    phrases_par_mot[mot].add(index_phrase)
                index_phrase += 1 
    # on ne va garder que les mots qui apparaissent dans moins de 50% des phrases
    seuil = index_phrase/2
    for mot in phrases_par_mot:
        if len(phrases_par_mot[mot]) > seuil:
            print ("Oublie",mot)
            phrases_par_mot[mot] = None
    return phrases_par_mot, phrases

def meilleures_reponses(question, phrases_par_mot, phrases, nombre):
    # on prend les mots de la phrase
    mots = decoupe_phrase(question)
    
    # Puis on retrouve toutes les phrases.
    p = []
    for mot in mots:
        s = phrases_par_mot[mot]
        if s is not None and len(s) > 0:
            # a la fin, la liste comprend toutes les phrases, parfois en plusieurs copies si elles
            # correspondent a plusieurs mots
            p.extend(list(s))
            #print (mot,s)

    # on compte les phrases qu'on a trouve
    reponses = Counter(p)

    # et on garde les meilleures
    resultat = []
    for r in reponses.most_common(nombre):
        phrase, frequence = r
        resultat.append((phrase, frequence, phrases[phrase]))
    return  resultat
    

if __name__ == '__main__':
    # 1. charger les articles et preparer les reponses
    phrases_par_mot, phrases = charger_et_preparer([
        "lune.txt",
        "terre.txt",
        "mars.txt",
        "systeme_solaire.txt",
        "chat.txt"
    ])
    # 2. poser des questions et repondre
    questions = [
        "Quelle est la masse de la lune par rapport a celle de la terre ?",
        "Quel est l'ordre des planètes dans le système solaire ?",
        "Que sont Uranus et Neptune ?",
        "Que mangent les chats ?",
        "Les chats sont-ils de bons animaux domestiques?"
    ]
    for q in questions:
        print ("\n>",q)
        for r in meilleures_reponses(q, phrases_par_mot, phrases, 1):
            print (r)
