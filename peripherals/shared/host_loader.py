def load_host_address(file:str ='host_address.txt'):
    with open(file, 'r') as file:
        line = file.readline()
        return line