import torch
from torch.utils.data import TensorDataset, DataLoader
from color_model import ColorModel

# Load data
X_train, y_train = torch.load('data/processed/train_data.pt')
X_test, y_test = torch.load('data/processed/test_data.pt')

# Create datasets and loaders
train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.FloatTensor(y_train))
test_dataset = TensorDataset(torch.FloatTensor(X_test), torch.FloatTensor(y_test))
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Initialize model, loss function, optimizer
model = ColorModel(input_dim=X_train.shape[1], output_dim=1)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 50
for epoch in range(epochs):
    model.train()
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        predictions = model(X_batch)
        loss = criterion(predictions, y_batch)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

# Save the model
torch.save(model.state_dict(), 'models/color_model.pt')
