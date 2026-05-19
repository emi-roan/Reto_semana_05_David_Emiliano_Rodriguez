#!/usr/bin/env python3
import argparse
import csv
import sys
import os

def es_valor_nulo(valor):
    if valor is None: return True
    if isinstance(valor, str) and valor.strip() == "": return True
    return False

def es_numerico(valor):
    try:
        float(str(valor).replace(',', '').strip())
        return True
    except (ValueError, TypeError):
        return False

def es_fecha(valor):
    v = str(valor).strip()
    if len(v) >= 10 and v[4] == '-' and v[7] == '-':
        return True
    return False

def es_booleano(valor):
    v = str(valor).strip().lower()
    return v in ['true', 'false', 'yes', 'no', 'si', '1', '0', 't', 'f']

def inferir_tipo(valores):
    valores_validos = [v for v in valores if not es_valor_nulo(v)]
    if not valores_validos: return "texto"
    
    total = len(valores_validos)
    umbral = 0.8
    
    if sum(1 for v in valores_validos if es_fecha(v)) / total >= umbral: return "fecha"
    if sum(1 for v in valores_validos if es_booleano(v)) / total >= umbral: return "booleano"
    if sum(1 for v in valores_validos if es_numerico(v)) / total >= umbral: return "numerico"
    return "texto"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} no encontrado")
        sys.exit(1)

    # Intento robusto de lectura de archivos
    lector = None
    encodings = ['utf-8-sig', 'utf-8', 'utf-16', 'latin-1']
    for enc in encodings:
        try:
            with open(args.input, 'r', encoding=enc) as f:
                lector = list(csv.reader(f))
                break
        except:
            continue
    
    if not lector:
        print("Error: No se pudo leer el archivo con ninguna codificación.")
        sys.exit(1)

    encabezados = lector[0]
    filas = lector[1:]
    perfiles = []

    for i, nombre in enumerate(encabezados):
        valores = [fila[i] if i < len(fila) else "" for fila in filas]
        
        total = len(valores)
        nulos = sum(1 for v in valores if es_valor_nulo(v))
        validos = [v for v in valores if not es_valor_nulo(v)]
        unicos = len(set(validos))
        
        perfiles.append({
            "nombre_columna": nombre,
            "tipo_inferido": inferir_tipo(valores),
            "total_registros": total,
            "valores_nulos": nulos,
            "porcentaje_nulos": f"{(nulos/total)*100:.2f}" if total > 0 else "0.00",
            "valores_unicos": unicos,
            "porcentaje_unicos": f"{(unicos/total)*100:.2f}" if total > 0 else "0.00",
            "ejemplo_valor": validos[0] if validos else ""
        })

    with open(args.output, 'w', encoding='utf-8', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=perfiles[0].keys())
        escritor.writeheader()
        escritor.writerows(perfiles)
    
    print(f"Reporte generado en: {args.output}")

if __name__ == "__main__":
    main()