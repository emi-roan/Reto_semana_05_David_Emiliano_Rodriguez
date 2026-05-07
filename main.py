import csv
import argparse
import os

def es_nulo(valor):
    return valor is None or str(valor).strip() == ""

def es_numerico(valor):
    try:
        float(str(valor).replace(',', '').strip())
        return True
    except (ValueError, TypeError):
        return False

def es_fecha(valor):
    v = str(valor).strip()
    # Detecta formato YYYY-MM-DD o similares
    if len(v) >= 10 and v[4] == '-' and v[7] == '-':
        return True
    return False

def inferir_tipo(valores):
    validos = [v for v in valores if not es_nulo(v)]
    if not validos: return "texto"
    total = len(validos)
    
    # Contadores para la regla del 80%
    fechas = sum(1 for v in validos if es_fecha(v))
    nums = sum(1 for v in validos if es_numerico(v))

    if fechas / total >= 0.8: return "fecha"
    if nums / total >= 0.8: return "numerico"
    return "texto"

def procesar(entrada, salida):
    if not os.path.exists(entrada):
        print(f"Error: {entrada} no encontrado")
        return

    # Usamos utf-8-sig para ignorar la marca de Windows si existe
    try:
        with open(entrada, 'r', encoding='utf-8-sig') as f:
            lector_lista = list(csv.DictReader(f))
            
        with open(entrada, 'r', encoding='utf-8-sig') as f:
            columnas = csv.DictReader(f).fieldnames
    except UnicodeDecodeError:
        # Si falla, intentamos con utf-16 que es el otro estándar de Windows
        with open(entrada, 'r', encoding='utf-16') as f:
            lector_lista = list(csv.DictReader(f))
        with open(entrada, 'r', encoding='utf-16') as f:
            columnas = csv.DictReader(f).fieldnames

    perfiles = []
    for col in columnas:
        valores = [fila[col] for fila in lector_lista]
        total = len(valores)
        nulos = sum(1 for v in valores if es_nulo(v))
        validos = [v for v in valores if not es_nulo(v)]
        unicos = len(set(validos))
        
        perfiles.append({
            "nombre_columna": col,
            "tipo_inferido": inferir_tipo(valores),
            "total_registros": total,
            "valores_nulos": nulos,
            "porcentaje_nulos": f"{(nulos/total)*100:.2f}",
            "valores_unicos": unicos,
            "porcentaje_unicos": f"{(unicos/total)*100:.2f}",
            "ejemplo_valor": validos[0] if validos else ""
        })

    with open(salida, 'w', encoding='utf-8', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=perfiles[0].keys())
        escritor.writeheader()
        escritor.writerows(perfiles)
    print(f"Reporte generado exitosamente en: {salida}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    procesar(args.input, args.output)