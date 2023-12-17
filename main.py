class KnapsackCryptosystem:
    def __init__(self, private_key, m, n):
        self.private_key = private_key
        self.m = m
        self.n = n
        self.public_key = []
        self.create_public_key()

    def create_public_key(self):
        for i in self.private_key:
            self.public_key.append((i * self.n) % self.m)

    def print_public_key(self):
        print("Public key: ", end="")
        for i in self.public_key:
            print(i, end=" ")
        print()

    def print_private_key(self):
        print("Private key: ", end="")
        for i in self.private_key:
            print(i, end=" ")
        print()

    def encrypt(self, message_text):
        splitted_binary_message = self.prepare_for_encrypt(message_text)
        encrypted_message = []
        for i in splitted_binary_message:
            summ = 0
            for j in range(len(i)):
                if i[j] == "1":
                    summ += self.public_key[j]
            encrypted_message.append(summ)
        return encrypted_message

    def prepare_for_encrypt(self, message_text):
        binary_message = "".join(f"{ord(i):08b}" for i in message_text)
        while len(binary_message) % len(self.private_key) != 0:
            binary_message = "0" + binary_message
        splitted_binary_message = []
        while len(binary_message) != 0:
            splitted_binary_message.append(binary_message[:len(self.private_key)])
            binary_message = binary_message[len(self.private_key):len(binary_message)]
        return splitted_binary_message

    def decrypt(self, encrypted_message):
        inverse_n = 0
        for i in range(self.m):
            if (self.n * i) % self.m == 1:
                inverse_n = i
                break
        splitted_binary_message = []
        for i in encrypted_message:
            summ = (i * inverse_n) % self.m
            binary = ""
            for j in range(len(self.private_key) - 1, -1, -1):
                if summ >= self.private_key[j]:
                    binary = "1" + binary
                    summ -= self.private_key[j]
                else:
                    binary = "0" + binary
            splitted_binary_message.append(binary)
        return self.after_decryption(splitted_binary_message)

    def after_decryption(self, splitted_binary_message):
        binary_message = ""
        for i in splitted_binary_message:       # Объединяем фрагменты
            binary_message += i
        while len(binary_message) % 8 != 0:     # Убираем незначащие нули
            binary_message = binary_message[1:]
        message_text = ""
        for i in range(0, len(binary_message), 8):
            temp = binary_message[i:i + 8]
            num = int(temp, 2)
            message_text += chr(num)
        return message_text


k = KnapsackCryptosystem([1, 2, 4, 10, 20, 40], 110, 31)
k.print_private_key()
k.print_public_key()
print()
#print(k.prepare_for_encrypt("Hello World!"))
encrypted_mes = k.encrypt("Hello World!")
print(encrypted_mes)
print(k.decrypt(encrypted_mes))
