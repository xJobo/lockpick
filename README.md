# Lockpick

Outil en ligne de commande pour tester la robustesse d'un mot de passe.

Petit projet perso pour mieux comprendre ce qui rend un mot de passe solide (ou pas).

## Fonctionnalités

- Vérification de la longueur
- Analyse de la complexité (minuscules, majuscules, chiffres, caractères spéciaux)
- Estimation du temps de crack en brute force (hypothèse : 10 milliards de tentatives/sec, GPU type hashcat)
- Comparaison avec une liste de ~150 mots de passe courants (basée sur RockYou + mots de passe français)
- Score sur 7 avec niveau de robustesse
- Conseils d'amélioration

## Utilisation

```bash
python lockpick.py
```

Ensuite il suffit de taper un mot de passe pour l'analyser. Tape `quitter` pour arrêter.

## Exemple

```
Mot de passe à tester : azerty

--- Analyse : 'azerty' ---

[!] ALERTE : Ce mot de passe est dans la liste des plus utilisés !
    Il serait cracké en moins d'une seconde par dictionnaire.

[Longueur]     Trop court (6 caractères — minimum 8)
[Complexité]   minuscules OK, pas de majuscules, pas de chiffres, pas de caractères spéciaux
[Temps crack]  environ 3 secondes

[Score]        1/7 — FAIBLE

[Conseils]
  • Allonge ton mot de passe à au moins 12 caractères
  • Ajoute au moins une lettre majuscule (ex: A, B, C...)
  • Ajoute des chiffres (ex: 1, 42, 99...)
  • Ajoute des caractères spéciaux (ex: @, #, !, $...)
  • Ce mot de passe est trop courant — change-le complètement
---
```

## Prérequis

- Python 3.6+
- Aucune dépendance externe

## Avertissement

Cet outil est à but éducatif. L'estimation du temps de crack est théorique et ne prend pas en compte les attaques par dictionnaire, rainbow tables ou les règles de mutation type hashcat. En conditions réelles, un mot de passe faible est cracké encore plus vite.
