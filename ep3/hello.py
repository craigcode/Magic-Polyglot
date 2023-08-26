from random import randint

def greeting(source,target):
    print(f'Hello {target}, I\'m {source}, good to meet you')
    print('I think this is the beginning of a beautiful friendship')

greeting('Python','Magic')

for i in range(5):
    print( randint(1,10))