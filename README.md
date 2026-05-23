# Reto Semana 5 - Perfilador de Datasets

Programación para Ciencia de Datos | IPN 2026
Alumno: Rodriguez Anduiza David Emiliano
Profesor: Mario Augusto Ramirez

## Perfilador de Datos Automatizado

Proyecto: 

## Reto Semana 5 | Programación para Ciencia de Datos | IPN 2026

## Descripción del Proyecto
Esta herramienta permite el diagnóstico rápido de archivos CSV mediante una interfaz de línea de 
comandos. 

El programa analiza automáticamente la estructura de los datos, detectando tipos, niveles de integridad y patrones de unicidad sin necesidad de librerías externas.

## Requisitos del Entorno
Lenguaje: Python 3.8+

Dependencias: Este desarrollo se construyó utilizando exclusivamente la biblioteca estándar de Python para garantizar máxima portabilidad y rapidez de ejecución.

## Instalación

Para poner en marcha el perfilador, ejecuta los siguientes comandos en tu terminal:
Bash# Descarga del repositorio
git clone https://github.com/emi-roan/Reto_semana_06_David_Emiliano_Rodriguez.git
cd Reto_semana_06_David_Emiliano_Rodriguez

# Configuración del entorno virtual
python -m venv .venv
# Activación
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalación de dependencias (archivo vacío según requerimiento)
pip install -r requirements.txt
Modo de Uso
El programa requiere la definición de un archivo de entrada y una ruta de salida para el reporte:
Bash
python main.py --input <archivo_fuente.csv> --output <archivo_reporte.csv>
Bandera
Propósito--input / -i

Especifica el archivo origen a perfilar.--output / -o
Especifica la ruta de destino donde se guardará el CSV con el resumen de calidad.

## Arquitectura del Proyecto
Plaintext/
├── main.py              # Lógica central de procesamiento
├── README.md            # Documentación técnica
├── requirements.txt     # Listado de dependencias
├── .gitignore           # Archivos ignorados por Git
├── data/                # Carpeta de carga (CSV de prueba)
└── outputs/             # Carpeta de reportes generados

## Ejemplo
## Entrada (data/ventas.csv):

fecha,producto,cantidad,precio,vendedor

2026-01-01,Laptop,2,15000.00,Ana

2026-01-02,Mouse,10,250.00,Bob

2026-01-03,Teclado,,800.00,Ana

2026-01-04,Monitor,3,,Carlos

2026-01-05,Laptop,1,15000.00,

Comando:

python3 main.py --input data/ventas.csv --output outputs/perfil_ventas_final.csv

## Salida (outputs/perfil_ventas_final.csv):

nombre_columna,tipo_inferido,total_registros,valores_nulos,porcentaje_nulos,valores_unicos,porcentaje_unicos,ejemplo_valor

fecha,fecha,5,0,0.00,5,100.00,2026-01-01

producto,texto,5,0,0.00,4,80.00,Laptop

cantidad,numerico,5,1,20.00,4,80.00,2

precio,numerico,5,1,20.00,3,60.00,15000.00

vendedor,texto,5,1,20.00,3,60.00,Ana

Reglas de procesamiento

Detección de nulos

Se considera nulo: celda vacía (,,), celda con solo espacios, None.

NO son nulos: 0, "0", "null", "None" (texto literal).


Lógica de Validación (Reglas de Negocio)
1. Detección de Nulidad
Se aplica una lógica estricta para identificar datos faltantes:
Se marcan como nulos: Celdas vacías (,,), cadenas con espacios en blanco y el tipo None.
Se preservan como valores válidos: El número 0, la cadena "0", y los literales "null" o "None".

2. Inferencia de Tipos
El motor de perfilado clasifica las columnas basándose en una cobertura del 80% de los datos no nulos bajo el siguiente orden de prioridad:
Fecha: Formato YYYY-MM-DD (rango 1900-2100).
Booleano: Representaciones como true/false, yes/no, 1/0 o t/f.
Numérico: Valores convertibles a float.
Texto: Clasificación por defecto si no se cumplen las condiciones anteriores.

3. Métricas de Unicidad
Los valores únicos se calculan omitiendo los nulos detectados, garantizando la distinción entre mayúsculas y minúsculas (ej. Ana ≠ ana).
