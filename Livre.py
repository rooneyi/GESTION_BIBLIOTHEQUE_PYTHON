import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from ttkthemes import ThemedStyle
from Livre import *

def valider_titre(titre):
    if titre.isnumeric():
        messagebox.showerror("Erreur", "Écrire un titre correct")
        return False
    return titre

def valider_genre(genre):
    if genre.isnumeric():
        messagebox.showerror("Erreur", "Écrire le genre du livre correctement")
        return False
    return genre

def valider_auteur(auteur):
    if auteur.isnumeric() or len(auteur) < 3:
        messagebox.showerror("Erreur", "Écrire le nom de l'auteur correctement ou la taille est inférieure à 3")
        return False
    return auteur

def nouveau_id(livres):
    if not livres:
        return 1
    else:
        _ids = [livre['id'] for livre in livres if 'id' in livre]
        return max(_ids) + 1

def verifier_doublon_titre(livres, titre):
    for livre in livres:
        if livre['Titre'].lower() == titre.lower():
            return True
    return False

def charger_livres():
    file_path = 'donnees.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            try:
                livres = json.load(json_file)
                if not isinstance(livres, list):
                    livres = [livres]
            except json.JSONDecodeError:
                livres = []
    else:
        livres = []
    return livres

def sauvegarder_livres(livres):
    file_path = 'donnees.json'
    with open(file_path, 'w') as json_file:
        json.dump(livres, json_file, indent=4)

def sauvegarder_emprunts(emprunts):
    file_path = 'emprunts.json'
    with open(file_path, 'w') as json_file:
        json.dump(emprunts, json_file, indent=4)

def afficher_livres(result):
    if result:
        return json.dumps(result, indent=4)
    else:
        return "Aucune donnée à afficher."

def afficher_livres_disponibles():
    livres = charger_livres()
    resultats = [livre for livre in livres if livre['Disponible']]
    return json.dumps(resultats, indent=4) if resultats else "Aucun livre disponible."

def ajouter_livre(titreLivre, auteur, genreLivre):
    livres = charger_livres()
    estDispo = True
    if valider_titre(titreLivre) and valider_genre(genreLivre) and valider_auteur(auteur):
        if verifier_doublon_titre(livres, titreLivre):
            return "Un livre avec ce titre existe déjà."

        idLivre = nouveau_id(livres)

        livre = {
            "id": idLivre,
            "Titre": titreLivre,
            "Auteur": auteur,
            "Genre": genreLivre,
            "Disponible": estDispo
        }

        livres.append(livre)
        sauvegarder_livres(livres)

        return "Les nouvelles données ont été ajoutées à donnees.json"
    else:
        return "Les informations fournies ne sont pas valides."

def modifier_livre(titreLivre, nouvel_auteur, nouveau_genre):
    livres = charger_livres()
    for livre in livres:
        if livre['Titre'].lower() == titreLivre.lower():
            if valider_auteur(nouvel_auteur) and valider_genre(nouveau_genre):
                livre['Auteur'] = nouvel_auteur
                livre['Genre'] = nouveau_genre
                sauvegarder_livres(livres)
                return f"Le livre '{titreLivre}' a été modifié."
            else:
                return "Informations de modification non valides."
    return "Livre non trouvé."

def rechercher_livre_par_titre(titre):
    livres = charger_livres()
    for livre in livres:
        if livre['Titre'].lower() == titre.lower():
            return json.dumps(livre, indent=4)
    return "Livre non trouvé."

def archiver_livre(titre):
    livres = charger_livres()
    for livre in livres:
        if livre['Titre'].lower() == titre.lower() and livre['Disponible']:
            livre['Disponible'] = False
            sauvegarder_livres(livres)
            return f"Le livre '{titre}' a été archivé."
    return "Livre non trouvé ou déjà archivé."

def supprimer_livre_definitivement(titre):
    livres = charger_livres()
    for livre in livres:
        if livre['Titre'].lower() == titre.lower():
            livres.remove(livre)
            sauvegarder_livres(livres)
            return f"Le livre '{titre}' a été supprimé."
    return "Livre non trouvé."

def emprunter_livre(titre):
    livres = charger_livres()
    emprunts = charger_livres_empruntes()

    for livre in livres:
        if livre['Titre'].lower() == titre.lower():
            if livre['Disponible']:
                livre['Disponible'] = False
                emprunts.append(livre)
                sauvegarder_livres(livres)
                sauvegarder_emprunts(emprunts)
                return f"Le livre '{titre}' a été emprunté."
            else:
                return "Le livre est déjà emprunté."
    return "Livre non trouvé."

def retourner_livre(titre):
    livres = charger_livres()
    emprunts = charger_livres_empruntes()

    for livre in livres:
        if livre['Titre'].lower() == titre.lower():
            if not livre['Disponible']:
                livre['Disponible'] = True
                for emprunt in emprunts:
                    if emprunt['Titre'].lower() == titre.lower():
                        emprunts.remove(emprunt)
                        break
                sauvegarder_livres(livres)
                sauvegarder_emprunts(emprunts)
                return f"Le livre '{titre}' a été retourné."
            else:
                return "Le livre est déjà disponible."
    return "Livre non trouvé."

def charger_livres_empruntes():
    file_path = 'emprunts.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            try:
                emprunts = json.load(json_file)
                if not isinstance(emprunts, list):
                    emprunts = [emprunts]
            except json.JSONDecodeError:
                emprunts = []
    else:
        emprunts = []
    return emprunts