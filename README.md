# Firearm Forensics : Masking Cartridge Case Images

### Project Overview
---
This project aims to use computer vision algorithms to build masks on top of fired cartridge cases images to identify areas of interest in a forensic investigation. These masks are used to compare the impressions on the cartridge case with the breech face and firing pin impressions of the firearm in question to ascertain if the cartridges in question came from the same or different firearms, which is information of great value in police investigations. 
In this project, the following areas of interest are masked -

- **Breech face impression**
- **Firing pin impression**
- **Firing pin drag**

For this algorithm to work as required it is important to use properly lit images focused on the firing-pin and the breech-face regions, including the grooves around the breech-face but *excluding the head-stamp region* of the case. Below is an image to illustrate the anatomy of a fired cartridge case -

![Fired Bullet Casing Image](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages/resources/bullet_casing.jpg)


There are two python scripts under the 'Services' folder -

- cartridge_masking.py : this is the main script that should be run from your terminal
- helper.py : This contains helper functions for the main script


### Dependencies
---
(This project was built on macOS Ventura 13.4.1)

**Python Version**: 3.8.10

**Python Libraries** (please refer requirements.txt):
- numpy==1.26.3
- opencv-python==4.9.0.80


### Dataset Description
---
This "Data" folder contains 5 images from 2 bullet cases.


### Results
---

![Original Casing Image](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages/data/o_1.jpg)


![Masked Casing Image](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages/data/masked_images/masked_o_1.jpg)


### Next Steps
---
- Explore [NIST Ballistics Toolmark Research Database](https://tsapps.nist.gov/NRBTD/Studies/Studies/Details/a023199a-b9f3-4a1a-89e8-c94054a7cf61)






