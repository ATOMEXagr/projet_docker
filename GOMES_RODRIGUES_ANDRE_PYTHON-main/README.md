Projet de Réservation de Créneaux de Formation


Ce projet a été réalisé dans le cadre de notre formation en développement web pour mettre en pratique nos compétences en programmation, gestion de base de données et développement d'application web avec Flask. L'application permet aux alternants de réserver des créneaux de formation avec des formateurs.

Auteurs

	DECOCHEREAUX LOÏC - RGI24

	GOMES RODRIGUES ANDRÉ - RGI24


Cette application de réservation de créneaux de formation permet aux alternants de rechercher des formateurs disponibles, réserver des créneaux et recevoir des notifications par email. Les formateurs peuvent également gérer leurs disponibilités et recevoir des notifications des réservations et annulations.

Fonctionnalités

	Alternants :
	
		Rechercher des formateurs par lieu et formation
		Réserver des créneaux disponibles
		Annuler des réservations
		Recevoir des notifications par email
  
	Formateurs :

     		Ajouter des réservations réservable par les alternants
       		Annuler ses réservations disponibles ou prises
	 	Recevoir un mail de réservation ou d'annulation


Utilisation
	Page d'accueil : Permet de se connecter ou de s'inscrire
	Tableau de bord : Accès aux fonctionnalités de réservation et gestion des créneaux
	Structure de la Base de Données
	Le fichier database_structure.sql contient la structure de la base de données sans données d'exemple. Il définit les tables suivantes :

		Lieu_formation
		Formation
		Alternants
		Formateurs
		Creneaux_Reservations
		
Le fichier database_data.sql contient des données fictives pour illustrer l'utilisation de l'application. Ces données comprennent :
		
		Des lieux de formation
		Des formations
		Des utilisateurs (alternants et formateurs)
		Des réservations de créneaux
		Identifiants de Connexion
		
Le fichier identifiants_connexion.pdf fourni dans le dépôt contient les identifiants de connexion pour les comptes alternants et formateurs de démonstration.
