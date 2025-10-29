import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import re
import numpy as np
from PIL import Image
import io
import base64

# Configuration de la page
st.set_page_config(
    page_title="🌿 Tisanes Réunionnaises - Plateforme Expert",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avancé
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 2.2rem;
        color: #2E8B57;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        border-left: 5px solid #2E8B57;
        padding-left: 15px;
    }
    .plant-card {
        background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 6px solid #2E8B57;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .plant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.15);
    }
    .benefit-badge {
        background: linear-gradient(135deg, #2E8B57 0%, #4CAF50 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 3px;
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .source-badge {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        margin-left: 5px;
        font-weight: 600;
    }
    .ird-badge {
        background: linear-gradient(135deg, #0055A4 0%, #1a73e8 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        margin-left: 5px;
        font-weight: 600;
    }
    .tnu-badge {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        margin-left: 5px;
        font-weight: 600;
    }
    .search-box {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #1a73e8;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.1);
    }
    .search-result {
        background: linear-gradient(135deg, #e6f7ff 0%, #f0f8ff 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 5px solid #1a73e8;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .search-result:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.12);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .sidebar-emoji {
        font-size: 5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .progress-bar {
        background: linear-gradient(135deg, #2E8B57 0%, #4CAF50 100%);
        height: 6px;
        border-radius: 3px;
        margin: 5px 0;
    }
    .ingredient-chip {
        background: #e8f5e8;
        color: #2E8B57;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 0.8rem;
        border: 1px solid #2E8B57;
    }
    .dark-text {
        color: #333333 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Données des plantes complètes
plantes_data = [
    {
        'Plante': 'Choca (Ayapana)',
        'Nom Scientifique': 'Ayapana triplinervis',
        'Famille': 'Asteraceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Amer, herbacé',
        'Intensité': 4,
        'Popularité': 9,
        'Rareté': 2,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, zones humides',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Digestive', 'Fébrifuge', 'Antioxydante', 'Décongestionnante'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '1 an à l\'abri de la lumière'
    },
    {
        'Plante': 'Tangor',
        'Nom Scientifique': 'Citrus reticulata',
        'Famille': 'Rutaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Fruité, doux',
        'Intensité': 2,
        'Popularité': 8,
        'Rareté': 1,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, vergers',
        'Culture': 'Très facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Calmante', 'Sédative', 'Digestive', 'Riche en vitamine C'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '6 mois'
    },
    {
        'Plante': 'Citronnelle',
        'Nom Scientifique': 'Cymbopogon citratus',
        'Famille': 'Poaceae',
        'Partie Utilisée': 'Tiges et feuilles',
        'Goût': 'Frais, citronné',
        'Intensité': 3,
        'Popularité': 7,
        'Rareté': 1,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, potagers',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Digestive', 'Fébrifuge', 'Anti-inflammatoire', 'Rafraîchissante'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '8 mois'
    },
    {
        'Plante': 'Vétiver',
        'Nom Scientifique': 'Chrysopogon zizanioides',
        'Famille': 'Poaceae',
        'Partie Utilisée': 'Racines',
        'Goût': 'Boisé, terreux',
        'Intensité': 4,
        'Popularité': 6,
        'Rareté': 3,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, zones arides',
        'Culture': 'Moyenne',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Digestive', 'Anti-nauséeuse', 'Apaisante', 'Sudorifique'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '2 ans'
    },
    {
        'Plante': 'Gingembre',
        'Nom Scientifique': 'Zingiber officinale',
        'Famille': 'Zingiberaceae',
        'Partie Utilisée': 'Racine',
        'Goût': 'Piquant, épicé',
        'Intensité': 5,
        'Popularité': 7,
        'Rareté': 1,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, potagers',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Tonifiante', 'Anti-nauséeuse', 'Anti-inflammatoire', 'Stimulante'],
        'Contre-indications': 'À éviter en cas d\'ulcère',
        'Conservation': '3 mois'
    },
    {
        'Plante': 'Curcuma',
        'Nom Scientifique': 'Curcuma longa',
        'Famille': 'Zingiberaceae',
        'Partie Utilisée': 'Racine',
        'Goût': 'Terreux, poivré',
        'Intensité': 3,
        'Popularité': 5,
        'Rareté': 2,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins',
        'Culture': 'Moyenne',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Anti-inflammatoire', 'Antioxydante', 'Hépatoprotectrice', 'Digestive'],
        'Contre-indications': 'Prudence en cas de calculs biliaires',
        'Conservation': '6 mois'
    },
    {
        'Plante': 'Faham',
        'Nom Scientifique': 'Jumellea fragrans',
        'Famille': 'Orchidaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Complexe, mielleux',
        'Intensité': 4,
        'Popularité': 3,
        'Rareté': 5,
        'Saison': 'Saison sèche',
        'Habitat': 'Forêts humides',
        'Culture': 'Difficile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Aphrodisiaque', 'Tonique', 'Expectorante', 'Stimulante'],
        'Contre-indications': 'Usage modéré',
        'Conservation': '1 an'
    },
    {
        'Plante': 'Quinquina',
        'Nom Scientifique': 'Cinchona officinalis',
        'Famille': 'Rubiaceae',
        'Partie Utilisée': 'Écorce',
        'Goût': 'Très amer',
        'Intensité': 5,
        'Popularité': 4,
        'Rareté': 4,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins botaniques',
        'Culture': 'Difficile',
        'Source': 'IRD ThesIndigo',
        'IRD_URI': 'https://uri.ird.fr/so/kos/thesindigo/75406',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Fébrifuge', 'Antipaludéenne', 'Tonique amère', 'Stomachique'],
        'Contre-indications': 'Déconseillé aux femmes enceintes',
        'Conservation': '2 ans'
    },
    {
        'Plante': 'Brin de Songe',
        'Nom Scientifique': 'Phyllanthus amarus',
        'Famille': 'Phyllanthaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Amer, astringent',
        'Intensité': 4,
        'Popularité': 6,
        'Rareté': 3,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, zones sauvages',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Diurétique', 'Hépatoprotecteur', 'Antidiabétique', 'Anti-inflammatoire'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '1 an'
    },
    {
        'Plante': 'Liane Jaune',
        'Nom Scientifique': 'Coptosperma borbonica',
        'Famille': 'Rubiaceae',
        'Partie Utilisée': 'Écorce',
        'Goût': 'Amer, tannique',
        'Intensité': 5,
        'Popularité': 5,
        'Rareté': 4,
        'Saison': 'Toute l\'année',
        'Habitat': 'Forêts',
        'Culture': 'Difficile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Fébrifuge', 'Antipaludéen', 'Digestif', 'Tonique'],
        'Contre-indications': 'Usage modéré',
        'Conservation': '2 ans'
    },
    {
        'Plante': 'Romarin',
        'Nom Scientifique': 'Rosmarinus officinalis',
        'Famille': 'Lamiaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Aromatique, camphré',
        'Intensité': 3,
        'Popularité': 6,
        'Rareté': 1,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, zones sèches',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Stimulante', 'Antioxydante', 'Digestive', 'Tonique'],
        'Contre-indications': 'Éviter fortes doses pendant grossesse',
        'Conservation': '1 an'
    },
    {
        'Plante': 'Menthe',
        'Nom Scientifique': 'Mentha spicata',
        'Famille': 'Lamiaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Frais, mentholé',
        'Intensité': 3,
        'Popularité': 8,
        'Rareté': 1,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, zones humides',
        'Culture': 'Très facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Digestive', 'Rafraîchissante', 'Antispasmodique', 'Stimulante'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '6 mois'
    },
    {
        'Plante': 'Basilic',
        'Nom Scientifique': 'Ocimum basilicum',
        'Famille': 'Lamiaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Aromatique, doux',
        'Intensité': 2,
        'Popularité': 7,
        'Rareté': 1,
        'Saison': 'Toute l\'année',
        'Habitat': 'Jardins, potagers',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Digestive', 'Calmante', 'Antioxydante', 'Anti-stress'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '6 mois'
    },
    {
        'Plante': 'Café Marron',
        'Nom Scientifique': 'Psychotria psy chotria',
        'Famille': 'Rubiaceae',
        'Partie Utilisée': 'Feuilles, écorce',
        'Goût': 'Amer, astringent',
        'Intensité': 4,
        'Popularité': 4,
        'Rareté': 4,
        'Saison': 'Toute l\'année',
        'Habitat': 'Forêts humides',
        'Culture': 'Difficile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Fébrifuge', 'Tonique', 'Digestive', 'Antioxydante'],
        'Contre-indications': 'Usage modéré',
        'Conservation': '1 an'
    },
    {
        'Plante': 'Bois de rongue',
        'Nom Scientifique': 'Psiadia altissima',
        'Famille': 'Asteraceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Amer, aromatique',
        'Intensité': 4,
        'Popularité': 3,
        'Rareté': 4,
        'Saison': 'Toute l\'année',
        'Habitat': 'Forêts de montagne',
        'Culture': 'Difficile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Fébrifuge', 'Anti-inflammatoire', 'Digestive'],
        'Contre-indications': 'Usage traditionnel contrôlé',
        'Conservation': '1 an'
    },
    {
        'Plante': 'Bois de balais',
        'Nom Scientifique': 'Dodonaea viscosa',
        'Famille': 'Sapindaceae',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Amer, astringent',
        'Intensité': 3,
        'Popularité': 4,
        'Rareté': 3,
        'Saison': 'Toute l\'année',
        'Habitat': 'Zones sèches',
        'Culture': 'Facile',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Anti-inflammatoire', 'Astringente', 'Fébrifuge'],
        'Contre-indications': 'Aucune connue',
        'Conservation': '1 an'
    },
    {
        'Plante': 'Bois d\'ortie',
        'Nom Scientifique': 'Obetia ficifolia',
        'Famille': 'Urticaceae',
        'Partie Utilisée': 'Feuilles, écorce',
        'Goût': 'Légèrement piquant',
        'Intensité': 3,
        'Popularité': 3,
        'Rareté': 4,
        'Saison': 'Toute l\'année',
        'Habitat': 'Forêts sèches',
        'Culture': 'Moyenne',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076'],
        'Propriétés': ['Diurétique', 'Anti-rhumatismal', 'Dépuratif'],
        'Contre-indications': 'Peut irriter la peau',
        'Conservation': '1 an'
    }
]

# TOUS LES MÉLANGES TRADITIONNELS COMPLETS
melanges_data = [
    {
        'Nom': 'Digestion Facile',
        'Plantes': ['Choca (Ayapana)', 'Vétiver', 'Citronnelle'],
        'Proportions': {'Choca (Ayapana)': 2, 'Vétiver': 1, 'Citronnelle': 1},
        'Instructions': 'Infusion 10 min - Boire après le repas',
        'Bienfaits': ['Digestion', 'Ballonnements', 'Nausées'],
        'Source': 'Tradition Réunionnaise + APLAMEDOM',
        'TNU_References': ['056', '076'],
        'Usage': 'Quotidien',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '15 min',
        'Score efficacité': 9,
        'Score goût': 7,
        'Notes': 'Mélange de base pour une digestion optimale',
        'Variantes': ['Ajouter du gingembre pour plus de tonicité'],
        'Histoire': 'Utilisé traditionnellement après les repas de fête'
    },
    {
        'Nom': 'Nuit Paisible',
        'Plantes': ['Tangor', 'Citronnelle'],
        'Proportions': {'Tangor': 3, 'Citronnelle': 1},
        'Instructions': 'Infusion 5-7 min - Boire avant le coucher',
        'Bienfaits': ['Sommeil', 'Relaxation', 'Stress'],
        'Source': 'Tradition Réunionnaise + APLAMEDOM',
        'TNU_References': ['056', '076'],
        'Usage': 'Soir',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '10 min',
        'Score efficacité': 8,
        'Score goût': 8,
        'Notes': 'Idéal pour une nuit reposante',
        'Variantes': ['Ajouter une pincée de vanille'],
        'Histoire': 'Recette familiale transmise de génération en génération'
    },
    {
        'Nom': 'Boost Immunité',
        'Plantes': ['Choca (Ayapana)', 'Gingembre', 'Citronnelle', 'Quinquina'],
        'Proportions': {'Choca (Ayapana)': 2, 'Gingembre': 1, 'Citronnelle': 1, 'Quinquina': 0.5},
        'Instructions': 'Décoction 15 min - Boire 2-3 fois/jour',
        'Bienfaits': ['Grippe', 'Fièvre', 'Fatigue', 'Immunité'],
        'Source': 'Synthèse Traditionnelle + IRD',
        'TNU_References': ['056', '076'],
        'Usage': 'Maladie',
        'Saison': 'Hiver',
        'Difficulté': 'Moyenne',
        'Temps préparation': '20 min',
        'Score efficacité': 9,
        'Score goût': 6,
        'Notes': 'Mélange puissant pour les états grippaux',
        'Variantes': ['Remplacer Quinquina par Liane Jaune si indisponible'],
        'Histoire': 'Inspiré des remèdes traditionnels contre la fièvre'
    },
    {
        'Nom': 'Tonique Énergétique',
        'Plantes': ['Gingembre', 'Curcuma', 'Faham'],
        'Proportions': {'Gingembre': 2, 'Curcuma': 1, 'Faham': 0.5},
        'Instructions': 'Décoction 20 min - Boire le matin',
        'Bienfaits': ['Énergie', 'Vitalité', 'Circulation'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Matin',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Moyenne',
        'Temps préparation': '25 min',
        'Score efficacité': 8,
        'Score goût': 7,
        'Notes': 'Parfait pour commencer la journée avec énergie',
        'Variantes': ['Ajouter du miel pour adoucir'],
        'Histoire': 'Utilisé par les travailleurs pour booster leur énergie'
    },
    {
        'Nom': 'Détox Foie',
        'Plantes': ['Choca (Ayapana)', 'Brin de Songe', 'Citronnelle'],
        'Proportions': {'Choca (Ayapana)': 2, 'Brin de Songe': 1, 'Citronnelle': 1},
        'Instructions': 'Infusion 10 min - Boire à jeun',
        'Bienfaits': ['Détoxification', 'Foie', 'Digestion'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Cure',
        'Saison': 'Printemps',
        'Difficulté': 'Facile',
        'Temps préparation': '15 min',
        'Score efficacité': 8,
        'Score goût': 6,
        'Notes': 'Cure détox de 3 semaines recommandée',
        'Variantes': ['Ajouter du romarin pour renforcer l\'effet détox'],
        'Histoire': 'Cure traditionnelle de printemps'
    },
    {
        'Nom': 'Anti-Grippe Puissant',
        'Plantes': ['Quinquina', 'Gingembre', 'Citronnelle', 'Liane Jaune'],
        'Proportions': {'Quinquina': 1, 'Gingembre': 1, 'Citronnelle': 1, 'Liane Jaune': 0.5},
        'Instructions': 'Décoction 20 min - Boire 3 fois/jour',
        'Bienfaits': ['Grippe', 'Fièvre', 'Infection'],
        'Source': 'Médecine Traditionnelle + IRD',
        'TNU_References': ['056', '076'],
        'Usage': 'Maladie aiguë',
        'Saison': 'Hiver',
        'Difficulté': 'Moyenne',
        'Temps préparation': '25 min',
        'Score efficacité': 9,
        'Score goût': 5,
        'Notes': 'Goût très amer mais très efficace',
        'Variantes': ['Ajouter du miel pour masquer l\'amertume'],
        'Histoire': 'Remède ancestral contre les fièvres'
    },
    {
        'Nom': 'Calmant Doux',
        'Plantes': ['Tangor', 'Vétiver'],
        'Proportions': {'Tangor': 2, 'Vétiver': 1},
        'Instructions': 'Infusion 5 min - Boire au coucher',
        'Bienfaits': ['Anxiété', 'Stress', 'Insomnie'],
        'Source': 'Tradition Familiale',
        'TNU_References': ['056', '076'],
        'Usage': 'Soir',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '10 min',
        'Score efficacité': 7,
        'Score goût': 8,
        'Notes': 'Doux et apaisant',
        'Variantes': ['Ajouter de la camomille pour plus d\'effet sédatif'],
        'Histoire': 'Recette de grand-mère pour les nuits agitées'
    },
    {
        'Nom': 'Digestion Lourde',
        'Plantes': ['Vétiver', 'Gingembre', 'Curcuma'],
        'Proportions': {'Vétiver': 2, 'Gingembre': 1, 'Curcuma': 0.5},
        'Instructions': 'Décoction 15 min - Boire après repas copieux',
        'Bienfaits': ['Digestion difficile', 'Lourdeurs', 'Ballonnements'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Occasionnel',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '20 min',
        'Score efficacité': 8,
        'Score goût': 7,
        'Notes': 'Spécial repas de fête',
        'Variantes': ['Ajouter des graines de fenouil'],
        'Histoire': 'Utilisé après les grands repas familiaux'
    },
    {
        'Nom': 'Tisane Tous Risques',
        'Plantes': ['Choca (Ayapana)', 'Tangor', 'Citronnelle', 'Vétiver'],
        'Proportions': {'Choca (Ayapana)': 2, 'Tangor': 1, 'Citronnelle': 1, 'Vétiver': 1},
        'Instructions': 'Infusion 10 min - Boire 1-2 fois/jour',
        'Bienfaits': ['Prévention', 'Bien-être général', 'Immunité'],
        'Source': 'Recette Familiale',
        'TNU_References': ['056', '076'],
        'Usage': 'Quotidien',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '15 min',
        'Score efficacité': 8,
        'Score goût': 8,
        'Notes': 'Mélange équilibré pour tous les jours',
        'Variantes': ['Adapter les proportions selon les goûts'],
        'Histoire': 'Recette polyvalente transmise dans les familles'
    },
    {
        'Nom': 'Aphrodisiaque Créole',
        'Plantes': ['Faham', 'Gingembre', 'Curcuma'],
        'Proportions': {'Faham': 1, 'Gingembre': 1, 'Curcuma': 0.5},
        'Instructions': 'Décoction 15 min - Boire le soir',
        'Bienfaits': ['Libido', 'Énergie', 'Vitalité'],
        'Source': 'Tradition Secrète',
        'TNU_References': ['056', '076'],
        'Usage': 'Occasionnel',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Moyenne',
        'Temps préparation': '20 min',
        'Score efficacité': 7,
        'Score goût': 6,
        'Notes': 'Effet tonifiant général',
        'Variantes': ['Ajouter du ginseng pour potentialiser l\'effet'],
        'Histoire': 'Savoir traditionnel bien gardé'
    },
    {
        'Nom': 'Décongestionnant Respiratoire',
        'Plantes': ['Choca (Ayapana)', 'Citronnelle', 'Gingembre'],
        'Proportions': {'Choca (Ayapana)': 2, 'Citronnelle': 1, 'Gingembre': 1},
        'Instructions': 'Inhalation + infusion 10 min',
        'Bienfaits': ['Toux', 'Rhume', 'Congestion'],
        'Source': 'Médecine Traditionnelle',
        'TNU_References': ['056', '076'],
        'Usage': 'Maladie',
        'Saison': 'Hiver',
        'Difficulté': 'Facile',
        'Temps préparation': '15 min',
        'Score efficacité': 8,
        'Score goût': 7,
        'Notes': 'Double action par inhalation et ingestion',
        'Variantes': ['Ajouter de l\'eucalyptus pour les inhalations'],
        'Histoire': 'Remède complet pour les voies respiratoires'
    },
    {
        'Nom': 'Anti-Diarrhéique',
        'Plantes': ['Brin de Songe', 'Vétiver', 'Curcuma'],
        'Proportions': {'Brin de Songe': 2, 'Vétiver': 1, 'Curcuma': 0.5},
        'Instructions': 'Décoction 15 min - Boire après chaque selle liquide',
        'Bienfaits': ['Diarrhée', 'Troubles intestinaux'],
        'Source': 'Usage Traditionnel',
        'TNU_References': ['056', '076'],
        'Usage': 'Curatif',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '20 min',
        'Score efficacité': 9,
        'Score goût': 5,
        'Notes': 'Goût amer mais très efficace',
        'Variantes': ['Diluer dans plus d\'eau si trop amer'],
        'Histoire': 'Utilisé pour les troubles digestifs aigus'
    },
    {
        'Nom': 'Draineur Rénal',
        'Plantes': ['Brin de Songe', 'Citronnelle', 'Tangor'],
        'Proportions': {'Brin de Songe': 2, 'Citronnelle': 1, 'Tangor': 1},
        'Instructions': 'Infusion 10 min - Boire matin et soir',
        'Bienfaits': ['Diurétique', 'Drainage', 'Élimination'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Cure',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '15 min',
        'Score efficacité': 8,
        'Score goût': 7,
        'Notes': 'Favorise l\'élimination des toxines',
        'Variantes': ['Augmenter la proportion de Brin de Songe pour plus d\'effet'],
        'Histoire': 'Utilisé pour purifier l\'organisme'
    },
    {
        'Nom': 'Anti-Douleur Articulaire',
        'Plantes': ['Curcuma', 'Gingembre', 'Citronnelle'],
        'Proportions': {'Curcuma': 2, 'Gingembre': 1, 'Citronnelle': 1},
        'Instructions': 'Décoction 20 min - Boire 2 fois/jour',
        'Bienfaits': ['Articulations', 'Inflammation', 'Douleur'],
        'Source': 'Médecine Traditionnelle',
        'TNU_References': ['056', '076'],
        'Usage': 'Curatif',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Moyenne',
        'Temps préparation': '25 min',
        'Score efficacité': 8,
        'Score goût': 6,
        'Notes': 'Anti-inflammatoire naturel',
        'Variantes': ['Ajouter du poivre noir pour potentialiser la curcumine'],
        'Histoire': 'Remède ancestral pour les douleurs articulaires'
    },
    {
        'Nom': 'Confort Menstruel',
        'Plantes': ['Vétiver', 'Citronnelle', 'Tangor'],
        'Proportions': {'Vétiver': 2, 'Citronnelle': 1, 'Tangor': 1},
        'Instructions': 'Infusion 10 min - Boire 3 fois/jour',
        'Bienfaits': ['Douleurs menstruelles', 'Spasmes', 'Détente'],
        'Source': 'Savoir Féminin Traditionnel',
        'TNU_References': ['056', '076'],
        'Usage': 'Cyclique',
        'Saison': 'Toute l\'année',
        'Difficulté': 'Facile',
        'Temps préparation': '15 min',
        'Score efficacité': 7,
        'Score goût': 8,
        'Notes': 'Apaisant et relaxant',
        'Variantes': ['Ajouter de l\'achillée millefeuille'],
        'Histoire': 'Transmis de mère en fille'
    }
]

# Données TNU
tnu_data = {
    '056': {
        'uri': 'https://uri.ird.fr/so/kos/tnu/056',
        'prefLabel': 'Plantes médicinales - Usage traditionnel',
        'definition': 'Plantes utilisées dans la médecine traditionnelle réunionnaise',
        'url': 'https://ref-science.ird.fr/tnu/fr/page/056',
        'related_concepts': ['212443', '75406']
    },
    '076': {
        'uri': 'https://uri.ird.fr/so/kos/tnu/076',
        'prefLabel': 'Plantes aromatiques et médicinales - Conservation',
        'definition': 'Méthodes de conservation et préservation des plantes médicinales',
        'url': 'https://ref-science.ird.fr/tnu/fr/page/076',
        'related_concepts': ['212443', '214560']
    }
}

# Initialisation de l'état de session
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'user_notes' not in st.session_state:
    st.session_state.user_notes = {}
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'benefits': [],
        'difficulty': 'Facile',
        'prep_time': 30
    }

# CORRECTION : Graphique réseau avec texte visible
def create_plant_network_graph():
    """Crée un graphique de réseau des relations entre plantes et mélanges avec texte visible"""
    try:
        fig = go.Figure()
        
        # Positions prédéfinies pour une meilleure stabilité
        positions = {
            # Plantes
            'Choca (Ayapana)': (0, 4),
            'Tangor': (2, 4),
            'Citronnelle': (4, 4),
            'Vétiver': (0, 2),
            'Gingembre': (2, 2),
            'Curcuma': (4, 2),
            'Faham': (1, 0),
            'Quinquina': (3, 0),
            'Brin de Songe': (0, 0),
            'Liane Jaune': (4, 0),
            'Romarin': (6, 4),
            'Menthe': (6, 2),
            'Basilic': (6, 0),
            # Mélanges
            'Digestion Facile': (8, 4),
            'Nuit Paisible': (10, 4),
            'Boost Immunité': (12, 4),
            'Tonique Énergétique': (8, 2),
            'Détox Foie': (10, 2),
            'Anti-Grippe Puissant': (12, 2),
            'Calmant Doux': (8, 0),
            'Digestion Lourde': (10, 0),
            'Tisane Tous Risques': (12, 0)
        }
        
        # Ajouter les nœuds des plantes
        plant_x, plant_y, plant_names = [], [], []
        for plante in plantes_data:
            if plante['Plante'] in positions:
                x, y = positions[plante['Plante']]
                plant_x.append(x)
                plant_y.append(y)
                plant_names.append(plante['Plante'])
        
        fig.add_trace(go.Scatter(
            x=plant_x, y=plant_y,
            mode='markers+text',
            marker=dict(size=25, color='#2E8B57', line=dict(width=2, color='white')),
            text=plant_names,
            textposition="middle center",
            textfont=dict(color='black', size=10, family="Arial Black"),
            name='Plantes',
            hoverinfo='text'
        ))
        
        # Ajouter les nœuds des mélanges
        melange_x, melange_y, melange_names = [], [], []
        for melange in melanges_data[:9]:
            if melange['Nom'] in positions:
                x, y = positions[melange['Nom']]
                melange_x.append(x)
                melange_y.append(y)
                melange_names.append(melange['Nom'])
        
        fig.add_trace(go.Scatter(
            x=melange_x, y=melange_y,
            mode='markers+text',
            marker=dict(size=20, color='#1a73e8', line=dict(width=2, color='white')),
            text=melange_names,
            textposition="middle center",
            textfont=dict(color='black', size=9, family="Arial"),
            name='Mélanges',
            hoverinfo='text'
        ))
        
        # Ajouter les liens de manière sécurisée
        for melange in melanges_data[:9]:
            if melange['Nom'] in positions:
                melange_x, melange_y = positions[melange['Nom']]
                for plante in melange['Plantes']:
                    if plante in positions:
                        plante_x, plante_y = positions[plante]
                        fig.add_trace(go.Scatter(
                            x=[plante_x, melange_x], y=[plante_y, melange_y],
                            mode='lines',
                            line=dict(width=1.5, color='gray', dash='solid'),
                            showlegend=False,
                            hoverinfo='none'
                        ))
        
        fig.update_layout(
            title=dict(
                text="Réseau des Plantes et Mélanges",
                x=0.5,
                font=dict(size=16, color='black')
            ),
            showlegend=True,
            height=600,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 14]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 5]),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )
        
        return fig
    except Exception as e:
        st.error(f"Erreur dans la création du graphique: {e}")
        return create_simple_fallback_chart()

def create_simple_fallback_chart():
    """Crée un graphique de secours simple avec texte visible"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[1, 2, 3], y=[4, 1, 2],
        mode='markers+text',
        marker=dict(size=20, color='#2E8B57'),
        text=['Plantes', 'Mélanges', 'Relations'],
        textposition="middle center",
        textfont=dict(color='black', size=12)
    ))
    fig.update_layout(
        title=dict(
            text="Réseau des Connaissances",
            x=0.5,
            font=dict(color='black')
        ),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig

def create_seasonal_calendar():
    """Crée un calendrier des saisons pour les plantes"""
    months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
              'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    
    data = []
    for plante in plantes_data:
        if plante['Saison'] == 'Toute l\'année':
            availability = [1] * 12
        elif plante['Saison'] == 'Hiver':
            availability = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        elif plante['Saison'] == 'Été':
            availability = [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        else:
            availability = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0]
        
        for i, avail in enumerate(availability):
            data.append({
                'Plante': plante['Plante'],
                'Mois': months[i],
                'Disponibilité': avail,
                'Saison': plante['Saison']
            })
    
    df = pd.DataFrame(data)
    
    fig = px.imshow(
        df.pivot(index='Plante', columns='Mois', values='Disponibilité'),
        title="Calendrier des Saisons des Plantes",
        color_continuous_scale=['lightgray', '#2E8B57'],
        aspect="auto"
    )
    
    return fig

def show_advanced_search():
    st.markdown('<div class="section-header">🔍 Recherche Avancée</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔎 Recherche par mots-clés:", placeholder="Ex: digestion, sommeil, fièvre...")
    
    with col2:
        search_type = st.selectbox("Type de recherche:", ["Plantes", "Mélanges", "Les deux"])
    
    # Filtres avancés
    st.subheader("🎯 Filtres Avancés")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        benefits_filter = st.multiselect(
            "Bienfaits recherchés:",
            list(set([benefit for m in melanges_data for benefit in m['Bienfaits']]))
        )
    
    with col2:
        difficulty_filter = st.selectbox(
            "Difficulté max:",
            ["Toutes", "Facile", "Moyenne", "Difficile"]
        )
    
    with col3:
        prep_time_filter = st.slider("Temps de préparation max (min):", 5, 60, 30)
    
    if st.button("🔍 Lancer la recherche", type="primary"):
        results = advanced_search(
            search_query, 
            search_type, 
            benefits_filter, 
            difficulty_filter, 
            prep_time_filter
        )
        display_search_results(results)
    
    st.markdown('</div>', unsafe_allow_html=True)

def advanced_search(query, search_type, benefits, difficulty, prep_time):
    """Effectue une recherche avancée"""
    results = []
    
    # Recherche dans les plantes
    if search_type in ["Plantes", "Les deux"]:
        for plante in plantes_data:
            score = 0
            
            # Recherche par mots-clés
            if query:
                query_terms = query.lower().split()
                for term in query_terms:
                    if (term in plante['Plante'].lower() or 
                        term in plante['Nom Scientifique'].lower() or
                        term in plante['Goût'].lower() or
                        any(term in prop.lower() for prop in plante['Propriétés'])):
                        score += 2
            
            # Filtre par bienfaits
            if benefits:
                matching_benefits = sum(1 for benefit in benefits if any(benefit.lower() in prop.lower() for prop in plante['Propriétés']))
                score += matching_benefits * 3
            
            if score > 0:
                results.append({
                    'type': 'Plante',
                    'data': plante,
                    'score': score
                })
    
    # Recherche dans les mélanges
    if search_type in ["Mélanges", "Les deux"]:
        for melange in melanges_data:
            score = 0
            
            # Recherche par mots-clés
            if query:
                query_terms = query.lower().split()
                for term in query_terms:
                    if (term in melange['Nom'].lower() or
                        term in melange['Instructions'].lower() or
                        any(term in benefit.lower() for benefit in melange['Bienfaits'])):
                        score += 2
            
            # Filtre par bienfaits
            if benefits:
                matching_benefits = sum(1 for benefit in benefits if benefit in melange['Bienfaits'])
                score += matching_benefits * 3
            
            # Filtre par difficulté
            if difficulty != "Toutes" and melange['Difficulté'] != difficulty:
                continue
            
            # Filtre par temps de préparation
            prep_time_num = int(melange['Temps préparation'].split()[0])
            if prep_time_num > prep_time:
                continue
            
            if score > 0:
                results.append({
                    'type': 'Mélange',
                    'data': melange,
                    'score': score
                })
    
    # Trier par score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def display_search_results(results):
    """Affiche les résultats de recherche"""
    if not results:
        st.warning("🔍 Aucun résultat trouvé pour votre recherche.")
        return
    
    st.success(f"🎯 **{len(results)} résultats** trouvés pour votre recherche")
    
    for result in results:
        with st.container():
            st.markdown('<div class="search-result">', unsafe_allow_html=True)
            
            if result['type'] == 'Plante':
                plante = result['data']
                st.write(f"### 🌿 {plante['Plante']}")
                st.write(f"**Nom scientifique:** {plante['Nom Scientifique']}")
                st.write(f"**Famille:** {plante['Famille']}")
                st.write(f"**Propriétés:** {', '.join(plante['Propriétés'])}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⭐ Ajouter aux favoris", key=f"search_fav_plant_{plante['Plante']}"):
                        if plante['Plante'] not in st.session_state.favorites:
                            st.session_state.favorites.append(plante['Plante'])
                            st.success("Ajouté aux favoris!")
                
            else:  # Mélange
                melange = result['data']
                st.write(f"### 🍵 {melange['Nom']}")
                st.write(f"**Plantes:** {', '.join(melange['Plantes'])}")
                st.write(f"**Bienfaits:** {', '.join(melange['Bienfaits'])}")
                st.write(f"**Difficulté:** {melange['Difficulté']} - **Temps:** {melange['Temps préparation']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⭐ Ajouter aux favoris", key=f"search_fav_melange_{melange['Nom']}"):
                        if melange['Nom'] not in st.session_state.favorites:
                            st.session_state.favorites.append(melange['Nom'])
                            st.success("Ajouté aux favoris!")
                
            st.markdown('</div>', unsafe_allow_html=True)

def show_melanges_advanced():
    st.markdown('<div class="section-header">🧪 Tous les Mélanges Traditionnels</div>', unsafe_allow_html=True)
    
    st.info(f"**{len(melanges_data)} mélanges traditionnels** documentés et validés - Patrimoine culturel réunionnais")
    
    # Filtres pour les mélanges
    col1, col2, col3 = st.columns(3)
    
    with col1:
        usage_filter = st.selectbox(
            "Usage:",
            ["Tous"] + list(set(m.get('Usage', 'Non spécifié') for m in melanges_data))
        )
    
    with col2:
        difficulty_filter = st.selectbox(
            "Difficulté:",
            ["Toutes"] + list(set(m.get('Difficulté', 'Non spécifié') for m in melanges_data))
        )
    
    with col3:
        season_filter = st.selectbox(
            "Saison:",
            ["Toutes"] + list(set(m.get('Saison', 'Non spécifié') for m in melanges_data))
        )
    
    # Appliquer les filtres
    filtered_melanges = melanges_data.copy()
    
    if usage_filter != "Tous":
        filtered_melanges = [m for m in filtered_melanges if m.get('Usage') == usage_filter]
    
    if difficulty_filter != "Toutes":
        filtered_melanges = [m for m in filtered_melanges if m.get('Difficulté') == difficulty_filter]
    
    if season_filter != "Toutes":
        filtered_melanges = [m for m in filtered_melanges if m.get('Saison') == season_filter]
    
    st.success(f"**{len(filtered_melanges)} mélanges** correspondent à vos critères")
    
    # Affichage des mélanges
    for i, melange in enumerate(filtered_melanges):
        with st.expander(f"🍵 {melange['Nom']} - ⭐{melange['Score efficacité']}/10 - {melange['Usage']}", expanded=i < 3):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**📝 Description :** {melange.get('Notes', 'Mélange traditionnel')}")
                
                st.write("**🌿 Plantes utilisées :**")
                for plante, proportion in melange['Proportions'].items():
                    st.write(f"- {plante} : {proportion} part(s)")
                
                st.write(f"**🕒 Instructions :** {melange['Instructions']}")
                
                st.write("**💚 Bienfaits principaux :**")
                for benefit in melange['Bienfaits']:
                    st.markdown(f'<span class="benefit-badge">{benefit}</span>', unsafe_allow_html=True)
                
                if melange.get('Variantes'):
                    st.write("**🔄 Variantes :**")
                    for variante in melange['Variantes']:
                        st.write(f"- {variante}")
                
                if melange.get('Histoire'):
                    st.write(f"**📖 Histoire :** {melange['Histoire']}")
            
            with col2:
                st.metric("Usage", melange.get('Usage', 'Non spécifié'))
                st.metric("Difficulté", melange.get('Difficulté', 'Non spécifié'))
                st.metric("Temps", melange.get('Temps préparation', 'Non spécifié'))
                
                # Barre de progression pour l'efficacité
                st.write("**Efficacité :**")
                efficiency = melange.get('Score efficacité', 0)
                st.markdown(f"""
                <div style="background: #f0f0f0; border-radius: 10px; padding: 3px;">
                    <div class="progress-bar" style="width: {efficiency * 10}%;"></div>
                </div>
                <small>{efficiency}/10</small>
                """, unsafe_allow_html=True)
                
                # Barre de progression pour le goût
                st.write("**Goût :**")
                gout = melange.get('Score goût', 0)
                st.markdown(f"""
                <div style="background: #f0f0f0; border-radius: 10px; padding: 3px;">
                    <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%); height: 6px; border-radius: 3px; width: {gout * 10}%;"></div>
                </div>
                <small>{gout}/10</small>
                """, unsafe_allow_html=True)
                
                if st.button("⭐ Ajouter aux favoris", key=f"fav_{melange['Nom']}"):
                    if melange['Nom'] not in st.session_state.favorites:
                        st.session_state.favorites.append(melange['Nom'])
                        st.success("Ajouté aux favoris!")
                    else:
                        st.info("Déjà dans vos favoris")

def show_plantes_advanced():
    st.markdown('<div class="section-header">🌿 Toutes les Plantes Médicinales</div>', unsafe_allow_html=True)
    
    st.info(f"**{len(plantes_data)} plantes** documentées et validées - Patrimoine naturel réunionnais")
    
    # Filtres pour les plantes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        family_filter = st.selectbox(
            "Famille:",
            ["Toutes"] + list(set(p['Famille'] for p in plantes_data))
        )
    
    with col2:
        rarity_filter = st.selectbox(
            "Rareté:",
            ["Toutes"] + list(set(p['Rareté'] for p in plantes_data))
        )
    
    with col3:
        culture_filter = st.selectbox(
            "Culture:",
            ["Toutes"] + list(set(p['Culture'] for p in plantes_data))
        )
    
    # Appliquer les filtres
    filtered_plantes = plantes_data.copy()
    
    if family_filter != "Toutes":
        filtered_plantes = [p for p in filtered_plantes if p['Famille'] == family_filter]
    
    if rarity_filter != "Toutes":
        filtered_plantes = [p for p in filtered_plantes if p['Rareté'] == rarity_filter]
    
    if culture_filter != "Toutes":
        filtered_plantes = [p for p in filtered_plantes if p['Culture'] == culture_filter]
    
    st.success(f"**{len(filtered_plantes)} plantes** correspondent à vos critères")
    
    # Affichage des plantes
    for i, plante in enumerate(filtered_plantes):
        with st.expander(f"🌿 {plante['Plante']} - {plante['Nom Scientifique']}", expanded=i < 3):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'<div class="plant-card">', unsafe_allow_html=True)
                st.write(f"**🔬 Nom scientifique :** {plante['Nom Scientifique']}")
                st.write(f"**🌾 Famille :** {plante['Famille']}")
                st.write(f"**🍃 Partie utilisée :** {plante['Partie Utilisée']}")
                st.write(f"**👅 Goût :** {plante['Goût']} (Intensité: {plante['Intensité']}/5)")
                st.write(f"**🏡 Habitat :** {plante['Habitat']}")
                st.write(f"**🌱 Culture :** {plante['Culture']}")
                st.write(f"**📅 Saison :** {plante['Saison']}")
                st.write(f"**⚠️ Contre-indications :** {plante['Contre-indications']}")
                st.write(f"**📦 Conservation :** {plante['Conservation']}")
                
                st.write("**💚 Propriétés :**")
                for propriete in plante['Propriétés']:
                    st.markdown(f'<span class="benefit-badge">{propriete}</span>', unsafe_allow_html=True)
                
                # Badges de source
                if plante['Source'] == 'APLAMEDOM':
                    st.markdown('<span class="source-badge">APLAMEDOM</span>', unsafe_allow_html=True)
                elif plante['Source'] == 'IRD ThesIndigo':
                    st.markdown('<span class="ird-badge">IRD ThesIndigo</span>', unsafe_allow_html=True)
                
                if plante['IRD_URI']:
                    st.markdown(f'<a href="{plante["IRD_URI"]}" target="_blank" class="ird-badge">IRD URI</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Popularité", f"{plante['Popularité']}/10")
                st.metric("Rareté", f"{plante['Rareté']}/5")
                st.metric("Intensité", f"{plante['Intensité']}/5")
                
                # Barre de progression pour la popularité
                st.write("**Popularité :**")
                popularity = plante.get('Popularité', 0)
                st.markdown(f"""
                <div style="background: #f0f0f0; border-radius: 10px; padding: 3px;">
                    <div style="background: linear-gradient(135deg, #2E8B57 0%, #4CAF50 100%); height: 6px; border-radius: 3px; width: {popularity * 10}%;"></div>
                </div>
                <small>{popularity}/10</small>
                """, unsafe_allow_html=True)
                
                if st.button("⭐ Ajouter aux favoris", key=f"fav_plant_{plante['Plante']}"):
                    if plante['Plante'] not in st.session_state.favorites:
                        st.session_state.favorites.append(plante['Plante'])
                        st.success("Ajouté aux favoris!")
                    else:
                        st.info("Déjà dans vos favoris")

def show_favorites():
    st.markdown('<div class="section-header">⭐ Mes Favoris</div>', unsafe_allow_html=True)
    
    if not st.session_state.favorites:
        st.warning("Vous n'avez pas encore de favoris. Explorez les plantes et mélanges pour en ajouter!")
        return
    
    st.success(f"**{len(st.session_state.favorites)} favoris** enregistrés")
    
    # Séparer les plantes et les mélanges
    favorite_plants = [p for p in st.session_state.favorites if any(p == plant['Plante'] for plant in plantes_data)]
    favorite_melanges = [m for m in st.session_state.favorites if any(m == melange['Nom'] for melange in melanges_data)]
    
    # Afficher les plantes favorites
    if favorite_plants:
        st.subheader("🌿 Plantes Favorites")
        for plant_name in favorite_plants:
            plante = next((p for p in plantes_data if p['Plante'] == plant_name), None)
            if plante:
                with st.expander(f"🌿 {plante['Plante']}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Nom scientifique :** {plante['Nom Scientifique']}")
                        st.write(f"**Propriétés :** {', '.join(plante['Propriétés'])}")
                        st.write(f"**Goût :** {plante['Goût']}")
                    with col2:
                        if st.button("❌ Retirer", key=f"remove_plant_{plante['Plante']}"):
                            st.session_state.favorites.remove(plante['Plante'])
                            st.experimental_rerun()
    
    # Afficher les mélanges favorites
    if favorite_melanges:
        st.subheader("🍵 Mélanges Favorites")
        for melange_name in favorite_melanges:
            melange = next((m for m in melanges_data if m['Nom'] == melange_name), None)
            if melange:
                with st.expander(f"🍵 {melange['Nom']}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Plantes :** {', '.join(melange['Plantes'])}")
                        st.write(f"**Bienfaits :** {', '.join(melange['Bienfaits'])}")
                        st.write(f"**Instructions :** {melange['Instructions']}")
                    with col2:
                        if st.button("❌ Retirer", key=f"remove_melange_{melange['Nom']}"):
                            st.session_state.favorites.remove(melange['Nom'])
                            st.experimental_rerun()

# Interface principale
def main():
    # Header principal avec navigation
    st.markdown('<h1 class="main-header">🌿 TISANES RÉUNIONNAISES</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Plateforme Expert de Connaissances Traditionnelles et Scientifiques</p>', unsafe_allow_html=True)
    
    # Navigation simplifiée
    nav_options = ["🏠 Tableau de Bord", "🔍 Recherche Avancée", "🧪 Mélanges", "🌿 Plantes", "⭐ Favoris"]
    
    selected_nav = st.radio("Navigation:", nav_options, horizontal=True)
    
    # Sections principales
    if selected_nav == "🏠 Tableau de Bord":
        show_dashboard()
    elif selected_nav == "🔍 Recherche Avancée":
        show_advanced_search()
    elif selected_nav == "🧪 Mélanges":
        show_melanges_advanced()
    elif selected_nav == "🌿 Plantes":
        show_plantes_advanced()
    elif selected_nav == "⭐ Favoris":
        show_favorites()

def show_dashboard():
    st.markdown('<div class="section-header">📊 Tableau de Bord Interactif</div>', unsafe_allow_html=True)
    
    # Métriques en temps réel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Plantes Documentées", len(plantes_data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Mélanges Traditionnels", len(melanges_data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Favoris Utilisateurs", len(st.session_state.favorites))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_searches = len(st.session_state.search_history)
        st.metric("Recherches", total_searches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_plant_network_graph(), use_container_width=True)
    
    with col2:
        # Graphique des bienfaits les plus populaires
        all_benefits = []
        for melange in melanges_data:
            all_benefits.extend(melange['Bienfaits'])
        
        benefit_counts = pd.Series(all_benefits).value_counts()
        
        fig = px.bar(
            x=benefit_counts.values,
            y=benefit_counts.index,
            orientation='h',
            title="Bienfaits les Plus Courants",
            color=benefit_counts.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Dernières activités
    st.markdown('<div class="section-header">📈 Activité Récente</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Dernières Recherches")
        if st.session_state.search_history:
            for search in st.session_state.search_history[-5:]:
                st.write(f"• {search}")
        else:
            st.write("Aucune recherche récente")
    
    with col2:
        st.subheader("⭐ Derniers Favoris")
        if st.session_state.favorites:
            for fav in st.session_state.favorites[-3:]:
                st.write(f"• {fav}")
        else:
            st.write("Aucun favori")

# Lancement de l'application
if __name__ == "__main__":
    main()
