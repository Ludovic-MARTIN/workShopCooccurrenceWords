# workShopCooccurrenceWords

Trois notebooks composent le projet, à cela s’ajoute un module python rassemblant les fonctions factorisant autant que possible l’implémentation du projet.

Ngc_claims-data-exploration : ce notebook n’est qu’une pré-étude de la modélisation mais il a permis de :
-	Explorer les données afin de développer ma sensibilité à la problématique
-	Etudier le clustering et analyser les outliers 
Le clustering n’a pas produit d’effets très expressifs, la réduction par composantes principales a sélectionnée plus de 50 dimensions non visuellement exploitables. Le KMeans++ n’a rien révélé à mes yeux, enfin la densité de points a permis d’identifier un état stable à 9 clusters.
L’application de ce nombre de cluster par KMeans++ fait parfois apparaître des départements proches. Ceci peut toutefois n’être qu’un mirage quant à la raison du rapprochement de ces points, nous pourrions tout aussi bien considérer que les densités de population, la typologie des commerces rapproches ces observations. La grande difficulté de notre analyse est de devoir analyser ces proximités alors que nous rapprochons potentiellement des observations de sinistres de types différents. Ces types de sinsitres étant anonyme, toute interprétation doit être relativisée.

-	Identifier et traiter les valorisations de catégories sous représentées
-	Gérer les valeurs manquantes 
-	Collecter des données externes et générer de nouvelles variables par fusion de lignes et calculs tels que des ratios (ex : Nombre de femmes par Homme) ou autres interactions (ex : sommes des sinistres de tous types par département, nombres de sinistres * temps d’exposition)
-	Analyser le déséquilibre des classes target et tentatives d’équilibrage par oversampling et undersampling. 



Ngc_claims-data-modelization-withoutInsee:
Certaines observations ne disposent pas de données INSEE, il n’y a aucun moyen de reconstituer cette donnée ; ainsi j’ai choisi de modéliser différemment ces observations de celles disposant de données INSEE que l’on peut enrichir de données externes liées à la localité.
La distribution de Poisson nous aurait permis d’exploiter l’exposition par offset, nous avons néanmoins opté pour une modélisation par arbre, en particulier par xgboost qui a produit des résultats supérieurs aux forêts aléatoires. Ce choix a été motivé essentiellement pour des raisons de dimension, environ 50 variables pour le modèle sans code Insee.
La variable exposition a été utilisée dans la construction de nouvelles variables. 
Dans les deux notebooks de modélisations une validation croisée à deux couches a été appliquée. L’une pour définir les hyperparamètres, l’autre pour définir la qualité du modèle généré encadré. Nous avons toutefois noté l’écart type de la qualité de prédiction produite dans les KFold comme approximation de l’écart type du modèle final.
Notons que les outliers n’ont été supprimés que sur le champ de données d’entraînement, ces points ont été conservé dans le datasets de test afin de reproduire des performances réelles.

Ngc_claims-data-modelization:
Dans ce notebook la sélection de variable a fait l’objet d’un travail spécifique au regard de ce qui a été fait dans la modélisation sans données de localité. Pour cela un premier modèle avec des hyper paramètres tiré au hasard a permis de lister les variables par importance. J’ai ensuite sélectionné ces variables en comparant les modèles 2 à 2 (avec et sans une nouvelle variable) dans l’ordre décroissant de l’importance des variables. Pour comparer les modèles, une estimation moyenne des modèles sur 4 Folders a été produite. 
La création de variables a également été davantage travaillée, en particulier j’ai tenté de reproduire le comportement d’un modèle ensembliste reposant sur des modèles relativement simples avec un encodage de la moyenne. Pour mettre en œuvre ces modèles produisant chacun une nouvelle variable, j’ai imputé une moyenne de la variable target en fonction d’un périmètre, par exemple le département, par validation croisée. S’il se trouve qu’une catégorie s’est à un moment de la validation croisée retrouvée isolé dans le folder d’imputation toute les lignes attachées à cette valorisation de catégorie aura produit des valeurs nulles sur la nouvelle variable. Alors c’est la moyenne générale qui permet d’imputer ces lignes.
J’ai ensuite procédé à une recherche des hyper paramètres.
