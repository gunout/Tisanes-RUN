import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import re

# Configuration de la page
st.set_page_config(
    page_title="Tisanes Réunionnaises - Moteur ThesIndigo",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .plant-card {
        background-color: #f8fff8;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #2E8B57;
    }
    .benefit-badge {
        background-color: #e6f7e6;
        color: #2E8B57;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 0.8rem;
    }
    .source-badge {
        background-color: #e6f3ff;
        color: #1a73e8;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-left: 5px;
    }
    .ird-badge {
        background-color: #0055A4;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-left: 5px;
    }
    .tnu-badge {
        background-color: #8B4513;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-left: 5px;
    }
    .taxonomy-tree {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        border: 1px solid #ddd;
    }
    .search-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #1a73e8;
        margin-bottom: 20px;
    }
    .search-result {
        background-color: #e6f7ff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1a73e8;
    }
    .sidebar-emoji {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Données des plantes
plantes_data = [
    {
        'Plante': 'Choca (Ayapana)',
        'Nom Scientifique': 'Ayapana triplinervis',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Amer, herbacé',
        'Intensité': 4,
        'Popularité': 9,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Tangor',
        'Nom Scientifique': 'Citrus reticulata',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Fruité, doux',
        'Intensité': 2,
        'Popularité': 8,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Citronnelle',
        'Nom Scientifique': 'Cymbopogon citratus',
        'Partie Utilisée': 'Tiges et feuilles',
        'Goût': 'Frais, citronné',
        'Intensité': 3,
        'Popularité': 7,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Vétiver',
        'Nom Scientifique': 'Chrysopogon zizanioides',
        'Partie Utilisée': 'Racines',
        'Goût': 'Boisé, terreux',
        'Intensité': 4,
        'Popularité': 6,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Gingembre',
        'Nom Scientifique': 'Zingiber officinale',
        'Partie Utilisée': 'Racine',
        'Goût': 'Piquant, épicé',
        'Intensité': 5,
        'Popularité': 7,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Curcuma',
        'Nom Scientifique': 'Curcuma longa',
        'Partie Utilisée': 'Racine',
        'Goût': 'Terreux, poivré',
        'Intensité': 3,
        'Popularité': 5,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Faham',
        'Nom Scientifique': 'Jumellea fragrans',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Complexe, mielleux',
        'Intensité': 4,
        'Popularité': 3,
        'Saison': 'Saison sèche',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Quinquina',
        'Nom Scientifique': 'Cinchona officinalis',
        'Partie Utilisée': 'Écorce',
        'Goût': 'Très amer',
        'Intensité': 5,
        'Popularité': 4,
        'Saison': 'Toute l\'année',
        'Source': 'IRD ThesIndigo',
        'IRD_URI': 'https://uri.ird.fr/so/kos/thesindigo/75406',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Brin de Songe',
        'Nom Scientifique': 'Phyllanthus amarus',
        'Partie Utilisée': 'Feuilles',
        'Goût': 'Amer, astringent',
        'Intensité': 4,
        'Popularité': 6,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    },
    {
        'Plante': 'Liane Jaune',
        'Nom Scientifique': 'Coptosperma borbonica',
        'Partie Utilisée': 'Écorce',
        'Goût': 'Amer, tannique',
        'Intensité': 5,
        'Popularité': 5,
        'Saison': 'Toute l\'année',
        'Source': 'APLAMEDOM',
        'IRD_URI': '',
        'TNU_References': ['056', '076']
    }
]

# Bienfaits détaillés enrichis
benefits_detail = {
    'Choca (Ayapana)': {
        'bienfaits': ['Digestif', 'Fébrifuge', 'Anti-grippe', 'Décongestionnant', 'Antioxydant'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Tangor': {
        'bienfaits': ['Calmant', 'Sédatif', 'Digestif', 'Anti-stress', 'Vitamine C'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Citronnelle': {
        'bienfaits': ['Digestif', 'Fébrifuge', 'Anti-inflammatoire', 'Rafraîchissant', 'Antispasmodique'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Vétiver': {
        'bienfaits': ['Digestif', 'Anti-nauséeux', 'Apaisant', 'Sudorifique'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Gingembre': {
        'bienfaits': ['Tonifiant', 'Anti-nauséeux', 'Anti-inflammatoire', 'Stimulant circulatoire', 'Aphrodisiaque'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Curcuma': {
        'bienfaits': ['Anti-inflammatoire', 'Antioxydant', 'Hépatoprotecteur', 'Digestif'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Faham': {
        'bienfaits': ['Aphrodisiaque', 'Tonique', 'Asthme', 'Stimulant', 'Expectorant'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Quinquina': {
        'bienfaits': ['Fébrifuge', 'Antipaludéen', 'Tonique amer', 'Stomachique'],
        'source': 'IRD ThesIndigo',
        'references': ['https://ref-science.ird.fr/thesindigo/fr/page/212443'],
        'tnu_references': ['056', '076']
    },
    'Brin de Songe': {
        'bienfaits': ['Diurétique', 'Hépatoprotecteur', 'Antidiabétique', 'Anti-inflammatoire'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    },
    'Liane Jaune': {
        'bienfaits': ['Fébrifuge', 'Antipaludéen', 'Digestif', 'Tonique'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/'],
        'tnu_references': ['056', '076']
    }
}

# Données RDF/XML de l'IRD
rdf_data = """
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
         xmlns:skos="http://www.w3.org/2004/02/skos/core#" 
         xmlns:owl="http://www.w3.org/2002/07/owl#">
    
    <skos:Concept rdf:about="https://uri.ird.fr/so/kos/thesindigo/214560">
        <skos:narrower rdf:resource="https://uri.ird.fr/so/kos/thesindigo/212443"/>
        <skos:prefLabel xml:lang="fr">MONDE VEGETAL</skos:prefLabel>
        <skos:definition xml:lang="fr">Ensemble du règne végétal et des plantes</skos:definition>
    </skos:Concept>
    
    <skos:Concept rdf:about="https://uri.ird.fr/so/kos/thesindigo/75406">
        <skos:broader rdf:resource="https://uri.ird.fr/so/kos/thesindigo/212443"/>
        <skos:prefLabel xml:lang="fr">QUINQUINA</skos:prefLabel>
        <skos:definition xml:lang="fr">Plante médicinale utilisée traditionnellement contre la fièvre</skos:definition>
    </skos:Concept>
    
    <skos:Concept rdf:about="https://uri.ird.fr/so/kos/thesindigo/212443">
        <skos:broader rdf:resource="https://uri.ird.fr/so/kos/thesindigo/214560"/>
        <skos:inScheme>
            <owl:Ontology rdf:about="https://uri.ird.fr/so/kos/thesindigo/">
                <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#ConceptScheme"/>
                <skos:prefLabel>thesindigo</skos:prefLabel>
            </owl:Ontology>
        </skos:inScheme>
        <skos:narrower rdf:resource="https://uri.ird.fr/so/kos/thesindigo/75406"/>
        <skos:prefLabel xml:lang="fr">PLANTE MEDICINALE</skos:prefLabel>
        <skos:closeMatch rdf:resource="https://uri.ird.fr/so/kos/tnu/056"/>
        <skos:closeMatch rdf:resource="https://uri.ird.fr/so/kos/tnu/076"/>
        <skos:definition xml:lang="fr">Plante possédant des propriétés médicinales utilisées en thérapeutique</skos:definition>
    </skos:Concept>
</rdf:RDF>
"""

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

# TOUS LES MÉLANGES TRADITIONNELS
melanges_data = [
    {
        'Nom': 'Digestion Facile',
        'Plantes': ['Choca (Ayapana)', 'Vétiver', 'Citronnelle'],
        'Proportions': '2 parts Choca, 1 part Vétiver, 1 part Citronnelle',
        'Instructions': 'Infusion 10 min - Boire après le repas',
        'Bienfaits': ['Digestion', 'Ballonnements', 'Nausées'],
        'Source': 'Tradition Réunionnaise + APLAMEDOM',
        'TNU_References': ['056', '076'],
        'Usage': 'Quotidien',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Nuit Paisible',
        'Plantes': ['Tangor', 'Citronnelle'],
        'Proportions': '3 parts Tangor, 1 part Citronnelle',
        'Instructions': 'Infusion 5-7 min - Boire avant le coucher',
        'Bienfaits': ['Sommeil', 'Relaxation', 'Stress'],
        'Source': 'Tradition Réunionnaise + APLAMEDOM',
        'TNU_References': ['056', '076'],
        'Usage': 'Soir',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Boost Immunité',
        'Plantes': ['Choca (Ayapana)', 'Gingembre', 'Citronnelle', 'Quinquina'],
        'Proportions': '2 parts Choca, 1 part Gingembre, 1 part Citronnelle, 1/2 part Quinquina',
        'Instructions': 'Décoction 15 min - Boire 2-3 fois/jour',
        'Bienfaits': ['Grippe', 'Fièvre', 'Fatigue', 'Immunité'],
        'Source': 'Synthèse Traditionnelle + IRD',
        'TNU_References': ['056', '076'],
        'Usage': 'Maladie',
        'Saison': 'Hiver'
    },
    {
        'Nom': 'Tonique Énergétique',
        'Plantes': ['Gingembre', 'Curcuma', 'Faham'],
        'Proportions': '2 parts Gingembre, 1 part Curcuma, 1/2 part Faham',
        'Instructions': 'Décoction 20 min - Boire le matin',
        'Bienfaits': ['Énergie', 'Vitalité', 'Circulation'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Matin',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Détox Foie',
        'Plantes': ['Choca (Ayapana)', 'Brin de Songe', 'Citronnelle'],
        'Proportions': '2 parts Choca, 1 part Brin de Songe, 1 part Citronnelle',
        'Instructions': 'Infusion 10 min - Boire à jeun',
        'Bienfaits': ['Détoxification', 'Foie', 'Digestion'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Cure',
        'Saison': 'Printemps'
    },
    {
        'Nom': 'Anti-Grippe Puissant',
        'Plantes': ['Quinquina', 'Gingembre', 'Citronnelle', 'Liane Jaune'],
        'Proportions': '1 part Quinquina, 1 part Gingembre, 1 part Citronnelle, 1/2 part Liane Jaune',
        'Instructions': 'Décoction 20 min - Boire 3 fois/jour',
        'Bienfaits': ['Grippe', 'Fièvre', 'Infection'],
        'Source': 'Médecine Traditionnelle + IRD',
        'TNU_References': ['056', '076'],
        'Usage': 'Maladie aiguë',
        'Saison': 'Hiver'
    },
    {
        'Nom': 'Calmant Doux',
        'Plantes': ['Tangor', 'Vétiver'],
        'Proportions': '2 parts Tangor, 1 part Vétiver',
        'Instructions': 'Infusion 5 min - Boire au coucher',
        'Bienfaits': ['Anxiété', 'Stress', 'Insomnie'],
        'Source': 'Tradition Familiale',
        'TNU_References': ['056', '076'],
        'Usage': 'Soir',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Digestion Lourde',
        'Plantes': ['Vétiver', 'Gingembre', 'Curcuma'],
        'Proportions': '2 parts Vétiver, 1 part Gingembre, 1/2 part Curcuma',
        'Instructions': 'Décoction 15 min - Boire après repas copieux',
        'Bienfaits': ['Digestion difficile', 'Lourdeurs', 'Ballonnements'],
        'Source': 'Tradition Réunionnaise',
        'TNU_References': ['056', '076'],
        'Usage': 'Occasionnel',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Tisane Tous Risques',
        'Plantes': ['Choca (Ayapana)', 'Tangor', 'Citronnelle', 'Vétiver'],
        'Proportions': '2 parts Choca, 1 part Tangor, 1 part Citronnelle, 1 part Vétiver',
        'Instructions': 'Infusion 10 min - Boire 1-2 fois/jour',
        'Bienfaits': ['Prévention', 'Bien-être général', 'Immunité'],
        'Source': 'Recette Familiale',
        'TNU_References': ['056', '076'],
        'Usage': 'Quotidien',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Aphrodisiaque Créole',
        'Plantes': ['Faham', 'Gingembre', 'Curcuma'],
        'Proportions': '1 part Faham, 1 part Gingembre, 1/2 part Curcuma',
        'Instructions': 'Décoction 15 min - Boire le soir',
        'Bienfaits': ['Libido', 'Énergie', 'Vitalité'],
        'Source': 'Tradition Secrète',
        'TNU_References': ['056', '076'],
        'Usage': 'Occasionnel',
        'Saison': 'Toute l\'année'
    },
    {
        'Nom': 'Décongestionnant Respiratoire',
        'Plantes': ['Choca (Ayapana)', 'Citronnelle', 'Gingembre'],
        'Proportions': '2 parts Choca, 1 part Citronnelle, 1 part Gingembre',
        'Instructions': 'Inhalation + infusion 10 min',
        'Bienfaits': ['Toux', 'Rhume', 'Congestion'],
        'Source': 'Médecine Traditionnelle',
        'TNU_References': ['056', '076'],
        'Usage': 'Maladie',
        'Saison': 'Hiver'
    },
    {
        'Nom': 'Anti-Diarrhéique',
        'Plantes': ['Brin de Songe', 'Vétiver', 'Curcuma'],
        'Proportions': '2 parts Brin de Songe, 1 part Vétiver, 1/2 part Curcuma',
        'Instructions': 'Décoction 15 min - Boire après chaque selle liquide',
        'Bienfaits': ['Diarrhée', 'Troubles intestinaux'],
        'Source': 'Usage Traditionnel',
        'TNU_References': ['056', '076'],
        'Usage': 'Curatif',
        'Saison': 'Toute l\'année'
    }
]

# Moteur de recherche ThesIndigo
def search_thesindigo(query, search_type="all"):
    """
    Recherche dans les données ThesIndigo, TNU et plantes
    """
    results = []
    query_lower = query.lower()
    
    # Recherche dans les concepts IRD
    ird_concepts = parse_ird_rdf(rdf_data)
    for uri, concept in ird_concepts.items():
        if (query_lower in concept.get('prefLabel', '').lower() or 
            query_lower in concept.get('definition', '').lower() or
            query_lower in concept.get('id', '').lower()):
            results.append({
                'type': 'Concept IRD',
                'titre': concept['prefLabel'],
                'description': concept.get('definition', ''),
                'uri': concept.get('uri', ''),
                'url': concept.get('url', ''),
                'score': calculate_relevance_score(query, concept['prefLabel'] + ' ' + concept.get('definition', ''))
            })
    
    # Recherche dans les concepts TNU
    for code, tnu in tnu_data.items():
        if (query_lower in tnu.get('prefLabel', '').lower() or 
            query_lower in tnu.get('definition', '').lower() or
            query_lower in code.lower()):
            results.append({
                'type': 'Concept TNU',
                'titre': f"TNU {code} - {tnu['prefLabel']}",
                'description': tnu.get('definition', ''),
                'uri': tnu.get('uri', ''),
                'url': tnu.get('url', ''),
                'score': calculate_relevance_score(query, tnu['prefLabel'] + ' ' + tnu.get('definition', ''))
            })
    
    # Recherche dans les plantes
    for plante in plantes_data:
        if (query_lower in plante['Plante'].lower() or 
            query_lower in plante['Nom Scientifique'].lower() or
            query_lower in plante['Goût'].lower() or
            any(query_lower in benefice.lower() for benefice in benefits_detail.get(plante['Plante'], {}).get('bienfaits', []))):
            
            plante_benefits = benefits_detail.get(plante['Plante'], {}).get('bienfaits', [])
            results.append({
                'type': 'Plante Médicinale',
                'titre': plante['Plante'],
                'description': f"{plante['Nom Scientifique']} - {', '.join(plante_benefits[:3])}",
                'details': plante,
                'score': calculate_relevance_score(query, plante['Plante'] + ' ' + plante['Nom Scientifique'] + ' ' + ' '.join(plante_benefits))
            })
    
    # Recherche dans les mélanges
    for melange in melanges_data:
        if (query_lower in melange['Nom'].lower() or 
            any(query_lower in plante.lower() for plante in melange['Plantes']) or
            any(query_lower in benefice.lower() for benefice in melange['Bienfaits'])):
            
            results.append({
                'type': 'Mélange Traditionnel',
                'titre': melange['Nom'],
                'description': f"Plantes: {', '.join(melange['Plantes'])} - {', '.join(melange['Bienfaits'][:3])}",
                'details': melange,
                'score': calculate_relevance_score(query, melange['Nom'] + ' ' + ' '.join(melange['Plantes']) + ' ' + ' '.join(melange['Bienfaits']))
            })
    
    # Trier par score de pertinence
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def calculate_relevance_score(query, text):
    """
    Calcule un score de pertinence basique
    """
    score = 0
    query_terms = query.lower().split()
    text_lower = text.lower()
    
    for term in query_terms:
        if term in text_lower:
            # Score plus élevé si le terme est au début
            position = text_lower.find(term)
            if position == 0:
                score += 3
            elif position < len(text) * 0.3:  # Dans les 30% premiers
                score += 2
            else:
                score += 1
                
            # Bonus pour les correspondances exactes
            if term == text_lower:
                score += 5
                
    return score

def parse_ird_rdf(rdf_string):
    """Parse le RDF de l'IRD et retourne les concepts structurés"""
    try:
        namespaces = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'skos': 'http://www.w3.org/2004/02/skos/core#',
            'owl': 'http://www.w3.org/2002/07/owl#'
        }
        
        root = ET.fromstring(rdf_string)
        concepts = {}
        
        for concept in root.findall('skos:Concept', namespaces):
            concept_uri = concept.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
            concept_id = concept_uri.split('/')[-1] if concept_uri else ''
            
            # Label préféré
            pref_label_elem = concept.find('skos:prefLabel', namespaces)
            pref_label = pref_label_elem.text if pref_label_elem is not None else ''
            
            # Définition
            definition_elem = concept.find('skos:definition', namespaces)
            definition = definition_elem.text if definition_elem is not None else ''
            
            # Relations broader
            broader_elem = concept.find('skos:broader', namespaces)
            broader = broader_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource') if broader_elem is not None else ''
            
            # Relations narrower
            narrower_elems = concept.findall('skos:narrower', namespaces)
            narrower = [elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource') for elem in narrower_elems]
            
            # Relations closeMatch
            close_match_elems = concept.findall('skos:closeMatch', namespaces)
            close_match = [elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource') for elem in close_match_elems]
            
            concepts[concept_uri] = {
                'id': concept_id,
                'prefLabel': pref_label,
                'definition': definition,
                'broader': broader,
                'narrower': narrower,
                'closeMatch': close_match,
                'uri': concept_uri,
                'url': f"https://ref-science.ird.fr/thesindigo/fr/page/{concept_id}" if concept_id else ''
            }
        
        return concepts
    except Exception as e:
        st.error(f"Erreur lors du parsing RDF: {e}")
        return {}

def main():
    # Header principal
    st.markdown('<h1 class="main-header">🔍 MOTEUR TISANES RÉUNIONNAISES</h1>', unsafe_allow_html=True)
    
    # Parser les données RDF
    ird_concepts = parse_ird_rdf(rdf_data)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-emoji">🌿</div>', unsafe_allow_html=True)
        st.title("Navigation")
        section = st.radio("", 
            ["🔍 Moteur de Recherche", 
             "🧪 Tous les Mélanges", 
             "🌿 Plantes Médicinales", 
             "🔬 Concepts IRD", 
             "📚 Références TNU",
             "🛒 Guide Pratique"])
        
        st.markdown("---")
        st.markdown("### 📊 Statistiques")
        st.metric("Mélanges", len(melanges_data))
        st.metric("Plantes", len(plantes_data))
        st.metric("Concepts", len(ird_concepts) + len(tnu_data))
        
        st.markdown("---")
        st.markdown("**Made with ❤️ from La Réunion**")
        st.caption("Dernière mise à jour: " + datetime.now().strftime("%d/%m/%Y"))
    
    # Sections principales
    if section == "🔍 Moteur de Recherche":
        show_search_engine()
    elif section == "🧪 Tous les Mélanges":
        show_all_melanges()
    elif section == "🌿 Plantes Médicinales":
        show_plantes_medicinales()
    elif section == "🔬 Concepts IRD":
        show_ird_concepts(ird_concepts)
    elif section == "📚 Références TNU":
        show_tnu_references()
    elif section == "🛒 Guide Pratique":
        show_guide()

def show_search_engine():
    st.header("🔍 Moteur de Recherche ThesIndigo")
    
    st.markdown("""
    ### 🌿 Recherche Multi-Sources
    
    Recherchez dans l'ensemble des connaissances sur les tisanes réunionnaises :
    - **Plantes médicinales** et leurs propriétés
    - **Mélanges traditionnels** et recettes
    - **Concepts scientifiques** IRD ThesIndigo
    - **Références TNU** (Thésaurus Numérique Unifié)
    """)
    
    # Interface de recherche
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔎 Entrez votre recherche:", 
                                   placeholder="Ex: digestion, choca, plante médicinale, TNU 056...")
    
    with col2:
        search_type = st.selectbox("Type de recherche:", 
                                 ["Tout", "Plantes", "Mélanges", "Concepts IRD", "Concepts TNU"])
    
    # Bouton de recherche
    if st.button("Rechercher", type="primary") and search_query:
        with st.spinner("Recherche en cours..."):
            results = search_thesindigo(search_query, search_type)
            
            if results:
                st.success(f"🎯 {len(results)} résultat(s) trouvé(s) pour '{search_query}'")
                
                for result in results:
                    with st.container():
                        st.markdown(f'<div class="search-result">', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            # Badge type
                            if result['type'] == 'Concept IRD':
                                st.markdown(f"**<span class='ird-badge'>{result['type']}</span>**", unsafe_allow_html=True)
                            elif result['type'] == 'Concept TNU':
                                st.markdown(f"**<span class='tnu-badge'>{result['type']}</span>**", unsafe_allow_html=True)
                            else:
                                st.markdown(f"**{result['type']}**")
                            
                            st.subheader(result['titre'])
                            st.write(result['description'])
                            
                            # Détails supplémentaires selon le type
                            if result['type'] == 'Plante Médicinale':
                                plante = result['details']
                                benefits = benefits_detail.get(plante['Plante'], {}).get('bienfaits', [])
                                st.write(f"**Goût:** {plante['Goût']} | **Partie utilisée:** {plante['Partie Utilisée']}")
                                st.write(f"**Bienfaits:** {', '.join(benefits[:3])}...")
                                
                            elif result['type'] == 'Mélange Traditionnel':
                                melange = result['details']
                                st.write(f"**Plantes:** {', '.join(melange['Plantes'])}")
                                st.write(f"**Usage:** {melange.get('Usage', 'Non spécifié')}")
                            
                        with col2:
                            if result.get('url'):
                                st.markdown(f"[🔗 Lien]({result['url']})")
                            st.metric("Pertinence", f"{result['score']}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Aucun résultat trouvé. Essayez avec d'autres termes.")
    
    # Recherches suggérées
    st.markdown("### 💡 Recherches suggérées")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌿 Plantes digestives"):
            st.experimental_set_query_params(search="digestion")
            st.rerun()
    
    with col2:
        if st.button("🔥 Anti-grippe"):
            st.experimental_set_query_params(search="grippe")
            st.rerun()
    
    with col3:
        if st.button("😴 Sommeil"):
            st.experimental_set_query_params(search="sommeil")
            st.rerun()
    
    with col4:
        if st.button("🔬 Concepts IRD"):
            st.experimental_set_query_params(search="plante médicinale")
            st.rerun()

def show_all_melanges():
    st.header("🧪 TOUS Les Mélanges Traditionnels")
    
    st.markdown(f"""
    ### 📚 Collection Complète
    **{len(melanges_data)} mélanges traditionnels** documentés et validés
    """)
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_usage = st.selectbox("Filtrer par usage:", 
                                  ["Tous"] + list(set(m.get('Usage', 'Non spécifié') for m in melanges_data)))
    
    with col2:
        filter_saison = st.selectbox("Filtrer par saison:", 
                                   ["Toutes"] + list(set(m.get('Saison', 'Toute l\'année') for m in melanges_data)))
    
    with col3:
        filter_plante = st.selectbox("Filtrer par plante:", 
                                   ["Toutes"] + list(set(plante for m in melanges_data for plante in m['Plantes'])))
    
    # Appliquer les filtres
    melanges_filtres = melanges_data
    
    if filter_usage != "Tous":
        melanges_filtres = [m for m in melanges_filtres if m.get('Usage') == filter_usage]
    
    if filter_saison != "Toutes":
        melanges_filtres = [m for m in melanges_filtres if m.get('Saison') == filter_saison]
    
    if filter_plante != "Toutes":
        melanges_filtres = [m for m in melanges_filtres if filter_plante in m['Plantes']]
    
    st.metric("Mélanges filtrés", len(melanges_filtres))
    
    # Affichage des mélanges
    for i, melange in enumerate(melanges_filtres):
        with st.expander(f"🍵 {melange['Nom']} - {len(melange['Plantes'])} plantes", expanded=i < 2):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**📝 Description :** Mélange traditionnel pour {', '.join(melange['Bienfaits'][:2])}")
                
                st.markdown("**🌿 Plantes utilisées :**")
                for plante in melange['Plantes']:
                    st.markdown(f"- {plante}")
                
                st.markdown(f"**⚖️ Proportions :** {melange['Proportions']}")
                st.markdown(f"**🕒 Instructions :** {melange['Instructions']}")
                
                st.markdown("**💚 Bienfaits principaux :**")
                for benefit in melange['Bienfaits']:
                    st.markdown(f'<span class="benefit-badge">{benefit}</span>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Usage", melange.get('Usage', 'Non spécifié'))
                st.metric("Saison", melange.get('Saison', 'Toute l\'année'))
                st.metric("Plantes", len(melange['Plantes']))
                
                # Sources
                st.markdown("**📚 Sources :**")
                st.write(melange['Source'])
                
                if melange.get('TNU_References'):
                    st.markdown("**🔗 TNU :**")
                    for tnu_ref in melange['TNU_References']:
                        st.markdown(f"<span class='tnu-badge'>TNU {tnu_ref}</span>", unsafe_allow_html=True)

def show_plantes_medicinales():
    st.header("🌿 Encyclopédie des Plantes Médicinales")
    
    df_plantes = pd.DataFrame(plantes_data)
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Plantes documentées", len(df_plantes))
    with col2:
        st.metric("Moyenne popularité", f"{df_plantes['Popularité'].mean():.1f}/10")
    with col3:
        st.metric("Plantes IRD", len([p for p in plantes_data if p['Source'] == 'IRD ThesIndigo']))
    with col4:
        st.metric("Références TNU", "2")
    
    # Recherche rapide
    search_plante = st.text_input("🔍 Rechercher une plante:", placeholder="Nom de la plante...")
    
    plantes_filtrees = df_plantes
    if search_plante:
        plantes_filtrees = df_plantes[df_plantes['Plante'].str.contains(search_plante, case=False, na=False)]
    
    # Affichage des plantes
    for _, plante in plantes_filtrees.iterrows():
        with st.expander(f"**{plante['Plante']}** - *{plante['Nom Scientifique']}*"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**🎯 Goût :** {plante['Goût']}")
                st.markdown(f"**🏷️ Partie utilisée :** {plante['Partie Utilisée']}")
                st.markdown(f"**📅 Saison :** {plante['Saison']}")
                
                # Badge source
                if plante['Source'] == 'IRD ThesIndigo':
                    st.markdown(f"**📚 Source :** <span class='ird-badge'>{plante['Source']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**📚 Source :** <span class='source-badge'>{plante['Source']}</span>", unsafe_allow_html=True)
                
                # Bienfaits
                st.markdown("**💚 Bienfaits :**")
                plant_data = benefits_detail.get(plante['Plante'], {})
                benefits = plant_data.get('bienfaits', [])
                for benefit in benefits:
                    st.markdown(f'<span class="benefit-badge">{benefit}</span>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Intensité", f"{plante['Intensité']}/5")
                st.metric("Popularité", f"{plante['Popularité']}/10")
                
                if plante['IRD_URI']:
                    st.success("🔬 Concept IRD")
                if plante.get('TNU_References'):
                    st.info("📚 Références TNU")

def show_ird_concepts(ird_concepts):
    st.header("🔬 Concepts IRD ThesIndigo")
    
    for concept_uri, concept_data in ird_concepts.items():
        with st.expander(f"**{concept_data['prefLabel']}** - `{concept_data['id']}`"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**URI :** `{concept_uri}`")
                st.markdown(f"**📖 Définition :** {concept_data['definition']}")
                
                # Relations
                if concept_data.get('broader'):
                    broader_uri = concept_data['broader']
                    broader_data = ird_concepts.get(broader_uri, {})
                    st.markdown(f"**⬆️ Concept parent :** [{broader_data.get('prefLabel', 'N/A')}]({broader_data.get('url', '')})")
                
                if concept_data.get('narrower'):
                    st.markdown("**⬇️ Concepts enfants :**")
                    for narrower_uri in concept_data['narrower']:
                        narrower_data = ird_concepts.get(narrower_uri, {})
                        st.markdown(f"- [{narrower_data.get('prefLabel', 'N/A')}]({narrower_data.get('url', '')})")
            
            with col2:
                if concept_data.get('url'):
                    st.markdown(f"[🌐 Page ThesIndigo]({concept_data['url']})")
                st.metric("ID Concept", concept_data['id'])

def show_tnu_references():
    st.header("📚 Références TNU")
    
    for tnu_code, tnu_info in tnu_data.items():
        with st.expander(f"**TNU {tnu_code}** - {tnu_info['prefLabel']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**URI :** `{tnu_info['uri']}`")
                st.markdown(f"**📖 Définition :** {tnu_info['definition']}")
                
                # Plantes associées
                plantes_associees = [p['Plante'] for p in plantes_data if tnu_code in p.get('TNU_References', [])]
                if plantes_associees:
                    st.markdown("**🌿 Plantes associées :**")
                    for plante in plantes_associees:
                        st.markdown(f"- {plante}")
            
            with col2:
                st.markdown(f"[🌐 Page TNU]({tnu_info['url']})")
                st.metric("Code TNU", tnu_code)

def show_guide():
    st.header("🛒 Guide Pratique")
    
    tab1, tab2 = st.tabs(["📖 Utilisation", "🔍 Recherche Avancée"])
    
    with tab1:
        st.markdown("""
        ### 📖 Guide d'Utilisation
        
        **Pour une recherche efficace :**
        1. Utilisez des termes simples et précis
        2. Essayez les noms scientifiques pour les plantes
        3. Utilisez les filtres par type de contenu
        4. Explorez les recherches suggérées
        
        **Exemples de recherches :**
        - "choca" → plante spécifique
        - "digestion" → plantes et mélanges pour la digestion
        - "TNU 056" → concept TNU spécifique
        - "plante médicinale" → concepts IRD
        """)
    
    with tab2:
        st.markdown("""
        ### 🔍 Recherche Avancée
        
        **Syntaxe de recherche :**
        - **Termes multiples** : "choca digestion"
        - **Recherche exacte** : mettre entre guillemets
        - **Filtrage par type** : utiliser le sélecteur
        
        **Types de contenu :**
        - **Plantes** : informations détaillées sur chaque plante
        - **Mélanges** : recettes traditionnelles complètes
        - **Concepts IRD** : taxonomie scientifique
        - **Concepts TNU** : thésaurus spécialisés
        """)

if __name__ == "__main__":
    main()