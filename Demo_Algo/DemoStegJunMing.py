import PIL
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os



class JunMingSteg():
    def __init__(self):
        self.key = '<eof>'
        self.img_width = 0
        self.img_height = 0
        self.channel = 0
        self.decoded_path= 'decoded.txt'
        self.file_name = ""
        self.ext = ".png"
        self.new_save_path = ""
    
    def convert_to_png_np(self, np_img):
        if np_img.shape[2] == 4:
            return np_img
        
        height, width, _ = np_img.shape
        alpha_channel = np.full((height, width, 1), 255)
        
        np_img_rgba = np.concatenate((np_img, alpha_channel), axis=2)
        return np_img_rgba
    
    def binned_key(self):
        key_bytes = self.key.encode('utf-8')
        binned_key = ''.join(format(byte,'08b') for byte in key_bytes)
        return binned_key
 

    def show_image(self, path):
        image = PIL.Image.open(path)
        plt.imshow(image)
        plt.show()
      
    def message_to_bits(self, message):
        
        message_bytes = message.encode('utf-8')
        message_bits = ''.join(format(byte, '08b') for byte in message_bytes)
    
        return message_bits  
    
    def bits_to_message(self, message_bits):
    
        message_bytes = bytearray(int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8)) 
        message = message_bytes.decode('utf-8')
        
        return message
      
    def file_txt_to_bits(self, path):
        
        with open(path, 'r', encoding='utf-8') as file:
            message = file.read()
        
        message_bits = self.message_to_bits(message)
    
        return message_bits
    
    def bits_to_file_txt(self, message_bits, decoded_path=''):
        
        message = self.bits_to_message(message_bits)

        with open(decoded_path, 'w', encoding='utf-8') as file:
            file.write(message)
        
        print('Saved message at: {}', decoded_path)
    
    def image_to_numpy(self,img_path):
        
        image = PIL.Image.open(img_path)
        np_img = np.array(image)
        np_img = self.convert_to_png_np(np_img)
        return np_img
    
    def steg_message_image(self, message, np_img):
        
        self.img_width, self.img_height, self.channel = np_img.shape

        message_bits = self.message_to_bits(message) + self.message_to_bits(self.key)
        np_encoded_img = np_img.flatten()

        for idx, bit in enumerate(message_bits):
            val = bin(np_encoded_img[idx])[2:].zfill(8)
            val = val[:-1] + bit
            np_encoded_img[idx] = int(val,2)

        np_encoded_img = np_encoded_img.reshape(self.img_width, self.img_height, self.channel)        
        print('Encode Sucessfully!')
        
        return np_encoded_img
    
    
    def steg_message_imagepath(self, message, img_path):
        
        base_name = os.path.basename(img_path)
        self.file_name, _ = os.path.splitext(base_name)
        
        np_img = self.image_to_numpy(img_path)
        return self.steg_message_image(message, np_img)
        
        
        
    def decode_np_image(self, np_img):
        
        np_decode_img = np_img.flatten()

        secret_bits = ''
        idx = 0

        while secret_bits[-len(self.binned_key()):] != self.binned_key():  
            if idx >= len(np_decode_img):
                break  
            val = bin(np_decode_img[idx])[2:].zfill(8)  
            secret_bits = secret_bits + val[-1]  
            idx = idx + 1

            if idx >= len(np_img):
                break  

        secret_bits = secret_bits[:-len(self.binned_key())] 

        return self.bits_to_message(secret_bits)
                
    def decode_image(self, path):

        np_img = self.image_to_numpy(path)
        print(self.decode_np_image(np_img))
        

    def read_file(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            file_mess = file.read()
        print(file_mess)
        
    def save_encoded_image(self, np_img, save_path):
    
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path)) 

        directory = os.path.dirname(save_path)
        base_name = os.path.basename(save_path)
        file_name, _ = os.path.splitext(base_name)
        
        if not save_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_path = "encoded_message/" + self.file_name
            file_name += '.png' 
        
        counter = 1
        new_save_path = save_path
        while os.path.exists(new_save_path):
            new_save_path = os.path.join(directory, f"{file_name}_{counter}{self.ext}")
            counter = counter + 1
        
        encoded_image = Image.fromarray(np_img.astype(np.uint8))
        encoded_image.save(new_save_path,format = "PNG")
        print(f'Encoded image saved at: {new_save_path}')
        self.new_save_path = new_save_path

    
    def steg_message_imagepath_savepath(self, message, image_path, save_path):
        np_encoded_img = self.steg_message_imagepath(message, image_path)
        self.save_encoded_image(np_encoded_img,save_path)
    
         

def main():
    steg = JunMingSteg()
    while(True):
        print('LSB_demo')
        print('Press 1 to encode, Press 2 to decode, Press 3 to end:')
        a = int(input())
        if (a == 1):
            print('Running encoding...')
            img_path = input('Enter the path to the image: ')
            np_img = steg.image_to_numpy(img_path)
            message = input('Enter the message to the image: ')
            np_encoded_img = steg.steg_message_image(message, np_img)
            save_path = input('Enter the path to save the encoded image: ')
            steg.save_encoded_image(np_encoded_img, save_path)
        elif (a == 2):
            print('Running decoding...')
            img_path = input('Enter the path to the image (or press Enter to use Default): ')
            if not img_path:
                img_path = 'encoded_images\encoded.png' 
            print('Decoded message: {}'.format(steg.decode_image(img_path)))
        elif (a == 3):
            break
        else:
            print('Wrong!, Do again')


if __name__=="__main__":
    main()