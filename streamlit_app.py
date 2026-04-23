import streamlit as st
from datetime import date, timedelta
from main import run_report

st.set_page_config(page_title="Reporte de Asistencia", page_icon="📋", layout="centered")

st.title("Reporte de Asistencia")
st.markdown("Seleccioná el período y descargá el reporte en Excel.")

col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Fecha inicio", value=date.today() - timedelta(days=30))
with col2:
    end = st.date_input("Fecha fin", value=date.today())

if st.button("Generar reporte", type="primary"):
    if start > end:
        st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
    else:
        with st.spinner("Generando reporte, esto puede tardar un minuto..."):
            try:
                data = run_report(str(start), str(end))
                filename = f"reporte_{start}_{end}.xlsx"
                st.success("Reporte generado.")
                st.download_button(
                    label="Descargar Excel",
                    data=data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            except Exception as e:
                st.error(f"Error al generar el reporte: {e}")
