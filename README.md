# Cut Out
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)

Cut out is a image segmentation implementation project that allows users to upload an image, select a region of interest and generate a cutout image with the selected region. In this project, I used Meta's [Segment Anything Model](https://github.com/facebookresearch/sam2/tree/main) which is state of the art deep learning model in the image segmentation task. To try the demo visit [here](https://huggingface.co/spaces/JaiSurya/cut-out). To try the Meta's demo try [here](https://segment-anything.com/demo). 

## Demo

https://github.com/user-attachments/assets/98ee0372-a640-419a-8580-1ebf100566ad


## Tech Stack
1. Python
2. Flask 
3. Numpy
4. Pillow
5. Ultralytics - `Mobile SAM` model
6. Torch
7. Torchvision
8. Werkzeug

## Installation

### Github
You can clone this repository by 
```bash
$ git clone https://github.com/jaisuryaprabu/cut-out.git
$ cd cut-out
```
### Create the virtual environment
```bash
$ python -m venv <your_venv_name>
$ .venv/Scripts/activate.ps1 <or> source .venv/Scripts/activate
$ pip install -r requirements.txt
```
### Export the FLASK_APP
Enter this command 
```bash
$ export FLASK_APP=main.py
```

### Run the app
```bash
$ python -m gevent.pywsgi -b 0.0.0.0:7860 main:app
```
## Contribution
Contributions are warmly welcomed 🤗 To contribute :
1. Fork this repository
2. Make your changes and commit them
3. Explain about the new feature or improvements
4. Open a pull request with a description of your changes

## Future Works
- [ ] Video segmentation