# NeuroYT
This repository contains only source code of [live project](http://neuro.nulla.tech). This is a demonstration project for CV, it doesn`t carry any value to the developers. 

## Algorithm, structure
![](https://raw.githubusercontent.com/Tessarium/NeuroYT/master/ImagesForGitHub/archi.png)
1) Once every two minutes recognition script triggered
2) After that, it sends information to frontend via websocket (update tables and images)


## Example of live recognising
Model - faster_rcnn_inception_resnet_v2_atrous_coco
![](https://raw.githubusercontent.com/Tessarium/NeuroYT/master/ImagesForGitHub/1.jpg)
![](https://raw.githubusercontent.com/Tessarium/NeuroYT/master/ImagesForGitHub/2.jpg)

## Addition
Project is still in development. In plans, change the model to mask rcnn and of course teach it. And rebuild some parths of the code and logick to make recognising faster (now it`s about 2 minutes)