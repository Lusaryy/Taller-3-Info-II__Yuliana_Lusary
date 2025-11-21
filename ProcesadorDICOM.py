import os
import pydicom
import pandas as pd
import numpy as np

class ProcesadorDICOM:
    def __init__(self, carpeta):
        self.carpeta = carpeta
        self.archivos = []
        self.dicom_objs = []
        self.dataframe = None


    def cargar_archivos(self):
        for root, dirs, files in os.walk(self.carpeta):
            for f in files:
                ruta = os.path.join(root, f)
                try:
                    dicom_obj = pydicom.dcmread(ruta)
                    self.archivos.append(ruta)
                    self.dicom_objs.append(dicom_obj)
                except Exception:
                    # Si no es dcm válido lo ignoramos
                    continue

        print(f"Archivos DICOM cargados: {len(self.dicom_objs)}\n")


    def extraer_metadatos(self):
        datos = []

        for obj, ruta in zip(self.dicom_objs, self.archivos):
            # En caso de que falten tags
            def safe_get(tag):
                return getattr(obj, tag, None)

            info = {
                "ID del paciente": safe_get("PatientID"),
                "Nombre del paciente": str(safe_get("PatientName")) if safe_get("PatientName") is not None else None,
                "ID único del estudio": safe_get("StudyInstanceUID"),
                "Descripción del estudio": safe_get("StudyDescription"),
                "Fecha del estudio": safe_get("StudyDate"),
                "Modalidad de la imagen": safe_get("Modality"),
                "Filas": safe_get("Rows"),
                "Columnas": safe_get("Columns")
            }

            datos.append(info)

        return datos


    def crear_dataframe(self):
        metadatos = self.extraer_metadatos()
        self.dataframe = pd.DataFrame(metadatos)

        orden = [
    "ID del paciente", "Nombre del paciente", "ID único del estudio",
    "Fecha del estudio", "Descripción del estudio", "Modalidad de la imagen",
    "Filas", "Columnas"]

        self.dataframe = self.dataframe[orden]
        return self.dataframe


    def calcular_intensidad_promedio(self):

        if self.dataframe is None:
            raise ValueError("~ Error. Inténtalo de nuevo ~")

        intensidades = []

        for obj in self.dicom_objs:
            try:
                arr = obj.pixel_array.astype(np.float32)
                intens_prom = np.mean(arr)
            except Exception:
                intens_prom = None   # Si el archivo no tiene pixel array

            intensidades.append(intens_prom)

        self.dataframe["IntensidadPromedio"] = intensidades
        return self.dataframe

if __name__=="__main__":

    RUTA_DICOM = input("Ingresa la ruta de la carpeta con archivos DICOM o enter para usar predeterminada: ").strip ()

    if not RUTA_DICOM:
        RUTA_DICOM ="./data"
        print(f"No se Ingreso ruta. usando ruta por defecto {RUTA_DICOM}\n")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 120)
    pd.set_option('display.colheader_justify', 'center')

    try:
        procesador = ProcesadorDICOM(RUTA_DICOM)


        procesador.cargar_archivos()
        procesador.crear_dataframe()
        procesador.calcular_intensidad_promedio()
        print("Resultados del procesamiento")
        print(procesador.dataframe)

    except FileNotFoundError as e:
        print(f"Error:{e}")
        print("Por favor, verifica la ruta de la carpeta DICOM")

    except Exception as e:
        print(f"Error inesperado:{e}")

