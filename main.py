#!/usr/bin/env python3
"""
Perfilador de Datasets CSV
Analiza cualquier archivo CSV y genera un reporte de calidad de datos.
"""
import argparse
import sys
import csv

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
        try:
            partes = v[:10].split('-')
            año, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
            return 1900 <= año <= 2100 and 1 <= mes <= 12 and 1 <= dia <= 31
        except (ValueError, IndexError):
            pass
    return False

def es_booleano(valor):
    v = str(valor).strip().lower()
    return v in ['true', 'false', 'yes', 'no', 'si', '1', '0', 't', 'f']

def inferir_tipo(valores):
    valores_validos = [v for v in valores if not es_valor_nulo(v)]
    if not valores_validos: return "texto"
    
    total = len(valores_validos)
    umbral = 0.8
    num_fechas = sum(1 for v in valores_validos if es_fecha(v))
    num_booleanos = sum(1 for v in valores_validos if es_booleano(v))
    num_numericos = sum(1 for v in valores_validos if es_numerico(v))
    
    if num_fechas / total >= umbral: return "fecha"
    elif num_booleanos / total >= umbral: return "booleano"
    elif num_numericos / total >= umbral: return "numerico"
    else: return "texto"

def perfilar_columna(nombre, valores):
    total = len(valores)
    nulos = sum(1 for v in valores if es_valor_nulo(v))
    valores_no_nulos = [v for v in valores if not es_valor_nulo(v)]
    unicos = len(set(valores_no_nulos))
    ejemplo = valores_no_nulos[0] if valores_no_nulos else ""
    
    return {
        "nombre_columna": nombre,
        "tipo_inferido": inferir_tipo(valores),
        "total_registros": total,
        "valores_nulos": nulos,
        "porcentaje_nulos": round(nulos / total * 100, 2) if total > 0 else 0.00,
        "valores_unicos": unicos,
        "porcentaje_unicos": round(unicos / total * 100, 2) if total > 0 else 0.00,
        "ejemplo_valor": ejemplo
    }

def leer_csv(ruta):
    # Usamos utf-8-sig para evitar el error de bytes 0xff al inicio del archivo
    with open(ruta, 'r', encoding='utf-8-sig') as f:
        lector = list(csv.reader(f))
        if not lector: return [], []
        return lector[0], lector[1:]

def escribir_csv(ruta, perfiles):
    columnas = ["nombre_columna", "tipo_inferido", "total_registros", "valores_nulos", 
                "porcentaje_nulos", "valores_unicos", "porcentaje_unicos", "ejemplo_valor"]
    with open(ruta, 'w', encoding='utf-8', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(perfiles)

def main():
    parser = argparse.ArgumentParser(description="Perfilador de Datasets CSV")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    try:
        encabezados, filas = leer_csv(args.input)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {args.input}")
        sys.exit(1)

    perfiles = [perfilar_columna(nombre, [fila[i] if i < len(fila) else "" for fila in filas]) 
                for i, nombre in enumerate(encabezados)]
    
    escribir_csv(args.output, perfiles)
    print(f"Completado! Perfil guardado en: {args.output}")

if __name__ == "__main__":
    main()