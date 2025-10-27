import pandas as pd
import numpy as np

df = pd.read_csv("Base_Membros_Desempenho.csv")

# Dicionario para as substituicoes
senioridade = {
    "Jr": "Júnior", 
    "JR": "Júnior", 
    "P": "Pleno", 
    "pleno": "Pleno", 
    "senior": "Sênior", 
    "N/D": np.nan
}

#--Nivel Senioridade--
# Substituis as abreviacoes da senioridade
df["Nivel_Senioridade"] = df["Nivel_Senioridade"].replace(senioridade)
# Calcula moda da senioridade
moda_senioridade = df["Nivel_Senioridade"].mode()[0]
# Substitui os vazios pela moda
df["Nivel_Senioridade"] = df["Nivel_Senioridade"].fillna(moda_senioridade)

#--Av Tecnica e Comportamental--
# Calcula media da av tecnica e comportamental
media_av_tecnica = df["Avaliacao_Tecnica"].mean()
media_av_comportamental = df["Avaliacao_Comportamental"].mean()
# Substitui os vazios pelas medias
df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].fillna(media_av_tecnica).round(2)
df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].fillna(media_av_comportamental).round(2) 

#--Engajamento PIGs--
# Remover caractere %
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].str.replace("%", "")
# Converter de str pra float / errors="coerce": converte os vazios para nulos
df["Engajamento_PIGs"] = pd.to_numeric(df["Engajamento_PIGs"], errors="coerce")
# Converte pra decimal
df["Engajamento_PIGs"] = (df["Engajamento_PIGs"] / 100)
# Calcula media do engajamento
media_engajamento = df["Engajamento_PIGs"].mean()
# Substitui os vazios pelas medias
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].fillna(media_engajamento)
# Arredonda para somente 2 casas decimais
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].round(2)

#--Score Desempenho--
df["Score_Desempenho"] = ((df["Avaliacao_Tecnica"] * 0.5) + (df["Avaliacao_Comportamental"] * 0.5)).round(2)

#--Status Membro--
condicao_score = (df["Score_Desempenho"] >= 7.0)
condicao_engajamento = (df["Engajamento_PIGs"] >= 0.8)
# Cria a nova coluna e substitui dependendo da condicao
df["Status_Membro"] = np.where(
    condicao_score & condicao_engajamento, 
    "Em Destaque", 
    "Padrão"
)
 
# Converte a coluna de Av Tecnica e Comportamental de . para ,
df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].astype(str).str.replace(".", ",")
df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].astype(str).str.replace(".", ",")

# Cria um novo arquivo
df.to_csv("Base_Membros_Desempenho_Final.csv", index=False, sep=';')
print(df)
