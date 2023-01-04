import json
from chat_utils import tokenize, stemming, bagofwords
from model import NeuralNet
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader




with open('intents.json','r') as f:
    intents = json.load(f)

print(intents)

all_words = []
tags = []
words_tags = []

for intent in intents['intents']:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        words_tags.append((w, tag))

ignore_words = ['?','!','.',',']
all_words = [stemming(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))
print(tags)

x_train = []
y_train = []

for (pattern_sentence, tag) in words_tags:
    bag = bagofwords(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) # crossentropyloss

x_train = np.array(x_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):
    def __init__ (self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples
    


# Hyperparameter
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0])
learning_rate=0.001
num_epochs = 1000

print(input_size, len(all_words))
print(output_size, tags)

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size = batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)


#loss and optimizer 
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, label) in train_loader:
        words = words.to(device)
        label = label.to(dtype=torch.long).to(device)

        #forward
        outputs = model(words)
        loss= criterion(outputs, label)


        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if (epoch +1) % 100 ==0:
        print(f"epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}")


print(f"final_loss, loss={loss.item():.4f}")


data={"model_state":model.state_dict(),
        "input_size": input_size,
        "output_size":output_size,
        "hidden_size":hidden_size,
        "all_words":all_words,
        "tags":tags}

file = "data.pth"
torch.save(data, file)
print(f"Training complete. File saved to{file}")