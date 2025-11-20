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


procesador = ProcesadorDICOM(" ")
procesador.cargar_archivos()
procesador.crear_dataframe()
procesador.calcular_intensidad_promedio()
print(procesador.dataframe)
