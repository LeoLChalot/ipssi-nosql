# À propos du Dataset...

## Overview

Le dataset du Bulletin d'Analyse des Accidents Corporels de la circulation routière (Fichier BAAC) se compose de quatre fichiers distincts, chacun contenant des informations spécifiques sur les accidents corporels en France. Voici une brève description de chaque fichier :

- Fichier "*caracteristiques.csv*" : Ce fichier contient les caractéristiques générales de chaque accident. Il inclut des informations telles que la date, l'heure et le lieu de l'accident, ainsi que des détails sur les circonstances particulières, comme les conditions météorologiques, l'éclairage et l'état de la route.

- Fichier "*lieux.csv*" : Ce fichier contient des données sur les lieux où les accidents se sont produits. Il comprend des informations sur le type de route (autoroute, route nationale, route départementale, etc.), la configuration du carrefour, les zones urbaines ou rurales, et d'autres détails géographiques.

- Fichier "*vehicules.csv*" : Ce fichier contient des informations sur les véhicules impliqués dans chaque accident. Il comprend des détails tels que le type de véhicule (voiture, moto, camion, etc.), la catégorie du véhicule (véhicule léger, poids lourd, etc.), et des informations sur les dommages subis par les véhicules.

- Fichier "*usagers.csv*" : Ce fichier contient des données sur les usagers impliqués dans chaque accident. Il inclut des informations sur le type d'usager (conducteur, passager, piéton, cycliste, etc.), l'âge, le sexe et le rôle de chaque usager dans l'accident.

## Liste complète des champs avec le détail de leur contenu pour chaque fichier

### `caracteristiques.csv`

| Libellé   | Détail                                                            |
|:----------|:------------------------------------------------------------------|
| Num_Acc   | Numéro d'identifiant de l’accident                                |
| jour      | Jour de l'accident                                                |
| mois      | Mois de l'accident                                                |
| an        | Année de l'accident                                               |
| hrmn      | Heure et minutes de l'accident                                    |
| lum       | Conditions d'éclairage dans lesquelles l'accident a eu lieu       |
| dep       | Département (code INSEE département)                              |
| com       | Commune (code INSEE département + 3 chiffres)                     |
| agg       | Localisation                                                      |
| int       | Type d'intersection                                               |
| atm       | Conditions atmosphériques                                         |
| col       | Type de collision                                                 |
| adr       | Adresse postale (accidents en agglomération )                     |
| lat       | Latitude                                                          |
| long      | Longitude                                                         |

### `lieux.csv`

| Libellé   | Détail                                                                    |
|:----------|:--------------------------------------------------------------------------|
| Num_Acc   | Numéro d'identifiant de l’accident                                        |
| catr      | Catégorie de la route                                                     |
| voie      | Numéro de la route                                                        |
| V1        | Indice numérique du numéro de route (exemple : 2 bis, 3 ter etc.)         |
| V2        | Lettre indice alphanumérique de la route                                  |
| circ      | Régime de circulation                                                     |
| nbv       | Nombre total de voies de circulation                                      |
| vosp      | Signale l’existence d’une voie réservée                                   |
| prof      | Profil en long décrit la déclivité de la route à l'endroit de l'accident  |
| pr        | Numéro du PR de rattachement                                              |
| pr1       | Distance en mètres du PR                                                  |
| plan      | Tracé du plan                                                             |
| larrout   | Largeur de la chaussée affectée à la circulation                          |
| surf      | Etat de la surface                                                        |
| infra     | Aménagement - Infrastructure                                              |
| situ      | Situation de l’accident                                                   |
| vma       | Vitesse maximale autorisée sur le lieu et au moment de l'accident         |

### `vehicules.csv`

| Libellé       | Détail                                                                                    |
|:--------------|:------------------------------------------------------------------------------------------|
| Num_Acc       | Numéro d'identifiant de l’accident                                                        |
| id_vehicule   | Identifiant unique du véhicule repris pour chacun des usagers occupant ce véhicule (num)  |
| Num_Veh       | Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (alpha num)   |
| senc          | Sens de circulation                                                                       |
| catv          | Catégorie du véhicule                                                                     |
| obs           | Obstacle fixe heurté                                                                      |
| obsm          | Obstacle mobile heurté                                                                    |
| choc          | Point de choc initial                                                                     |
| manv          | Manoeuvre principale avant l’accident                                                     |
| motor         | Type de motorisation du véhicule                                                          |
| occutc        | Nombre d’occupants dans le transport en commun                                            |

### `usagers.csv`

| Libellé       | Détail                                                                                            |
|:--------------|:--------------------------------------------------------------------------------------------------|
| Num_Acc       | Numéro d'identifiant de l’accident                                                                |
| id_usager     | Identifiant unique de l'usager                                                                    |
| id_vehicule   | Identifiant unique du véhicule repris pour chacun des usagers occupant ce véhicule (num)          |
| num_Veh       | Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (alpha num)           |
| place         | Place occupée dans le véhicule par l'usager au moment de l'accident                               |
| catu          | Catégorie d'usager                                                                                |
| grav          | Gravité de blessure de l'usager                                                                   |
| sexe          | Sexe de l'usager                                                                                  |
| An_nais       | Année de naissance de l'usager                                                                    |
| trajet        | Motif du déplacement au moment de l’accident                                                      |
| secu1 à 3     | Le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité    |
| locp          | Localisation du piéton                                                                            |
| actp          | Action du piéton                                                                                  |
| etatp         | préciser si le piéton accidenté était seul ou non                                                 |

## Relations et Cardinalités

## Schéma final cible

```json
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d0"),
  "Num_Acc": 20240001,
  "date": "2024-10-12T14:30:00Z",
  "jour": 12,
  "mois": 10,
  "an": 2024,
  "hrmn": "14:30",
  "lum": 1,
  "dep": "75",
  "com": "75115",
  "agg": 2,
  "int": 1,
  "atm": 1,
  "col": 2,
  "adr": "Avenue des Champs-Élysées",
  "coordonnees": {
    "type": "Point",
    "coordinates": [2.3084, 48.8698]
  },
  "lieu": {
    "catr": 3,
    "voie": "N13",
    "circ": 2,
    "nbv": 4,
    "surf": 1,
    "vma": 50
  },
  "vehicules": [
    {
      "id_vehicule": "VEH_01",
      "Num_Veh": "A01",
      "catv": 7,
      "motor": 1,
      "choc": 1,
      "usagers": [
        {
          "id_usager": "USG_01",
          "place": 1,
          "catu": 1,
          "grav": 1,
          "sexe": 1,
          "An_nais": 1985
        }
      ]
    }
  ]
}
```

