def ajouter_utilisateur(bibliotheque, id, nom, email):
    bibliotheque['utilisateurs'].append({
        'id': id,
        'nom': nom,
        'email': email
    })

def supprimer_utilisateur(bibliotheque, id):
    bibliotheque['utilisateurs'] = [utilisateur for utilisateur in bibliotheque['utilisateurs'] if utilisateur['id'] != id]

def lister_utilisateurs(bibliotheque):
    return bibliotheque['utilisateurs']

