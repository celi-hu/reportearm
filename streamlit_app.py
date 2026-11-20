import traceback
from datetime import date, timedelta

import streamlit as st

import main as reporte

st.set_page_config(page_title="Reporte de asistencia", page_icon="🕒", layout="centered")

# ---------- (Opcional) Contraseña de acceso ----------
# Si definís APP_PASSWORD en los secrets, la app pide clave antes de mostrarse.
_app_password = st.secrets.get("APP_PASSWORD", None) if hasattr(st, "secrets") else None
if _app_password:
    if not st.session_state.get("auth_ok"):
        pwd = st.text_input("Contraseña", type="password")
        if pwd:
            if pwd == _app_password:
                st.session_state["auth_ok"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        st.stop()

# ---------- UI ----------
st.title("🕒 Reporte de asistencia")
st.caption("Genera el Excel de Detalle diario y Resumen General a partir de Time Tracking de Humand.")

hoy = date.today()
col1, col2 = st.columns(2)
with col1:
    desde = st.date_input("Desde", value=hoy - timedelta(days=30), format="YYYY-MM-DD")
with col2:
    hasta = st.date_input("Hasta", value=hoy, format="YYYY-MM-DD")

if desde > hasta:
    st.error("La fecha 'Desde' no puede ser posterior a 'Hasta'.")
    st.stop()

if st.button("Generar reporte", type="primary"):
    try:
        with st.spinner("Consultando la API y armando el Excel… puede tardar unos minutos."):
            data = reporte.run_report(desde.strftime("%Y-%m-%d"), hasta.strftime("%Y-%m-%d"))
        st.session_state["excel_bytes"] = data
        st.session_state["excel_name"] = f"reporte_basico_{desde}_{hasta}.xlsx"
        st.success("Reporte generado.")
    except Exception as e:
        st.session_state.pop("excel_bytes", None)
        st.error(f"Error al generar el reporte: {e}")
        with st.expander("Detalle técnico"):
            st.code(traceback.format_exc())

if "excel_bytes" in st.session_state:
    st.download_button(
        "⬇️ Descargar Excel",
        data=st.session_state["excel_bytes"],
        file_name=st.session_state["excel_name"],
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
