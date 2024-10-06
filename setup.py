from setuptools import setup, find_packages

setup(name="beatCraftSdk",
      version="0.0.1",
      author="Arul and friends",
      author_email="arif.akbarul@amikom.ac.id",
      description="while you are focus on the game logic, "
                  "BeatCraft help you to make an authentic music for your game",
      url="",
      packages=find_packages(),
      install_requires=[
        'click',
        'MIDIUtil',
        'pyo',
        'pygame',
        'numpy==1.26.4',
        'sounddevice',
        'mido',
        'python-rtmidi',
        'pretty_midi',
        'torch==2.1.0',
        'torchaudio==2.1.0',
        'torchtext==0.16.0',
        'torchvision==0.16.0',
        'transformers==4.45.1',
        'xformers==0.0.22.post7',
        'audiocraft==1.3.0',
        'midi2audio',
        'librosa'
      ],
      classifiers=[
          "Programming language :: Python :: 3"
          "License :: OSI Approved :: MIT License"
      ],
      python_requires=">=3.6")