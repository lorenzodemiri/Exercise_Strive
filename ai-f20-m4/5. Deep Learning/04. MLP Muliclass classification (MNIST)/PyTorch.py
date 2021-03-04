from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
import time
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms


class Network(nn.Module):
    #Define the structure of the layers---> 128,64,10 units each
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(800, 400)
        self.fc2 = nn.Linear(400, 200)
        self.fc3 = nn.Linear(200, 100)
        
    def forward(self, x):
        x = F.relu(x)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        # Softmax (similar to sigmoid) squashes the input between 0 and 1 , but it also
        # normalize so that all the values sum to one like a probablity distribution
        x = F.softmax(x, dim=1)
        return x

def load_dataset(batch_size = 64):
    # Defining a Traforms to normalize the data (PREPROCESSING)
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5), (0.5))])
    # Download and load the training data (TRAINING DATA)
    trainset = datasets.MNIST('MNiST_data/', download =True, train=True, transform=transform)
    trainloader  = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)
    # Download and load the test data
    testset = datasets.MNIST('MNIST_data/', download=True, train=False, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True)

    return trainloader, testloader

def iter_data(trainset):
    temp = iter(trainloader)
    return temp.next()

#Init the model
model = Network()
#Init the Bias filling it with 0s
model.fc1.bias.data.fill_(0)
#Init Weights with random normal and standart deviation = 0.01
model.fc1.weight.data.normal_(std=0.01)

# Init the Test and Train Datasets
trainloader, testloader = load_dataset(64)

'''
SO BY ITERATING THE DATAITER WE CAN FIND INSIDE OF IT THE IMAGES AND THE RELATED LABEL
dataiter = iter(trainloader)
images, labels = dataiter.next()
'''
# Define the loss function
# Because of the Softmax output we use     
criterion = nn.CrossEntropyLoss()
# For the optimizer we are using SGD with a learining rate of 0.003
optimizer = optim.SGD(model.parameters(), lr=0.003)
#images, labels = next(iter(trainloader))


epochs = 3
print_every = 40
for e in range(epochs):
    running_loss = 0
    print("Epoch: {}/{}".format(e + 1, epochs))
    
    for i, (images, labels) in enumerate(iter(trainloader)):
        # Flatten the MNIST images into a 784 long vector
        images.resize_(images.size()[0], 784)

        optimizer.zero_grad()

        output = model.forward(images)   # 1) Forward Pass
        loss = criterion(output, labels) # 2) Compute loss
        loss.backward()                  # 3) Backward Pass
        optimizer.step()                 # 4) Update model

        running_loss += loss.item()

        if i % print_every == 0:
            print(f"\tIteration: {i}\t Loss: {running_loss/print_every:.4f}")
            running_loss = 0

