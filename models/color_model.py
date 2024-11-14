import torch.nn as nn

class ColorModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ColorModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)
