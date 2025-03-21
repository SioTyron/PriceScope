Requête SQL MAJ DB
##Catégories Rayons
Produits frais : Fruits, légumes, viandes, poissons, produits laitiers (comme le lait, yaourts, fromages), œufs.

Épicerie : Conserves, pâtes, riz, légumineuses, farines, sucre, épices, sauces.

Boissons : Eaux, jus, sodas, boissons alcoolisées (bières, vins, spiritueux).

Boulangerie et pâtisserie : Pain, viennoiseries, gâteaux.

Produits surgelés : Glaces, légumes, viandes, plats préparés.

Snacks et confiseries : Chips, biscuits, chocolats, bonbons.

Hygiène et beauté : Produits de soin du corps, cosmétiques, produits d'hygiène (savons, shampooings, dentifrices).

Entretien et maison : Produits de nettoyage, lessives, articles pour la maison.

Petite alimentation animale : Croquettes, aliments pour animaux de compagnie.

Produits pour bébé : Couches, petits pots, laits infantiles.

Ajouter la catégorie de rayon pour les articles de test

- Ajouter prouits frais

UPDATE articles
SET categorie_Rayon = "Épicerie"
WHERE lib_Article = "ART001";

[connections.mysql]
dialect = "sql"
host = "127.0.0.1"
port = 8888
database = "Price_Scope"
username = "root"
password = "root"
