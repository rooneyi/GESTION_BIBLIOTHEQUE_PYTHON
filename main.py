import tkinter as tk
from tkinter import messagebox, ttk,filedialog
import csv
import json
import os
from ttkthemes import ThemedStyle
import datetime
from Livre import *


def main():
    # Fonctions UI
    def ajouter_livre_ui():
        titre = entry_titre.get()
        auteur = entry_auteur.get()
        genre = entry_genre.get()
        message = ajouter_livre(titre, auteur, genre)
        messagebox.showinfo("Résultat", message)
        enregistrer_transaction("Ajouter", titre)
        afficher_livres_ui()
        reset_fields()

    def afficher_livres_ui():
        for item in tree.get_children():
            tree.delete(item)
        livres = charger_livres()
        for livre in livres:
            tree.insert("", "end", values=(livre['id'], livre['Titre'], livre['Auteur'], livre['Genre'], "Oui" if livre['Disponible'] else "Non"))

    def afficher_livres_disponibles_ui():
        for item in tree.get_children():
            tree.delete(item)
        livres = charger_livres()
        disponibles = [livre for livre in livres if livre['Disponible']]
        for livre in disponibles:
            tree.insert("", "end", values=(livre['id'], livre['Titre'], livre['Auteur'], livre['Genre'], "Oui" if livre['Disponible'] else "Non"))

    def supprimer_livre_ui():
        titre = entry_titre.get()
        result = supprimer_livre_definitivement(titre)
        messagebox.showinfo("Résultat", result)
        enregistrer_transaction("Supprimer", titre)
        afficher_livres_ui()
        reset_fields()

    def archiver_livre_ui():
        titre = entry_titre.get()
        result = archiver_livre(titre)
        messagebox.showinfo("Résultat", result)
        enregistrer_transaction("Archiver", titre)
        afficher_livres_ui()
        reset_fields()

    def emprunter_livre_ui():
        titre = entry_titre.get()
        result = emprunter_livre(titre)
        messagebox.showinfo("Résultat", result)
        enregistrer_transaction("Emprunter", titre)
        afficher_livres_ui()
        reset_fields()

    def modifier_livre_ui():
        ancien_titre = entry_titre.get()
        auteur = entry_auteur.get()
        genre = entry_genre.get()
        result = modifier_livre(ancien_titre, auteur, genre)
        messagebox.showinfo("Résultat", result)
        enregistrer_transaction("Modifier", ancien_titre)
        afficher_livres_ui()
        reset_fields()

    def retourner_livre_ui():
        titre = entry_titre.get()
        result = retourner_livre(titre)
        messagebox.showinfo("Résultat", result)
        enregistrer_transaction("Retourner", titre)
        afficher_livres_ui()
        reset_fields()
    def importer_csv():
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        titre = row['Titre']
                        auteur = row['Auteur']
                        genre = row['Genre']
                        ajouter_livre(titre, auteur, genre)
                messagebox.showinfo("Importation réussie", "Les livres ont été importés avec succès.")
                afficher_livres_ui()
            except Exception as e:
                messagebox.showerror("Erreur lors de l'importation", f"Une erreur est survenue : {str(e)}")
    def enregistrer_transaction(action, titre):
        transaction = {
            "Action": action,
            "Livre": titre,
            "Date": str(datetime.datetime.now())
        }
        sauvegarder_transaction(transaction)

    def reset_fields():
        entry_titre.delete(0, tk.END)
        entry_auteur.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_nouveau_titre.delete(0, tk.END)

    # Configuration de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Gestion des Livres")

    style = ThemedStyle(fenetre)
    style.set_theme("arc")

    # Titre principal
    ttk.Label(fenetre, text="Gestion des Livres", font=("Helvetica", 16)).pack(pady=10)

    frame = ttk.Frame(fenetre, padding=15)
    frame.pack()

    # Champs de saisie
    input_frame = ttk.LabelFrame(frame, text="Informations sur le livre")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    ttk.Label(input_frame, text="Titre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entry_titre = ttk.Entry(input_frame)
    entry_titre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Nouveau Titre (pour modification):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    entry_nouveau_titre = ttk.Entry(input_frame)
    entry_nouveau_titre.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Auteur:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    entry_auteur = ttk.Entry(input_frame)
    entry_auteur.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Genre:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    entry_genre = ttk.Entry(input_frame)
    entry_genre.grid(row=3, column=1, padx=5, pady=5)

    # Boutons d'action
    button_frame = ttk.LabelFrame(frame, text="Actions")
    button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    action_buttons = [
        ("Ajouter Livre", ajouter_livre_ui, "success.TButton"),
        ("Modifier Livre", modifier_livre_ui, "info.TButton"),
        ("Supprimer Livre", supprimer_livre_ui, "danger.TButton"),
        ("Archiver Livre", archiver_livre_ui, "warning.TButton"),
        ("Emprunter Livre", emprunter_livre_ui, "info.TButton"),
        ("Retourner Livre", retourner_livre_ui, "primary.TButton")
    ]

    display_buttons = [
        ("Afficher Tous les Livres", afficher_livres_ui),
        ("Afficher Livres Disponibles", afficher_livres_disponibles_ui)
    ]

    for idx, (text, command, style) in enumerate(action_buttons):
        btn = ttk.Button(button_frame, text=text, command=command, style=style)
        btn.grid(row=idx, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

    for idx, (text, command) in enumerate(display_buttons):
        btn = ttk.Button(button_frame, text=text, command=command)
        btn.grid(row=len(action_buttons) + idx, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

    # Ajouter styles pour les boutons colorés
    s = ttk.Style()
    s.configure("success.TButton", background="#5cb85c", foreground="white")
    s.configure("danger.TButton", background="#d9534f", foreground="white")
    s.configure("info.TButton", background="#5bc0de", foreground="white")
    s.configure("warning.TButton", background="#f0ad4e", foreground="white")
    s.configure("primary.TButton", background="#0275d8", foreground="white")

    # Table pour afficher les livres
    columns = ("ID", "Titre", "Auteur", "Genre", "Disponible")
    tree = ttk.Treeview(fenetre, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Titre", text="Titre")
    tree.heading("Auteur", text="Auteur")
    tree.heading("Genre", text="Genre")
    tree.heading("Disponible", text="Disponible")
    tree.pack(pady=10)

    afficher_livres_ui()  # Afficher les livres au démarrage

    fenetre.mainloop()

if __name__ == "__main__":
    main()