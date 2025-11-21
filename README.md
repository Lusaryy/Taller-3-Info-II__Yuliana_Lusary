
# Procesador de Archivos DICOM

# Informática 2: Unidad 3 – Taller Evaluativo
# Integrantes:
      Yuliana Salcedo Salgado
      Lusary Suarez Guillen




# 4.5. INFORME Y DISCUSIÓN

**1. Descripción del proyecto**

Este proyecto consiste en desarrollar una aplicación en Python capaz de leer, extraer, organizar y analizar metadatos de archivos DICOM, utilizando librerías de software libre como pydicom, numpy y pandas.
La idea es simular una parte del flujo real de un sistema PACS, automatizando la carga de archivos, la obtención de información relevante del estudio (como paciente, modalidad, fecha, tamaño de la imagen, etc.) y un análisis sencillo de intensidad promedio de los píxeles.
Todo el código está estructurado en programación orientada a objetos para mantener la lógica clara y modular.

# Requisitos:
  - Python 3.7 o superior
  - Librerias necesarias:
    - pydicom
    - pandas
    - numpy

# Instalación:
- Clonar el repositorio:
git clone https://github.com/Lusaryy/Taller-3-Info-II__Yuliana_Lusary.git
cd TU_REPOSITORIO

- Crear entorno virtual:
python -m venv venv

  Activación:
  - En Windows:
    venv\Scripts\activate
  - En Linux/Mac:
    source venv/bin/activate

- Intalar dependencias:
pip install pydicom numpy pandas

# Uso:
Ejecutara el programa principal:
python ProcesadorDICOM.py

El programa solicitará la ruta de la carpeta con archivos DICOM.
Si no se ingresa ninguna ruta, utilizará la carpeta predeterminada ./data.

Ejemplo de ejecución:
Ingresa la ruta de la carpeta con archivos DICOM o enter para usar predeterminada:
No se ingresó ruta. Usando ruta por defecto ./data
Archivos DICOM cargados: 15

Resultados del procesamiento:
[Tabla de metadatos...]

# Funcionalidades principales:

La clase ProcesadorDICOM implementa:

- cargar_archivos()
Escanea el directorio y carga todos los archivos DICOM válidos.

- extraer_metadatos()
Obtiene tags del estándar DICOM:
  - ID del paciente
  - Nombre
  - StudyInstanceUID
  - Descripción del estudio
  - Fecha
  - Modalidad
  - Filas y columnas
    Maneja archivos anonimizados o tags ausentes.

- crear_dataframe()
Organiza los metadatos en un DataFrame de Pandas.

- calcular_intensidad_promedio()
Calcula intensidad promedio usando pixel_array y numpy.

**2. Explica brevemente por qué DICOM y HL7 son cruciales para la interoperabilidad en salud y en qué se diferencian conceptualmente.**

En informática médica, la interoperabilidad no es algo insignificante, sino que es lo que permite que hospitales, modalidades de imagen, sistemas administrativos y aplicaciones clínicas puedan comunicarse sin depender del fabricante.
DICOM se encarga del mundo de las imágenes médicas. Define:
  - Cómo se guarda la imagen
  - Cómo se estructuran los metadatos
  - Cómo se envían los estudios entre dispositivos (modalidades, PACS, workstations)

HL7, por otro lado, se enfoca en la información clínica y administrativa: datos del paciente, órdenes médicas, resultados de laboratorio, historia clínica, etc.
Aunque son estándares distintos, se complementan. Gracias a ellos un estudio puede viajar desde un tomógrafo hasta un PACS, y luego a una estación de trabajo, sin que nada se “pierda” o quede incompatible.


**3. Pregunta teórica: ¿Qué relevancia clínica o de pre-procesamiento podría tener el análisis de de la distribucion de intensidades en una imágen médica?**

Analizar la distribución de intensidades en una imagen médica es más importante de lo que parece. A nivel clínico y de preprocesamiento permite:
- Evaluar la calidad del estudio (por ejemplo, detectar imágenes demasiado oscuras o saturadas)
- Identificar patrones generales de tejido, ya que diferentes intensidades pueden corresponder a densidades o características específicas
- Normalizar o estandarizar imágenes antes de aplicar algoritmos de segmentación, filtrado o aprendizaje automático
- Detectar artefactos o valores atípicos que podrían afectar el diagnóstico o el procesamiento posterior

Incluso un cálculo tan básico como la intensidad promedio ya puede orientar si la imagen está dentro de rangos normales o si tiene problemas de adquisición.


**4. Mencionar dificultades encontradas y la importancia de las herramientas de Python para el analisis de datos médicos.**
Dificultades en el taller:
- Tags DICOM ausentes o anonimizados, lo que nos obligó a manejar excepciones para evitar que el programa falle
- Advertencias del estándar DICOM, especialmente con valores inválidos del tipo UI, que ocupaban mucho espacio en el output
- Variabilidad entre estudios, ya que no todos los archivos contienen los mismos metadatos o estructuras internas
- Carga de múltiples archivos, que requiere recorrer directorios completos y manejar errores de lectura

Las herramientas de Python que facilitan bastante este trabajo:
- Pydicom permite leer el contenido de un archivo DICOM como si fuera un objeto de Python, acceder a los tags y manejarlos sin convertirlos manualmente
- Numpy hace posible procesar los valores de píxeles con velocidad y precisión
- Pandas organiza los metadatos en un DataFrame, lo cual vuelve el análisis y la consulta muchísimo más prácticos


