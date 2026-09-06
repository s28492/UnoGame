import torch
import torch.nn as nn
import torch.nn.functional as F

class NNModel(nn.Module):
    def __init__(self, in_features=16, h1=100, h2=100,
                 out_features=64, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Defining network layers
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, out_features)

    def forward(self, x):
        # Applying ReLu activation function
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # Calculating output
        x = self.out(x)
        return x

    def get_weights(self):
        return [self.fc1.weight, self.fc2.weight]

    def set_weights(self, weights):
        self.fc1 = weights[0]
        self.fc2 = weights[1]