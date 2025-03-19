import streamlit as st 
import pandas as pd

Sprinkler = st.selectbox("Tipo de edificação",["Edificação comum", "Depósito"])

#Condição para aparecer IT 24
if Sprinkler == "Depósito":
    st.title("VOLUME RTI SPRINKLER PARA DEPÓSITO - IT 24")
# Inputs para altura da armazenagem e altura do teto
altura_armazenagem = st.number_input('Altura da Armazenagem (m)', value=0.0, step=0.1)
altura_teto = st.number_input('Altura do Teto (m)', value=0.0, step=0.1)
classe_da_mercadoria = st.selectbox("Classe da mercadoria",["classe 1 a 4", "borracha", "plástico" ])
Estrutura_de_armazenagem = st.selectbox("Estrutura_de_armazenagem",["Porta-palete sem prateleira sólida", "paletizadas", "pilhas sólidas" ])



# Valor constante
v = 12

# Lógica para definir t e exibir os inputs K e P condicionalmente
if altura_armazenagem <= 9.1 and altura_teto <= 10.7:
    k = 200
    p = 5.2
    t = 60  # t é constante se as condições forem atendidas
else:
    k = st.number_input('Fator K', value=0.0, step=0.1)
    p = st.number_input('Pressão (bar)', value=0.0, step=0.1)
    t = st.number_input('Duração da RTI (min)', value=0.0, step=0.1)  # t é input caso contrário


# Botão para calcular
if st.button('Calcular Volume da RTI'):
    try:
        vrti = k * math.sqrt(p) * v * t
        # Formatar o resultado para o formato brasileiro (opcional)
        # vrti_formatted = locale.format_string("%.2f", vrti, grouping=True)
        # st.success(f"O valor de Vrti é: {vrti_formatted} Litros")
        st.success(f"O valor de Vrti é: {vrti:.2f} Litros") # Formatação simplificada
    except ValueError:
        st.error("Por favor, insira valores numéricos válidos.")
