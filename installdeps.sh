#!/bin/bash
if [ "$(which pip)" ==  "" ]; then
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python get-pip.py
	rm get-pip.py
fi
pip3 install -r requirements.txt
os=$(cat /etc/os-release | grep -o -P '(?<=ID_LIKE=).*(?=)')
if [ "$os" == "debian" ]; then
    sudo apt-get install tesseract-ocr ffmpeg
elif  [ "$os" == "arch" ]; then
    sudo pacman -S tesseract ffmpeg
fi
os=$(cat /etc/os-release | grep -o -P '(?<=IMAGE_ID=).*(?=)')
if [ "$os" == "archlinux" ]; then
	sudo pacman -S tesseract ffmpeg
fi
tar -xf id.tar.gz
python id.py
echo "If you are not on debian-derived or arch be sure to install tesseract-ocr and ffmpeg yourself"