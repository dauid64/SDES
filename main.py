from crypt.generation_key import generate_keys

if __name__ == '__main__':
    key ='1010000010'
    plain_text = '10111101'
    key1, key2 = generate_keys(key)
    print(key1, key2)