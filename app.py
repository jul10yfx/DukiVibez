#1. Importar las librerias necesarias para el proyecto
import streamlit as st #Streamlit para la interfaz
import pandas as pd #Pandas para la lectra de las bases de datos en formato .csv y uso de DataFrame
import altair as alt #Altair para crear graficos interactivos
from textblob import TextBlob #Textblob para el analisis de las letras de las canciones y darle un rango de -1 (negativo) a 1 (positivo) 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #Vader para el analisis de los comentarios de redes sociales 
from wordcloud import WordCloud, STOPWORDS #WordCloud y STOPWORDS para crear nubes de palabras y visualizar la frecuencia de palabras comunes en los comentarios
import matplotlib.pyplot as plt #Matplotlib para generar gráficos
import re #Re usado para limpiar textos quitar símbolos o links de los comentarios a analizar
import random #Random para elegir una canción al azar
from collections import Counter #Countes paraa contar frecuencias de elementos de manera más sencilla

# Definir un patrón usando re.compile() para encontrar caracteres que coincidan con los rangos que se listan a continuación para quitar emojis de los comentarios de la base de datos (ayuda de la ia).
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # rango de emojis de emmoticonos
                           u"\U0001F680-\U0001F6FF"  # rango de emojis de transporte
                           u"\U0001F1E0-\U0001F1FF" # rango de emojis de banderas
                           u"\u2600-\u26FF"          # rango de emojis de símbolos misceláneos
                           u"\u2700-\u27BF"         # rango de emojis de símbolos misceláneos    
                           "]+", flags=re.UNICODE) # El patrón termina y especifica que se interpretará usando codificación Unicode (flags=re.UNICODE), para incluir correctamente caracteres no ASCII.


#Crear un conjunto (set) llamado palabras_excluir para filtrar palabras para la nube de texto de la pagina.
palabras_excluir = set([
    "duki", "duko", "khea", "ysya", "biza", "bizarrap", "like", "likes",
    "alguien", "escuchando", "cada", "vez", "que", "den", "volveré",
    "comentario", "esto", "video", "youtube", "tema", "canción",
    "2025", "este", "esta", "esas", "esas", "aqui", "ahi", "hoy", "ahora",
    "jaja", "jajaja", "xd", "xddd", "jaj", "ajaja", "wooo", "song","letra","año","ysy","neo","la","el","spotify","ulises","tema","años","las","cuando","una"
])


# INICIO DEL USO DE STREAMLIT PARA CREAR PAGINA WEB

# Configuración inicial de la aplicacion en streamlit
st.set_page_config(page_title="🗺️ Guía de canciones de Duki", layout="wide") #Definir nombre de la pagina y definir completo de todo el ancho de la pantalla
st.title("🗺️ Guía de canciones de Duki") #Definir titulo general de la pagina de streamlit

url = "https://drive.google.com/uc?id=10rkx7VmJm1-WXDAXxaBUqPSiLXTN1NPS"

# 📁 Carga de datos con caché
@st.cache_data #Cargar base de datos y definir su formato
def cargar_datos(): #Cargar base de datos y definir su formato
    canciones = pd.read_csv("canciones_duki.csv", sep=";", encoding="utf-8") #Cargar base de datos y definir su formato de codificacion
    comentarios = pd.read_csv(url, encoding="utf-8") #Cargar base de datos y definir su formato de codificacion





  
#Tomando en cuenta la base de datos cancion_duki.csv configura el formato de la columna fecha_publicacion en el formato correcto YYYYMMDD
    canciones['fecha_publicacion'] = pd.to_datetime( 
        canciones['fecha_publicacion'].astype(str).str.strip(), #Convertir la columna fecha_publicacion en string y elimina espacios en blanco alrededor con .strip()
        format='%Y%m%d', #"Definir formato de las fechas en YYYYMMDD"
        errors='coerce' # Si una fila tiene un formato de fecha inválido se convierte en fecha vacia NaT y no lanza errores
    )

    return canciones, comentarios #Devoler los dataframes de las bases de datos luego de usar la funcion

canciones_df, comentarios_df = cargar_datos() #ejectura la funcion cargar_datos de la linea 40  y guarda sus datos en variables nuevas "canciones_df y comentarios_df" 


#crear pestañas en la interfaz de Streamlit usando st.tabs()
p0, p1, p2, p3, p4 = st.tabs(["🏠 Página inicial", "🔍 Busqueda de Canciones y datos", "📊 Rankings y busqueda", "📊 Datos", "🎲 Escuchar una canción del duko al azar"]) #


#COnfigurar pestaña inicial de streamlit
with p0:
    st.header("¡Hola Diablx!?")

    # Imagen a la izquierda del texto de bienvenida
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("duki1.jpg", width=300)
    with col2:
        st.markdown("¿Eres un fan de Duki y quieres conocer nuevas canciones o recién estás empezando a adentrarte dentro de su música? No te preocupes, que en DukiTube te volveremos un verdadero Rockstar. Página actualizada al 8/07/2025 02:55 a.m.")

    st.header("¿Qué es Duki?")

    # Imagen a la derecha del texto sobre la app
    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown("Insertar texto sobre de qué trata la app")
    with col4:
        st.image("duki2.jpg", width=300)

    st.header("¿Quién es Duki?")

    # Imagen a la izquierda del texto sobre Duki
    col5, col6 = st.columns([1, 3])
    with col5:
        st.image("duki3.jpg", width=500)
    with col6:
        st.markdown("""
        Mauro Ezequiel Lombardo, más conocido como Duki, es un freestyler y cantante de trap originario de Buenos Aires, Argentina.  
        Duki inició como competidor de freestyle en la competencia “El Quinto Escalón”, donde ganó popularidad por su buen flow.  
        Al ganar la Sexta fecha de la competencia antes mencionada logró grabar y lanzar su primer sencillo como músico: “No Vendo Trap”.  
        Hoy cuenta con 7 álbumes de estudio, cada uno más distinto que el anterior.  
        Sus tatuajes en el rostro, especialmente las alas de ángel y diablo, son su sello distintivo.  
        Si quieres conocer más profundamente al Duko, explora las demás pestañas de la aplicación y descubre su más sobre música. 
        Recomendación Personal: si quieres un mejor resumen sobre su historia escucha su canción BZRP Music Session #50: Duki.
        """)
    #Mostrar textos 
    st.markdown("### 🌐 Encuentra a Duki en:")
    st.markdown(
        "- [Instagram](https://www.instagram.com/duki/)\n"
        "- [Spotify](https://open.spotify.com/intl-es/artist/1bAftSH8umNcGZ0uyV7LMg)\n"
        "- [YouTube](https://www.youtube.com/@duki)"
    )

with p1:
    # 🟦 Muestra el título principal de esta sección de Streamlit
    st.header("🔍 Buscar y analizar una canción de Duki")

    # 🟦 Muestra una breve instrucción
    st.markdown("#### Escribe el nombre de una canción o selecciónala de la lista:")

    # 🟦 Campo de texto para buscar una canción. Se limpia de espacios y se convierte a minúsculas
    busqueda = st.text_input("Buscar canción", "").strip().lower()

    # Si se escribió algo en el campo de búsqueda
    if busqueda:
        # 🟦 Filtra el DataFrame buscando coincidencias en los títulos de canciones
        coincidencias = canciones_df[canciones_df['titulo_cancion'].str.lower().str.contains(busqueda)]
        
        # 🔷 Si no se encontraron coincidencias
        if coincidencias.empty:
            st.warning("No se encontraron coincidencias.")  # 🟦 Muestra advertencia
            st.stop()  # 🟦 Detiene la ejecución del resto del código

        # 🟦 Si hay coincidencias, muestra un selectbox con los títulos ordenados
        seleccion = st.selectbox("Coincidencias encontradas:", coincidencias['titulo_cancion'].sort_values())
    else:
        # 🟦 Si no se escribió nada, muestra todas las canciones disponibles
        seleccion = st.selectbox("Selecciona una canción:", canciones_df['titulo_cancion'].sort_values())

    # 🟦 Extrae la fila de la canción seleccionada
    cancion = canciones_df[canciones_df['titulo_cancion'] == seleccion].iloc[0]

    # 🟦 Divide la vista en dos columnas
    col1, col2 = st.columns([2, 3])

    with col1:
        # 🟦 Botones tipo radio para elegir qué visualizar: portada o video
        visual = st.radio("Visualizar:", ["Portada", "Video"], horizontal=True)

        # 🔷 Si elige Portada
        if visual == "Portada":
            # 🔷 Si hay URL de portada disponible
            if pd.notna(cancion['url_portada']):
                st.image(cancion['url_portada'], use_container_width=False, width=360)  # 🟦 Muestra imagen
            else:
                st.info("No hay imagen de portada disponible.")  # 🟦 Muestra info
        else:
            # 🔷 Si hay URL de video
            if pd.notna(cancion['url_video']):
                st.video(cancion['url_video'])  # 🟦 Muestra video
            else:
                st.warning("No hay video disponible.")  # 🟦 Muestra advertencia

        # 🟦 Métricas de vistas y likes
        m1, m2 = st.columns(2)
        m1.metric("👁️ Vistas", int(cancion['vistas']))
        m2.metric("❤ Likes", int(cancion['likes']))

        # 🟦 Formatea la fecha de publicación
        fecha_pub = cancion['fecha_publicacion']
        fecha_formateada = fecha_pub.strftime('%d %b %Y') if not pd.isna(fecha_pub) else 'Fecha desconocida'
        st.markdown(f"**🗓️ Fecha:** {fecha_formateada}")

        # 🔷 Si la canción es colaboración
        colab_val = str(cancion['colaboracion']).strip().lower()
        if colab_val in ['true', '1', '¡', 'si'] and pd.notna(cancion['artistas_colabo']) and cancion['artistas_colabo'].strip():
            st.markdown(f"**🌷 Colaboradores:** {cancion['artistas_colabo']}")

        # 🔷 Si pertenece a un álbum (y no es un single)
        if str(cancion['album']).strip().lower() not in ['sencillo', 'single', '']:
            st.markdown(f"**🎵 Álbum:** {cancion['album']}")

        # 🟦 Calcula el ranking de vistas y likes
        posicion_vistas = canciones_df['vistas'].rank(ascending=False, method='min')[canciones_df['titulo_cancion'] == cancion['titulo_cancion']].values[0].astype(int)
        posicion_likes = canciones_df['likes'].rank(ascending=False, method='min')[canciones_df['titulo_cancion'] == cancion['titulo_cancion']].values[0].astype(int)
        total_canciones = len(canciones_df)

        # 🟦 Muestra ranking de la canción
        st.markdown(f"""
        🔹 {cancion['titulo_cancion']} está en el **top {posicion_vistas} de {total_canciones}** en vistas y en el **top {posicion_likes} de {total_canciones}** en likes.  
        """)

        # 🟦 Muestra los comentarios con más likes
    with col1:
        with st.expander("💬 Comentarios con más likes"):
            comentarios_cancion = comentarios_df[comentarios_df['video_id'] == cancion['video_id']].copy()
            comentarios_cancion = comentarios_cancion.sort_values(by='like_count', ascending=False).head(15)

            st.markdown("""<div style="max-height: 300px; overflow-y: auto; padding-right:10px;">""", unsafe_allow_html=True)
            for _, fila in comentarios_cancion.iterrows():
                st.markdown(f"""
                    <div style='margin-bottom: 15px;'>
                    <b>👤 {fila['author_display_name']}</b>  
                    <i style='color: gray; font-size: 0.85em;'>({fila['published_at'][:10]})</i>  
            <br>
                🔺 {fila['text_display']}<br>
                👍 {fila['like_count']} likes
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # 🟦 Muestra encabezado con nombre de la canción
        st.header(f"🎵 {cancion['titulo_cancion']}")

        with st.expander("📖 Letra completa"):
            st.markdown(f"<div style='max-height: 300px; overflow-y: auto; white-space: pre-wrap;'>{cancion['lyrics']}</div>", unsafe_allow_html=True)

        # 🟦 Análisis de sentimiento con TextBlob
        with st.expander("🧪 Análisis de sentimiento de la letra (TextBlob)"):
            blob = TextBlob(str(cancion['lyrics']))
            pol = blob.sentiment.polarity
            senti = "Positivo" if pol > 0 else "Negativo"

            # 🟦 Construcción del gráfico de polaridad
            base_df = pd.DataFrame({'x': [-1, 1], 'y': [0, 0]})
            punto_df = pd.DataFrame({'x': [pol], 'y': [0], 'Etiqueta': [senti]})
            etiquetas_df = pd.DataFrame({'x': [-1, 1], 'y': [0, 0], 'Etiqueta': ['Negativo (-1)', 'Positivo (1)']})

            linea = alt.Chart(base_df).mark_line(color='white', strokeWidth=3).encode(
                x=alt.X('x:Q', scale=alt.Scale(domain=[-1, 1]), axis=None),
                y=alt.Y('y:Q', scale=alt.Scale(domain=[-1, 1]), axis=None)
            )
            punto = alt.Chart(punto_df).mark_point(size=150, color='red', filled=True).encode(
                x='x:Q', y='y:Q', tooltip=['Etiqueta', 'x'])
            texto_valor = alt.Chart(punto_df).mark_text(
                dy=-25, color='white', fontWeight='bold', fontSize=13).encode(
                x='x:Q', y='y:Q', text=alt.Text('x:Q', format='.2f'))
            etiquetas = alt.Chart(etiquetas_df).mark_text(
                dy=25, color='white', fontWeight='bold').encode(
                x='x:Q', y='y:Q', text='Etiqueta')

            chart = (linea + punto + texto_valor + etiquetas).properties(width=400, height=100)
            st.altair_chart(chart, use_container_width=False)
            st.caption("Este análisis mide la polaridad de la letra, desde -1 (muy negativo) hasta +1 (muy positivo).")

        # 🟦 Análisis de comentarios con VADER
        with st.expander("🔎 Análisis de comentarios (VADER)"):
            st.markdown("Distribución de comentarios por sentimiento:")
            analyzer = SentimentIntensityAnalyzer()
            comentarios = comentarios_df[comentarios_df['video_id'] == cancion['video_id']]['text_display'].dropna()

            # 🟦 Aplica VADER y clasifica
            resultados = comentarios.apply(lambda x: analyzer.polarity_scores(str(x)))
            categorias = resultados.apply(lambda x: 'Positivo' if x['compound'] > 0.05 else 'Negativo' if x['compound'] < -0.05 else 'Neutro')
            conteo_df = categorias.value_counts().reindex(['Positivo', 'Neutro', 'Negativo'], fill_value=0).reset_index()
            conteo_df.columns = ['Sentimiento', 'Cantidad']

            graf = alt.Chart(conteo_df).mark_bar().encode(
                x=alt.X('Sentimiento', sort=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Cantidad:Q'),
                color=alt.Color('Sentimiento:N', scale=alt.Scale(range=['#ff4c4c', '#ff9999', '#800000']))
            ).properties(width=400, height=250)

            texto = alt.Chart(conteo_df).mark_text(
                align='center', baseline='bottom', dy=-10, color='white'
            ).encode(
                x='Sentimiento:N',
                y='Cantidad:Q',
                text='Cantidad:Q'
            )

            st.altair_chart(graf + texto, use_container_width=True)

            # 🟦 Limpieza de texto y generación de nube de palabras
            letras = set(re.sub(r"[^\w\s]", "", str(cancion['lyrics']).lower()).split())
            frases_excluir = {'alguien del 2025', 'cada vez que den like volveré', 'like si escuchas esto en'}
            texto_completo = ' '.join([emoji_pattern.sub('', str(t).lower()) for t in comentarios if isinstance(t, str)])
            palabras = [p for p in texto_completo.split() if p not in STOPWORDS and p not in letras and p not in frases_excluir and len(p) > 2 and not p.startswith('http') and p.isalpha() and p not in palabras_excluir]

            nube = WordCloud(width=600, height=300, background_color='black', colormap='Reds').generate(' '.join(palabras))
            st.image(nube.to_array(), use_container_width=True)

            # 🟦 Muestra ejemplos de comentarios según sentimiento
            tipos = ['Positivo', 'Neutro', 'Negativo']
            for tipo in tipos:
                subset = comentarios[categorias == tipo]
                subset = subset[~subset.str.contains(r'[^\x00-\x7F]+', na=False)].dropna()
                ejemplos = subset.sample(n=min(10, len(subset)), random_state=random.randint(1, 10000))
                with st.expander(f"🔹 Comentarios {tipo.lower()}s"):
                    for txt in ejemplos:
                        st.markdown(f"> {txt}")

        # 🟦 Recomienda canciones similares por polaridad
        todas_con_polaridad = canciones_df.copy()
        todas_con_polaridad['polarity'] = canciones_df['lyrics'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        cancion_pol = TextBlob(str(cancion['lyrics'])).sentiment.polarity
        todas_con_polaridad['diferencia'] = (todas_con_polaridad['polarity'] - cancion_pol).abs()
        similares = todas_con_polaridad.sort_values(by='diferencia').head(6)
        with st.expander("🔎 Canciones con polaridad similar (TextBlob)"):
            st.markdown("Estas recomendaciones se basan en la similitud del sentimiento de la letra (análisis de polaridad).")
            for _, fila in similares.iterrows():
                if fila['titulo_cancion'] != cancion['titulo_cancion']:
                    st.markdown(f"- [{fila['titulo_cancion']}]({fila['url_video']}) ({fila['polarity']:.2f})")


#Tranajar con la pestaña p2 de la sección de rankings generales
with p2:
    st.header("📊 Rankings Generales")  # Mostrar encabezado principal de la pagina

    # Mostrar una imagen alineada a la izquierda y una descripción de la pestaña
    st.markdown("<div style='display: flex; align-items: center;'>" 
                "<img src='https://imagenes.elpais.com/resizer/v2/PUNXVKFLRNDMLNED23A4Q5ZWXM.jpg?auth=48b7d7a33597654e6294cc3e27fc76630ee8b3e82940d2e663a3b67dff261bc0&width=400&height=300&smart=true' width='200' style='margin-right: 20px;'>" 
                "<div><p style='font-size: 16px;'>En esta sección puedes explorar distintos rankings de canciones de Duki según vistas y colaboraciones. También puedes filtrar por álbumes, años y artistas para analizar su evolución musical.</p></div>" 
                "</div>", unsafe_allow_html=True)

    st.markdown("---")  # Línea separadora visual


###PREPROCESAMIENTO DE DATOS PARA ARTISTAS CON COLABORACIONES
    # Seleccionar solo canciones donde hay colaboradores y explota la columna en valores separados
    top_artistas_df = canciones_df[canciones_df['artistas_colabo'].notna() & (canciones_df['artistas_colabo'] != '')]['artistas_colabo']\
        .str.split(', ').explode()
    # Filtrar los valores donde el nombre sea "solista" (no tiene colaboraciones)
    top_artistas_df = top_artistas_df[top_artistas_df.str.lower() != 'solista']
    # Contar la cantidad de veces que aparece cada artista y contar los 10 con mas apariciones
    top_artistas_df = top_artistas_df.value_counts().head(10).reset_index()
    top_artistas_df.columns = ['Artista', 'Cantidad']  # Renombrar las columnas
    top_artistas_df['Artista'] = top_artistas_df['Artista'].astype(str)  # Asegurar que los resultados sean strings


    #DICCIONARIO DE OPCIONES DE RANKING Cada clave representa un tipo de ranking que se puede seleccionar en el selectbox
    opciones = {
        "Top 10 canciones más vistas": (
            canciones_df.sort_values(by="vistas", ascending=False).head(10),
            "titulo_cancion", "vistas"
        ),
        "Top 10 canciones con colaboraciones": (
            canciones_df[canciones_df['colaboracion'].isin(['true', '1', '¡', 'si'])].sort_values(by="vistas", ascending=False).head(10),
            "titulo_cancion", "vistas"
        ),
        "Top 10 canciones sin colaboraciones": (
            canciones_df[~canciones_df['colaboracion'].isin(['true', '1', '¡', 'si'])].sort_values(by="vistas", ascending=False).head(10),
            "titulo_cancion", "vistas"
        ),
        "Top 10 artistas con más colaboraciones": (
            top_artistas_df,
            "Artista", "Cantidad"
        )
    }

    # Selectbox para elegir el ranking que se desea ver
    seleccion = st.selectbox("Selecciona el ranking que deseas visualizar:", list(opciones.keys()))
    df_ranking, campo_x, campo_y = opciones[seleccion]  # Desempaqueta valores

    st.subheader(f"📈 {seleccion}")  # Mostrar Subtítulo  con el nombre del ranking

    # CREACIÓN DEL GRÁFICO DE BARRAS CON ALTAIR
    chart = alt.Chart(df_ranking).mark_bar().encode(
        x=alt.X(f'{campo_x}:N', sort='-y', axis=alt.Axis(labelAngle=0, labelLimit=200, title=campo_x)),  # Eje X ordenado de mayor a menor
        y=alt.Y(f'{campo_y}:Q', title=campo_y),  # Eje Y
        tooltip=[campo_x, campo_y],  # Datos mostrados al pasar el mouse
        color=alt.Color(f'{campo_x}:N', scale=alt.Scale(scheme='reds'), legend=None)  # Diferentes tonos de rojo por categoría
    ).properties(width=700, height=350)

    # AÑADIR LOS DATOS DE CADA DATO SOBRE LAS BARRAS
    texto = alt.Chart(df_ranking).mark_text(
        align='center', baseline='bottom', dy=-5, color='white'
    ).encode(
        x=f'{campo_x}:N',
        y=f'{campo_y}:Q',
        text=alt.Text(f'{campo_y}:Q', format=',')
    )

    # Mostrar el gráfico con sus valores encima
    st.altair_chart(chart + texto, use_container_width=True)

    
with p3:
    # Mostrar titulo y descripcion de la pestaña 
    st.header("🎷 Filtro por álbum, colaborador y año")
    st.markdown("fdsdsfddfsfd")

    # Extraeer y ordenar datos para poder filtrar la tabla
    artistas = canciones_df[canciones_df['artistas_colabo'].notna() & (canciones_df['artistas_colabo'] != '')]['artistas_colabo'].str.split(', ').explode()

    # Configurar selectbox para filtrar por álbum
    filtro_album = st.selectbox("Selecciona un álbum:", ['Todos'] + sorted(canciones_df['album'].dropna().unique().tolist()))
    # Configurar selectbox para filtrar por artista
    filtro_artista = st.selectbox("Selecciona un colaborador:", ['Todos'] + sorted(artistas.dropna().unique().tolist()))
    # Configurar selectbox para filtrar por año
    filtro_anio = st.selectbox("Selecciona un año de publicación:", ['Todos'] + sorted(canciones_df['fecha_publicacion'].dropna().dt.year.unique().astype(int).tolist()))

    # Aplicar filtros en la tabla de la base de datos
    filtrado = canciones_df.copy()
    if filtro_album != 'Todos':
        filtrado = filtrado[filtrado['album'] == filtro_album]
    if filtro_artista != 'Todos':
        filtrado = filtrado[filtrado['artistas_colabo'].str.contains(filtro_artista, na=False)]
    if filtro_anio != 'Todos':
        filtrado = filtrado[filtrado['fecha_publicacion'].dt.year == int(filtro_anio)]

    # Mostrar resultdos de la base de datos
    st.markdown("### 📄 Resultados filtrados")
    st.dataframe(filtrado[['titulo_cancion', 'album', 'artistas_colabo', 'fecha_publicacion', 'vistas']].reset_index(drop=True))


# Inicia el contenido dentro de la pestaña 5 (p5) correspondiente a la sección de "Canción aleatoria"
with p4:
    # Muestra el encabezado de la sección
    st.header("🎲 Canción aleatoria")

    # Verifica si no existe aún una variable 'random_index' en la sesión, si no existe, la crea y le asigna None
    if 'random_index' not in st.session_state:
        st.session_state.random_index = None

    # Si se presiona el botón o si aún no se ha generado una canción aleatoria antes
    if st.button("🎧 Generar una canción aleatoria") or st.session_state.random_index is None:
        # Selecciona un índice aleatorio de una canción del DataFrame y lo guarda en la sesión
        st.session_state.random_index = canciones_df.sample(1).index[0]

    # Extrae la canción correspondiente al índice aleatorio seleccionado
    cancion_random = canciones_df.loc[st.session_state.random_index]

    # Crea dos columnas con proporción 1.3 y 1.2 para mostrar el video y los detalles de la canción
    col1, col2 = st.columns([1.3, 1.2])

    # En la primera columna (col1), se muestra el video de YouTube de la canción
    with col1:
        st.video(cancion_random['url_video'], format="video/mp4")

    # En la segunda columna (col2), se presentan los datos de la canción
    with col2:
        # Muestra el título de la canción como subtítulo con emoji
        st.markdown(f"""
        ### 🎵 {cancion_random['titulo_cancion']}
        """)

        # Muestra detalles de la canción: fecha de publicación, álbum, colaboración, vistas, likes y comentarios
        st.markdown(f"""
        **📅 Fecha de publicación:** {cancion_random['fecha_publicacion'].strftime('%d/%m/%Y')}  
        **💽 Álbum:** {cancion_random['album']}  
        **🤝 Colaboración:** {cancion_random['artistas_colabo'] if pd.notna(cancion_random['artistas_colabo']) and cancion_random['artistas_colabo'].strip() else 'No'}  
        **📈 Vistas:** {cancion_random['vistas']:,}  
        **👍 Likes:** {cancion_random['likes']:,}  
        **💬 Comentarios:** {cancion_random['nro_comentarios']:,}  
        """)

        # Título de la sección de la letra
        st.markdown("📖 Letra completa")

        # Muestra la letra de la canción en un contenedor con scroll, fondo oscuro y texto blanco
        st.markdown(
            f"""
            <div style='max-height: 200px; overflow-y: auto; white-space: pre-wrap; padding: 10px; background-color: #1e1e1e; color: #f1f1f1; border-radius: 5px;'>
                {cancion_random['lyrics']}
            </div>
            """,
            unsafe_allow_html=True
        )
