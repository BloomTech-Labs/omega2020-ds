
#import torch.nn.functional as F
#import torch.nn as nn
from sklearn import datasets, svm, metrics
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from PIL import Image
import cv2


# First NN Built
# class ConvolutionalNetwork(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.conv1 = nn.Conv2d(1, 6, 3, 1)
#         self.conv2 = nn.Conv2d(6, 16, 3, 1)
#         self.fc1 = nn.Linear(5*5*16, 120)
#         self.fc2 = nn.Linear(120, 84)
#         self.fc3 = nn.Linear(84,10)

#     def forward(self, X):
#         X = F.relu(self.conv1(X))
#         X = F.max_pool2d(X, 2, 2)
#         X = F.relu(self.conv2(X))
#         X = F.max_pool2d(X, 2, 2)
#         X = X.view(-1, 5*5*16)
#         X = F.relu(self.fc1(X))
#         X = F.relu(self.fc2(X))
#         X = self.fc3(X)
#         return F.log_softmax(X, dim=1)


# # Build the model

# #Hira's Second NN Build
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
#         self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
#         self.conv2_drop = nn.Dropout2d()
#         self.fc1 = nn.Linear(320, 50)
#         self.fc2 = nn.Linear(50, 10)

#     def forward(self, x):
#         x = F.relu(F.max_pool2d(self.conv1(x), 2))
#         x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
#         x = x.view(-1, 320)
#         x = F.relu(self.fc1(x))
#         x = F.dropout(x, training=self.training)
#         x = self.fc2(x)
#         return F.log_softmax(x)

# class Predict:
#     def __init__(self, cells):
#         self.cells = cells

#     def transformation(cells):
#         transform = transforms.ToTensor()
#         tensors = []
#         for cell in cells:
#             tensors.append((transform(cell).view(1,28,28).type(torch.FloatTensor)))
#         return tensors

#     def load_model(self):
#         model = ConvolutionalNetwork()
#         model = model.load_state_dict(torch.load('model1.pth'))

#     def convert(tensor): # always be passing in an array
#         grid = []
#         for i in range(len(tensor)):
#             if tensor[i].mean().item() <= 52:
#                 grid.append(".")
#             else:
#                 grid.append(str(model(tensor[i].view(1,1,28,28)).argmax().item()))
#         return grid

class KNN:
    #this KNN class will pull in MNIST data to bootstrap an end to end KNN model for predictions.
    #this should not be used in production, but is handy for loading the reference .sav model file
    #set train to false to skip the downloading and formatting of the MNIST dataset.
    def __init__(self, k, train=True):
        self.train_state = train
        self.k = k
        if self.train_state:
            self.mnist = datasets.fetch_openml(
                'mnist_784', data_home='mnist_dataset/')
            nonzero_indexes = []
            for i in range(len(self.mnist['target'])):
                if int(self.mnist['target'][i]) > 0:
                    nonzero_indexes.append(i)
                else:
                    pass

            self.digits = self.mnist['data'][nonzero_indexes]
            self.target = self.mnist['target'][nonzero_indexes]
            self.classifier = KNeighborsClassifier(n_neighbors=k)

            #share of values is created because to bootstrap a blank class, it is necessary to create a collection of blank arrays with the same class so the KNN model knows what a blank cell looks like.
            share_of_values = int(len(self.digits) // 9)
            blank_img = np.zeros((share_of_values, 784))
            test_dig = self.digits
            test_dig = np.append(blank_img, test_dig)
            test_dig = test_dig.reshape(
                (len(self.digits) + share_of_values), 784)

            blank_class = np.repeat(str(999), share_of_values)
            class_targets = self.target
            class_targets = np.append(blank_class, class_targets)

            self.digits = test_dig
            self.target = class_targets
        else:
            pass

    def mk_dataset(self, test_size=0.20):
        X_Train, X_Test, y_train, y_test = train_test_split(
            self.digits, self.target, test_size=test_size, random_state=1337)
        return np.array(X_Train), np.array(
            X_Test), np.array(y_train), np.array(y_test)

    def skl_knn(self):
        X_Train, X_Test, y_train, y_test = KNN.mk_dataset(self)
        self.classifier.fit(X_Train, y_train)
        y_pred = self.classifier.predict(X_Test)
        report = classification_report(y_test, y_pred)
        filename = str(self.k) + "_" + 'knn.sav'
        pickle.dump(self.classifier, open(filename, 'wb'))
        print(report)

    def load_knn(self, modelpath):
        #loads the .sav reference model file
        self.modelpath = modelpath
        self.model = pickle.load(open(self.modelpath, 'rb'))

    def predict(self, imgpath):
        img = Image.fromarray(imgpath)
        img.load()
        data = np.asarray(img, dtype="int32")
        #need to flatten the numpy array for predictions.
        img_array = data.reshape(1, -1)
        pred = self.model.predict(img_array)
        return pred[0]
