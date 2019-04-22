import numpy as np
import matplotlib.pyplot as plt;
import scipy.signal as signal
import LinearFIR
from scipy.stats import kurtosis

#Daniela Acevedo León 1.115.089651
#Melissa Echarría Guarín 1.152.710.589
#Trabajo final señales

class signal_treatment: 
    
    def __init__(self,parent=None):
        self.Signal_Data=[]
        self.Filtered_Signal=[]
        self.Segment_Data=[]
        self.Segment_Time=[]
        self.Total_Data=[]
        self.Adjust=[]
        self.Kurtosis_Data=[]
        self.Espectral_Differences=[]
        self.Final_Signal=[]
        self.Final_Time=[]
        
    #Extrae los canales de la señal EEG            
    def load_file(self,File):
        self.Signal_Data=np.loadtxt(File, delimiter=',', skiprows=6, usecols=[1,2,3,4,5,6,7,8])
        return self.Signal_Data
    
    #Filtrado de la señal utilizando LinearFIR    
    def signal_filtering(self,Signal_Data,Fs):
        self.Filtered_Signal=LinearFIR.eegfiltnew(Signal_Data,Fs,1,50,0,0);
        return self.Filtered_Signal
    
    #Grafica los canales de la señal sin filtrar     
    def unfiltered_signal_graphics(self,Signal_Data,Fs):
        Time_Vector=np.arange(0,len(Signal_Data)/Fs,1/Fs)
        #Ciclo for que recorre los 8 canales y grafica cada uno
        for x in range (0,8):
            Channel=Signal_Data[:,x]
            plt.plot(Time_Vector, Channel)
        
        plt.title("Unfiltered signals for all channels")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude [µV]")
        plt.show()
        plt.grid()
    
    #Grafica los canales de la señal filtrada y agrega un nivel DC para visualizar mejor la señal    
    def filtered_signal_graphics(self,Signal_Data,Fs):
        Time_Vector=np.arange(0,len(Signal_Data)/Fs,1/Fs)
        DC_Vector=[0,200,400,600,800,900,1000,1200]
        #Ciclo for que recorre los 8 canales y grafica cada uno
        for x in range (0,8):
            Channel=Signal_Data[:,x]
            plt.plot(Time_Vector, Channel+DC_Vector[x])
        
        plt.title("Filtered signals for all channels")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude [µV]")
        plt.show()
        plt.grid()
    
    #Calcula y grafica la densidad espectral de potencia a las señales de cada canal y agrega un nivel DC    
    def welch_periodogram(self,Signal_Data,Fs):
        DC_Vector=[0,10,20,30,40,50,60,70]
        #Ciclo for que recorre los 8 canales y grafica cada uno
        for x in range (0,8):
            Channel=Signal_Data[:,x]
            Frequency, Power_Density = signal.welch(Channel, 250)
            plt.plot(Frequency, np.sqrt(Power_Density)+DC_Vector[x])
        
        plt.title('Welch Periodogram')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Spectral power density [V**2/Hz]')
        plt.grid()
        plt.show()
    
    #Función encargada de segmentar la señal  
    def signal_segmentation(self,Signal_Data,Fs,Epochs_Time):
        size=Signal_Data.shape
        #Cálculo del módulo del total de muestras
        Module=size[0]%(Fs*Epochs_Time)
        Data_Time=size[0]/Fs
        #Segmentación de la señal
        #Se resta el módulo a la señal para evitar que la división de la muestras totales sobre las épocas
        #sea un npumero inexactp
        self.Segment_Data=np.split(Signal_Data[0:size[0]-Module,:],int(Data_Time//Epochs_Time))
        self.Segment_Data=np.array(self.Segment_Data)
        #Segmentación del vector de tiempo 
        Time_Vector=np.arange(0,len(Signal_Data)/Fs,1/Fs)
        self.Segment_Time=np.split(Time_Vector[0:(size[0]-Module)],int(Data_Time//Epochs_Time))
        self.Segment_Time=np.array(self.Segment_Time)
        #Devuelve un vector de datos segmentados y otro de tiempo
        return self.Segment_Data,self.Segment_Time
    
    #Grafica la época que el usuario desee
    def segmentation_graph(self,Signal_Data,Segment_time,Epoch,Fs):
        DC_Vector=[0,200,400,600,800,900,1000,1200]
        Epoch_Data=Signal_Data[Epoch,:,:]
        Time_Vector=Segment_time[Epoch,:]
        for x in range (0,8):
            Channel=Epoch_Data[:,x]
            plt.plot(Time_Vector, Channel+DC_Vector[x])
        
        plt.title("Channel epoch")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude [µV]")
        plt.show()
        plt.grid()
        
    #Método de los valores extremos     
    def extreme_values(self,Signal_Data,Minimun_Value,Maximun_Value):
        size=Signal_Data.shape
        self.Total_Data=[]
        #Genera una matriz de unos para realizar la comparación
        Ones_Array=np.ones(size[0])
        
        for x in range (0,size[2]):
            Segment_Data=Signal_Data[:,:,x]
            Ext_Val_Data=[]
            for i in range (0,size[0]):
                Temporal_Data=Segment_Data[i,:]
                #Condición que verifica que el valor máximo de la época esté dentro del umbral
                if Temporal_Data.max() >= Maximun_Value:
                    #Si la condición es cierta agrega un cero a la matriz de unos en esa posición
                    Ones_Array[i]=0
                #Condición que verifica que el valor mínimo de la época esté dentro del umbral    
                if Temporal_Data.min() <= Minimun_Value:
                    #Si la condición es cierta agrega un cero a la matriz de unos en esa posición
                    Ones_Array[i]=0
        
        #Devuelve una matriz con las épocas que no fueron rechazadas
        #Sobreescribe en la matriz solo los datos del canal que corresponden a los índices que tienen un 1 en la matriz de unos.
        self.Total_Data=Signal_Data[Ones_Array==1,:,:]
        return self.Total_Data      
    
    #Método de tendencias lineales, calcula un ajuste a la señal EEG y compara con un umbral dado
    def linear_trends (self,Signal_Data,Segment_Time,Minimun_Value,Maximun_Value):
        size=Signal_Data.shape
        Ones_Array=np.ones(size[0])
        self.Adjust=[]
        
        #Este ciclo es similar al de la función anterior, solo cambian los datos que recibe 
        for x in range (0,size[2]):
            channel=Signal_Data[:,:,x]           
            for y in range(0,size[0]):
                #Con el comando polyfit se calcula el valor de pendiente 
                #Las datos son almacenados en una nueva matriz y comparados con el umbral que da el usuario
                m=np.polyfit(Segment_Time[y,:],channel[y,:],1)
                if m[0]>=Maximun_Value:
                    Ones_Array[y]=0
                if m[0]<=Minimun_Value:
                    Ones_Array[y]=0
        
        #Devuelve una matriz con las épocas que no fueron rechazadas
        self.Adjust=Signal_Data[Ones_Array==1,:,:]
        return self.Adjust
    
    #Función con el método de improbabilidad calculando la curtosis de los datos                  
    def kurtosis(self,Signal_Data,Minimun_Value,Maximun_Value):
        size=Signal_Data.shape
        Ones_Array=np.ones(size[0])
        #calcula la curtosis para cada época en cada canal
        Apply_Kurtosis=kurtosis(Signal_Data,axis=1)
        self.Kurtosis_Data=[]
        
        #Comparación de los datos obtenidos de la curtosis con el umbral
        for x in range (0,8):
            Channel=Apply_Kurtosis[:,x]
            for y in range (0,len(Channel)):
                Temporal_Data=Channel[y]
                if Temporal_Data>=Maximun_Value:
                    Ones_Array[y]=0
                if Temporal_Data<=Minimun_Value:
                    Ones_Array[y]=0
                    
        #Devuelve una matriz con las épocas que no fueron rechazadas
        self.Kurtosis_Data=Signal_Data[Ones_Array==1,:,:] 
        return self.Kurtosis_Data 
    
    #Método del patrón de espectro 
    def spectral_pattern(self,Signal_Data,Minimun_Value,Maximun_Value):
        size=Signal_Data.shape
        self.Espectral_Differences=[]
        Ones_Array=np.ones(size[0])
        
        for i in range (0,size[2]):
            Channel=Signal_Data[:,:,i]
            for j in range (0,size[0]):
                Segment=Channel[j,:]
                #Calcula a la densidad de potencia a cada época con el método de welch
                Frequency, Power_Density = signal.welch(Segment, 250)
                #Calcula la media de los resultados de la densidad de potencia
                Medium_Power= np.mean(Power_Density)
                #Resta los resultados de la densidad de potencia con los de la media
                Resulting_Power=Power_Density-Medium_Power
                #Realiza la comparación con el umbral
                if Resulting_Power.max()>=Maximun_Value:
                    Ones_Array[j]=0
                if Resulting_Power.min()<=Minimun_Value:
                    Ones_Array[j]=0
                    
        #Devuelve una matriz con las épocas que no fueron rechazadas
        self.Espectral_Differences=Signal_Data[Ones_Array==1,:,:]
        return self.Espectral_Differences
    
    #Une todos los segmentos después de procesar la señal para convertirlos en único canal nuevamente 
    def signal_union(self,Signal_Data,Fs):
        size=Signal_Data.shape
        self.Final_Signal=np.empty((size[0]*size[1],size[2]))
        
        for i in range (0,size[2]):
            self.Final_Signal[:,i]=np.ravel(Signal_Data[:,:,i])
            
        return self.Final_Signal
    
    #Calcula nuevamente la densidad de potencia a la señal procesada
    def final_welch_periodogram(self,Signal_Data,Fs,Channel):
        Channel_Data=Signal_Data[:,Channel]
        Frequency, Power_Density = signal.welch(Channel_Data, 250)
        
        plt.plot(Frequency[0:50], np.sqrt(Power_Density[0:50]))
        plt.title('Welch periodogram for the processed signal')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Spectral power density  [V**2/Hz]')
        plt.grid()
        plt.show()

