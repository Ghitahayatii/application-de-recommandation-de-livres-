import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import os

class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Recommandations de Livres 🎯")
        self.root.geometry("900x650")
        
        # Palette de couleurs professionnelles
        self.colors = {
            "primary": "#1a237e",     # Bleu foncé
            "secondary": "#5c6bc0",   # Bleu moyen
            "accent": "#7986cb",      # Bleu clair
            "background": "#f5f5f5",  # Gris très clair
            "text": "#212121",        # Gris très foncé
            "light_text": "#757575",  # Gris moyen
            "white": "#ffffff"        # Blanc
        }
        
        self.root.configure(bg=self.colors["background"])
        
        # Initialiser la base de données
        self.create_database()
        
        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TButton", 
                            font=("Helvetica", 12),
                            background=self.colors["primary"], 
                            foreground=self.colors["white"])
        self.style.map("TButton",
                      background=[('active', self.colors["secondary"])],
                      foreground=[('active', self.colors["white"])])
        self.style.configure("TLabel", 
                            font=("Helvetica", 12),
                            background=self.colors["background"],
                            foreground=self.colors["text"])
        self.style.configure("Header.TLabel", 
                            font=("Helvetica", 24, "bold"),
                            background=self.colors["background"],
                            foreground=self.colors["primary"])
        self.style.configure("Result.TFrame",
                            background=self.colors["white"])
        self.style.configure("Result.TLabel", 
                            font=("Helvetica", 12),
                            background=self.colors["white"],
                            foreground=self.colors["text"],
                            wraplength=700)
        self.style.configure("Subtitle.TLabel", 
                            font=("Helvetica", 14),
                            background=self.colors["background"],
                            foreground=self.colors["light_text"])
        
        self.create_widgets()
    
    def create_database(self):
        """Créer et initialiser la base de données SQLite"""
        # Vérifier si le fichier de base de données existe déjà
        db_exists = os.path.exists("livres.db")
        
        # Créer ou connecter à la base de données
        self.conn = sqlite3.connect("livres.db")
        self.cursor = self.conn.cursor()
        
        # Si la base de données n'existe pas, créer les tables et ajouter des données
        if not db_exists:
            # Créer les tables
            self.cursor.execute('''
                CREATE TABLE genres (
                    id INTEGER PRIMARY KEY,
                    nom TEXT UNIQUE
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE livres (
                    id INTEGER PRIMARY KEY,
                    titre TEXT NOT NULL,
                    auteur TEXT NOT NULL,
                    description TEXT,
                    genre_id INTEGER,
                    annee_publication INTEGER,
                    note REAL,
                    FOREIGN KEY (genre_id) REFERENCES genres (id)
                )
            ''')
            
            # Insérer les genres
            genres = ["Roman", "Science-Fiction", "Fantaisie", "Policier", "Non-Fiction", "Biographie", "Poésie"]
            for genre in genres:
                self.cursor.execute("INSERT INTO genres (nom) VALUES (?)", (genre,))
            
            # Insérer les livres
            livres = [
                # Romans
                ("L'Étranger", "Albert Camus", "Un homme qui assiste à l'enterrement de sa mère sans manifester de tristesse, puis tue un Arabe sur une plage.", 1, 1942, 4.8),
                ("Les Misérables", "Victor Hugo", "L'histoire de Jean Valjean, un ancien forçat qui tente de se racheter.", 1, 1862, 4.7),
                ("Le Petit Prince", "Antoine de Saint-Exupéry", "Un conte poétique sur un petit prince qui visite différentes planètes.", 1, 1943, 4.9),
                ("Notre-Dame de Paris", "Victor Hugo", "L'histoire de Quasimodo, le sonneur bossu de Notre-Dame, et de la belle Esmeralda.", 1, 1831, 4.5),
                ("Madame Bovary", "Gustave Flaubert", "L'histoire d'Emma Bovary qui s'ennuie dans son mariage et cherche le bonheur dans des liaisons amoureuses.", 1, 1857, 4.6),
                
                # Science-Fiction
                ("Dune", "Frank Herbert", "L'histoire de Paul Atréides sur la planète désertique Arrakis, source de l'épice la plus précieuse de l'univers.", 2, 1965, 4.8),
                ("Fondation", "Isaac Asimov", "L'effondrement d'un empire galactique et la création d'une fondation pour préserver le savoir.", 2, 1951, 4.7),
                ("Neuromancien", "William Gibson", "Un hacker engagé pour une mission mystérieuse dans un futur cyberpunk.", 2, 1984, 4.5),
                ("Le Guide du voyageur galactique", "Douglas Adams", "Les aventures de Arthur Dent à travers la galaxie après la destruction de la Terre.", 2, 1979, 4.8),
                ("1984", "George Orwell", "Une dystopie totalitaire où la pensée est contrôlée par le gouvernement.", 2, 1949, 4.9),
                
                # Fantaisie
                ("Le Seigneur des Anneaux", "J.R.R. Tolkien", "L'épopée de Frodon Sacquet pour détruire l'Anneau unique et vaincre Sauron.", 3, 1954, 4.9),
                ("Harry Potter à l'école des sorciers", "J.K. Rowling", "Les aventures d'un jeune sorcier qui découvre un monde magique.", 3, 1997, 4.8),
                ("Le Nom du Vent", "Patrick Rothfuss", "L'histoire de Kvothe, un musicien devenu mage, guerrier et assassin.", 3, 2007, 4.7),
                ("Les Chroniques de Narnia", "C.S. Lewis", "Des enfants découvrent un monde magique accessible à travers une armoire.", 3, 1950, 4.7),
                ("American Gods", "Neil Gaiman", "Une guerre entre les anciens dieux et les nouveaux dieux de la technologie et des médias.", 3, 2001, 4.6),
                
                # Policier
                ("Les Dix Petits Nègres", "Agatha Christie", "Dix personnes invitées sur une île sont accusées de crimes et commencent à mourir une par une.", 4, 1939, 4.7),
                ("Le Chien des Baskerville", "Arthur Conan Doyle", "Sherlock Holmes enquête sur une malédiction impliquant un chien démoniaque.", 4, 1902, 4.8),
                ("Millénium", "Stieg Larsson", "Un journaliste et une hackeuse enquêtent sur des crimes en Suède.", 4, 2005, 4.6),
                ("Maigret et le corps sans tête", "Georges Simenon", "Le commissaire Maigret enquête sur un cadavre démembré trouvé dans le canal.", 4, 1955, 4.5),
                ("Le Silence des agneaux", "Thomas Harris", "Une jeune recrue du FBI cherche l'aide d'un tueur en série cannibale pour en capturer un autre.", 4, 1988, 4.8),
                
                # Non-Fiction
                ("Sapiens: Une brève histoire de l'humanité", "Yuval Noah Harari", "L'histoire de l'humanité, de l'âge de pierre jusqu'à l'ère contemporaine.", 5, 2011, 4.8),
                ("L'Art de la guerre", "Sun Tzu", "Un ancien traité militaire chinois sur la stratégie et la tactique.", 5, -500, 4.7),
                ("De l'origine des espèces", "Charles Darwin", "La théorie de l'évolution par la sélection naturelle.", 5, 1859, 4.9),
                ("Une vie", "Simone Veil", "L'autobiographie d'une femme politique française qui a survécu à l'Holocauste.", 5, 2007, 4.8),
                ("Le Journal d'Anne Frank", "Anne Frank", "Le journal intime d'une adolescente juive cachée pendant l'occupation nazie.", 5, 1947, 4.9),
                
                # Biographie
                ("Steve Jobs", "Walter Isaacson", "La biographie officielle du fondateur d'Apple.", 6, 2011, 4.7),
                ("Moi, Malala", "Malala Yousafzai", "L'histoire de la plus jeune lauréate du prix Nobel de la paix.", 6, 2013, 4.8),
                ("Les Confessions", "Jean-Jacques Rousseau", "Une autobiographie philosophique.", 6, 1782, 4.6),
                ("Mandela : Un long chemin vers la liberté", "Nelson Mandela", "L'autobiographie de l'homme qui a lutté contre l'apartheid.", 6, 1994, 4.9),
                ("Marie Curie", "Eve Curie", "La biographie de la scientifique écrite par sa fille.", 6, 1937, 4.5),
                
                # Poésie
                ("Les Fleurs du mal", "Charles Baudelaire", "Un recueil de poèmes sur la beauté, l'ennui, le temps qui passe.", 7, 1857, 4.8),
                ("Alcools", "Guillaume Apollinaire", "Un recueil poétique qui mélange tradition et modernité.", 7, 1913, 4.7),
                ("Les Contemplations", "Victor Hugo", "Un recueil de poèmes lyriques sur la vie, la mort et l'amour.", 7, 1856, 4.6),
                ("Illuminations", "Arthur Rimbaud", "Un recueil de poèmes en prose visionnaires.", 7, 1886, 4.7),
                ("Paroles", "Jacques Prévert", "Des poèmes simples et touchants sur la vie quotidienne.", 7, 1946, 4.8)
            ]
            
            for livre in livres:
                self.cursor.execute('''
                    INSERT INTO livres (titre, auteur, description, genre_id, annee_publication, note)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', livre)
            
            # Sauvegarder les changements
            self.conn.commit()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Titre
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=20)
        
        title_label = ttk.Label(header_frame, 
                                text="Application de Recommandations de Livres 🎯", 
                                style="Header.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                text="Trouvez votre prochaine lecture préférée!", 
                                style="Subtitle.TLabel")
        subtitle_label.pack(pady=10)
        
        # Frame de sélection
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=20)
        
        # Sélection du genre
        genre_label = ttk.Label(selection_frame, text="Genre:", font=("Helvetica", 12, "bold"))
        genre_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        # Récupérer les genres depuis la base de données
        self.cursor.execute("SELECT nom FROM genres ORDER BY nom")
        genres = [row[0] for row in self.cursor.fetchall()]
        
        self.genre_var = tk.StringVar()
        self.genre_combobox = ttk.Combobox(selection_frame, 
                                          textvariable=self.genre_var, 
                                          values=genres,
                                          width=25,
                                          font=("Helvetica", 12))
        self.genre_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.genre_combobox.current(0)
        
        # Note minimale
        note_label = ttk.Label(selection_frame, text="Note minimale:", font=("Helvetica", 12, "bold"))
        note_label.grid(row=0, column=2, padx=(30, 10), pady=10, sticky=tk.W)
        
        self.note_var = tk.DoubleVar(value=4.0)
        note_scale = ttk.Scale(selection_frame, 
                              from_=1.0, 
                              to=5.0, 
                              orient="horizontal", 
                              variable=self.note_var,
                              length=150)
        note_scale.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)
        
        self.note_label = ttk.Label(selection_frame, textvariable=self.note_var)
        self.note_label.grid(row=0, column=4, padx=5, pady=10, sticky=tk.W)
        
        # Actualiser l'affichage de la note
        def update_note_label(*args):
            self.note_label.config(text=f"{self.note_var.get():.1f}")
        
        self.note_var.trace("w", update_note_label)
        update_note_label()
        
        # Bouton de recommandation
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        recommendation_button = tk.Button(button_frame, 
                                         text="Recommander un livre", 
                                         command=self.recommend_book,
                                         font=("Helvetica", 12, "bold"),
                                         bg=self.colors["primary"],
                                         fg=self.colors["white"],
                                         activebackground=self.colors["secondary"],
                                         activeforeground=self.colors["white"],
                                         padx=15,
                                         pady=8,
                                         relief=tk.RAISED,
                                         borderwidth=2)
        recommendation_button.pack(pady=10)
        
        # Frame de résultat
        result_outer_frame = ttk.Frame(main_frame)
        result_outer_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_frame = ttk.Frame(result_outer_frame, style="Result.TFrame")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2, ipadx=20, ipady=20)
        
        # Labels pour afficher la recommandation
        self.result_title = ttk.Label(self.result_frame, text="", style="Result.TLabel", font=("Helvetica", 18, "bold"))
        self.result_title.pack(fill=tk.X, pady=5)
        
        self.result_author = ttk.Label(self.result_frame, text="", style="Result.TLabel", font=("Helvetica", 14, "italic"))
        self.result_author.pack(fill=tk.X, pady=5)
        
        self.result_extra = ttk.Label(self.result_frame, text="", style="Result.TLabel")
        self.result_extra.pack(fill=tk.X, pady=5)
        
        self.result_description = ttk.Label(self.result_frame, text="", style="Result.TLabel")
        self.result_description.pack(fill=tk.X, pady=10)
        
        # Label statistiques
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, 
                                   text="Base de données: 0 livres dans 0 genres", 
                                   font=("Helvetica", 10, "italic"),
                                   foreground=self.colors["light_text"])
        self.stats_label.pack(side=tk.LEFT, padx=5)
        
        # Mettre à jour les statistiques
        self.update_stats()
        
        # Label décoratif
        footer_label = ttk.Label(main_frame, 
                               text="📚 Bonne lecture! 📚", 
                               font=("Helvetica", 12, "italic"),
                               foreground=self.colors["secondary"])
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def update_stats(self):
        """Mettre à jour les statistiques de la base de données"""
        self.cursor.execute("SELECT COUNT(*) FROM livres")
        livre_count = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM genres")
        genre_count = self.cursor.fetchone()[0]
        
        self.stats_label.config(text=f"Base de données: {livre_count} livres dans {genre_count} genres")
    
    def recommend_book(self):
        """Recommander un livre selon les critères sélectionnés"""
        selected_genre = self.genre_var.get()
        min_note = self.note_var.get()
        
        try:
            # Récupérer l'ID du genre
            self.cursor.execute("SELECT id FROM genres WHERE nom = ?", (selected_genre,))
            genre_id = self.cursor.fetchone()[0]
            
            # Récupérer tous les livres qui correspondent aux critères
            self.cursor.execute('''
                SELECT titre, auteur, description, annee_publication, note
                FROM livres
                WHERE genre_id = ? AND note >= ?
            ''', (genre_id, min_note))
            
            livres = self.cursor.fetchall()
            
            if livres:
                # Choisir un livre aléatoire
                random_book = random.choice(livres)
                titre, auteur, description, annee, note = random_book
                
                # Mettre à jour les labels avec la recommandation
                self.result_title.configure(text=titre)
                self.result_author.configure(text=f"par {auteur}")
                self.result_extra.configure(text=f"Année: {annee} | Note: {'⭐' * int(note)}")
                self.result_description.configure(text=description)
                
                # Ajouter un effet visuel
                self.result_frame.configure(style="Result.TFrame")
                self.root.update()
            else:
                messagebox.showinfo("Aucun livre trouvé", 
                                    f"Aucun livre du genre '{selected_genre}' avec une note d'au moins {min_note:.1f} n'a été trouvé.\n\nEssayez de réduire la note minimale.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def __del__(self):
        """Fermer la connexion à la base de données à la fermeture de l'application"""
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()