class SDES:
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]

    S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]
    
    S1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]

    def __init__(self, key):
        """Inicializa o S-DES com uma chave de 10 bits."""
        if len(key) != 10:
            raise ValueError("A chave deve ter 10 bits")
        self.key = key
        self.k1, self.k2 = self._generate_subkeys()

    def _permute(self, data, table):
        """Realiza uma permutação nos dados usando a tabela fornecida."""
        return [data[i-1] for i in table]

    def _split(self, data):
        """Divide os dados em duas metades."""
        mid = len(data) // 2
        return data[:mid], data[mid:]

    def _shift_left(self, data, shifts):
        """Realiza um deslocamento circular à esquerda."""
        return data[shifts:] + data[:shifts]

    def _generate_subkeys(self):
        """Gera as subchaves K1 e K2."""
        key = self._permute(self.key, self.P10)
        
        left, right = self._split(key)
        
        left = self._shift_left(left, 1)
        right = self._shift_left(right, 1)
        
        k1 = self._permute(left + right, self.P8)
        
        left = self._shift_left(left, 2)
        right = self._shift_left(right, 2)
        
        k2 = self._permute(left + right, self.P8)
        
        return k1, k2

    def _sbox(self, data, sbox):
        """Aplica uma S-Box nos dados."""
        row = data[0] * 2 + data[3]
        col = data[1] * 2 + data[2]
        val = sbox[row][col]
        return [val >> 1 & 1, val & 1]

    def _f_function(self, right, subkey):
        """Implementa a função F do S-DES."""
        expanded = self._permute(right, self.EP)
        
        xored = [a ^ b for a, b in zip(expanded, subkey)]
        
        left, right = xored[:4], xored[4:]
        
        s0_result = self._sbox(left, self.S0)
        s1_result = self._sbox(right, self.S1)

        return self._permute(s0_result + s1_result, self.P4)

    def _feistel_round(self, left, right, subkey):
        """Executa uma rodada da rede de Feistel."""
        f_result = self._f_function(right, subkey)
        new_right = [a ^ b for a, b in zip(left, f_result)]
        return right, new_right

    def encrypt(self, plaintext):
        """Encripta um bloco de 8 bits."""
        if len(plaintext) != 8:
            raise ValueError("O texto deve ter 8 bits")

        data = self._permute(plaintext, self.IP)
        
        left, right = self._split(data)
        
        left, right = self._feistel_round(left, right, self.k1)
        
        right, left = self._feistel_round(left, right, self.k2)
        
        return self._permute(left + right, self.IP_INV)

    def decrypt(self, ciphertext):
        """Decripta um bloco de 8 bits."""
        if len(ciphertext) != 8:
            raise ValueError("O texto cifrado deve ter 8 bits")

        data = self._permute(ciphertext, self.IP)
        
        left, right = self._split(data)
        
        left, right = self._feistel_round(left, right, self.k2)
        
        right, left = self._feistel_round(left, right, self.k1)
        
        return self._permute(left + right, self.IP_INV)

def str_to_bits(s):
    return [int(bit) for bit in s]

def bits_to_str(bits):
    return ''.join(str(bit) for bit in bits)

if __name__ == "__main__":
    key = str_to_bits("1010000010")
    plaintext = str_to_bits("11010111")
    
    sdes = SDES(key)

    encrypted = sdes.encrypt(plaintext)
    print(f"Texto original: {bits_to_str(plaintext)}")
    print(f"Texto cifrado: {bits_to_str(encrypted)}")
    
    decrypted = sdes.decrypt(encrypted)
    print(f"Texto decifrado: {bits_to_str(decrypted)}")