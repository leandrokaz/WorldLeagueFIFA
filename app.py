import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import random

# Configuración de la página Streamlit
st.set_page_config(page_title="Simulador FIFA - Sistema Suizo", layout="wide")

# Configuración estética para gráficos
sns.set_theme(style="whitegrid")

# ==========================================
# 1. BASE DE DATOS OFICIAL FIFA COMPLETA (211 SELECCIONES)
# ==========================================
@st.cache_data
def cargar_datos_fifa():
    return {
        "Argentina": 1877, "España": 1874, "Francia": 1870, "Inglaterra": 1828, "Portugal": 1767,
        "Brasil": 1765, "Marruecos": 1755, "Países Bajos": 1753, "Bélgica": 1742, "Alemania": 1735,
        "Croacia": 1714, "Italia": 1704, "Colombia": 1698, "México": 1687, "Senegal": 1684,
        "Uruguay": 1673, "EE. UU.": 1671, "Japón": 1661, "Suiza": 1650, "RI de Irán": 1619,
        "Dinamarca": 1619, "Turquía": 1605, "Ecuador": 1598, "Austria": 1597, "República de Corea": 1591,
        "Nigeria": 1585, "Australia": 1579, "Argelia": 1571, "Egipto": 1562, "Canadá": 1559,
        "Noruega": 1557, "Ucrania": 1549, "Costa de Marfil": 1540, "Panamá": 1539, "Rusia": 1529,
        "Polonia": 1526, "Gales": 1516, "Suecia": 1509, "Hungría": 1506, "Chequia": 1505,
        "Paraguay": 1505, "Escocia": 1503, "Serbia": 1502, "Camerún": 1481, "Túnez": 1476,
        "RD Congo": 1474, "Eslovaquia": 1473, "Grecia": 1473, "Venezuela": 1469, "Uzbekistán": 1458,
        "Chile": 1458, "Perú": 1457, "Costa Rica": 1456, "Rumanía": 1455, "Mali": 1455,
        "Catar": 1450, "Irak": 1446, "República de Irlanda": 1441, "Eslovenia": 1441, "Sudáfrica": 1428,
        "Arabia Saudí": 1423, "Burkina Faso": 1406, "Jordania": 1387, "Bosnia y Herzegovina": 1387, "Honduras": 1378,
        "Albania": 1376, "Islas de Cabo Verde": 1371, "Emiratos Árabes Unidos": 1370, "Macedonia del Norte": 1369, "Irlanda del Norte": 1365,
        "Jamaica": 1357, "Georgia": 1355, "Ghana": 1346, "Islandia": 1342, "Finlandia": 1341,
        "Israel": 1333, "Bolivia": 1326, "Kosovo": 1319, "Omán": 1306, "Montenegro": 1301,
        "Guinea": 1295, "Curazao": 1294, "Haití": 1293, "Siria": 1283, "Nueva Zelanda": 1275,
        "Gabón": 1272, "Bulgaria": 1271, "Angola": 1265, "Uganda": 1264, "Zambia": 1255,
        "RP China": 1254, "Baréin": 1254, "Benín": 1252, "Tailandia": 1250, "Palestina": 1243,
        "Bielorrusia": 1242, "Guatemala": 1238, "Luxemburgo": 1232, "Vietnam": 1225, "El Salvador": 1225,
        "Tayikistán": 1224, "Trinidad y Tobago": 1219, "Mozambique": 1218, "Madagascar": 1202, "Guinea Ecuatorial": 1195,
        "Kirguizistán": 1192, "Armenia": 1189, "Comoras": 1187, "Kenia": 1185, "Libia": 1182,
        "Kazajistán": 1180, "Tanzania": 1180, "Mauritania": 1176, "Níger": 1175, "Líbano": 1172,
        "Gambia": 1159, "Sudán": 1157, "Indonesia": 1157, "Togo": 1152, "RPD de Corea": 1151,
        "Namibia": 1148, "Sierra Leona": 1147, "Islas Feroe": 1136, "Chipre": 1133, "Surinam": 1132,
        "Azerbaiyán": 1132, "Estonia": 1130, "Ruanda": 1126, "Malaui": 1122, "Zimbabue": 1119,
        "Nicaragua": 1114, "Guinea-Bisáu": 1108, "Kuwait": 1106, "Congo": 1105, "Filipinas": 1100,
        "Malasia": 1086, "Letonia": 1085, "India": 1084, "República Centroafricana": 1080, "Liberia": 1080,
        "Turkmenistán": 1078, "Burundi": 1078, "Etiopía": 1077, "República Dominicana": 1076, "Yemen": 1065,
        "Lesoto": 1064, "Botsuana": 1063, "Singapur": 1057, "Lituania": 1056, "Guyana": 1049,
        "Nueva Caledonia": 1036, "San Cristóbal y Nieves": 1036, "Islas Salomón": 1031, "Puerto Rico": 1024, "Fiyi": 1024,
        "Hong Kong": 1024, "Tahití": 1019, "Myanmar": 1010, "Moldavia": 1008, "Vanuatu": 1002,
        "Malta": 992, "Antigua y Barbuda": 986, "Granada": 981, "Cuba": 981, "Suazilandia": 979,
        "Santa Lucía": 976, "Bermuda": 975, "Papúa Nueva Guinea": 974, "Sudán del Sur": 970, "San Vicente y las Granadinas": 968,
        "Afganistán": 968, "Andorra": 946, "Maldivas": 943, "China Taipéi": 923, "Camboya": 922,
        "Montserrat": 916, "Nepal": 914, "Mauricio": 911, "Barbados": 909, "Belice": 907,
        "Bangladés": 902, "Dominica": 897, "Chad": 896, "Eritrea": 887, "Laos": 885,
        "Islas Cook": 877, "Sri Lanka": 876, "Samoa": 876, "Aruba": 875, "Mongolia": 874,
        "Samoa Estadounidense": 871, "Bután": 870, "Macao": 858, "Brunéi Darusalam": 857, "Santo Tomé y Príncipe": 855,
        "Yibuti": 853, "Islas Caimán": 850, "Pakistán": 840, "Somalia": 839, "Tonga": 835,
        "Timor Oriental": 831, "Gibraltar": 820, "Guam": 819, "Seychelles": 804, "Islas Turcas y Caicos": 803,
        "Liechtenstein": 797, "Bahamas": 786, "Islas Vírgenes Estadounidenses": 779, "Islas Vírgenes Británicas": 777, "Anguilla": 760,
        "San Marino": 721
    }

# ==========================================
# 2. FUNCIONES DE SIMULACIÓN Y ELO
# ==========================================
def simular_partido(elo1, elo2):
    prob_1 = 1 / (10 ** ((elo2 - elo1) / 400) + 1)
    goles_1, goles_2 = 0, 0
    for _ in range(random.randint(2, 5)):
        if random.random() < prob_1: 
            goles_1 += 1 if random.random() > 0.35 else 0
        else: 
            goles_2 += 1 if random.random() > 0.35 else 0
    p1 = 3 if goles_1 > goles_2 else (1 if goles_1 == goles_2 else 0)
    p2 = 3 if goles_2 > goles_1 else (1 if goles_1 == goles_2 else 0)
    return goles_1, goles_2, p1, p2

def calcular_cambio_elo(elo1, elo2, p1):
    K = 20
    esperada = 1 / (10 ** ((elo2 - elo1) / 400) + 1)
    real = p1 / 3
    return round(K * (real - esperada), 1)

# ==========================================
# 3. MOTOR DE EMPAREJAMIENTOS (DUTCH SWISS + GRAFOS)
# ==========================================
def generar_emparejamientos(equipos_ordenados, ronda, selecciones, historial_torneo):
    partidos_formateados = []
    equipos_a_emparejar = equipos_ordenados.copy()

    # Rul 1: BYE estricto para el peor rankeado si la cantidad es impar
    if len(equipos_a_emparejar) % 2 != 0:
        for eq in reversed(equipos_a_emparejar):
            if "BYE" not in selecciones[eq]["rivales"]:
                partidos_formateados.append((eq, "BYE"))
                equipos_a_emparejar.remove(eq)
                break

    # Rul 2: Regla especial para Ronda 1 (Alternancia L-V perfecta y cruces por mitades)
    if ronda == 1:
        mitad = len(equipos_a_emparejar) // 2
        for i in range(mitad):
            eq1, eq2 = equipos_a_emparejar[i], equipos_a_emparejar[i + mitad]
            if i % 2 == 0:
                partidos_formateados.append((eq1, eq2))
            else:
                partidos_formateados.append((eq2, eq1))
        # Ordenar por Mesa 1
        partidos_formateados.sort(key=lambda x: selecciones[x[0]]["elo"], reverse=True)
        return partidos_formateados

    # Rul 3: Sistema de Mitades (Dutch System) + Grafos para Rondas 2 en adelante
    grupos_puntos = {}
    for eq in equipos_a_emparejar:
        pts = selecciones[eq]["puntos"]
        if pts not in grupos_puntos: 
            grupos_puntos[pts] = []
        grupos_puntos[pts].append(eq)
        
    info_mitades = {}
    banco_floater = None
    grupo_id = 0
    
    for pts in sorted(grupos_puntos.keys(), reverse=True):
        grupo = grupos_puntos[pts]
        if banco_floater:
            grupo.insert(0, banco_floater)
            banco_floater = None
        if len(grupo) % 2 != 0:
            banco_floater = grupo.pop()
            
        mitad_len = len(grupo) // 2
        for i, eq in enumerate(grupo):
            m = 1 if i < mitad_len else 2
            r = i if i < mitad_len else i - mitad_len
            info_mitades[eq] = (grupo_id, m, r)
        grupo_id += 1
        
    if banco_floater:
        info_mitades[banco_floater] = (grupo_id, 1, 0)
        
    G = nx.Graph()
    for i in range(len(equipos_a_emparejar)):
        eq1 = equipos_a_emparejar[i]
        for j in range(i+1, len(equipos_a_emparejar)):
            eq2 = equipos_a_emparejar[j]
            
            if eq2 not in selecciones[eq1]["rivales"]:
                peso = 1000000000 
                
                # Control estricto de alternancia L-V mediante historial real
                l1 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[0] == eq1)
                v1 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[2] == eq1)
                l2 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[0] == eq2)
                v2 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[2] == eq2)
                
                b1, b2 = l1 - v1, l2 - v2
                if (b1 > 0 and b2 > 0) or (b1 < 0 and b2 < 0):
                    peso -= 500000000
                
                # Puntos y mitades
                diff_pts = abs(selecciones[eq1]["puntos"] - selecciones[eq2]["puntos"])
                peso -= diff_pts * 10000
                
                g1, m1, r1 = info_mitades[eq1]
                g2, m2, r2 = info_mitades[eq2]
                if g1 == g2 and m1 != m2:
                    peso += 1000000
                    
                G.add_edge(eq1, eq2, weight=peso)
                
    matching = nx.max_weight_matching(G, maxcardinality=True)
    
    for n1, n2 in matching:
        l1 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[0] == n1)
        v1 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[2] == n1)
        l2 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[0] == n2)
        v2 = sum(1 for r_prev in range(1, ronda) for p in historial_torneo[r_prev] if p[2] == n2)
        
        b1, b2 = l1 - v1, l2 - v2
        if b1 < b2:
            eq_l, eq_v = n1, n2
        elif b2 < b1:
            eq_l, eq_v = n2, n1
        else:
            eq_l, eq_v = (n1, n2) if random.choice([True, False]) else (n2, n1)
            
        partidos_formateados.append((eq_l, eq_v))
        
    def importancia_partido(match):
        if match[1] == "BYE": 
            return (-1, -1)
        return (max(selecciones[match[0]]["puntos"], selecciones[match[1]]["puntos"]), 
                max(selecciones[match[0]]["elo"], selecciones[match[1]]["elo"]))
        
    partidos_formateados.sort(key=importancia_partido, reverse=True)
    return partidos_formateados

# ==========================================
# 4. INTERFAZ DE STREAMLIT
# ==========================================
st.title("🏆 Simulador Profesional de Torneo FIFA - Sistema Suizo")
st.markdown("Generación de fixture dinámico con alternancia L-V tipo ajedrez, cálculo de ELO en vivo y sistema Buchholz.")

st.sidebar.header("Opciones de Configuración")
n_rondas = st.sidebar.slider("Número de Rondas", 5, 15, 11)

if st.sidebar.button("🚀 Simular Torneo Completo", type="primary"):
    with st.spinner("Simulando las rondas y calculando coeficientes..."):
        datos_fifa = cargar_datos_fifa()
        selecciones = {k: {"elo": v, "puntos": 0, "gf": 0, "gc": 0, "rivales": [], "delta_elo": 0.0} for k, v in datos_fifa.items()}
        historial_torneo = {}
        evolucion_puntos = {k: [0] for k in selecciones.keys()}

        # Simulación ronda por ronda
        for ronda in range(1, n_rondas + 1):
            historial_torneo[ronda] = []
            equipos_actuales = sorted(selecciones.keys(), key=lambda x: selecciones[x]["elo"], reverse=True) if ronda == 1 else sorted(selecciones.keys(), key=lambda x: (selecciones[x]["puntos"], selecciones[x]["elo"]), reverse=True)
            
            partidos = generar_emparejamientos(equipos_actuales, ronda, selecciones, historial_torneo)
            
            for eq1, eq2 in partidos:
                if eq2 == "BYE":
                    selecciones[eq1]["puntos"] += 3
                    selecciones[eq1]["rivales"].append("BYE")
                    historial_torneo[ronda].append((eq1, "BYE", "Fecha Libre (+3 pts)", ""))
                    continue
                    
                g1, g2, p1, p2 = simular_partido(selecciones[eq1]["elo"], selecciones[eq2]["elo"])
                
                # Actualizar Elo
                delta1 = calcular_cambio_elo(selecciones[eq1]["elo"], selecciones[eq2]["elo"], p1)
                delta2 = calcular_cambio_elo(selecciones[eq2]["elo"], selecciones[eq1]["elo"], p2)
                selecciones[eq1]["delta_elo"] += delta1
                selecciones[eq2]["delta_elo"] += delta2
                
                # Actualizar puntos y goles
                selecciones[eq1]["puntos"] += p1
                selecciones[eq1]["gf"] += g1
                selecciones[eq1]["gc"] += g2
                selecciones[eq1]["rivales"].append(eq2)
                
                selecciones[eq2]["puntos"] += p2
                selecciones[eq2]["gf"] += g2
                selecciones[eq2]["gc"] += g1
                selecciones[eq2]["rivales"].append(eq1)
                
                historial_torneo[ronda].append((eq1, g1, eq2, g2))
                
            for k in selecciones.keys():
                evolucion_puntos[k].append(selecciones[k]["puntos"])

        def calcular_buchholz(equipo):
            return sum(selecciones[riv]["puntos"] for riv in selecciones[equipo]["rivales"] if riv != "BYE")

        tabla_final_ordenada = sorted(selecciones.keys(), key=lambda x: (selecciones[x]["puntos"], calcular_buchholz(x)), reverse=True)

        st.success(f"¡Torneo finalizado! Campeón: **{tabla_final_ordenada[0].upper()} 🏆**")

        # --- SECCIÓN 1: GRÁFICOS ---
        st.subheader("📈 Evolución de los 10 Líderes Ronda a Ronda")
        fig, ax = plt.subplots(figsize=(12, 6))
        for nacion in tabla_final_ordenada[:10]:
            ax.plot(range(0, n_rondas + 1), evolucion_puntos[nacion], marker='o', linewidth=2, label=nacion)
        ax.set_xlabel("Rondas")
        ax.set_ylabel("Puntos Acumulados")
        ax.set_xticks(range(0, n_rondas + 1))
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
        st.pyplot(fig)

        # --- SECCIÓN 2: TABLA DE CLASIFICACIÓN ---
        st.subheader("🥇 Clasificación General")
        
        data_tabla = []
        for pos, eq in enumerate(tabla_final_ordenada, 1):
            diff = selecciones[eq]["gf"] - selecciones[eq]["gc"]
            bh = calcular_buchholz(eq)
            l_reales = sum(1 for r in range(1, n_rondas + 1) for p in historial_torneo[r] if p[0] == eq)
            v_reales = sum(1 for r in range(1, n_rondas + 1) for p in historial_torneo[r] if p[2] == eq)
            delta = selecciones[eq]["delta_elo"]
            
            data_tabla.append({
                "Pos": f"#{pos}",
                "Selección": eq,
                "Elo Inicial": selecciones[eq]["elo"],
                "Puntos": selecciones[eq]["puntos"],
                "Buchholz": bh,
                "Balance L-V": f"{l_reales}L - {v_reales}V",
                "Elo +/-": f"{delta:+g}",
                "DG": f"{diff:+d}"
            })
            
        df_display = pd.DataFrame(data_tabla)
        st.dataframe(df_display, use_container_width=True, height=450)

        # --- SECCIÓN 3: BITÁCORA DE PARTIDOS ---
        st.subheader("📅 Bitácora Completa de Partidos")
        for r in range(1, n_rondas + 1):
            with st.expander(f"Ronda {r} ({len(historial_torneo[r])} partidos disputados)"):
                cols = st.columns(2)
                for idx, partido in enumerate(historial_torneo[r]):
                    col_idx = idx % 2
                    with cols[col_idx]:
                        if len(partido) == 4 and partido[1] == "BYE":
                            st.info(f"🗓️ **{partido[0]}** recibe Fecha Libre (+3 pts)")
                        else:
                            eq_l, g_l, eq_v, g_v = partido
                            st.markdown(f"**M{idx+1}**: `{eq_l} (L)` **{g_l} - {g_v}** `(V) {eq_v}`")