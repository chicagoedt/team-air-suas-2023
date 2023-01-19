import torch
import torchvision
from torchvision import transforms

# Define a transform to normalize the data
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# Load the data
data = torchvision.datasets.ImageFolder('path/to/runway/images', transform=transform)
data_loader = torch.utils.data.DataLoader(data, batch_size=4, shuffle=True)

# Define a convolutional neural network
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 6, 5) # 3 input channels, 6 output channels, 5x5 kernel size
        self.pool = torch.nn.MaxPool2d(2, 2) # 2x2 max pooling kernel
        self.conv2 = torch.nn.Conv2d(6, 16, 5) # 6 input channels, 16 output channels, 5x5 kernel size
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 120) # fully connected layer with 120 output neurons
        self.fc2 = torch.nn.Linear(120, 84) # fully connected layer with 84 output neurons
        self.fc3 = torch.nn.Linear(84, 2) # fully connected layer with 2 output neurons

    def forward(self, x):
        x = self.pool(torch.nn.functional.relu(self.conv1(x)))
        x = self.pool(torch.nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x

net = Net()

# Define a loss function and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# Train the network
for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(data_loader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
    print('Epoch %d loss: %.3f' % (epoch + 1, running_loss / (i + 1)))

print('Finished Training')

# Test the network on a new image
test_image = transform(Image.open('path/to/test/image'))
outputs
