####### EJEMPLO 1 #######
#########################

#En este caso se utilizan todas las funciones de la librería en orden y se observa el comportamiento de la señal 

#Primero importamos la librería
from Analysis_Signal import * 

#Llamamos la librería
ex1=signal_treatment()
#Cargamos el archivo donde se encuentran los datos de la señal con su función load_file
unfiltered_data=ex1.load_file("P1_RAWEEG_2018-11-15_Electrobisturí1_3min.txt")

#Ahora los datos de la señal han quedado guardados en data y se utilizan para graficar
#La frecuencia de muestrepo es de 250
#También se gráfica el periodograma de Welch para evidenciar en que frecuencias de la señal se encuentra ruido
ex1.unfiltered_signal_graphics(unfiltered_data,250)
ex1.welch_periodogram(unfiltered_data,250)

#Ahora que se ha visualizado la señal, se filtra y se gráfica nuevamente junto con el periodograma
data_filter=ex1.signal_filtering(unfiltered_data,250)
ex1.filtered_signal_graphics(data_filter,250)
ex1.welch_periodogram(data_filter,250)

#Se procede a segmentar la señal y se gráfica uno de estos segmentos
segment_data,segment_time=ex1.signal_segmentation(data_filter,250,2)
ex1.segmentation_graph(segment_data,segment_time, 10, 250)

#Teniendo segmentada la señal, se aplican las funciones para detección de épocas atípicas
#Primero se eliminan los valores por encima del umbral seleccionado
analysis_data=ex1.extreme_values(segment_data,-75,75)

#En segundo lugar se realiza la regresión lineal con los datos obtenido anteriormente
analysis_data2=ex1.linear_trends(analysis_data,segment_time,-5,5)

#En tercer lugar, se implementa con los datos anteriores la curtosis
analysis_data3=ex1.kurtosis(analysis_data2,-3,3)

#Por último se evalúan las frecuencias con el periodograma de welch en la función spectral_pattern
analysis_data4=ex1.spectral_pattern(analysis_data3,-100,100)

#Al haber eliminado épocas atípicas se procede a graficar la señal nuevamente completa junto con su periodograma
signal=ex1.signal_union(analysis_data4,250)
ex1.filtered_signal_graphics(signal, 250)
ex1.final_welch_periodogram(signal, 250,1)
