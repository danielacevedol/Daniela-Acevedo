####### EJEMPLO2 #######
#########################

#En este caso se rechazan las épocas atípicas empleando solo curtosis y el espectro de frecuencias, después de filtrar la señal 

#Primero importamos la librería
from Analysis_Signal import * 

#Llamamos la librería
ex2=signal_treatment()
#Cargamos el archivo donde se encuentran los datos de la señal con su función load_file
unfiltered_data=ex2.load_file("P1_RAWEEG_2018-11-15_Electrobisturí2_2min.txt")

#Ahora los datos de la señal han quedado guardados en data y se utilizan para graficar
#La frecuencia de muestrepo es de 250
#También se gráfica el periodograma de Welch para evidenciar en que frecuencias de la señal se encuentra ruido
ex2.unfiltered_signal_graphics(unfiltered_data,250)
ex2.welch_periodogram(unfiltered_data,250)

#Ahora que se ha visualizado la señal, se filtra y se gráfica nuevamente junto con el periodograma
data_filter=ex2.signal_filtering(unfiltered_data,250)
ex2.filtered_signal_graphics(data_filter,250)
ex2.welch_periodogram(data_filter,250)

#Se procede a segmentar la señal y se gráfica uno de estos segmentos
segment_data,segment_time=ex2.signal_segmentation(data_filter,250,2)
ex2.segmentation_graph(segment_data,segment_time, 10, 250)

#En primer lugar, se implementa con los datos anteriores la curtosis
analysis_data1=ex2.kurtosis(segment_data,-3,3)

#En segundo lugar se evalúan las frecuencias con el periodograma de welch en la función spectral_pattern
analysis_data2=ex2.spectral_pattern(analysis_data1,-100,100)

#Finalment, eliminando las épocas atípicas se procede a graficar la señal nuevamente completa junto con su periodograma
signal=ex2.signal_union(analysis_data2,250)
ex2.filtered_signal_graphics(signal, 250)
ex2.final_welch_periodogram(signal, 250,1)
