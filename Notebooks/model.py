import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.utils import make_grid
import cv2
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from torch import optim


class Predict:

    def __init__(self, model):
        self.model = model
        self.final_images = final_images


    def transform(self, final_images):

        tensors = []
        for num in final_images:
            tensors.append((transform(num).view(1,28,28).type(torch.FloatTensor)))

        return tensors


    def load_model(self, model):

        model = model.load_state_dict(torch.load('model1.pth'))

    
    def convert(tensor): # always be passing in an array
        grid = []
        for i in range(len(tensor)):
            if tensor[i].mean().item() <= 22:
                grid.append(".")
            else:
                grid.append(str(model(tensor[i].view(1,1,28,28)).argmax().item()))
        return grid
    
