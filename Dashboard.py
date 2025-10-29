import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json

# Configuration de la page
st.set_page_config(
    page_title="Tisanes Réunionnaises - IRD ThesIndigo",
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
    .taxonomy-tree {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        border: 1px solid #ddd;
    }
    .concept-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .skos-relation {
        background-color: #e8f4f8;
        padding: 8px;
        border-radius: 5px;
        margin: 5px 0;
        border-left: 3px solid #1a73e8;
    }
    .sidebar-emoji {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# CORRECTION : Restructuration des données en liste de dictionnaires
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
        'IRD_URI': ''
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
        'IRD_URI': ''
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
        'IRD_URI': ''
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
        'IRD_URI': ''
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
        'IRD_URI': ''
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
        'IRD_URI': ''
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
        'IRD_URI': ''
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
        'IRD_URI': 'https://uri.ird.fr/so/kos/thesindigo/75406'
    }
]

# Bienfaits détaillés enrichis
benefits_detail = {
    'Choca (Ayapana)': {
        'bienfaits': ['Digestif', 'Fébrifuge', 'Anti-grippe', 'Décongestionnant', 'Antioxydant'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Tangor': {
        'bienfaits': ['Calmant', 'Sédatif', 'Digestif', 'Anti-stress', 'Vitamine C'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Citronnelle': {
        'bienfaits': ['Digestif', 'Fébrifuge', 'Anti-inflammatoire', 'Rafraîchissant', 'Antispasmodique'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Vétiver': {
        'bienfaits': ['Digestif', 'Anti-nauséeux', 'Apaisant', 'Sudorifique'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Gingembre': {
        'bienfaits': ['Tonifiant', 'Anti-nauséeux', 'Anti-inflammatoire', 'Stimulant circulatoire', 'Aphrodisiaque'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Curcuma': {
        'bienfaits': ['Anti-inflammatoire', 'Antioxydant', 'Hépatoprotecteur', 'Digestif'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Faham': {
        'bienfaits': ['Aphrodisiaque', 'Tonique', 'Asthme', 'Stimulant', 'Expectorant'],
        'source': 'APLAMEDOM',
        'references': ['https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/']
    },
    'Quinquina': {
        'bienfaits': ['Fébrifuge', 'Antipaludéen', 'Tonique amer', 'Stomachique'],
        'source': 'IRD ThesIndigo',
        'references': ['https://ref-science.ird.fr/thesindigo/fr/page/212443']
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

# Parser les données RDF
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

# Données de taxonomie enrichies
taxonomy_data = {
    'MONDE VEGETAL': {
        'uri': 'https://uri.ird.fr/so/kos/thesindigo/214560',
        'enfants': ['PLANTE MEDICINALE'],
        'definition': 'Ensemble du règne végétal et des plantes',
        'niveau': 0
    },
    'PLANTE MEDICINALE': {
        'uri': 'https://uri.ird.fr/so/kos/thesindigo/212443',
        'parent': 'MONDE VEGETAL',
        'enfants': ['QUINQUINA', 'CHOCA', 'TANGOR', 'CITRONNELLE', 'VETIVER', 'GINGEMBRE', 'CURCUMA', 'FAHAM'],
        'sources_externes': ['APLAMEDOM', 'TNU 056', 'TNU 076'],
        'definition': 'Plante possédant des propriétés médicinales utilisées en thérapeutique',
        'niveau': 1,
        'url': 'https://ref-science.ird.fr/thesindigo/fr/page/212443'
    },
    'QUINQUINA': {
        'uri': 'https://uri.ird.fr/so/kos/thesindigo/75406',
        'parent': 'PLANTE MEDICINALE',
        'definition': 'Plante médicinale utilisée traditionnellement contre la fièvre',
        'niveau': 2,
        'url': 'https://ref-science.ird.fr/thesindigo/fr/page/75406'
    }
}

# Mélanges typiques
melanges_data = [
    {
        'Nom': 'Digestion Facile',
        'Plantes': ['Choca (Ayapana)', 'Vétiver', 'Citronnelle'],
        'Proportions': '2 parts Choca, 1 part Vétiver, 1 part Citronnelle',
        'Instructions': 'Infusion 10 min - Boire après le repas',
        'Bienfaits': ['Digestion', 'Ballonnements', 'Nausées'],
        'Source': 'Tradition Réunionnaise + APLAMEDOM'
    },
    {
        'Nom': 'Nuit Paisible',
        'Plantes': ['Tangor', 'Citronnelle'],
        'Proportions': '3 parts Tangor, 1 part Citronnelle',
        'Instructions': 'Infusion 5-7 min - Boire avant le coucher',
        'Bienfaits': ['Sommeil', 'Relaxation', 'Stress'],
        'Source': 'Tradition Réunionnaise + APLAMEDOM'
    },
    {
        'Nom': 'Boost Immunité',
        'Plantes': ['Choca (Ayapana)', 'Gingembre', 'Citronnelle', 'Quinquina'],
        'Proportions': '2 parts Choca, 1 part Gingembre, 1 part Citronnelle, 1/2 part Quinquina',
        'Instructions': 'Décoction 15 min - Boire 2-3 fois/jour',
        'Bienfaits': ['Grippe', 'Fièvre', 'Fatigue', 'Immunité'],
        'Source': 'Synthèse Traditionnelle + IRD'
    }
]

def main():
    # Header principal
    st.markdown('<h1 class="main-header">🍃 TISANES RÉUNIONNAISES - RÉFÉRENTIEL IRD</h1>', unsafe_allow_html=True)
    
    # Parser les données RDF
    ird_concepts = parse_ird_rdf(rdf_data)
    
    # Introduction avec sources
    st.markdown("""
    **🌿 Base de connaissances intégrée** - Ce dashboard combine les données de l'APLAMEDOM avec le référentiel scientifique 
    **IRD ThesIndigo**, offrant une vision complète des plantes médicinales réunionnaises validée par la recherche.
    
    **🔗 Sources intégrées :**
    - 🌿 [APLAMEDOM Réunion](https://www.aplamedom.fr/les-plantes-medicinales-de-la-reunion/)
    - 🔬 [IRD ThesIndigo](https://ref-science.ird.fr/thesindigo/fr/index)
    """)
    
    # Sidebar
    with st.sidebar:
        # Correction : utiliser markdown pour l'émoji au lieu de st.image
        st.markdown('<div class="sidebar-emoji">🧪</div>', unsafe_allow_html=True)
        st.title("Navigation")
        section = st.radio("", 
            ["🏠 Accueil", 
             "🌿 Plantes Médicinales", 
             "🔬 Concepts IRD", 
             "🧪 Mélanges Traditionnels", 
             "📚 Références Croisées",
             "🛒 Guide Pratique"])
        
        st.markdown("---")
        st.markdown("### 📊 Filtres")
        selected_benefit = st.selectbox("Filtrer par bienfait", 
                                      ["Tous"] + list(set([benefit for plant_data in benefits_detail.values() for benefit in plant_data['bienfaits']])))
        
        selected_source = st.selectbox("Filtrer par source", 
                                     ["Toutes", "APLAMEDOM", "IRD ThesIndigo", "Tradition Réunionnaise"])
        
        st.markdown("---")
        st.markdown("**Made with ❤️ from La Réunion**")
        st.caption("Dernière mise à jour: " + datetime.now().strftime("%d/%m/%Y"))
    
    # Sections principales
    if section == "🏠 Accueil":
        show_accueil(ird_concepts)
    elif section == "🌿 Plantes Médicinales":
        show_plantes(selected_benefit, selected_source, ird_concepts)
    elif section == "🔬 Concepts IRD":
        show_ird_concepts(ird_concepts)
    elif section == "🧪 Mélanges Traditionnels":
        show_melanges(selected_source)
    elif section == "📚 Références Croisées":
        show_references()
    elif section == "🛒 Guide Pratique":
        show_guide()

def show_accueil(ird_concepts):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌺 Référentiel Scientifique Intégré
        
        **🎯 Nouveautés avec l'intégration IRD ThesIndigo :**
        
        **🔬 Données structurées SKOS :**
        - Concepts scientifiques normalisés
        - Relations sémantiques (broader/narrower)
        - Alignement avec thésaurus internationaux
        - URI persistantes pour chaque concept
        
        **🌿 Integration APLAMEDOM + IRD :**
        - 7 plantes documentées par l'APLAMEDOM
        - 1 plante référencée par l'IRD (Quinquina)
        - Taxonomie scientifique unifiée
        - Métadonnées enrichies
        
        **📊 Interopérabilité :**
        - Format RDF/XML standard
        - Web sémantique et linked data
        - Références croisées TNU
        - Alignement SKOS/XLS
        """)
        
        # Métriques des sources
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            st.metric("Concepts IRD", len(ird_concepts))
        with col1_2:
            st.metric("Plantes APLAMEDOM", "7")
        with col1_3:
            st.metric("Relations SKOS", "6+")
    
    with col2:
        # Carte conceptuelle simplifiée
        st.plotly_chart(create_concept_map(ird_concepts), use_container_width=True)
        
        # Accès rapide aux concepts
        st.markdown("### 🔗 Concepts IRD")
        for concept_uri, concept_data in ird_concepts.items():
            if concept_data.get('url'):
                st.markdown(f"• [{concept_data['prefLabel']}]({concept_data['url']})")

def show_plantes(selected_benefit, selected_source, ird_concepts):
    st.header("🌿 Encyclopédie des Plantes Médicinales")
    
    # CORRECTION : Convertir en DataFrame pour faciliter le filtrage
    df_plantes = pd.DataFrame(plantes_data)
    
    # Application des filtres
    filtered_plantes = df_plantes.copy()
    
    if selected_benefit != "Tous":
        plantes_filtrees = [
            plante for plante, data in benefits_detail.items() 
            if selected_benefit in data['bienfaits']
        ]
        filtered_plantes = filtered_plantes[filtered_plantes['Plante'].isin(plantes_filtrees)]
    
    if selected_source != "Toutes":
        filtered_plantes = filtered_plantes[filtered_plantes['Source'] == selected_source]
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Plantes documentées", len(filtered_plantes))
    with col2:
        ird_count = len(filtered_plantes[filtered_plantes['Source'] == 'IRD ThesIndigo'])
        st.metric("Plantes IRD", ird_count)
    with col3:
        st.metric("Concepts liés", "3")
    with col4:
        st.metric("SKOS Relations", "6")
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique de popularité par source
        fig_pop = px.bar(filtered_plantes, x='Plante', y='Popularité', 
                        color='Source',
                        title='Popularité des Plantes par Source',
                        color_discrete_map={
                            'APLAMEDOM': '#2E8B57',
                            'IRD ThesIndigo': '#0055A4'
                        })
        st.plotly_chart(fig_pop, use_container_width=True)
    
    with col2:
        # Relations avec IRD
        st.markdown("### 🔗 Liens avec IRD ThesIndigo")
        for _, plante in filtered_plantes.iterrows():
            if plante['IRD_URI']:
                concept_data = ird_concepts.get(plante['IRD_URI'], {})
                st.markdown(f"""
                **{plante['Plante']}** → 
                [Concept IRD]({concept_data.get('url', '')}) | 
                SKOS: `{plante['IRD_URI'].split('/')[-1]}`
                """)
    
    # Détails des plantes
    for _, plante in filtered_plantes.iterrows():
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
                
                # Affichage des bienfaits
                st.markdown("**💚 Bienfaits :**")
                plant_data = benefits_detail.get(plante['Plante'], {})
                benefits = plant_data.get('bienfaits', [])
                for benefit in benefits:
                    st.markdown(f'<span class="benefit-badge">{benefit}</span>', unsafe_allow_html=True)
                
                # Références
                references = plant_data.get('references', [])
                if references:
                    st.markdown("**🔗 Références :**")
                    for ref in references:
                        st.markdown(f"- [{ref}]({ref})")
            
            with col2:
                st.metric("Intensité", f"{plante['Intensité']}/5")
                st.metric("Popularité", f"{plante['Popularité']}/10")
                
                if plante['IRD_URI']:
                    st.success("🔬 Concept IRD")
                else:
                    st.info("🌿 Donnée APLAMEDOM")

def show_ird_concepts(ird_concepts):
    st.header("🔬 Concepts IRD ThesIndigo")
    
    st.markdown("""
    ### 📚 Référentiel Scientifique Structuré
    
    L'IRD ThesIndigo utilise le standard **SKOS** (Simple Knowledge Organization System) pour structurer 
    les connaissances sur la biodiversité réunionnaise selon les principes du web sémantique.
    """)
    
    # Affichage des concepts
    for concept_uri, concept_data in ird_concepts.items():
        with st.expander(f"**{concept_data['prefLabel']}** - `{concept_data['id']}`"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**URI :** `{concept_uri}`")
                
                if concept_data.get('definition'):
                    st.markdown(f"**📖 Définition :** {concept_data['definition']}")
                
                # Relations broader
                if concept_data.get('broader'):
                    broader_uri = concept_data['broader']
                    broader_data = ird_concepts.get(broader_uri, {})
                    st.markdown(f"**⬆️ Concept parent :** [{broader_data.get('prefLabel', 'N/A')}]({broader_data.get('url', '')})")
                
                # Relations narrower
                if concept_data.get('narrower'):
                    st.markdown("**⬇️ Concepts enfants :**")
                    for narrower_uri in concept_data['narrower']:
                        narrower_data = ird_concepts.get(narrower_uri, {})
                        st.markdown(f"- [{narrower_data.get('prefLabel', 'N/A')}]({narrower_data.get('url', '')})")
                
                # Relations closeMatch
                if concept_data.get('closeMatch'):
                    st.markdown("**🔗 Concepts équivalents :**")
                    for match_uri in concept_data['closeMatch']:
                        st.markdown(f"- `{match_uri}`")
            
            with col2:
                if concept_data.get('url'):
                    st.markdown(f"[🌐 Page ThesIndigo]({concept_data['url']})")
                
                # Métriques du concept
                st.metric("ID Concept", concept_data['id'])
                
                relation_count = len(concept_data.get('narrower', [])) + len(concept_data.get('closeMatch', []))
                if concept_data.get('broader'):
                    relation_count += 1
                st.metric("Relations SKOS", relation_count)
    
    # Arbre taxonomique interactif
    st.markdown("### 🌳 Arbre des Concepts SKOS")
    display_skos_tree(ird_concepts)

def show_melanges(selected_source):
    st.header("🧪 Mélanges Traditionnels Documentés")
    
    # Filtrage des mélanges
    melanges_filtres = melanges_data
    if selected_source != "Toutes":
        melanges_filtres = [m for m in melanges_data if selected_source in m.get('Source', '')]
    
    # CORRECTION : Créer un mapping pour les sources des plantes
    plante_source_mapping = {p['Plante']: p['Source'] for p in plantes_data}
    
    for melange in melanges_filtres:
        with st.container():
            st.markdown(f'<div class="plant-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"🍵 {melange['Nom']}")
                st.markdown(f"**Plantes :** {', '.join(melange['Plantes'])}")
                st.markdown(f"**Proportions :** {melange['Proportions']}")
                st.markdown(f"**Instructions :** ⏱️ {melange['Instructions']}")
                st.markdown(f"**Source :** {melange.get('Source', 'Tradition')}")
                
                st.markdown("**💚 Bienfaits :**")
                for benefit in melange['Bienfaits']:
                    st.markdown(f'<span class="benefit-badge">{benefit}</span>', unsafe_allow_html=True)
            
            with col2:
                # CORRECTION : Utiliser le mapping pour les sources
                sources_count = {}
                for plante in melange['Plantes']:
                    source = plante_source_mapping.get(plante, 'Inconnue')
                    sources_count[source] = sources_count.get(source, 0) + 1
                
                st.markdown("**📚 Sources des plantes :**")
                for source, count in sources_count.items():
                    if source == 'IRD ThesIndigo':
                        st.markdown(f"- <span class='ird-badge'>{source}</span> ({count})", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- <span class='source-badge'>{source}</span> ({count})", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_references():
    st.header("📚 Références Croisées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔗 Alignement des Données
        
        **Standards utilisés :**
        - **SKOS/RDF** : Structure sémantique des concepts
        - **URI persistantes** : Identifiants uniques et stables
        - **Linked Data** : Interconnexion des données
        - **TNU** : Thésaurus numériques unifiés
        
        **Flux de données :**
        ```
        APLAMEDOM (Données terrain)
                ↓
        IRD ThesIndigo (Structuration)
                ↓
        Dashboard (Visualisation)
                ↓
        Utilisateurs (Diffusion)
        ```
        """)
    
    with col2:
        st.markdown("""
        ### 🌐 Interopérabilité
        
        **Points d'accès :**
        - 📡 **Endpoint SPARQL** : Requêtes sémantiques
        - 🔗 **API REST** : Données structurées JSON-LD
        - 📊 **Export RDF/XML** : Format standard
        - 🌍 **Linked Open Data** : Données liées
        
        **Alignements externes :**
        - AGROVOC (FAO)
        - DBpedia
        - Wikidata
        - TAXREF (INPN)
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📖 Bibliographie
    
    **Références principales :**
    1. **APLAMEDOM** - *Plantes médicinales de La Réunion* (2023)
    2. **IRD ThesIndigo** - *Thésaurus de la biodiversité* (2023)
    3. **SKOS Reference** - W3C Recommendation (2009)
    4. **Linked Data Patterns** - Leigh Dodds (2012)
    
    **Standards techniques :**
    - SKOS Primer - W3C
    - RDF 1.1 Concepts - W3C  
    - JSON-LD 1.1 - W3C
    - URI Persistence Best Practices
    """)

def show_guide():
    st.header("🛒 Guide d'Utilisation des Données")
    
    tab1, tab2, tab3 = st.tabs(["🔍 Recherche", "📊 Analyse", "🤝 Contribution"])
    
    with tab1:
        st.markdown("""
        ### 🔍 Guide de Recherche
        
        **Recherche par concepts :**
        - Utilisez les URI IRD pour une recherche précise
        - Naviguez via les relations SKOS (broader/narrower)
        - Exploitez les alignements (closeMatch)
        
        **Exemples de requêtes :**
        - "Plantes médicinales" → Concept IRD 212443
        - "Quinquina" → Concept IRD 75406
        - "Monde végétal" → Concept IRD 214560
        
        **Outils de recherche :**
        - [Moteur de recherche ThesIndigo](https://ref-science.ird.fr/thesindigo/fr/index)
        - Navigateur SKOS
        - Client SPARQL
        """)
    
    with tab2:
        st.markdown("""
        ### 📊 Analyse des Données
        
        **Métriques clés :**
        - Nombre de concepts par domaine
        - Densité des relations SKOS
        - Couverture géographique
        - Alignements externes
        
        **Visualisations disponibles :**
        - Arbres taxonomiques interactifs
        - Graphes de relations sémantiques
        - Cartes de concepts
        - Analyses de réseau
        """)
    
    with tab3:
        st.markdown("""
        ### 🤝 Contribution aux Données
        
        **Pour les chercheurs :**
        - Proposer de nouveaux concepts
        - Améliorer les alignements
        - Documenter les relations
        - Valider les données
        
        **Processus de contribution :**
        1. Identification du besoin
        2. Création/modification du concept
        3. Ajout des relations SKOS
        4. Alignement avec référentiels
        5. Validation par les pairs
        6. Publication dans ThesIndigo
        
        **Contacts :**
        - 📧 IRD : thesindigo@ird.fr
        - 🌿 APLAMEDOM : contact@aplamedom.fr
        """)

def create_concept_map(ird_concepts):
    """Crée une visualisation des concepts IRD"""
    nodes = []
    links = []
    
    # Ajouter les nœuds
    for uri, data in ird_concepts.items():
        nodes.append({
            'id': data['prefLabel'],
            'group': 1,
            'value': len(data.get('narrower', [])) + 1
        })
    
    # Ajouter les liens
    for uri, data in ird_concepts.items():
        if data.get('broader'):
            broader_uri = data['broader']
            broader_data = ird_concepts.get(broader_uri, {})
            if broader_data.get('prefLabel'):
                links.append({
                    'source': broader_data['prefLabel'],
                    'target': data['prefLabel'],
                    'value': 1
                })
    
    # Créer un graphique simple
    if nodes:
        node_names = [node['id'] for node in nodes]
        source_indices = []
        target_indices = []
        
        for link in links:
            if link['source'] in node_names and link['target'] in node_names:
                source_indices.append(node_names.index(link['source']))
                target_indices.append(node_names.index(link['target']))
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_names,
                color="blue"
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=[1] * len(source_indices)
            )
        )])
        
        fig.update_layout(title_text="Relations SKOS entre concepts IRD", height=300)
        return fig
    else:
        # Fallback si pas de données
        fig = go.Figure()
        fig.update_layout(
            title="Aucune donnée de concept disponible",
            xaxis_title="Concepts",
            yaxis_title="Relations",
            height=300
        )
        return fig

def display_skos_tree(ird_concepts):
    """Affiche l'arbre des concepts SKOS"""
    st.markdown('<div class="taxonomy-tree">', unsafe_allow_html=True)
    
    # Trouver le concept racine (sans broader)
    root_concepts = []
    for uri, data in ird_concepts.items():
        if not data.get('broader'):
            root_concepts.append(data)
    
    for root in root_concepts:
        display_concept_hierarchy(root, ird_concepts, 0)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_concept_hierarchy(concept, ird_concepts, level):
    """Affiche récursivement la hiérarchie des concepts"""
    indent = "  " * level
    concept_url = concept.get('url', '')
    
    if concept_url:
        st.markdown(f"{indent}🌿 **[{concept['prefLabel']}]({concept_url})** `{concept['id']}`")
    else:
        st.markdown(f"{indent}🌿 **{concept['prefLabel']}** `{concept['id']}`")
    
    if concept.get('definition'):
        st.markdown(f"{indent}   📖 *{concept['definition']}*")
    
    # Afficher les concepts enfants
    for narrower_uri in concept.get('narrower', []):
        narrower_data = ird_concepts.get(narrower_uri, {})
        if narrower_data:
            display_concept_hierarchy(narrower_data, ird_concepts, level + 1)

if __name__ == "__main__":
    main()