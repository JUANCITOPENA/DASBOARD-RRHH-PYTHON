import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
import numpy as np  # Asegurarse de importar numpy
import folium
from streamlit_folium import st_folium
import datetime
import math


# Configurar el layout para que sea de ancho completo
st.set_page_config(layout="wide")

# Cargar datos desde Excel
df = pd.read_excel("BASE_DE_DATOS_EMPLEADOS_ANALISIS_RRHH_DASHBOARD.xlsx")

# Limpiar nombres de columnas para evitar errores
df.columns = df.columns.str.strip()

# Calcular indicadores clave
total_empleados = df.shape[0]
empleados_activos = df[df["Status"] == "Activo"].shape[0]
empleados_inactivos = df[df["Status"] != "Activo"].shape[0]
departamentos = df["Departamento"].nunique()
nomina_mensual = df["Sueldo"].sum()

# Calcular total de renuncias y despedidos
total_renuncias = df[df["Status"] == "Renuncia"].shape[0]
total_despedidos = df[df["Status"] == "Despedido"].shape[0]

# Calcular porcentajes
porcentaje_renuncias = (total_renuncias / total_empleados) * 100
porcentaje_despedidos = (total_despedidos / total_empleados) * 100
porcentaje_activos = (empleados_activos / total_empleados) * 100
porcentaje_inactivos = (empleados_inactivos / total_empleados) * 100

# Estilos para las tarjetas y centrado
st.markdown(
    """
<style>
.center-text {
    text-align: center;
}

    .card_kpi {
        padding: 20px;
        border: 1px sólido #ddd;
        border-radius: 10px;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
        background-color: #f9f9f9;
        text-align: center;  /* Centrar el texto horizontalmente */
        width: 160px;  /* Ancho fijo */
        height: 130px;  /* Alto fijo */
        display: flex;  /* Uso de flex para centrar el contenido */
        flex-direction: column;  /* Alineación vertical del contenido */
        align-items: center;  /* Centrar horizontalmente dentro del contenedor */
        justify-content: center;  /* Centrar verticalmente dentro del contenedor */
        margin: 5px;  /* Espacio entre tarjetas */
        overflow: hidden;  /* Asegurar que el contenido no se desborde */
        font-size: 14px;
    }
    .card_kpi p {
        margin: 0;  /* Eliminar márgenes para un mejor ajuste */
    }
    .card_kpi strong {
        font-weight: bold;  /* Negrita para texto destacado */
    }

    @media (max-width: 768px) {
        .card_kpi {
            width: 98%;  # Ancho para dispositivos móviles
            height: auto;  # Permitir que el alto sea dinámico
            flex-direction: row;  # Cambiar la dirección del contenido
            justify-content: flex-start;  # Alinear a la izquierda
            font-size: 20px;
        }

        .card_kpi + .card_kpi {
            margin-top: 10px;  # Espacio entre tarjetas cuando se apilan
             font-size: 20px;
        }
    }
</style>



    """,
    unsafe_allow_html=True
)

# Título y subtítulo centrados
st.markdown('<h1 class="center-text">🧑‍💼 ¡Bienvenidos al informe de Recursos Humanos! 👥</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="center-text">Creado por Juancito Peña</h3>', unsafe_allow_html=True)


# Título para la tabla con emoji, centrado
st.markdown("<h2 style='text-align: center;'>📊 Indicadores </h2>", unsafe_allow_html=True)


# Crear nueve columnas para las tarjetas
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)  # Nueve columnas para tarjetas



# Tarjeta para Total Gral. de Empleados
with col1:
    st.markdown(
        f"<div class='card_kpi'>👥 Total Emp.<br><strong>{total_empleados}</strong></div>",
        unsafe_allow_html=True
    )
# Tarjeta para Empleados Activos (Número Total)
with col2:
    st.markdown(
        f"<div class='card_kpi'>✅ Activos<br><strong>{empleados_activos}</strong></div>",
        unsafe_allow_html=True
    )

# Tarjeta para Empleados Inactivos (Número Total)
with col3:
    st.markdown(
        f"<div class='card_kpi'>❌ Inactivos<br><strong>{empleados_inactivos}</strong></div>",
        unsafe_allow_html=True
    )


# Tarjeta para Empleados Activos
with col4:
    st.markdown(
        f"<div class='card_kpi'>💼 % Activos<br><strong>{porcentaje_activos:.2f}%</strong></div>",
        unsafe_allow_html=True
    )

# Tarjeta para Empleados Inactivos
with col5:
    st.markdown(
        f"<div class='card_kpi'>⛔ % Inactivos<br><strong>{porcentaje_inactivos:.2f}%</strong></div>",
        unsafe_allow_html=True
    )

# Tarjeta para Departamentos
with col6:
    st.markdown(
        f"<div class='card_kpi'>🏢 Departamentos<br><strong>{departamentos}</strong></div>",
        unsafe_allow_html=True
    )

# Tarjeta para Nómina Mensual
with col7:
    st.markdown(
        f"<div class='card_kpi'>💰 Nómina<br><strong>${nomina_mensual:,.2f}</strong></div>",
        unsafe_allow_html=True
    )

# Tarjeta para Porcentaje de Empleados que Renunciaron
with col8:
    st.markdown(
        f"<div class='card_kpi'>⚠️ % Renuncias<br><strong>{porcentaje_renuncias:.2f}%</strong></div>",
        unsafe_allow_html=True
    )

# Tarjeta para Porcentaje de Empleados Despedidos
with col9:
    st.markdown(
        f"<div class='card_kpi'>❌ % Despedidos<br><strong>{porcentaje_despedidos:.2f}%</strong></div>",
        unsafe_allow_html=True
    )

 # Espacio adicional para separar
st.write("")  # Espacio para mejorar visualización
    



# Título para la tabla con emoji, centrado
st.markdown("<h2 style='text-align: center;'>📊 Narrativa de los Indicadores </h2>", unsafe_allow_html=True)



# Estilo CSS para centrado y ajuste del tamaño de fuente
st.markdown(
    """
    <style>
    .narrativa {
        text-align: center;  # Centramos el texto
        font-size: 50px;  # Ajustamos el tamaño de la fuente a 20px
        line-height: 1.5;  # Ajustamos el espaciado entre líneas para mayor legibilidad
        padding: 10px;  # Espacio para evitar que el texto quede pegado a los bordes
        font-weight: bold;  # Asegura que la negrita se mantenga
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Calcular indicadores clave
total_empleados = df.shape[0]
empleados_activos = df[df["Status"] == "Activo"].shape[0]
empleados_inactivos = df[df["Status"] != "Activo"].shape[0]
departamentos = df["Departamento"].nunique()
nomina_total = df["Sueldo"].sum()

# Calcular total de renuncias y despedidos
total_renuncias = df[df["Status"] == "Renuncia"].shape[0]
total_despedidos = df[df["Status"] == "Despedido"].shape[0]

# Calcular porcentajes
porcentaje_activos = (empleados_activos / total_empleados) * 100
porcentaje_inactivos = (empleados_inactivos / total_empleados) * 100
porcentaje_renuncias = (total_renuncias / total_empleados) * 100
porcentaje_despedidos = (total_despedidos / total_empleados) * 100

# Crear narrativa explicativa con el formato centrado y tamaño de fuente ajustado
narrativa = f"""
<div class='narrativa'>
En nuestra empresa, contamos con un total de **{total_empleados} empleados acumulados**. De estos, **{empleados_activos} están activos** ✅, representando un **{porcentaje_activos:.2f}%** del total. Por otro lado, **{empleados_inactivos} están inactivos** ❌, representando un **{porcentaje_inactivos:.2f}%**.

La nómina total de la empresa asciende a **${nomina_total:,.2f}** 💰. En cuanto a salidas, **{total_renuncias} empleados renunciaron** ⚠️, representando un **{porcentaje_renuncias:.2f}%**, y **{total_despedidos} empleados fueron despedidos** ❌, lo cual equivale a un **{porcentaje_despedidos:.2f}%**.

En términos de departamentos, contamos con **{departamentos} departamentos** 🏢, con una distribución de **49.7% empleados masculinos** y **50.3% empleados femeninos** 👨‍💼👩‍💼.

Actualmente, hay **{df["Posición"].nunique()} posiciones únicas** en la empresa, proporcionando una amplia variedad de roles y responsabilidades.
</div>
"""

# Mostrar la narrativa en Streamlit con estilo aplicado
st.markdown(narrativa, unsafe_allow_html=True)








# Línea horizontal para dividir secciones
st.markdown("<hr>", unsafe_allow_html=True)


 # Espacio adicional para separar
st.write("")  # Espacio para mejorar visualización
    

    
    
# Título para la sección de gráficos, con emoji y centrado
st.markdown("<h2 style='text-align: center;'>📊 Gráficos de Empleados por Año y Mes</h2>", unsafe_allow_html=True)


# Supongamos que tienes un DataFrame 'df' con las siguientes columnas:
# - "Fecha_Ingreso": la fecha de ingreso de cada empleado.
# - "Nombre_Empleado": el nombre del empleado.
# - "Departamento": el departamento del empleado.
# - "Salario": el salario del empleado.



# Asegúrate de que la columna de fecha está en formato datetime
df['Fecha_Ingreso'] = pd.to_datetime(df['Fecha_Ingreso'])

# Calcular empleados acumulados por año
df['Año_Ingreso'] = df['Fecha_Ingreso'].dt.year
empleados_acumulados_por_ano = df.groupby('Año_Ingreso').size().cumsum().reset_index(name='Total_Empleados')

# Calcular empleados por mes independientemente del año
df['Mes'] = df['Fecha_Ingreso'].dt.strftime('%m')  # Extrae solo el mes
empleados_por_mes = df.groupby('Mes').size().reset_index(name='Total_Empleados')

# Crear dos columnas para mostrar los gráficos en la misma sección
col1, col2 = st.columns(2)

# Gráfico de área para empleados acumulados por año
with col1:
    st.plotly_chart(
        px.area(
            empleados_acumulados_por_ano,
            x='Año_Ingreso',
            y='Total_Empleados',
            title='Empleados Acumulados por Año 📈',
            color_discrete_sequence=['#28a745'],  # Color verde distintivo
            line_shape='spline',  # Línea suave
            hover_data={'Total_Empleados': ':.0f'}  # Tooltip con valor exacto
        ).update_layout(
            xaxis_title='Año',
            yaxis_title='Empleados Acumulados'
        ),
        use_container_width=True
    )

# Gráfico de barras para empleados por mes
with col2:
    st.plotly_chart(
        px.bar(
            empleados_por_mes,
            x='Mes',
            y='Total_Empleados',
            title='Empleados por Mes 📊',
            color_discrete_sequence=['#17a2b8'],  # Color azul distintivo
            text_auto=True,  # Mostrar valores en las barras
            hover_data={'Total_Empleados': ':.0f'}  # Tooltip con valor exacto
        ).update_traces(
            textposition='outside'  # Texto fuera de las barras para claridad
        ).update_layout(
            xaxis_title='Mes',
            yaxis_title='Total de Empleados'
        ),
        use_container_width=True
    )

# Asegurarse de que la columna 'Fecha_Salida' esté en formato datetime
df['Fecha_Salida'] = pd.to_datetime(df['Fecha_Salida'])

# Filtrar por renuncias y despidos
renuncias_df = df[df['Status'] == 'Renuncia']
despidos_df = df[df['Status'] == 'Despedido']

# Calcular renuncias por año
renuncias_df['Año_Salida'] = renuncias_df['Fecha_Salida'].dt.year
renuncias_por_ano = renuncias_df.groupby('Año_Salida').size().reset_index(name='Total_Renuncias')

# Calcular despidos por año
despidos_df['Año_Salida'] = despidos_df['Fecha_Salida'].dt.year
despidos_por_ano = despidos_df.groupby('Año_Salida').size().reset_index(name='Total_Despidos')

# Crear dos columnas para mostrar dos gráficos
col1, col2 = st.columns(2)

# Gráfico de barras para renuncias por año
with col1:
    st.plotly_chart(
        px.bar(
            renuncias_por_ano,
            x='Año_Salida',
            y='Total_Renuncias',
            title='Renuncias por Año 🚪',
            labels={'Año_Salida': 'Año', 'Total_Renuncias': 'Total de Renuncias'},
            color_discrete_sequence=['#FF5733'],  # Color distintivo
            text_auto=True,
            hover_data={'Total_Renuncias': ':.0f'}
        ).update_traces(
            textposition='outside'  # Texto fuera de las barras
        ),
        use_container_width=True
    )

# Gráfico de barras para despidos por año
with col2:
    st.plotly_chart(
        px.bar(
            despidos_por_ano,
            x='Año_Salida',
            y='Total_Despidos',
            title='Despidos por Año 🔥',
            labels={'Año_Salida': 'Año', 'Total_Despidos': 'Total de Despidos'},
            color_discrete_sequence=['#C70039'],
            text_auto=True,
            hover_data={'Total_Despidos': ':.0f'}
        ).update_traces(
            textposition='outside'
        ),
        use_container_width=True
    )

# Asegúrate de que la columna 'Fecha_Salida' esté en formato datetime
df['Fecha_Salida'] = pd.to_datetime(df['Fecha_Salida'])

# Filtrar por renuncias y despidos
renuncias_df = df[df['Status'] == 'Renuncia']
despidos_df = df[df['Status'] == 'Despedido']

# Calcular renuncias por mes (sin importar el año)
renuncias_df['Mes_Salida'] = renuncias_df['Fecha_Salida'].dt.strftime('%m')
renuncias_por_mes = renuncias_df.groupby('Mes_Salida').size().reset_index(name='Total_Renuncias')

# Calcular despidos por mes (sin importar el año)
despidos_df['Mes_Salida'] = despidos_df['Fecha_Salida'].dt.strftime('%m')
despidos_por_mes = despidos_df.groupby('Mes_Salida').size().reset_index(name='Total_Despidos')

# Crear dos columnas para gráficos
col1, col2 = st.columns(2)

# Gráfico de barras para renuncias por mes
with col1:
    st.plotly_chart(
        px.bar(
            renuncias_por_mes,
            x='Mes_Salida',
            y='Total_Renuncias',
            title='Renuncias por Mes 📅',
            color_discrete_sequence=['#FF5733'],  # Color distintivo para renuncias
            text_auto=True,  # Mostrar valores sobre las barras
            hover_data={'Total_Renuncias': ':.0f'}  # Datos adicionales en tooltip
        ).update_traces(
            textposition='outside'  # Ubicar texto fuera de las barras para mayor claridad
        ).update_layout(
            xaxis_title='Mes',
            yaxis_title='Total de Renuncias'
        ),
        use_container_width=True
    )

# Gráfico de barras para despidos por mes
with col2:
    st.plotly_chart(
        px.bar(
            despidos_por_mes,
            x='Mes_Salida',
            y='Total_Despidos',
            title='Despidos por Mes 🔥',
            color_discrete_sequence=['#C70039'],  # Color distintivo para despidos
            text_auto=True,
            hover_data={'Total_Despidos': ':.0f'}  # Datos adicionales en tooltip
        ).update_traces(
            textposition='outside'
        ).update_layout(
            xaxis_title='Mes',
            yaxis_title='Total de Despidos'
        ),
        use_container_width=True
    )




# Cargar datos desde Excel
df = pd.read_excel("BASE_DE_DATOS_EMPLEADOS_ANALISIS_RRHH_DASHBOARD.xlsx")

# Definir estilo CSS para las tarjetas
style_card = """
    <style>
    .custom-card {
        border: 1px solid black;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(50, 205, 50, 0.2);  # Sombra verde limón
        background-color: white;
        padding: 10px;
        text-align: center;
    }
    
    .custom-card h1 {
        font-weight: bold;
        color: red;  # Color rojo para valores numéricos
    }
    
    .custom-card p {
        font-weight: bold;
    }
    </style>
"""


# Aplicar el estilo CSS personalizado
st.markdown(style_card, unsafe_allow_html=True)

# Sección para las tarjetas
st.subheader("📊Resumen de Registros")

# Filtrar por "Renuncia" y "Despedido"
renuncia_df = df[df["Status"] == "Renuncia"]
despido_df = df[df["Status"] == "Despedido"]

# Crear tarjetas para conteos
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="custom-card">
            <p>Número de Registros de Renuncia</p>
            <h1>{len(renuncia_df)}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="custom-card">
            <p>Número de Registros de Despido</p>
            <h1>{len(despido_df)}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Sección para los gráficos
st.subheader("📊Gráficos de Motivos de Renuncia y Despido")

# Segmentador para empleados de renuncia y despido
empleados_renuncia = renuncia_df["Nombre Empleado"].unique()
empleados_despido = despido_df["Nombre Empleado"].unique()

# Agregar segmentador para empleados de renuncia
empleados_seleccionados_renuncia = st.multiselect(
    "Seleccione empleados para el gráfico de renuncia:",
    empleados_renuncia,
)

# Agregar segmentador para empleados de despido
empleados_seleccionados_despido = st.multiselect(
    "Seleccione empleados para el gráfico de despido:",
    empleados_despido,
)





# Filtrar por empleados seleccionados antes de crear gráficos
if empleados_seleccionados_renuncia:
    renuncia_df = renuncia_df[renuncia_df["Nombre Empleado"].isin(empleados_seleccionados_renuncia)]

if empleados_seleccionados_despido:
    despido_df = despido_df[despido_df["Nombre Empleado"].isin(empleados_seleccionados_despido)]

# Gráfico de barras horizontales para motivos de renuncia
if not renuncia_df.empty:
    # Agrupar y pintar barras con diferentes colores
    renuncia_motivos = renuncia_df.groupby("Motivos Renuncia/Despiedos").size().reset_index(name="Empleados")

    renuncia_bar = px.bar(
        renuncia_motivos,
        x="Empleados",  # El número de empleados en el eje X
        y="Motivos Renuncia/Despiedos",  # El motivo en el eje Y
        orientation='h',
        color="Motivos Renuncia/Despiedos",  # Diferentes colores para cada motivo
        title="🤝 Motivos de Renuncia"
    )
    renuncia_bar.update_layout(
        yaxis_title="Motivos de Renuncia",
        xaxis_title="Número de Empleados",
        height=400
    )

    st.plotly_chart(renuncia_bar, use_container_width=True)

# Gráfico de barras horizontales para motivos de despido
if not despido_df.empty:
    # Agrupar y pintar barras con diferentes colores
    despido_motivos = despido_df.groupby("Motivos Renuncia/Despiedos").size().reset_index(name="Empleados")

    despido_bar = px.bar(
        despido_motivos,
        x="Empleados",  # El número de empleados en el eje X
        y="Motivos Renuncia/Despiedos",  # El motivo en el eje Y
        orientation='h',
        color="Motivos Renuncia/Despiedos",  # Diferentes colores para cada motivo
        title="❌ Motivos de Despido"
    )
    despido_bar.update_layout(
        yaxis_title="Motivos de Despido",
        xaxis_title="Número de Empleados",
        height=400
    )

    st.plotly_chart(despido_bar, use_container_width=True)



# Título para las tablas, centrado y con emojis
st.markdown("<h2 style='text-align: center;'>🚪 Empleados que Renunciaron y 🔥 Fueron Despedidos 📊</h2>", unsafe_allow_html=True)

# Filtrar por empleados que renunciaron y empleados que fueron despedidos
renuncias_df = df[df["Status"] == "Renuncia"]
despidos_df = df[df["Status"] == "Despedido"]

# Ordenar por "Código" (anteriormente "ID Empleado") de menor a mayor
renuncias_df = renuncias_df.sort_values(by="ID Empleado", ascending=True)
despidos_df = despidos_df.sort_values(by="ID Empleado", ascending=True)

# Definir estilo CSS para tablas con cuadrículas, bordes y sombras
st.markdown(
    """
    <style>
    .styled-table {
        border-collapse: collapse;  /* Asegura que las celdas estén bien definidas */
        margin: 25px 0;  /* Margen para separarlo de otros elementos */
        font-size: 14px;  /* Tamaño de fuente más pequeño */
        text-align: left;  /* Alineación del texto */
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);  /* Sombra para dar profundidad */
    }
    .styled-table thead tr {
        background-color: darkblue;  /* Fondo para el encabezado */
        color: white;  /* Color del texto en el encabezado */
        text-transform: uppercase;  /* Texto en mayúsculas */
        font-size: 16px;  /* Tamaño de fuente más grande para encabezados */
    }
    .styled-table th, .styled-table td {
        padding: 8px 12px;  /* Espaciado interno */
        border-radius: 10px;  /* Bordes redondeados */
        border: 1px solid #ddd;  /* Bordes visibles */
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;  /* Separadores horizontales */
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;  /* Color de fondo para filas pares */
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid darkblue;  /* Borde más grueso al final */
    }
    .styled-table tbody tr:hover {
        background-color: #f1f1f1;  /* Color de fondo al pasar el cursor */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Crear dos columnas para tablas en la misma sección
col1, col2 = st.columns(2)

# Tabla para empleados que renunciaron
with col1:
    st.write(
        renuncias_df[["ID Empleado", "Nombre Empleado", "Motivos Renuncia/Despiedos"]]
            .rename(columns={"ID Empleado": "Código"})  # Cambiar nombre de la columna
            .to_html(index=False, classes="styled-table"),  # Aplicar estilo
        unsafe_allow_html=True
    )

# Tabla para empleados que fueron despedidos
with col2:
    st.write(
        despidos_df[["ID Empleado", "Nombre Empleado", "Motivos Renuncia/Despiedos"]]
            .rename(columns={"ID Empleado": "Código"})  # Cambiar nombre de la columna
            .to_html(index=False, classes="styled-table"),  # Aplicar estilo
        unsafe_allow_html=True
    )
    
# FIN DE LA TABLA CON LOS DATOS DE RENUNCIA Y DESPIDOS:




# Asegurarse de que las columnas para filtrar existen en el DataFrame
required_columns = ["ID Empleado", "Nombre Empleado", "Departamento", "Posición"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Las siguientes columnas no están presentes en el DataFrame: {missing_columns}")

# Crear un contenedor para la caja de búsqueda
with st.container():
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    search_term = st.text_input("Buscar por código, nombre, departamento o posición:", key="search_term")
    search_button = st.button("🔍 Buscar", key="search_button")
    st.markdown("</div>", unsafe_allow_html=True)

# Filtrar el DataFrame según el término de búsqueda
filtered_df = df  # Mostrar todo por defecto

# Si el término de búsqueda tiene contenido, aplica el filtro
if search_term:
    filtered_df = df[
        df.apply(
            lambda row: any(
                search_term.lower() in str(row[col]).lower() for col in required_columns
            ),
            axis=1,
        )
    ]

# Si se presiona el botón y no hay término de búsqueda, limpiar
if search_button and not search_term:
    filtered_df = df  # Restablecer la tabla completa

# Mostrar la tabla paginada centrada
st.dataframe(filtered_df.style.set_properties(**{'text-align': 'center'}))






     
 # Espacio adicional para separar
st.write("")  # Espacio para mejorar visualización
    
     
# SECCION ":  
  

# Mapa de colores para géneros
color_map = {
    "Femenino": "#FDA7DF",  # Rosa para Femenino
    "Masculino": "#0652DD"  # Azul para Masculino
}

# Crear dos columnas para gráficos
col1, col2 = st.columns(2)

# Gráfico de barras para "Sueldo por Departamento"
with col1:
    st.plotly_chart(
        px.bar(
            df,
            x="Departamento",
            y="Sueldo",
            color="Género",
            title="Sueldo por Departamento",
            color_discrete_map=color_map  # Aplicar el mapa de colores
        ),
        use_container_width=True
    )

# Gráfico circular para "Distribución por Género"
with col2:
        # Gráfico circular para "Distribución por Género"
    st.plotly_chart(
        px.pie(
            df,
            names='Género',  # Columna para definir segmentos
            title='Distribución por Género',
            color='Género',  # Usar la columna correcta para el color
            color_discrete_map=color_map,  # Aplicar el mapa de colores
            hole=0.4  # Estilo rosquilla para un look más moderno
        ).update_traces(
            textinfo='label+percent+value',  # Mostrar nombre, porcentaje y valor
            textfont=dict(size=14),  # Tamaño de fuente para mayor legibilidad
            hoverinfo='label+percent+value',  # Información en tooltip
            insidetextorientation='radial'  # Orientación del texto dentro del gráfico
        ).update_layout(
            uniformtext_minsize=14,  # Tamaño mínimo del texto
            uniformtext_mode='hide'  # Esconder texto si no cabe para evitar solapamientos
        ),
        use_container_width=True
    )

# Espacio adicional para separar
st.write("")  # Espacio para mejorar visualización
    



# Filtrar por renuncias y despidos
renuncias_df = df[df['Status'] == 'Renuncia']
despidos_df = df[df['Status'] == 'Despedido']

# Mapa de colores para diferenciarlos
color_map = {
    'Femenino': '#FDA7DF',  # Rosa para Femenino
    'Masculino': '#0652DD'  # Azul para Masculino
}

# Crear dos columnas para gráficos
col1, col2 = st.columns(2)

# Gráfico circular para "Distribución por Género" en Renuncias
with col1:
    st.plotly_chart(
        px.pie(
            renuncias_df,
            names='Género',  # Columna para definir segmentos
            title='Distribución por Género en Renuncias 🚪',
            color='Género',  # Usar la columna correcta para el color
            color_discrete_map=color_map,  # Aplicar el mapa de colores
            hole=0.4  # Estilo rosquilla para un look más moderno
        ).update_traces(
            textinfo='label+percent+value',  # Mostrar etiqueta, porcentaje y valor
            textfont=dict(size=14),  # Tamaño de fuente para mayor legibilidad
            hoverinfo='label+percent+value'  # Información en tooltip
        ),
        use_container_width=True
    )

# Gráfico circular para "Distribución por Género" en Despidos
with col2:
    st.plotly_chart(
        px.pie(
            despidos_df,
            names='Género',  # Columna para definir segmentos
            title='Distribución por Género en Despidos 🔥',
            color='Género',  # Usar la columna correcta para el color
            color_discrete_map=color_map,  # Aplicar el mapa de colores
            hole=0.4  # Estilo rosquilla para un look más moderno
        ).update_traces(
            textinfo='label+percent+value',  # Mostrar etiqueta, porcentaje y valor
            textfont=dict(size=14),  # Tamaño de fuente para mayor legibilidad
            hoverinfo='label+percent+value'  # Información en tooltip
        ),
        use_container_width=True
    )



# Datos para empleados despedidos y que renunciaron
despedidos_df = df[df["Status"] == "Despedido"]
renuncia_df = df[df["Status"] == "Renuncia"]

# Conteo de empleados despedidos por departamento
despedidos_por_departamento = despedidos_df["Departamento"].value_counts()

# Conteo de empleados que renunciaron por departamento
renuncia_por_departamento = renuncia_df["Departamento"].value_counts()

# Gráfico de barras para empleados despedidos por departamento, con etiquetas de valor y conteo
despedidos_bar = px.bar(
    despedidos_df,
    x="Departamento",
    y="Nombre Empleado",
    title="Empleados Despedidos por Departamento",
    color="Departamento",
    text_auto=True,  # Mostrar el nombre del empleado como etiqueta
    labels={"Nombre Empleado": "Empleado"}  # Etiqueta para el eje
)

# Agregar el conteo por departamento debajo de la etiqueta del eje x
despedidos_bar.update_layout(
    xaxis_title=f"Departamento (Conteo: {despedidos_por_departamento.to_dict()})"
)

st.plotly_chart(despedidos_bar, use_container_width=True)

# Gráfico de barras para empleados que renunciaron por departamento, con etiquetas de valor y conteo
renuncia_bar = px.bar(
    renuncia_df,
    x="Departamento",
    y="Nombre Empleado",
    title="Empleados que Renunciaron por Departamento",
    color="Departamento",
    text_auto=True,  # Mostrar el nombre del empleado como etiqueta
    labels={"Nombre Empleado": "Empleado"}  # Etiqueta para el eje
)

# Agregar el conteo por departamento debajo de la etiqueta del eje x
renuncia_bar.update_layout(
    xaxis_title=f"Departamento (Conteo: {renuncia_por_departamento.to_dict()})"
)

st.plotly_chart(renuncia_bar, use_container_width=True)

# Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad



# Función para determinar la generación según el año de nacimiento
def determinar_generacion(year):
    if year >= 1946 and year <= 1964:
        return "Baby Boomers (1946-1964)"
    elif year >= 1965 and year <= 1980:
        return "Generación X (1965-1980)"
    elif year >= 1981 and year <= 1996:
        return "Milénial (Generación Y) (1981-1996)"
    elif year >= 1997 and year <= 2012:
        return "Generación Z (1997-2012)"
    elif year >= 2013:
        return "Generación Alpha (2013-?)"
    else:
        return "Desconocido"

# Crear una nueva columna que tenga la generación con el rango de años
df["Generación con Rango"] = df["Nacimiento"].apply(lambda x: determinar_generacion(x.year))

# Contar la cantidad de empleados por generación con rango
generacion_rango_counts = df["Generación con Rango"].value_counts().reset_index()
generacion_rango_counts.columns = ["Generación", "Cantidad"]

# Crear dos columnas para gráficos
col1, col2 = st.columns(2)

# Gráfico de barras para "Cantidad de Empleados por Generación con Rango"
with col1:
    st.plotly_chart(
        px.bar(
            generacion_rango_counts,
            x="Generación",
            y="Cantidad",
            title="Cantidad de Empleados por Generación (con Rango)",
            labels={"Generación": "Generación", "Cantidad": "Número de Empleados"},
            text_auto=True  # Mostrar etiquetas automáticas con valores
        ),
        use_container_width=True
    )

# Gráfico de barras para "Distribución por Género en Cada Generación"
with col2:
    st.plotly_chart(
        px.histogram(
            df,
            x="Generación con Rango",
            color="Género",
            title="Distribución por Género en Cada Generación (con Rango)",
            labels={"Generación": "Generación", "Género": "Género"},
            color_discrete_map={
                "Femenino": "pink",  # Rosa para Femenino
                "Masculino": "blue"  # Azul para Masculino
            },
            text_auto=True  # Mostrar etiquetas automáticas con valores
        ),
        use_container_width=True
    )
    
    
    
 # Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad
   
    
# Crear dos columnas para los gráficos de pastel
col1, col2 = st.columns(2)

# Gráfico de pastel para empleados por región
with col1:
    pie_chart_region = px.pie(
        df,
        names="Región",
        title="Distribución de Empleados por Región",
        hole=0.4,  # Estilo de rosquilla
        color_discrete_sequence=px.colors.qualitative.Pastel  # Colores pasteles
    )
    
    # Configurar las etiquetas para mostrar valor y porcentaje
    pie_chart_region.update_traces(
        textinfo="label+value+percent",  # Mostrar etiqueta, valor y porcentaje
        textfont_size=12  # Tamaño del texto
    )
    
    # Mostrar el gráfico
    st.plotly_chart(pie_chart_region, use_container_width=True)

# Gráfico de pastel para empleados por estatus
with col2:
    pie_chart_status = px.pie(
        df,
        names="Status",
        title="Distribución de Empleados por Estatus",
        hole=0.4,  # Estilo de rosquilla
        color_discrete_sequence=px.colors.qualitative.Pastel  # Colores pasteles
    )
    
    # Configurar las etiquetas para mostrar valor y porcentaje
    pie_chart_status.update_traces(
        textinfo="label+value+percent",  # Mostrar etiqueta, valor y porcentaje
        textfont_size=12  # Tamaño del texto
    )
    
    # Mostrar el gráfico
    st.plotly_chart(pie_chart_status, use_container_width=True)
  
  # Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad

 
# Encontrar el empleado con la evaluación más alta y más baja
max_evaluacion_index = df["Evaluación"].idxmax()  # Índice de la evaluación más alta
min_evaluacion_index = df["Evaluación"].idxmin()  # Índice de la evaluación más baja

max_evaluacion_employee = df.loc[max_evaluacion_index, "Nombre Empleado"]  # Empleado con la evaluación más alta
min_evaluacion_employee = df.loc[min_evaluacion_index, "Nombre Empleado"]  # Empleado con la evaluación más baja

# Encontrar el empleado con la edad más alta y más baja
max_edad_index = df["Edad"].idxmax()  # Índice de la edad más alta
min_edad_index = df["Edad"].idxmin()  # Índice de la edad más baja

max_edad_employee = df.loc[max_edad_index, "Nombre Empleado"]  # Empleado con la edad más alta
min_edad_employee = df.loc[min_edad_index, "Nombre Empleado"]  # Empleado con la edad más baja

# Crear dos columnas para mostrar los gráficos
col1, col2 = st.columns(2)  # Dividir en dos columnas

# Gráfico de barras para evaluación máxima y mínima por empleado
with col1:
    df_evaluacion = pd.DataFrame({
        "Empleado": [max_evaluacion_employee, min_evaluacion_employee],  # Nombres de empleados
        "Evaluación": [df.loc[max_evaluacion_index, "Evaluación"], df.loc[min_evaluacion_index, "Evaluación"]]  # Evaluación
    })

    bar_evaluacion = px.bar(
        df_evaluacion,
        x="Empleado",
        y="Evaluación",
        title="Evaluación Máxima y Mínima por Empleado",
        text_auto=True,  # Mostrar etiquetas automáticamente
        color="Empleado",  # Variación de colores
        orientation="v"  # Barras verticales
    )
    
    # Ajustar la posición del texto y otras configuraciones
    bar_evaluacion.update_traces(
        textposition='outside',  # Colocar etiquetas fuera de las barras para mayor claridad
        textfont=dict(size=12, color='black', weight='bold')  # Texto en negrita
    )
    
    bar_evaluacion.update_layout(
        height=500,  # Aumentar la altura del gráfico
        bargap=0.3,  # Espacio entre barras para claridad
        xaxis_title="Empleado",
        yaxis_title="Evaluación"
    )
    
    st.plotly_chart(bar_evaluacion, use_container_width=True)  # Mostrar el gráfico

# Gráfico de barras para edad máxima y mínima por empleado
with col2:
    df_edad = pd.DataFrame({
        "Empleado": [max_edad_employee, min_edad_employee],  # Empleados
        "Edad": [df.loc[max_edad_index, "Edad"], df.loc[min_edad_index, "Edad"]]  # Edad
    })

    bar_edad = px.bar(
        df_edad,
        x="Empleado",
        y="Edad",
        title="Edad Máxima y Mínima por Empleado",
        text_auto=True,
        color="Empleado",  # Variación de colores
        orientation="v"  # Barras verticales
    )
    
    # Ajustar la posición del texto y otras configuraciones
    bar_edad.update_traces(
        textposition='outside',  # Colocar etiquetas fuera de las barras para mayor claridad
        textfont=dict(size=12, color='black', weight='bold')  # Texto en negrita
    )
    
    bar_edad.update_layout(
        height=500,  # Aumentar la altura del gráfico
        bargap=0.3,  # Espacio entre barras para claridad
        xaxis_title="Empleado",
        yaxis_title="Edad (años)"
    )
    
    st.plotly_chart(bar_edad, use_container_width=True)  # Mostrar el gráfico

# Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad



# Centrar el mapa en República Dominicana con un nivel de zoom apropiado
republica_dominicana_coords = [18.7357, -70.1627]  # Coordenadas de República Dominicana
nivel_de_zoom = 8  # Ajustar el nivel de zoom para una vista panorámica de la isla

# Crear un mapa centrado en República Dominicana
mapa = folium.Map(location=republica_dominicana_coords, zoom_start=nivel_de_zoom, tiles="OpenStreetMap")

# Agrupar por región para contar empleados
region_counts = df.groupby(["Región", "Longitud", "Latitud"]).size().reset_index(name="Total Empleados")

# Agregar marcadores con el tooltip personalizado
for _, row in region_counts.iterrows():
    region = row["Región"]
    total_empleados = row["Total Empleados"]
    tooltip_text = f"Región: {region}\nTotal Empleados: {total_empleados}"  # Texto para el tooltip
    
    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        tooltip=tooltip_text,  # Mostrar el tooltip con información de la región y empleados
        icon=folium.Icon(color="blue", icon="info-sign")  # Personalizar el color y el icono
    ).add_to(mapa)

# Mostrar el mapa en Streamlit ocupando todo el ancho
st.subheader("🌎 Mapa de Empleados por Región (República Dominicana)")
st_folium(mapa, width='100%', height=600)  # Ancho completo para el mapa



# Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad


# SECCION TABLA CON CUMPLEANOS CON FORMATO CONDICIONAL:

# Asegurarse de que las fechas están en formato datetime
df["Fecha_Ingreso"] = pd.to_datetime(df["Fecha_Ingreso"])
df["Fecha_Actual"] = pd.to_datetime("today")

# Calcular "Antiguedad" como años con un decimal
df["Antiguedad"] = ((df["Fecha_Actual"] - df["Fecha_Ingreso"]).dt.days / 365.25).round(1)  # Considerar años bisiestos

# Definir la función para calcular el próximo cumpleaños
def calcular_proximo_cumpleanos(nacimiento, fecha_actual):
    cumpleanos = nacimiento.replace(year=fecha_actual.year)
    if cumpleanos < fecha_actual:
        cumpleanos = cumpleanos.replace(year=fecha_actual.year + 1)
    return cumpleanos

# Agregar la columna "Fecha Cumpleaños Calculado"
fecha_actual = df["Fecha_Actual"].iloc[0]
df["Fecha Cumpleaños Calculado"] = df["Nacimiento"].apply(lambda x: calcular_proximo_cumpleanos(x, fecha_actual))

# Calcular la cantidad de días hasta el próximo cumpleaños
df["Días hasta Cumpleaños"] = (df["Fecha Cumpleaños Calculado"] - fecha_actual).dt.days

# Filtrar para mostrar solo empleados con cumpleaños dentro de 3 meses (30 días)
df_3_meses = df[df["Días hasta Cumpleaños"] <= 30]

# Ordenar por fecha de cumpleaños más cercana
df_3_meses = df_3_meses.sort_values(by="Fecha Cumpleaños Calculado")

# Definir la función para asignar colores basados en la proximidad del cumpleaños
def obtener_color(dias):
    if dias == 0:
        return "green"
    elif dias <= 10:
        return "red"
    elif dias <= 15:
        return "orange"
    else:
        return "gray"

# Aplicar el color a la tabla filtrada
df_3_meses["Color Cumpleaños"] = df_3_meses["Días hasta Cumpleaños"].apply(obtener_color)

# Aplicar formato condicional a la fecha de cumpleaños
df_3_meses["Fecha Cumpleaños Calculado"] = df_3_meses.apply(
    lambda row: f"<span style='color:{row['Color Cumpleaños']}'>{row['Fecha Cumpleaños Calculado'].strftime('%Y-%m-%d')}</span>",
    axis=1
)

# Mostrar la tabla con el formato condicional y ordenada por fecha más cercana
st.subheader("🎂 Empleados con Cumpleaños Dentro de 30 Dias 🎉")

st.write(
    df_3_meses[
        ["ID Empleado", "Nombre Empleado", "Departamento", "Posición", "Nacimiento", "Género", "Edad", "Antiguedad", "Fecha Cumpleaños Calculado"]
    ].to_html(escape=False),
    unsafe_allow_html=True
)



# FIN SECCION TABLA CON CUMPLEANOS CON FORMATO CONDICIONAL:
















# Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad



# Asegurarse de que no haya valores nulos en las columnas críticas
df = df.dropna(subset=["Ciudad", "Sueldo", "Status"])

# Obtener el top 10 de empleados por ciudad y sueldos
df_ciudades = df.groupby("Ciudad").agg({
    "ID Empleado": "count",
    "Sueldo": "sum"
}).sort_values(by="ID Empleado", ascending=False).reset_index()

# Crear gráficos de barras para empleados por ciudad y sueldos por ciudad
bar_ciudades = px.bar(
    df_ciudades.head(10),  # Top 10 ciudades por cantidad de empleados
    x="Ciudad",
    y="ID Empleado",
    color="Ciudad",
    title="Top 10 Ciudades por Cantidad de Empleados",
    text_auto=True
)

bar_sueldos = px.bar(
    df_ciudades.head(10),  # Top 10 ciudades por sueldos
    x="Ciudad",
    y="Sueldo",
    color="Ciudad",
    title="Top 10 Ciudades por Total de Sueldos",
    text_auto=True
)

# Crear dos columnas para la primera sección
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(bar_ciudades, use_container_width=True)  # Gráfico para empleados por ciudad

with col2:
    st.plotly_chart(bar_sueldos, use_container_width=True)  # Gráfico para sueldos por ciudad

# Segunda sección para empleados por estatus
st.markdown("<hr>", unsafe_allow_html=True)  # Separador para claridad

# Formato condicional para estatus
df["Status"] = df["Status"].apply(lambda x: f"<span style='color: {'green' if x == 'Activo' else 'red' if x == 'Inactivo' else 'blue'}; font-weight: bold;'>{x}</span>")

# Gráfico para empleados por ciudad y estatus
bar_estatus = px.bar(
    df,
    x="Ciudad",
    y="ID Empleado",
    color="Status",
    title="Empleados por Ciudad y Estatus",
    text_auto=True,
    color_discrete_map={
        "Activo": "green",
        "Inactivo": "red",
        "Vacaciones": "blue"
    }
)

st.plotly_chart(bar_estatus, use_container_width=True)  # Gráfico para empleados por estatus




# Título para la sección de gráficos, con emoji y centrado
st.markdown("<h3 style='text-align: center;'> 📊 Distribucion por Departamentos.📊</h3>", unsafe_allow_html=True)

# Obtener conteo de empleados por posición
posiciones = df["Posición"].value_counts().reset_index()
posiciones.columns = ["Posición", "Cantidad de Empleados"]

# Dividir el DataFrame en tres partes
total_posiciones = len(posiciones)  # Total de posiciones
segment_size = math.ceil(total_posiciones / 3)  # Tamaño de cada segmento

# Crear tres subconjuntos del DataFrame
posiciones_1 = posiciones.iloc[:segment_size]  # Primer segmento
posiciones_2 = posiciones.iloc[segment_size:2 * segment_size]  # Segundo segmento
posiciones_3 = posiciones.iloc[2 * segment_size:]  # Tercer segmento

# Crear gráficos de barras verticales para cada subconjunto
grafico_1 = px.bar(
    posiciones_1,
    x="Posición",
    y="Cantidad de Empleados",
    title="Distribución de Empleados por Posición - Segmento 1",
    text_auto=True,
    color="Posición",
    template="plotly_white",
)

grafico_2 = px.bar(
    posiciones_2,
    x="Posición",
    y="Cantidad de Empleados",
    title="Distribución de Empleados por Posición - Segmento 2",
    text_auto=True,
    color="Posición",
    template="plotly_white",
)

grafico_3 = px.bar(
    posiciones_3,
    x="Posición",
    y="Cantidad de Empleados",
    title="Distribución de Empleados por Posición - Segmento 3",
    text_auto=True,
    color="Posición",
    template="plotly_white",
)

# Crear tres columnas en una fila para los gráficos
col1, col2, col3 = st.columns(3)

# Mostrar gráficos de barras verticales, cada uno en su columna
with col1:
    st.plotly_chart(grafico_1, use_container_width=True)

with col2:
    st.plotly_chart(grafico_2, use_container_width=True)

with col3:
    st.plotly_chart(grafico_3, use_container_width=True)



# Línea horizontal para dividir secciones
st.markdown("<hr>", unsafe_allow_html=True)


 # Espacio adicional para separar
st.write("")  # Espacio para mejorar visualización





    # Agregar un salto de línea para separar
st.write("")  # Esto crea un espacio adicional

###---------------------------------------------------------------------------###


st.markdown(
    """
    
     <p style='text-align: center; color: black; font-size: 30px;'>
       📤 Comparte este reporte:
    </p>
    
    <div style='text-align: center;'>
        <a href='https://twitter.com/intent/tweet?text=¡Mira%20este%20reporte!&url=https%3A%2F%2Fexample.com' target='_blank'>
            <img src='https://img.icons8.com/color/48/000000/twitter.png' alt='Twitter' />
        </a>
        <a href='https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fexample.com' target='_blank'>
            <img src='https://img.icons8.com/color/48/000000/facebook-new.png' alt='Facebook' />
        </a>
        <a href='https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fexample.com' target='_blank'>
            <img src='https://img.icons8.com/color/48/000000/linkedin.png' alt='LinkedIn' />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)



    # Agregar un salto de línea para separar
st.write("")  # Esto crea un espacio adicional





st.markdown(
    """
    <style>
    /* Animación para el borde circular con gradiente cónico y movimiento fluido */
    @keyframes waterFlow {
        0% {
            background-position: 100% 0; /* Posición inicial */
        }
        100% {
            background-position: -100% 0; /* Movimiento del fondo para crear el efecto de flujo */
        }
    }y

    /* Animación para el efecto de latido */
    @keyframes heartbeat {
        0% {
            transform: scale(1); /* Escala normal */
        }
        50% {
            transform: scale(1.05); /* Expansión para simular latido */
        }
        100% {
            transform: scale(1); /* Regreso a escala normal */
        }
    }

    /* Estilo para centrar el contenido */
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 50px; /* Margen superior ajustable */
        padding-bottom: 50px; /* Margen inferior ajustable */
    }

    /* Aplicación de animaciones y bordes al contenedor circular */
    .profile-image {
        width: 200px; /* Tamaño del contenedor */
        height: 200px; /* Tamaño del contenedor */
        border-radius: 50%; /* Forma circular */
        overflow: hidden; /* Para evitar desbordamientos */
        border: 8px solid transparent; /* Borde transparente para espacio del gradiente */
        background: conic-gradient(
            from 0deg,
            red 0%, 
            blue 25%, 
            green 50%, 
            yellow 75%, 
            rgb(231, 199, 231) 100%
        ); /* Gradiente cónico con cinco colores */
        animation: waterFlow 6s infinite linear, heartbeat 3s infinite; /* Animaciones de flujo y latido */
        background-size: 400% 100%; /* Permite movimiento fluido del gradiente */
        background-position: 100% 0; /* Posición inicial para el efecto de flujo */
        clip-path: circle(); /* Mantener forma circular, prevenir bordes extraños */
    }

    /* Estilo para la imagen dentro del contenedor circular */
    .profile-image img {
        width: 100%; /* Imagen cubre todo el contenedor */
        height: 100%; /* Imagen cubre todo el contenedor */
        object-fit: cover; /* Ajuste para que la imagen no se deforme */
        border-radius: 50%; /* Mantener la forma circular */
    }

    </style>
    
   
    """,
    unsafe_allow_html=True
)


# Definir el estilo CSS para resaltar palabras clave y usar negrita
css_style = """
<style>
.description-quien_soy {
  width: 70%; /* Ocupa el 70% del contenedor */
  color: black; /* Texto blanco */
  background-color: transparent; /* Fondo transparente */
  text-align: center; /* Texto centrado */
  font-size: 18px; /* Tamaño de letra para los párrafos */
  line-height: 1.6; /* Espacio entre líneas para mejorar la legibilidad */
  margin: 0 auto; /* Centrar horizontalmente dentro del contenedor */
  padding: 20px; /* Añadir espacio alrededor del contenido */
}

.description-quien_soy h2 {
  font-size: 30px; /* Tamaño de letra más grande para h2 */
  margin-bottom: 1em; /* Espacio debajo del título */
  color: black; /* Color verde limón fluorescente */
}

.parrafo {
  margin-bottom: 1.5em; /* Aumentar la separación entre párrafos */
  font-size: 20px; /* Tamaño de letra para los párrafos */
  color: black; /* Color verde limón fluorescente */
}

.highlight {
  font-weight: bold; /* Texto en negrita */
  color: color: black; /* Color verde limón fluorescente */; /* Color verde limón fluorescente */
}
</style>
"""

# Aplicar el estilo CSS
st.markdown(css_style, unsafe_allow_html=True)

# Sección de descripción personal
description_html = """
<div class="description-quien_soy">
  <h2>🤔 ¿Quién Soy? 🇩🇴</h2>
  
  
  
  <div class="centered">
    <img src="https://avatars.githubusercontent.com/u/38921558?v=4" class="profile-image" alt="Tu Fotografía">
  </div>


  <p class="parrafo">
    🙋 ¡Hola! Mi nombre es <span class="highlight">Juancito Peña V.</span>   💻. Soy un entusiasta del 📊 análisis de datos, las tecnologías, y la programación 💻,
    con más de 15 años de experiencia trabajando, educando, aprendiendo e innovando en sistemas orientados a procesos tecnológicos,
    administrativos, productivos y de marketing. Creo en el poder de la tecnología para mejorar la productividad 🚀, los
    negocios 💼 y la educación 🎓.
  </p>

  <p class="parrafo">
    🎓 Mi formación académica incluye un título en <span class="highlight">Ingeniería en Sistemas y Computación</span> 🎓, una especialidad en <span class="highlight">Desarrollo
    de Software</span> 🛠️, y una maestría en <span class="highlight">Sistemas con mención Gerencial</span>. Recientemente, he iniciado una nueva maestría en
    <span class="highlight">Ciencia de Datos para Negocios (Big Data & Business Analytics)</span> en CEUPE - Centro Europeo de Postgrado CEUPE/CESUMA 📚.
  </p>

  <p class="parrafo">
   🧬 Mis habilidades técnicas incluyen el uso avanzado de herramientas de Business Intelligence como: <span class="highlight">Excel 📊</span>, 
    <span class="highlight">SQL Server 💾</span>, <span class="highlight">Power BI</span>, <span class="highlight">Python</span> 🐍, y Crystal Reports 📊, 
    así como otras herramientas de Desarollo de Software como:  <span class="highlight"> Xamarin, .NET MAUI, C#, .NET Framework</span>, <span class="highlight">HTML</span>, <span class="highlight">CSS</span>, <span class="highlight">JavaScript, Python, PHP, 
    Wordpress, Balsamiq y Figma.</span> y otras herramientas y  Software ERP como: <span class="highlight">SAP HANA,
    Mseller App, Macola, EasySales</span>
  </p>

  <p class="parrafo">
    👷 He trabajado en implementaciones de software 💻, aplicaciones móviles para ventas 📱, almacén, distribución 🚚, así
    como en la creación y generación de reportes 📑, informes 📃, y dashboards para Business Intelligence, con el fin 
    de mejorar la toma de decisiones 🎯 en la empresa.  Desde el planteamiento del problema hasta el lanzamiento, 
    abarcando actividades como 📏 prototipado, 🔍 testing y 🧪 QA, hasta la documentación 📄 y la capacitación del personal 🧑‍🏫
  </p>
  
<p class="parrafo">
    🫡 Soy un guerrero en el mundo laboral, un ejemplo de resiliencia y determinación. Vengo de una familia humilde, 
    con escasos recursos, y he enfrentado mil ⚔️ batallas para llegar a donde estoy. He 🤕 caído muchas veces, pero me he 💪 levantado 
    mil y una, siempre con más fuerza y 🏃 determinación. Amo lo que hago ❤️, y esa pasión me impulsa a seguir adelante incluso
    cuando el camino es difícil.
</p>

<p class="parrafo">
    🤔 Si crees que te puedo ayudar con tus proyectos, no dudes en contactarme a través de mis redes sociales 📱,
    mi correo 📧, o por WhatsApp 💬. Estoy aquí para ayudarte a lograr tus objetivos y a superar cualquier desafío.
</p>





  
</div>
"""

st.markdown(description_html, unsafe_allow_html=True)

# Fin de la sección de descripción personal

# FIN SECCIÓN DE DESCRIPCIÓN PERSONAL

# Agregar una línea horizontal para dividir secciones
st.markdown("<hr>", unsafe_allow_html=True)
###---------------------------------------------------------------------------###


# SECCIÓN DEL PIE DE PÁGINA
footer_html = """

   <p style='text-align: center; color: black; font-size: 20px;'>
       Sígueme en mis Redes Sociales, Comparte y Comenta.
    </p>

    <div style='text-align: center; font-size: 18px; font-weight: bold;'>
      <br>
      <a href='https://www.youtube.com/@JuancitoPenaV' target='_blank' style='font-size: 18px;'>
        <img src='https://img.icons8.com/color/48/000000/youtube-play.png' alt='YouTube' width='24' /> YouTube
      </a> | 
      <a href='https://www.linkedin.com/in/juancitope%C3%B1a/' target='_blank' style='font-size: 18px;'>
        <img src='https://img.icons8.com/color/48/000000/linkedin-circled.png' alt='LinkedIn' width='24' /> LinkedIn
      </a> | 
      <a href='https://github.com/JUANCITOPENA/Analisis_Datos_Pedidos_Entregas_Python' target='_blank' style='font-size: 18px;'>
        <img src='https://img.icons8.com/material-rounded/48/4A90E2/github.png' alt='GitHub' width='24' /> GitHub
      </a> |
      <a href='https://www.instagram.com/' target='_blank' style='font-size: 18px;'>
        <img src='https://img.icons8.com/fluency/48/000000/instagram-new.png' alt='Instagram' width='24' /> Instagram
      </a> | 
      <a href='https://www.facebook.com/' target='_blank' style='font-size: 18px;'>
        <img src='https://img.icons8.com/color/48/000000/facebook-new.png' alt='Facebook' width='24' /> Facebook
      </a> | 
      <a href='https://chat.whatsapp.com/GrzUtfJXvTDFPW1jSa3NWR' target='_blank' style='font-size: 18px;'>
        <img src='https://img.icons8.com/color/48/000000/whatsapp.png' alt='WhatsApp' width='24' /> WhatsApp
      </a> |
      <a href='mailto:juancito.pena@gmail.com' target='_blank' style='font-size: 18px;'>
        <img src='https://cdn.icon-icons.com/icons2/1826/PNG/48/4202011emailgmaillogomailsocialsocialmedia-115677_115624.png' alt='Correo Electrónico' width='24' /> Correo Electrónico
      </a>
      <br><br>
      <h3>© 2023 Advisertecnology - Todos los derechos reservados | 
        <a href='https://advisertecnology.com/' target='_blank' style='font-size: 25x; color: #009432;'>www.advisertecnology.com</a>
      </h3>
    </div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

###---------------------------------------------------------------------------###

# Instrucciones para ejecutar el dashboard
# Desde la consola, en la carpeta de tu proyecto, ejecuta: `streamlit run Dashboard.py`