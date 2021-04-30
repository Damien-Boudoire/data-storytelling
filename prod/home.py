import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

layout=html.Div([
        html.P( "L'impact négatif du covid sur l'économie est aujourd'hui un consensus parmi les experts."\
                " Si nous avons pu mesurer en partie son impact sur l'économie mondiale en 2020, "\
                "il est difficile aujourd'hui de faire des conjectures sur le futur."),
        html.P( "Ce projet a pour vocation de présenter les données de manière à évaluer "\
                "la situation actuelle de la manière la plus exhaustive et objective possible, "\
                "afin que chacun puisse en tirer ses propres conclusions."),
        html.P( ["Le jeu de donné utilisé dans cette étude a été collecté sur ",
                html.A("https://data.mendeley.com/datasets/b2wvnbnpj9/1", href="https://data.mendeley.com/datasets/b2wvnbnpj9/1"),". "\
                "Il présente pour 170 pays avec une granularité journalière l’impact de la maladie en 2020 (nombre de cas, nombre de décès), "\
                "ainsi qu’un l’indice de sévérité de réponse (STI : composition de 9 sous-indices parmi lesquels : fermeture des écoles, des bureaux, "\
                "restrictions de voyage, …). Nous mettrons ces mesures en relation avec les données économiques suivantes : "\
                "PIB par habitant, population et indice de développement humain (HDI)."]),
        html.P( "Les variables économiques présentées dans notre jeu de données ont été mesurées en 2019, "\
                "et les données 2020 n’ont pas encore été publiées par la WorldBank. "\
                "Il nous est donc impossible de chiffrer l’impact de la COVID sur ces indicateurs. "\
                "En revanche nous pouvons d’ores et déjà tirer les quelques conclusions basées sur notre perception de la situation, "\
                "ainsi que les chiffres du PIB en Europe publiés par Eurostat et présentant une récession de 6.1% en 2020."),
        html.P( "La COVID 19 a eu un impact négatif fort sur l’économie mondiale. Les restrictions mises en place ont impacté à la fois l’offre et la demande, "\
                "et auront nécessairement un impact à long terme dû aux effets secondaires profonds (santé, investissements publics, éducation, …). "\
                "La population et la santé des habitants des différents pays a également clairement été impactée. "\
                "Nous pouvons donc affirmer avec une raisonnable certitude que l’impact économique négatif du covid sera corrélés aux 3 variables "\
                "TC, TD, et STI, sans pour autant être capable d’évaluer cette corrélation. "\
                "Nous nous contenterons donc de présenter l’évolution de ces variables au cours du temps et d’étudier "\
                "leur corrélation avec nos trois indicateurs économiques.")
        ])
