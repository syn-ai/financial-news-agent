#!/bin/bash

pip install torch torchaudio torchvision numpy git+https://github.com/huggingface/transformers git+https://github.com/huggingface/datasets beautifulsoup4 requests
pip install sentencepiece
sudo apt-get install cmake build-essential pkg-config libgoogle-perftools-dev

sudo rm /usr/lib/wsl/lib/libcuda.so.1
ln -s /sbin/ldconfig.real /usr/lib/wsl/lib/libcuda.so.1

git clone https://github.com/google/sentencepiece.git 
cd sentencepiece
mkdir build
cd build
cmake ..
make -j $(nproc)
sudo make install
sudo ldconfig -v
cd ../python
python setup.py bdist_wheel

 sudo apt install python3-sentencepiece libsentencepiece-dev sentencepiece