import pandas as pd
import streamlit as st

# Leitura do arquivo Excel com as ocupações
df = pd.read_excel("ocupação.xlsx").fillna(method='ffill')
print(df)

# Criar lista única de tipos de edificação
tipos_edificacao = df['Tipo de edificação'].unique().tolist()

# Criar o primeiro selectbox para Tipo de edificação
tipo_selecionado = st.selectbox('Selecione o tipo de edificação:', tipos_edificacao)

# Filtrar as ocupações baseado no tipo de edificação selecionado
ocupacoes_filtradas = df[df['Tipo de edificação'] == tipo_selecionado]

# Criar lista de ocupações com seus respectivos grupos
opcoes_ocupacao = [f"{row['Ocupação']} (Grupo {row['Grupo']})"
                   for _, row in ocupacoes_filtradas.iterrows()]

# Criar o segundo selectbox para Ocupação com informação do Grupo
ocupacao_selecionada = st.selectbox('Selecione a ocupação:', opcoes_ocupacao)

# Extrair apenas a ocupação (removendo a parte do Grupo) para usar nas consultas
ocupacao_sem_grupo = ocupacao_selecionada.split(' (Grupo')[0]

# Encontrar o Grupo correspondente à ocupação selecionada
grupo_correspondente = df[df['Ocupação'] == ocupacao_sem_grupo]['Grupo'].iloc[0]

# Criar inputs numéricos para área e altura
area = st.number_input('Digite a área da edificação (m²):', min_value=0.0, value=0.0, step=0.1)
altura = st.number_input('Digite a altura da edificação (m):', min_value=0.0, value=0.0, step=0.1)

# Select box para área entre 3001.01 e 5000
ocupacoes_com_condicao = ["Comércio de pequeno porte", "Comércio de médio porte", "Comércio de grande porte", "Escritórios", "Agências bancárias", "Laboratórios e estúdios", "Serviços de reparação", "Escolas em geral", "Escolas especiais", "Locais para cultura física", "Pré-escolas"]

if (3000 < area < 5000.01) and (ocupacao_sem_grupo in ocupacoes_com_condicao):
    opcao_selecionada = st.selectbox(
        "A edificação possui vãos, com área superior a 3000 m², que não possuem compartimentação horizontal resistente ao fogo por no mínimo 02 horas?",
        ["Não", "Sim"]
    )
else:
    opcao_selecionada = "Não"

# Mover o dicionário de regras para uma função separada
def get_regras_ocupacao():
    return {
        #OCUPAÇÕES
        # RESIDENCIAL
        "Residenciais multifamiliares": {
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "glp", "spda"]
            },
            "nivel6": {
                "condicoes": {"altura": 60.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                 
            }
        },

        # TRANSITÓRIOS
        "Habitações coletivas": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda", "glp"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            }
        },

        "Hotéis": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            }
        },

        "Hotéis residenciais": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            }
        },

        # COMERCIAIS
        "Comércio de pequeno porte": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # Adicionada para área > 3000
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

        "Comércio de médio porte": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # : Adicionada para área > 3001.01
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

        "Comércio de grande porte": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # Adicionada para área > 3000
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

         #SERVIÇOS PROFISSIONAIS
        "Escritórios": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # Adicionada para área > 3000
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

        "Agências bancárias": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # : Adicionada para área > 3000
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

        "Laboratórios e estúdios": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # Adicionada para área > 3000
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

         "Serviços de reparação": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            # Adicionada para área > 3000
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }
        },

         # ESCOLARES
         # Grupo 13
        "Escolas em geral": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
    
        },
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            },
             "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Alarme"]
             }
    },
         # Grupo 14
         "Escolas especiais": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
        
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            },

            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Alarme"]
             }
        },
        # Grupo 15
         "Locais para cultura física": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura":9.01},
                "sistemas": ["Hidrante", "spda", "Alarme"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
        
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            }

        },

         # Grupo 16
         "Pré-escolas": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
        
            "nivel3": {
                "condicoes": {"area": 3000.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"],
                "requer_confirmacao": True
            },

            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Alarme"]
             }
        },
         # Grupo 17
         "Escolas para portadores de deficiências": {
            "glp": True,  # "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "spda"]
            },
            "nivel2": {
                "condicoes": {"area": 3000.01, "altura": 6.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["Alarme"]
             }
        },
        # CONCENTRAÇÃO DE PÚBLICO
         # Grupo 18
         "Museus e bibliotecas": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["spda"]
             }
        },
        # Grupo 19.01
         "Templos religiosos": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["spda"]
             }
        },
         # Grupo 20
         "Centros esportivos e de exibição": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["spda"]
             }
        },
         # Grupo 21
         "Terminais de passageiros": {
            "glp": True,  # Adicionado "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 1200.01, "altura": 9.01},
                "sistemas": ["Hidrante", "Alarme"]
            },
            "nivel2": {
                "condicoes": {"area": 5000.01, "altura": 12.01},
                "sistemas": ["Detecção de incêndio", "Chuveiros automáticos"]
            },
            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["spda"]
             }
        },
        # Grupo 22
         "Artes cênicas e auditórios": {
            "glp": True,  # "glp" em qualquer situação, conforme NT 01/16
            "nivel1": {
                "condicoes": {"area": 500.01, "altura": 1000},
                "sistemas": ["Hidrante", "Alarme"]
            },
            "nivel2": {
                "condicoes": {"area": 500.01, "altura": 3.01},
                "sistemas": ["Detecção de incêndio"]
            },
            "nivel5": {
                "condicoes": {"area": 3.01, "altura": 3.01},
                "sistemas": ["chuveiros automáticos"]
            },

            "nivel4": {
                "condicoes": {"area": 750.01, "altura": 9.01},
                "sistemas": ["spda"]
             }
         }
    }
# No início da lógica de verificação, obter as regras
regras_ocupacao = get_regras_ocupacao()

# Verificar siar todos os campos foram preenchidos
if tipo_selecionado and ocupacao_selecionada and area > 0 and altura > 0:
    # Mostrar as informações obrigatórias
    st.title("SISTEMAS OBRIGATÓRIOS")
    st.write("Saída de emergência")
    st.write("Sinalização de emergência")
    st.write("Iluminação de emergência")
    st.write("Extintores de incêndio")

    # **[ADICIONADO]** Define a variável regras com um valor padrão (None)
    regras = None

    # Verificar regras específicas da ocupação
    if ocupacao_sem_grupo in regras_ocupacao:
        regras = regras_ocupacao[ocupacao_sem_grupo]

        # Exibir "glp" sempre, mas apenas para as ocupações específicas (Transitórias, comerciais)
        if regras.get("glp"):  # Verifica si a chave "glp" existe e é True
            st.write("glp")

           # **[ADICIONADO]** Lista para rastrear os sistemas já exibidos
    sistemas_exibidos = []

    # Verificar primeiro nível de exigência
    if "nivel1" in regras:
        nivel1 = regras["nivel1"]
        if area >= nivel1["condicoes"]["area"] or altura >= nivel1["condicoes"]["altura"]:
            for sistema in nivel1["sistemas"]:
                st.write(sistema)
                # **[ADICIONADO]** Adiciona o sistema à lista de exibidos
                sistemas_exibidos.append(sistema)

    # Verificar segundo nível de exigência
    if "nivel2" in regras:
        nivel2 = regras["nivel2"]
        if area >= nivel2["condicoes"]["area"] or altura >= nivel2["condicoes"]["altura"]:
            for sistema in nivel2["sistemas"]:
                # **[ALTERADO]** Verifica se o sistema já foi exibido antes de exibir
                if sistema not in sistemas_exibidos:
                    st.write(sistema)
                    # **[ADICIONADO]** Adiciona o sistema à lista de exibidos
                    sistemas_exibidos.append(sistema)

    # Verificar nível 3 (área > 3000)
    if "nivel3" in regras and opcao_selecionada == "Sim":
        for sistema in regras["nivel3"]["sistemas"]:
            # Verifica se o sistema já foi exibido antes de exibir
            if sistema not in sistemas_exibidos:
                st.write(sistema)
                #  Adiciona o sistema à lista de exibidos
                sistemas_exibidos.append(sistema)

     # Verificar segundo nível de exigência
    if "nivel4" in regras:
        nivel4 = regras["nivel4"]
        if area >= nivel4["condicoes"]["area"] or altura >= nivel4["condicoes"]["altura"]:
            for sistema in nivel4["sistemas"]:
                # **[ALTERADO]** Verifica se o sistema já foi exibido antes de exibir
                if sistema not in sistemas_exibidos:
                    st.write(sistema)
                    # **[ADICIONADO]** Adiciona o sistema à lista de exibidos
                    sistemas_exibidos.append(sistema)
    
 # Verificar segundo nível de exigência
    if "nivel5" in regras:
        nivel5 = regras["nivel5"]
        if area >= nivel5["condicoes"]["area"] or altura >= nivel5["condicoes"]["altura"]:
            for sistema in nivel5["sistemas"]:
                # **[ALTERADO]** Verifica se o sistema já foi exibido antes de exibir
                if sistema not in sistemas_exibidos:
                    st.write(sistema)
                    # **[ADICIONADO]** Adiciona o sistema à lista de exibidos
                    sistemas_exibidos.append(sistema)
    
 # Verificar segundo nível de exigência
    if "nivel6" in regras:
        nivel6 = regras["nivel6"]
        if altura >= nivel6["condicoes"]["altura"]:
            for sistema in nivel6["sistemas"]:
                # Verifica se o sistema já foi exibido antes de exibir
                if sistema not in sistemas_exibidos:
                    st.write(sistema)
                    # Adiciona o sistema à lista de exibidos
                    sistemas_exibidos.append(sistema)
else:
    st.info('Por favor, preencha todos os campos acima para ver os sistemas obrigatórios.')