import os
import pickle,gzip
import urllib.request
import numpy as np
import tarfile
import time
from tqdm import tqdm
from scipy.io.wavfile import read as wav_read


class speech_commands:
    """speech commands classification

    source: https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html

    The dataset has 65,000 one-second long utterances of 30 short
    words, by thousands of different people, contributed by
    members of the public through the AIY website. It’s released
    under a Creative Commons BY 4.0 license, and will continue to
    grow in future releases as more contributions are received.
    The dataset is designed to let you build basic but useful
    voice interfaces for applications, with common words like
    “Yes”, “No”, digits, and directions included. The
    infrastructure we used to create the data has been open
    sourced too, and we hope to see it used by the wider community
    to create their own versions, especially to cover underserved
    languages and applications.

    """

    name2class = {'blues':0, 'classical':1, 'country': 2,
                  'disco': 3, 'hiphop': 4, 'jazz': 5, 'metal': 6,
                  'pop': 7, 'reggae': 8, 'rock': 9}
 
    def download(path=None):
        if path is None:
            path = os.environ['DATASET_path']
        path += 'speech_commands/'
        t0 = time.time()
    
        print('Downloading speech commands')
    
        # Check if directory exists
        if not os.path.isdir(path):
            print('\tCreating Directory')
            os.mkdir(path)
    
        # Check if file exists
        if not os.path.exists(path + 'speech_commands_v0.01.tar.gz'):
            url = 'http://download.tensorflow.org/data/speech_commands_v0.01.tar.gz'
            urllib.request.urlretrieve(url, path + 'speech_commands_v0.01.tar.gz')
    
    
    def load(path=None):
    
        if path is None:
            path = os.environ['DATASET_PATH']
        speech_commands.download(path)
    
        t0 = time.time()
    
        print('Loading speech command')
    
        tar = tarfile.open(path+'speech_commands/speech_commands_v0.01.tar.gz', 'r:gz')
    
        # Load train set
        wavs = list()
        labels = list()
        noises = list()
        noise_labels = list()
        names = tar.getmembers()
        for name in tqdm(names, ascii=True):
            if 'wav' not in name.name:
                continue
            f = tar.extractfile(name.name)#.read()
            wav = wav_read(f)[1]
            if 'noise' in name.name:
                noises.append(wav)
                noise_labels.append(name.name.split('/')[-1])
            else:
                left = 16000 - len(wav)
                to_pad = left // 2
                wavs.append(np.pad(wav, [[to_pad, left - to_pad]]))
                labels.append(name.name.split('/')[-2])
        labels = np.array(labels)
        unique_labels = np.unique(labels)
        y = np.squeeze(np.array([np.nonzero(label == unique_labels)[0]
                        for label in labels]).astype('int32'))
    
        print('Dataset speech commands loaded in{0:.2f}s.'.format(time.time()-t0))
    
        return np.array(wavs).astype('float32'), y, labels, noises, noise_labels