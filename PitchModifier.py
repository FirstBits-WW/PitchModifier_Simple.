import pyaudio
import numpy as np

def pitch_shift(samples, pitch_factor):
    """Muda o Pitch do sinal por um determinado fator."""
    n_samples = len(samples)
    n_samples_shifted = int(n_samples / pitch_factor)
    
    # Usa Interpolação linear para Reamostrar o sinal
    indices = np.arange(n_samples_shifted) * pitch_factor
    indices = indices.astype('int32')
    resampled = np.interp(indices, np.arange(n_samples), samples).astype('float32')
    
    #Preencher ou truncar o sinal reamostrado conforme necessário
    if n_samples_shifted > n_samples:
        resampled = resampled[:n_samples]
    else:
        resampled = np.pad(resampled, (0, n_samples - n_samples_shifted), 'constant')
    
    return resampled

# Inicializar o PyAudio
p = pyaudio.PyAudio()

# Abre a Entrada de aúdio Padrão
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

# Abre a saída de aúdio Padrão
stream_out = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

# Faz um loop na entrada de áudio, mude o Pitch e emite o áudio
while True:
    # Lê o buffer de entrada de áudio
    buffer = stream.read(1024)
    
    # Converte buffer em array NumPy
    samples = np.frombuffer(buffer, dtype='float32')
    
    # Muda o Pitch do áudio
    shifted = pitch_shift(samples, 44100, 1.2)
    
    # Converte a matriz NumPy de volta ao buffer
    buffer_out = shifted.tobytes()
    
    # Envia o buffer para a saída de áudio
    stream_out.write(buffer_out)