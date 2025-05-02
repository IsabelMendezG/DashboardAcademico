import streamlit as st
import pandas as pd
import altair as alt

st.title("📚 Dashboard Educativo de Calificaciones")

# Subir archivo CSV
archivo = st.file_uploader("Carga un archivo CSV con las calificaciones", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)

    # Validar columnas requeridas
    columnas_esperadas = {'Grupo', 'Alumno', 'Materia', 'Tema', 'Calificación'}
    if not columnas_esperadas.issubset(df.columns):
        st.error("❌ El archivo debe contener las columnas: Grupo, Alumno, Materia, Tema, Calificación")
    else:
        grupos = df['Grupo'].unique()
        materias = df['Materia'].unique()

        # Filtros
        grupo_sel = st.selectbox("Selecciona un grupo:", grupos)
        materia_sel = st.selectbox("Selecciona una materia:", materias)

        df_filtrado = df[(df['Grupo'] == grupo_sel) & (df['Materia'] == materia_sel)]

        # Promedio por alumno
        promedios = df_filtrado.groupby('Alumno')['Calificación'].mean().reset_index()
        promedios['En Riesgo'] = promedios['Calificación'] < 6

        st.subheader("Promedios por Alumno")
        chart = alt.Chart(promedios).mark_bar().encode(
            x='Alumno',
            y='Calificación',
            color=alt.condition(
                alt.datum['En Riesgo'],
                alt.value('red'),
                alt.value('steelblue')
            ),
            tooltip=['Alumno', 'Calificación']
        ).properties(width=700).interactive()
        st.altair_chart(chart)

        # Porcentaje de aprobación por tema
        df_tema = df_filtrado.copy()
        df_tema['Aprobado'] = df_tema['Calificación'] >= 6
        aprobacion = df_tema.groupby('Tema')['Aprobado'].mean().reset_index()
        aprobacion['% Aprobación'] = aprobacion['Aprobado'] * 100

        st.subheader("Porcentaje de Aprobación por Tema")
        st.bar_chart(aprobacion.set_index('Tema')['% Aprobación'])

        # Tabla de alerta
        st.subheader("⚠️ Alumnos en Riesgo (Promedio < 6)")
        en_riesgo = promedios[promedios['En Riesgo']][['Alumno', 'Calificación']]
        st.dataframe(en_riesgo, use_container_width=True)
else:
    st.info("Por favor, carga un archivo CSV para comenzar.")
