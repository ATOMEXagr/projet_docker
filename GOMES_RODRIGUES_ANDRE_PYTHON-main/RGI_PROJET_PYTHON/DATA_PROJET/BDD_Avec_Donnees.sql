#------------------------------------------------------------
#        Base de données
#        Dernière vérification - 20 06 2024
#------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS reservation_rdv_promeo;
USE reservation_rdv_promeo;

DROP TABLE IF EXISTS Creneaux_Reservations;
DROP TABLE IF EXISTS Formateurs;
DROP TABLE IF EXISTS Alternants;
DROP TABLE IF EXISTS Formation;
DROP TABLE IF EXISTS Lieu_Formation;

#------------------------------------------------------------
# Table: Lieu_Formation
#------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Lieu_Formation (
    id_lieu INT AUTO_INCREMENT NOT NULL,
    nom_lieu VARCHAR(50) NOT NULL,
    CONSTRAINT Lieu_formation_PK PRIMARY KEY (id_lieu)
) ENGINE=InnoDB;

#------------------------------------------------------------
# Table: Formation
#------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Formation (
    id_formation INT AUTO_INCREMENT NOT NULL,
    nom_formation VARCHAR(50) NOT NULL,
    CONSTRAINT Formation_PK PRIMARY KEY (id_formation)
) ENGINE=InnoDB;

#------------------------------------------------------------
# Table: Alternants
#------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Alternants (
    id_alternant INT AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL,
    id_formation INT NOT NULL,
    id_lieu INT NOT NULL,
    email VARCHAR(70) NOT NULL,
    CONSTRAINT Alternants_PK PRIMARY KEY (id_alternant),
    CONSTRAINT Alternants_Formation0_FK FOREIGN KEY (id_formation) REFERENCES Formation(id_formation),
    CONSTRAINT Alternants_Lieu_formation_FK FOREIGN KEY (id_lieu) REFERENCES Lieu_Formation(id_lieu)
) ENGINE=InnoDB;

#------------------------------------------------------------
# Table: Formateurs
#------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Formateurs (
    id_formateur INT AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL,
    id_formation INT NOT NULL,
    id_lieu INT NOT NULL,
    email VARCHAR(70) NOT NULL,
    CONSTRAINT Formateurs_PK PRIMARY KEY (id_formateur),
    CONSTRAINT Formateurs_Formation_FK FOREIGN KEY (id_formation) REFERENCES Formation(id_formation),
    CONSTRAINT Formateurs_Lieu_formation0_FK FOREIGN KEY (id_lieu) REFERENCES Lieu_Formation(id_lieu)
) ENGINE=InnoDB;

#------------------------------------------------------------
# Table: Creneaux_Reservations
#------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Creneaux_Reservations (
    id_reservation INT AUTO_INCREMENT NOT NULL,
    date_reservation DATE NOT NULL,
    horaire_reservation VARCHAR(50) NOT NULL,
    etat_reservation BOOL NOT NULL,
    id_alternant INT,
    id_formateur INT NOT NULL,
    CONSTRAINT Creneaux_Reservations_PK PRIMARY KEY (id_reservation),
    CONSTRAINT Creneaux_Reservations_Alternants_FK FOREIGN KEY (id_alternant) REFERENCES Alternants(id_alternant),
    CONSTRAINT Creneaux_Reservations_Formateurs0_FK FOREIGN KEY (id_formateur) REFERENCES Formateurs(id_formateur)
) ENGINE=InnoDB;

-- Insérer des données dans la table Lieu_Formation
INSERT INTO Lieu_Formation (id_lieu, nom_lieu) VALUES
    (1, 'BEAUVAIS'),
    (2, 'COMPIEGNE'),
    (3, 'Centre de Formation Alpha'),
    (4, 'Institut Beta'),
    (5, 'École Gamma');

-- Insérer des données dans la table Formation
INSERT INTO Formation (id_formation, nom_formation) VALUES
    (1, 'RGI'),
    (2, 'CYBER'),
    (3, 'Développement Web'),
    (4, 'Data Science'),
    (5, 'Gestion de Projet');

-- Insérer des données dans la table Alternants
INSERT INTO Alternants (id_alternant, nom, prenom, username, password, id_lieu, id_formation, email) VALUES
    (1, 'DECOCHEREAUX', 'LOIC', 'loicd', 'e37f0136aa3ffaf149b351f6a4c948e9', 1, 2, 'loic.decochereaux@gmail.com'),
    (2, 'GOMES RODRIGUES', 'André', 'andreg', 'a0fb2daa33c637d078d1d276dd453ea2', 1, 2, 'zxagrxz@gmail.com'),
    (3, 'Dupont', 'Jean', 'jean_dupont', '5a7e42bc6e6f87048ca5d5fe55b0d1eb', 1, 1, 'loic.decochereaux@gmail.com'),
    (4, 'Durand', 'Marie', 'marie_durand', '7379217c1f17f3aafebe7ae720d3ae11', 2, 2, 'loic.decochereaux@gmail.com'),
    (5, 'Martin', 'Luc', 'luc_martin', '85aba739c42c7913f059dbd4e06f198d', 3, 3, 'loic.decochereaux@gmail.com');

-- Insérer des données dans la table Formateurs
INSERT INTO Formateurs (id_formateur, nom, prenom, username, password, id_formation, id_lieu, email) VALUES
    (1, 'DELPECH', 'Nicolas', 'nicod', '47bce5c74f589f4867dbd57e9ca9f808', 2, 1, 'loic.decochereaux@gmail.com'),
    (2, 'BERHAULT', 'William', 'willb', '08f8e0260c64418510cefb2b06eee5cd', 2, 1, 'loic.decochereaux@gmail.com'),
    (3, 'Tremblay', 'Sophie', 'sophie_tremblay', '5a7e42bc6e6f87048ca5d5fe55b0d1eb', 1, 1, 'loic.decochereaux@promeo-alternaute.fr'),
    (4, 'Gagnon', 'Pierre', 'pierre_gagnon', '7379217c1f17f3aafebe7ae720d3ae11', 2, 2, 'loic.decochereaux@promeo-alternaute.fr'),
    (5, 'Roy', 'Isabelle', 'isabelle_roy', '85aba739c42c7913f059dbd4e06f198d', 3, 3, 'loic.decochereaux@promeo-alternaute.fr');

-- Insérer des données dans la table Creneaux_Reservations
INSERT INTO Creneaux_Reservations (id_reservation, date_reservation, horaire_reservation, etat_reservation, id_alternant, id_formateur) VALUES
    (10, '2024-06-08', '09:30-11:00', TRUE, 1, 1),
    (14, '2024-06-06', '11:00-12:30', FALSE, NULL, 1),
    (15, '2024-06-15', '11:00-12:30', TRUE, 1, 1),
    (16, '2024-06-16', '08:00-09:30', TRUE, 2, 2),
    (17, '2024-06-17', '16:30-18:00', TRUE, 3, 3);
