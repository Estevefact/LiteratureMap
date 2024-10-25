import ast
import os

import numpy as np
import pandas as pd

short_coem_numbers = pd.read_excel('embeddings_total.xlsx')
short_coem_metadata =  pd.read_excel('coem_authors_enriched.xlsx')
shorc_metadata = pd.read_excel('coem_cuentos_authors.xlsx')
Totals_df1 = pd.merge(short_coem_numbers, shorc_metadata, left_on="vector_id" ,right_on='uuid_story', how='left')
Totals_df1=Totals_df1[["vector_id","values","author_uuid","story_name","reading_time_min"]].copy()
Totals_df = pd.merge(Totals_df1, short_coem_metadata, left_on="author_uuid" ,right_on='UUID', how='left')
Totals_df=Totals_df[['vector_id', 'values', 'story_name', 'reading_time_min',
       'Author', 'LastName', 'Name', 'country', 'genera',
        'Wiki_URL', 'cats', 'linked_authors','Birth Year', 'Death Year']].copy()#'Summary'
Totals_df_labels = Totals_df.drop(Totals_df.columns[:2], axis=1)
Totals_df_labels = Totals_df_labels.replace('\t', '', regex=True)
Totals_df_labels = Totals_df_labels.replace('\n', '', regex=True)
Totals_df_labels = Totals_df_labels.replace('ñ', 'n', regex=True)


non_numeric_mapping_death = {
    '1863 y 1786': 1863,  # Assuming you want to take the first year
    'c.1400': 1400,
    '1976 (desaparecido)': 1976,
    'nan':np.nan
}

# Replace known non-numeric values using the mapping
Totals_df_labels['Death Year'].replace(non_numeric_mapping_death,inplace=True)

Totals_df_labels['Death Year'] = pd.to_numeric(Totals_df_labels['Death Year'], errors='coerce')
# Convert all values to numeric, setting errors='coerce' will convert non-numeric values to NaN
country_mapping = {
    'Estadounidense': "Estados Unidos",  # Assuming you want to take the first year
    'Inglesa': "Inglaterra",
    'Argentino': "Argentina",
    'Espana': "España",
    'nan':np.nan,
    "Cubano":"Cuba",
    "Puertorriqueno": "Puerto Rico",
    "Nueva Zelandia": "Nueva Zelanda"
}

# Replace known non-numeric values using the mapping
Totals_df_labels['country'].replace(country_mapping,inplace=True)

non_numeric_mapping_birth = {
    'Siglo VI AC': -600,   # 6th century BC
    'Siglo XII': 1200      # 12th century
}

# Replace known non-numeric values using the mapping
Totals_df_labels['Birth Year'].replace(non_numeric_mapping_birth,inplace=True)

Totals_df_labels['Birth Year'] = pd.to_numeric(Totals_df_labels['Birth Year'], errors='coerce')
#FillNAs
Totals_df_labels['Name'] = Totals_df_labels['Name'].fillna("Unknown")
Totals_df_labels['country'] = Totals_df_labels['country'].fillna("Unknown")
Totals_df_labels['genera'] = Totals_df_labels['genera'].fillna("Unknown")
Totals_df_labels['cats'] = Totals_df_labels['cats'].fillna("Unknown")
Totals_df_labels['Wiki_URL'] = Totals_df_labels['Wiki_URL'].fillna("Unknown")
Totals_df_labels['linked_authors'] = Totals_df_labels['linked_authors'].fillna("Unknown")
Totals_df_labels['Birth Year'] = Totals_df_labels['Birth Year'].fillna(0)
Totals_df_labels['Death Year'] = Totals_df_labels['Death Year'].fillna(0)


#rename columns
new_column_names = {
    'story_name': 'Título',
    'reading_time_min': 'Tiempo de Lectura (min)',
    'Author': 'Nombre Completo Autor',
    'LastName': 'Apellido Autor',
    'Name': 'Primer Nombre Autor',
    'country': 'País',
    'genera': 'Género',
    'Wiki_URL': 'URL Wikipedia',
    'cats': 'Categorías',
    'linked_authors': 'Autores relacionados',
    'Birth Year': 'Año de nacimiento',
    'Death Year': 'Año de muerte'
}

Totals_df_labels.rename(columns=new_column_names, inplace=True)

Totals_df_labels=Totals_df_labels[["Título",'Tiempo de Lectura (min)','Primer Nombre Autor','Apellido Autor','Nombre Completo Autor','País','Género','Año de nacimiento','Año de muerte','Autores relacionados','Categorías']].copy()
##### Saving
directory=os.path.join(os.path.dirname(__file__))
filname= os.path.join(directory, "stories_metadata.tsv")
Totals_df_labels.to_csv(filname, sep='\t', index=False, header=True)
Totals_df_vals=Totals_df.iloc[:, 1:2].copy()
Totals_df_vals['values'] = Totals_df_vals['values'].apply(ast.literal_eval)
array_2d = np.array(Totals_df_vals['values'].tolist())
print(array_2d.shape)
filname= os.path.join(directory, "stories_tensors.bytes")
array_2d.tofile(filname)
Stories_tensors=pd.DataFrame(Totals_df_vals['values'].tolist())
filname=os.path.join(directory, "stories_tensors.tsv")
Stories_tensors.to_csv(filname, sep='\t', index=False, header=False)

#English change
new_column_names_english = {
    'Título': 'Title',
    'Tiempo de Lectura (min)': 'Reading time (min)',
    'Primer Nombre Autor': 'Author',
    'Apellido Autor':'Last Name' ,
    'Nombre Completo Autor': 'Name',
    'País': 'Country',
    'Género': 'Genre',
    'URL Wikipedia': 'Wiki URL',
    'Categorías': 'Categories',
    'Autores relacionados':'Linked Authors',
    'Año de nacimiento':'Birth Year' ,
    'Año de muerte':'Death Year'
}
translation_dict_genre = {
    'Romanticismo': 'Romanticism',
    'Unknown': 'Unknown',
    'Histórico': 'Historical',
    'Rural': 'Rural',
    'Modernismo': 'Modernism',
    'Dramaturgia': 'Dramaturgy',
    'Pedagógico': 'Pedagogical',
    'Fantasía': 'Fantasy',
    'Realismo': 'Realism',
    'Periodismo': 'Journalism',
    'Suspenso': 'Suspense',
    'modernismo': 'Modernism',
    'Comedia': 'Comedy',
    'Ficción': 'Fiction',
    'Historieta': 'Comic Strip',
    'Paranoia': 'Paranoia',
    'historias cortas': 'Short Stories',
    'Ambiental': 'Environmental',
    'Surrealismo': 'Surrealism',
    'Chejov': 'Chekhov'
}

country_translation_dict = {
    'Espana': 'Spain',
    'Estados Unidos': 'United States',
    'Uruguay': 'Uruguay',
    'Cuba': 'Cuba',
    'Grecia': 'Greece',
    'Francia': 'France',
    'Argentina': 'Argentina',
    'Unknown': 'Unknown',
    'Italia': 'Italy',
    'India': 'India',
    'Mexico': 'Mexico',
    'Rusia': 'Russia',
    'Inglaterra': 'England',
    'África': 'Africa',
    'Brasil': 'Brazil',
    'Portugal': 'Portugal',
    'Arabia': 'Arabia',
    'Guatemala': 'Guatemala',
    'Dinamarca': 'Denmark',
    'Irlanda': 'Ireland',
    'Colombia': 'Colombia',
    'Peru': 'Peru',
    'Alemania': 'Germany',
    'Checoslovaquia': 'Czechoslovakia',
    'Hungria': 'Hungary',
    'Venezuela': 'Venezuela',
    'Belgica': 'Belgium',
    'Chile': 'Chile',
    'Líbano': 'Lebanon',
    'Noruega': 'Norway',
    'Puerto Rico': 'Puerto Rico',
    'Reino Unido': 'United Kingdom',
    'Suiza': 'Switzerland',
    'Japon': 'Japan',
    'Polonia': 'Poland',
    'Republica Dominicana': 'Dominican Republic',
    'Oriente': 'East',
    'Nicaragua': 'Nicaragua',
    'China': 'China',
    'Nueva Zelanda': 'New Zealand',
    'Escocia': 'Scotland',
    'Ecuador': 'Ecuador',
    'Suecia': 'Sweden',
    'Egipto': 'Egypt',
    'El Salvador': 'El Salvador',
    'Paraguay': 'Paraguay',
    'Prusia': 'Prussia',
    'Costa Rica': 'Costa Rica',
    'Gales': 'Wales'
}


Totals_df_labels.rename(columns=new_column_names_english, inplace=True)
Totals_df_labels['Genre'] = Totals_df_labels['Genre'].map(translation_dict_genre)
Totals_df_labels['Country'] = Totals_df_labels['Country'].map(country_translation_dict)
print(Totals_df_labels['Country'].unique())
Totals_df_labels['Country'] = Totals_df_labels['Country'].fillna("Unknown")
filname= os.path.join(directory, "stories_metadata_english.tsv")
Totals_df_labels.to_csv(filname, sep='\t', index=False, header=True)


#50 is the max Categorical
# TODO
# Missing filling the dataframe more. add Children category and category of how hard is it to
# understand, also deploy this in github.io for people to explore and docs

