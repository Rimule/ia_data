											Notice readme

###############################################################################################################################################

Contexte :

L'objectif de nos séance était de produire un IDS intelligent afin de faire une veille sur le réseau sur lequel il est connecté. Pour cela, on a utilisé les outils suivants :

	-Elasticsearch (kibana, filebeat)
	-Iptables
	-Machine learning avec python.

Pour la partie machine learning, nous utiliserons un apprentissage supervisé en utilisant du One Hot encoding.
###############################################################################################################################################

Comment ça fonctionne :

Dans un premier temps, iptables récupère les des informations en fonctions des règles établie. Ces données sont enregistrées dans un fichier spécifique. Ce fichier est ensuite traité
par logstash afin de pouvoir être compris et utilisé dans elasticsearch et dans kibana. Ces données seront affiché dans Kibana et enregistré dans elastic.

Dans un second temps, avec un script python, nous allons créer une IA qui va récupérer les informations enregistré dans elastic et s'en servir. Dans un premier temps, on les encode
en fonction de règles de test pour ensuite faire apprendre a notre IA comment reconnaitre un traffic légitime et un traffic illégitime dans un premier temps. 

Pour lancer un test :

	-modifier légèrement le code pour le lier au fichier.csv
	-lancer le test.
Pour le faire avec votre Logstash/Elastic, il vous fait entrer la ligne sur la photo2

###############################################################################################################################################

Résultat :

On arrive a voir les données saisies dans notre Kibana et Elastic. Avec le fichier de log suivant, on obtient un score de 0.98% de réussite selon 3 types d'information reçu. Dans l'idéal,
on pourrais rajouter des types d'attaques, des critères de filtrage ainsi que de nouvelles ips.

#################################################################################################################################################

Conclusion : 

Ce projet était interessant car il mèle deux discpline différentes et les lies pour faire de la sécurité. Ce projet cependant peut être amélioré et avec un peu plus de temps,
nous pourrions faire un vrai système capable de voir tous ce qu'il ne va pas.

##################################################################################################################################################
 


