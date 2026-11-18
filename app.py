import streamlit as st

st.set_page_config(page_title="Billy Walters Betting Model", page_icon="🏈", layout="centered")

st.title("📊 Billy Walters Betting Engine")
st.markdown("Modelo cuantitativo para detección de valor (Value Bets) y gestión de Bankroll mediante Criterio de Kelly.")

with st.sidebar:
    st.header("⚙️ Configuración de Bankroll")
    bankroll_total = st.number_input("Bankroll Total ($)", min_value=10.0, value=1000.0, step=50.0)
    kelly_fraction = st.slider("Fracción de Kelly (Seguridad)", min_value=0.1, max_value=1.0, value=0.25, step=0.05, 
                               help="Billy Walters utilizaba fracciones conservadoras (25% o 0.25) para evitar la ruina ante la varianza.")
    st.info("💡 **Consejo de Walters:** Nunca arriesgues el total matemático de Kelly puro.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Datos del Mercado")
    cuota_decimal = st.number_input("Cuota Decimal del Casino (Odds)", min_value=1.01, value=1.95, step=0.01)

with col2:
    st.subheader("2. Tu Modelo Estadístico")
    probabilidad_estimada = st.slider("Probabilidad Real Estimada (%)", min_value=1.0, max_value=99.0, value=55.0, step=0.5)

# Cálculos cuantitativos
prob_decimal = probabilidad_estimada / 100.0
implied_probability = 1.0 / cuota_decimal
expected_value = (prob_decimal * cuota_decimal) - 1.0

b = cuota_decimal - 1.0
q = 1.0 - prob_decimal
kelly_puro = (b * prob_decimal - q) / b if b > 0 else 0.0
kelly_sugerido = max(0.0, kelly_puro * kelly_fraction)
monto_apuesta = bankroll_total * kelly_sugerido

st.divider()
st.subheader("📈 Resultados del Análisis de Valor")

m1, m2, m3 = st.columns(3)
m1.metric(label="Probabilidad Implícita", value=f"{implied_probability*100:.2f}%")
m2.metric(label="Valor Esperado (EV)", value=f"{expected_value*100:+.2f}%", 
          delta="Rentable" if expected_value > 0 else "Sin Valor")
m3.metric(label="Apuesta Sugerida (Kelly)", value=f"${monto_apuesta:.2f}", delta=f"{kelly_sugerido*100:.2f}% del Bank")

if expected_value > 0:
    st.success(f"✅ **¡Apuesta Recomendada!** Tu modelo indica un {prob_decimal*100}% de acierto frente al {implied_probability*100}% implícito de la casa.")
else:
    st.warning("⚠️ **No Apostar.** El Valor Esperado (EV) es negativo o nulo.")
  
