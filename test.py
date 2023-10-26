import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import re # Expression régulière pour s'assurer que l'adresse e-mail est dans un format correct

class ContactManager:

    def __init__(self, root):
        # Initialisation de la fenêtre racine
        self.root = root
        self.root.title('Gestionnaire de Contacts')  # Titre de la fenêtre
        self.root.geometry("600x550")  # Définition de la taille de la fenêtre (largeur x hauteur)
        self.root.configure(bg="#e1e5ea")  # Couleur de fond de la fenêtre

        # Variables
        self.contacts = []  # Liste vide pour stocker les contacts

        # Frame pour l'ajout de contacts
        frame = ttk.LabelFrame(self.root, text="Nouveau contact", padding=(20, 10))
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Interface utilisateur pour ajouter un contact
        self.nom_var = tk.StringVar()
        self.prenom_var = tk.StringVar()
        self.num_var = tk.StringVar()
        self.email_var = tk.StringVar()  # Variable pour l'adresse e-mail

        # Étiquettes et champs de saisie pour le nom, le prénom, le numéro de téléphone et l'adresse e-mail
        ttk.Label(frame, text="Nom").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(frame, text="Prénom").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(frame, text="Numéro de téléphone").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(frame, text="Adresse e-mail").grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Champs de saisie pour les informations du contact
        ttk.Entry(frame, textvariable=self.nom_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.prenom_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.num_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.email_var).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Bouton "Ajouter" pour ajouter un contact
        ttk.Button(frame, text="Ajouter", command=self.add_contact).grid(row=4, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

        # Barre de recherche
        self.search_var = tk.StringVar()
        ttk.Label(self.root, text="Rechercher un contact").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.search_var).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(self.root, text="Rechercher", command=self.search_contact).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Liste des contacts
        self.listbox = tk.Listbox(self.root, height=10)
        self.listbox.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Cadre pour les boutons
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.grid(row=3, column=2, padx=10, pady=10, sticky="n")

        # Boutons pour supprimer, modifier et enregistrer les contacts
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_contact).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_buttons, text="Modifier", command=self.modify_contact).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_buttons, text="Enregistrer", command=self.save_contacts).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    # Méthode pour ajouter un contact
    def add_contact(self):
        nom = self.nom_var.get()
        prenom = self.prenom_var.get()
        num = self.num_var.get()
        email = self.email_var.get()
        # Vérification de la validité des données du contact
        if not nom or not prenom or not num or not self.is_valid_email(email):
            messagebox.showerror("Erreur", "Veuillez entrer un mail valide.")
            return
        contact = {"nom": nom, "prenom": prenom, "num": num, "email": email}
        self.contacts.append(contact)
        self.listbox.insert(tk.END, f"{prenom} {nom} ({num}) - {email}")
        self.clear_fields()

    # Méthode pour valider une adresse e-mail avec une expression régulière
    def is_valid_email(self, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email)

    # Méthode pour effacer les champs de saisie
    def clear_fields(self):
        self.nom_var.set("")
        self.prenom_var.set("")
        self.num_var.set("")
        self.email_var.set("")

    # Méthode pour supprimer un contact
    def delete_contact(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.listbox.delete(index)
            del self.contacts[index]

    # Méthode pour modifier un contact
    def modify_contact(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            contact = self.contacts[index]
            self.nom_var.set(contact["nom"])
            self.prenom_var.set(contact["prenom"])
            self.num_var.set(contact["num"])
            self.email_var.set(contact["email"])
            self.delete_contact()

    # Méthode pour afficher les informations détaillées d'un contact
    def edit_contact(self, event):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            contact = self.contacts[index]
            messagebox.showinfo("Informations", f"Nom: {contact['nom']}\nPrénom: {contact['prenom']}\nNuméro: {contact['num']}\nEmail: {contact['email']}")

    # Méthode pour sauvegarder les contacts dans un fichier JSON
    def save_contacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f)
        messagebox.showinfo("Sauvegardé", "Contacts sauvegardés avec succès!")

    # Méthode pour rechercher des contacts
    def search_contact(self):
        query = self.search_var.get().lower()
        results = [contact for contact in self.contacts if query in contact["nom"].lower() or query in contact["prenom"].lower()]
        self.populate_listbox(results)

    # Méthode pour remplir la liste des contacts
    def populate_listbox(self, contacts=None):
        self.listbox.delete(0, tk.END)
        contacts = contacts if contacts is not None else self.contacts
        for contact in contacts:
            self.listbox.insert(tk.END, f"{contact['prenom']} {contact['nom']} ({contact['num']}) - {contact['email']}")

if __name__ == "__main__":
    # Création de la fenêtre racine et de l'instance de ContactManager
    root = tk.Tk()
    app = ContactManager(root)
    # Lancement de la boucle principale de l'interface utilisateur
    root.mainloop()