# Firearm Forensics : Masking Cartridge Case Images


### Results
---
**Original Casing Image** | **Masked Casing Image**
:-------------------------:|:-------------------------:
![alt text](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages/blob/master/resources/o_1.jpg) | ![alt text](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages/blob/master/resources/masked_o_1.jpg)


### Project Overview
---
This project employs computer vision algorithms and creates a tool to build masks on top of fired cartridge case images identifying regions of interest to aid in forensic investigations. These masks are used to compare the impressions on the cartridge case with the breech face and firing pin impressions of the firearm in question to ascertain if the cartridges came from the same or different firearm, which is information of great value in police investigations. 
This tool masks the following regions of interest -

- **Breech face impression**
- **Firing pin impression**
- **Firing pin drag**

For this algorithm to work as required it is important to use properly lit images focused on the firing pin and the breech face regions, including the grooves around the breech face but *excluding the head stamp region* of the case. Below is an image to illustrate the anatomy of a fired cartridge case -

1. Head stamp region
2. Breech face impression
3. Firing pin impression
4. Firing pin drag


**Fired Cartridge Case Image**

![alt text](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages/blob/master/resources/bullet_casing.jpg)


### Running this Project
---
**Setting up the environment -**

From your terminal -
1. Using conda
	- `conda create --name cartridge_masking python=3.9.15`
	- `conda activate cartridge_masking`
	- `pip3 install -r requirements.txt`

2. Using pyenv
	- `pyenv virtualenv 3.9.15 cartridge_masking`
	- `pyenv activate cartridge_masking`
	- `pip3 install -r requirements.txt`

**Running the project -**

There are two python scripts under the 'Services' folder -

- *cartridge_masking.py* : this is the main script that should be run from your terminal
- *helper.py* : This contains helper functions for the main script

From your terminal -
1. Clone the repository using: `git clone https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages.git`
2. Change the directory using: `cd FirearmForensics-MaskingCartridgeCaseImages/`
3. Activate the virtual environment using: `conda activate cartridge_masking` or `pyenv activate cartridge_masking`
4. Run the main script using: `python3 services/cartridge_masking.py`


### Dependencies
---
(This project was built on macOS Ventura 13.4.1)

**Python Version**: 3.9.15

**Python Libraries** (please refer requirements.txt):
- numpy: 1.26.3
- opencv-python: 4.9.0.80


### Dataset Description
---
This "Data" folder contains 5 images from 2 bullet cases.


### Next Steps
---
- Explore [NIST Ballistics Toolmark Research Database](https://tsapps.nist.gov/NRBTD/Studies/Studies/Details/a023199a-b9f3-4a1a-89e8-c94054a7cf61)






