####### EJEMPLO3 #######
#########################

#Primero se filtrará la señal
#Para luego rechazar las épocas atípicas empleando solo el rechazo de valores extremos y la regresión lineal
#Primero importamos la librería
from Analysis_Signal import * 

#Llamamos la librería
ex3=signal_treatment()
#Cargamos el archivo donde se encuentran los datos de la señal con su función load_file
unfiltered_data=ex3.load_file("P1_RAWEEG_2018-11-15_OjosCerrados_2min.txt")

#Ahora los datos de la señal han quedado guardados en data y se utilizan para graficar
#La frecuencia de muestrepo es de 250
#También se gráfica el periodograma de Welch para evidenciar en que frecuencias de la señal se encuentra ruido
ex3.unfiltered_signal_graphics(unfiltered_data,250)
ex3.welch_periodogram(unfiltered_data,250)

#Ahora que se ha visualizado la señal, se filtra y se gráfica nuevamente junto con el periodograma
data_filter=ex3.signal_filtering(unfiltered_data,250)
ex3.filtered_signal_graphics(data_filter,250)
ex3.welch_periodogram(data_filter,250)

#Se procede a segmentar la señal y se gráfica uno de estos segmentos
segment_data,segment_time=ex3.signal_segmentation(data_filter,250,2)
ex3.segmentation_graph(segment_data,segment_time, 10, 250)

#Teniendo segmentada la señal, se aplican las funciones para detección de épocas atípicas
#Primero se eliminan los valores por encima del umbral seleccionado
analysis_data=ex3.extreme_values(segment_data,-75,75)

#En segundo lugar se realiza la regresión lineal con los datos obtenido anteriormente
analysis_data2=ex3.linear_trends(analysis_data,segment_time,-5,5)

#Finalment, eliminando las épocas atípicas se procede a graficar la señal nuevamente completa junto con su periodograma
signal=ex3.signal_union(analysis_data2,250)
ex3.filtered_signal_graphics(signal, 250)
ex3.final_welch_periodogram(signal, 250,1)