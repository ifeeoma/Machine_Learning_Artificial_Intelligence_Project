#this is a test file for making a crescendo set of layers where the number of neurons doubles per layer until the middle point.
import math


start_neurons = 9
layers = 3

#Depending on the parity of layers, this outputs the powers of 2 that go into each neuron layer for an escalating neuron make-up. It will double the amount of start_neurons until it reaches the middle layer.
layers = layers -2
neuron_numbers = []
if layers == 1:
    neuron_numbers = [0]
    
elif (layers % 2) == 0:
    for i in range(0,math.floor(layers/2)):
        neuron_numbers.append(i)
    
    rev_numbers = list(reversed(neuron_numbers))
    for j in rev_numbers:
        neuron_numbers.append(j)
    
elif (layers % 2) !=0:
    for i in range(0,math.floor(layers/2)):
        neuron_numbers.append(i)
        rev_numbers = list(reversed(neuron_numbers))
    neuron_numbers.append(math.floor(layers/2))
    for j in rev_numbers:
        neuron_numbers.append(j)

for k in neuron_numbers:
    print(start_neurons*(2**k))

print(neuron_numbers)
