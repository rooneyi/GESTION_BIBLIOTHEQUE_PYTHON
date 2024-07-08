import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from ttkthemes import ThemedStyle
from Livre import *

def main():
    def ajouter_livre_ui():
        titre = entry_titre.get()
        auteur = entry_auteur.get()
        genre = entry_genre.get()
        message = ajouter_livre(titre, auteur, genre)
        messagebox.showinfo("Résultat", message)
        reset_fields()

    def afficher_livres_ui():
        livres = charger_livres()
        result = afficher_livres(livres)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)

    def afficher_livres_disponibles_ui():
        result = afficher_livres_disponibles()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)

    def supprimer_livre_ui():
        titre = entry_titre.get()
        result = supprimer_livre_definitivement(titre)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)
        reset_fields()

    def archiver_livre_ui():
        titre = entry_titre.get()
        result = archiver_livre(titre)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)
        reset_fields()

    def emprunter_livre_ui():
        titre = entry_titre.get()
        result = emprunter_livre(titre)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)
        reset_fields()

    def modifier_livre_ui():
        ancien_titre = entry_titre.get()
        nouveau_titre = entry_nouveau_titre.get()
        auteur = entry_auteur.get()
        genre = entry_genre.get()
        result = modifier_livre(ancien_titre, nouveau_titre, auteur, genre)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)
        reset_fields()

    def retourner_livre_ui():
        titre = entry_titre.get()
        result = retourner_livre(titre)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)
        reset_fields()

    def reset_fields():
        entry_titre.delete(0, tk.END)
        entry_auteur.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_nouveau_titre.delete(0, tk.END)

    fenetre = tk.Tk()
    fenetre.title("Gestion des Livres")

    style = ThemedStyle(fenetre)
    style.set_theme("arc")  # Choix du thème (par exemple "arc")

    frame = ttk.Frame(fenetre, padding=15)
    frame.pack()

    # Champs de saisie
    ttk.Label(frame, text="Titre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entry_titre = ttk.Entry(frame)
    entry_titre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Nouveau Titre (pour modification):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    entry_nouveau_titre = ttk.Entry(frame)
    entry_nouveau_titre.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Auteur:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    entry_auteur = ttk.Entry(frame)
    entry_auteur.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Genre:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    entry_genre = ttk.Entry(frame)
    entry_genre.grid(row=3, column=1, padx=5, pady=5)

    # Boutons
    btn_ajouter = ttk.Button(frame, text="Ajouter Livre", command=ajouter_livre_ui)
    btn_ajouter.grid(row=4, columnspan=2, pady=5)

    btn_afficher = ttk.Button(frame, text="Afficher Tous les Livres", command=afficher_livres_ui)
    btn_afficher.grid(row=5, columnspan=2, pady=5)

    btn_afficher_disponibles = ttk.Button(frame, text="Afficher Livres Disponibles", command=afficher_livres_disponibles_ui)
    btn_afficher_disponibles.grid(row=6, columnspan=2, pady=5)

    btn_supprimer = ttk.Button(frame, text="Supprimer Livre", command=supprimer_livre_ui)
    btn_supprimer.grid(row=7, columnspan=2, pady=5)

    btn_archiver = ttk.Button(frame, text="Archiver Livre", command=archiver_livre_ui)
    btn_archiver.grid(row=8, columnspan=2, pady=5)

    btn_emprunter = ttk.Button(frame, text="Emprunter Livre", command=emprunter_livre_ui)
    btn_emprunter.grid(row=9, columnspan=2, pady=5)

    btn_modifier = ttk.Button(frame, text="Modifier Livre", command=modifier_livre_ui)
    btn_modifier.grid(row=10, columnspan=2, pady=5)

    btn_retourner = ttk.Button(frame, text="Retourner Livre", command=retourner_livre_ui)
    btn_retourner.grid(row=11, columnspan=2, pady=5)

    text_area = tk.Text(fenetre, height=20, width=80)
    text_area.pack(pady=10)

    fenetre.mainloop()

if __name__ == "__main__":
    main()
