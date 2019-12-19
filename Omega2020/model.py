import torch.nn.functional as F
import torch.nn as nn
class ConvolutionalNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 3, 1)
        self.conv2 = nn.Conv2d(6, 16, 3, 1)
        self.fc1 = nn.Linear(5*5*16, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84,10)

    def forward(self, X):
        X = F.relu(self.conv1(X))
        X = F.max_pool2d(X, 2, 2)
        X = F.relu(self.conv2(X))
        X = F.max_pool2d(X, 2, 2)
        X = X.view(-1, 5*5*16)
        X = F.relu(self.fc1(X))
        X = F.relu(self.fc2(X))
        X = self.fc3(X)
        return F.log_softmax(X, dim=1)

class Predict:
    def __init__(self, cells):
        self.cells = cells

    def transformation(cells):
        transform = transforms.ToTensor()
        tensors = []
        for cell in cells:
            tensors.append((transform(cell).view(1,28,28).type(torch.FloatTensor)))
        return tensors

    def load_model(self):
        model = ConvolutionalNetwork()
        model = model.load_state_dict(torch.load('model1.pth'))

    def convert(tensor): # always be passing in an array
        grid = []
        for i in range(len(tensor)):
            if tensor[i].mean().item() <= 52:
                grid.append(".")
            else:
                grid.append(str(model(tensor[i].view(1,1,28,28)).argmax().item()))
        return grid