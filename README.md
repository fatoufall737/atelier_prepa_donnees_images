# Atelier de préparation de données images

Ce projet fournit un petit atelier Python pour préparer un ensemble d’images avant apprentissage automatique ou traitement d’images.

## Fonctionnalités

- redimensionner les images
- convertir en niveaux de gris optionnellement
- normaliser la luminosité
- exporter les résultats dans un dossier dédié

## Installation

```bash
python -m venv .venv
. .venv/bin/activate  # Linux/macOS
# ou sur Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
python atelier.py --input ./images --output ./output --size 224 --grayscale
```

Options :
- `--input`: dossier source contenant des images
- `--output`: dossier de sortie
- `--size`: taille cible pour les images (par défaut 224)
- `--grayscale`: convertir les images en niveaux de gris
- `--normalize`: normaliser les pixels entre 0 et 1

## Exemple

Un petit lot d’images est généré automatiquement dans `demo_images` pour tester le projet.
