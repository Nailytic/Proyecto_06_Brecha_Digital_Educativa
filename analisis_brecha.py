import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from fpdf import FPDF

# Cargar datos
df = pd.read_csv("data/acceso_tecnologico.csv")

# Agrupación por zona y nivel económico
zona_eco = df.groupby(["Zona", "Nivel_Economico"]).agg({
    "Acceso_Internet": "mean",
    "Dispositivos_por_Alumno": "mean"
}).reset_index()

# Crear visualización
plt.figure(figsize=(8, 5))
sns.barplot(x="Zona", y="Acceso_Internet", hue="Nivel_Economico", data=zona_eco)
plt.title("Acceso a Internet por Zona y Nivel Económico")
plt.ylabel("Acceso Promedio")
plt.tight_layout()
plt.savefig("images/mapa_conectividad.png")
plt.close()

# Exportar resumen en PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "Informe de Brecha Digital Educativa", ln=True, align="C")
pdf.ln(10)

resumen = df.groupby("Zona").agg({
    "Acceso_Internet": "mean",
    "Dispositivos_por_Alumno": "mean"
}).round(2)

for zona in resumen.index:
    pdf.cell(200, 10,
             f"{zona}: Acceso medio: {resumen.loc[zona, 'Acceso_Internet']}, "
             f"Dispositivos por alumno: {resumen.loc[zona, 'Dispositivos_por_Alumno']}",
             ln=True)

pdf.output("output/brecha_resumen.pdf")
print("Análisis completado. Informe PDF generado.")
