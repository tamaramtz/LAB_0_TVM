# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Repaso de python 3 y analisis de precios OHLC                              -- #
# -- Codigo: principal.py - script principal de proyecto                                  -- #
# -- Rep: https://github.com/ITESOIF/MyST/tree/master/Notas_Python/Notas_RepasoPython     -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# -- ------------------------------------------------------------- Importar con funciones -- #

import funciones as fn                              # Para procesamiento de datos
import visualizaciones as vs                        # Para visualizacion de datos
import pandas as pd                                 # Procesamiento de datos
from datos import OA_Ak                             # Importar token para API de OANDA

# -- --------------------------------------------------------- Descargar precios de OANDA -- #

# token de OANDA

OA_In = "EUR_USD"                                   # Instrumento
OA_Gn = "D"                                         # Granularidad de velas
fini = pd.to_datetime("2018-07-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

# Descargar precios masivos
df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                             p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)

# -- --------------------------------------------------------------- Graficar OHLC plotly -- #

vs_grafica1 = vs.g_velas(p0_de=df_pe.iloc[0:120, :])
vs_grafica1.show()

# -- ------------------------------------------------------------------- Conteno de velas -- #

# multiplicador de precios
pip_mult = 10000

# -- 0A.1: Hora
df_pe['hora'] = [df_pe['TimeStamp'][i].hour for i in range(0, len(df_pe['TimeStamp']))]

# -- 0A.2: Dia de la semana.
df_pe['dia'] = [df_pe['TimeStamp'][i].weekday() for i in range(0, len(df_pe['TimeStamp']))]

# -- 0B: Boxplot de amplitud de velas (close - open).
df_pe['co'] = (df_pe['Close'] - df_pe['Open']) * pip_mult

# -- ------------------------------------------------------------ Graficar Boxplot plotly -- #
vs_grafica2 = vs.g_boxplot_varios(p0_data=df_pe[['co']], p1_norm=False)
vs_grafica2.show()

# -- 01 Mes en el que ocurrió la vela.
df_pe['mes'] = [df_pe['TimeStamp'][i].month for i in range(0, len(df_pe['TimeStamp']))]

# -- 02 Sesion de la vela.
for i in range(0, len(df_pe['hora'])):
    if df_pe['hora'][i] in [22, 23, 0, 1, 2, 3, 4, 5, 6, 7]:
        df_pe['sesion'] = 'asia'
    elif df_pe['hora'][i] in [8]:
        df_pe['sesion'] = 'asia_europa'
    elif df_pe['hora'][i] in [9, 10, 11, 12]:
        df_pe['sesion'] = 'europa'
    elif df_pe['hora'][i] in [13, 14, 15, 16]:
        df_pe['sesion'] = 'europa_america'
    elif df_pe['hora'][i] in [17, 18, 19, 20, 21]:
        df_pe['sesion'] = 'america'

# -- 03 Amplitud de vela (en pips).
df_pe['oc'] = (df_pe['Open'] - df_pe['Close'])*pip_mult

# -- 04 Amplitud de los extremos (en pips).
df_pe['hl'] = (df_pe['High'] - df_pe['Low'])*pip_mult

# -- 05 Sentido de la vela (alcista o bajista)
df_pe['sentido'] = ["alcista" if df_pe['Close'][i] >= df_pe['Open'][i] else "bajista"
                            for i in range(0, len(df_pe['Close']))]

# -- 06 Conteo de velas consecutivas alcistas/bajistas.
df_pe.loc[0,'conteo_c'] = 0
x=0
for i in range(1, len(df_pe['sentido'])):
    if df_pe['sentido'][i] == df_pe['sentido'][i-1]:
        x += 1
        df_pe.loc[i,'conteo_c'] = x
    else:
        x = 0
        df_pe.loc[i,'conteo_c'] = x

# -- 07 Ventanas móviles de volatilidad.
df_pe['volatilidad_5'] = df_pe.iloc[:, 11].rolling(window=5).mean() #volalitilidad con 5
df_pe['volatilidad_25'] = df_pe.iloc[:, 11].rolling(window=25).mean() #volalitilidad con 25
df_pe['volatilidad_50'] = df_pe.iloc[:, 11].rolling(window=50).mean() #volalitilidad con 50





