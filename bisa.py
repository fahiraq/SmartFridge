import torch
from matplotlib import pyplot as plt
import numpy as np 
import cv2
import uuid
import os
import time 
import pyrebase
import serial
import RPi.GPIO as GPIO
import telepot

TELEGRAM_BOT_TOKEN = '6665828180:AAGB5fQdfRa8Z16QdKXstFyYINNZKZ6OKEA'
chat_id = '848692193'  # Ganti dengan chat ID penerima

# Konfigurasi Firebase
config = {
    "apiKey": "AIzaSyDQvuLYUkr-EoNz_YMKKn9p0ffE8bbzJ94",
    "authDomain": "percobaan-6fc20.firebaseapp.com",
    "databaseURL": "https://percobaan-6fc20-default-rtdb.firebaseio.com",
    "projectId": "percobaan-6fc20",
    "storageBucket": "percobaan-6fc20.appspot.com",
    "messagingSenderId": "132825533855",
    "appId": "1:132825533855:web:961b88ec7e1595106bc1aa",
    "measurementId": "G-JQ4HH98W3E"
    }

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)

def led():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)

def led_off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)



def capture_and_detect():
    camera = cv2.VideoCapture(0)
    time.sleep(2)
    print("Melakukan penangkapan citra")
    return_value, image = camera.read()
        # # Simpan gambar ke path yang ditentukan
    image_path = '/home/pi/Dokumen/data/images/foto.png'
    cv2.imwrite(image_path, image)
    del(camera)
    
        # # Panggil fungsi run_object_detection dengan menyediakan path gambar
    run_object_detection(image_path)

def run_object_detection(image_path):
    model = torch.hub.load('.','custom',path='/home/pi/yolov5/best.pt',source='local')
    #img = os.path.join('data','images','foto.png')
    img = os.path.join('/home/pi/Dokumen/data/images/foto.png')
    results = model(img)
    current_time = time.localtime()
    timenow = current_time.tm_hour, current_time.tm_min

    print(results)

    # Dictionary untuk melacak jumlah setiap kelas
    class_counts = {}

    # Loop deteksi
    for obj in results.xyxy[0]:
        class_index = int(obj[-1])
        class_name = model.names[class_index]
        confidence = obj[4]  # Confidence value is at index 4 in the results

        # Mengecek jenis kelas dan menambahkan ke dictionary
        if class_name in class_counts:
            class_counts[class_name].append(confidence)
        else:
            class_counts[class_name] = [confidence]

    # Mengecek jumlah akhir dan mencetak pesan
    for class_name, confidences in class_counts.items():
        count = len(confidences)
        average_confidence = sum(confidences) / count if count > 0 else 0
        if class_name == "fresh-tomato" and average_confidence > 0.50:
            print(f"tomatsegar : {count}. Confidence: {average_confidence:.2f}")
        
        # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'tomatsegar': count,
                'akurasi': f"{average_confidence}",
            }
            db.child('tomatsegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
    
        # Mengecek jenis kelas dan menampilkan hasil spesifik
        # elif class_name == "fresh-watermelon" and average_confidence > 0.50:
        #     print(f"semangkasegar : {count} Confidence: {average_confidence:.2f}")
        #     # Kirim data ke Pyrebase
        #     firebase = pyrebase.initialize_app(config)
        #     db = firebase.database()
        #     sensor_to_upload = {
        #         'semangkasegar': count,
        #         'akurasi': f"{average_confidence}",
        #         }
        #     db.child('semangkasegar').set(sensor_to_upload)
        #     print("Data sent to Pyrebase.")
        elif class_name == "unfresh-watermelon" and average_confidence > 0.50:
            print(f"semangkatidaksegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'semangkatidaksegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('semangkatidaksegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} buah semangka tidak segar. \nMohon untuk segera dikonsumsi!"
            send_telegram_message(message_body)
        elif class_name == "rotten-watermelon" and average_confidence > 0.50:
            print(f"semangkabusuk : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'semangkabusuk': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('semangkabusuk').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} buah semangka busuk. \nMohon untuk segera dibuang! \n Link Pembelian Buah Semangka : https://shopee.co.id/search?keyword=semangka&locations=Kota%20Bandung&noCorrection=true&page=0&sortBy=relevancy "
            send_telegram_message(message_body)

        elif class_name == "fresh-apple" and average_confidence > 0.50:
            print(f"apelsegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'apelsegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('apelsegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
        elif class_name == "unfresh-apple" and average_confidence > 0.50:
            print(f"apeltidaksegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'apeltidaksegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('apeltidaksegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} buah apel tidak segar. \nMohon untuk segera dikonsumsi!"
            send_telegram_message(message_body)
        elif class_name == "rotten-apple" and average_confidence > 0.50:
            print(f"apelbusuk : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'apelbusuk': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('apelbusuk').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} buah apel busuk. \nMohon untuk segera dibuang! \n Link Pembelian Apel : https://shopee.co.id/search?keyword=apel%20hijau&locations=Kota%20Bandung%2CJawa%20Barat&noCorrection=true&page=0&sortBy=relevancy "
            send_telegram_message(message_body)     

        elif class_name == "fresh-dragonfruit" and average_confidence > 0.50:
            print(f"nagasegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'nagasegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('nagasegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
        elif class_name == "unfresh-dragonfruit" and average_confidence > 0.50:
            print(f"nagatidaksegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'nagatidaksegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('nagatidaksegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} buah naga tidak segar. \nMohon untuk segera dikonsumsi!"
            send_telegram_message(message_body)
        elif class_name == "rotten-dragonfruit" and average_confidence > 0.50:
            print(f"nagabusuk : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'nagabusuk': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('nagabusuk').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} buah naga busuk. \nMohon untuk segera dibuang! \n Link Pembelian Buah Naga : https://shopee.co.id/search?keyword=buah%20naga&locations=Kota%2520Bandung&noCorrection=true&page=0 "
            send_telegram_message(message_body)

        elif class_name == "unfresh-tomato" and average_confidence > 0.50:
            print(f"tomattidaksegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'tomattidaksegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('tomattidaksegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} tomat tidak segar. \nMohon untuk segera dikonsumsi!"
            send_telegram_message(message_body)
        elif class_name == "rotten-tomato" and average_confidence > 0.50:
            print(f"tomatbusuk : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'tomatbusuk': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('tomatbusuk').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} tomat busuk. \nMohon untuk segera dibuang! \n Link Pembelian Tomat : https://shopee.co.id/search?keyword=tomat&locations=Kota%2520Bandung&noCorrection=true&page=0 "
            send_telegram_message(message_body)

        elif class_name == "fresh-chilli" and average_confidence > 0.50:
            print(f"cabaisegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'cabaisegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('cabaisegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
        elif class_name == "unfresh-chilli" and average_confidence > 0.50:
            print(f"cabaitidaksegar : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'cabaitidaksegar': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('cabaitidaksegar').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} cabai tidak segar. \nMohon untuk segera dikonsumsi!"
            send_telegram_message(message_body)
        elif class_name == "rotten-chilli" and average_confidence > 0.50:
            print(f"cabaibusuk : {count} Confidence: {average_confidence:.2f}")
            # Kirim data ke Pyrebase
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            sensor_to_upload = {
                'cabaibusuk': count,
                'akurasi': f"{average_confidence}",
                }
            db.child('cabaibusuk').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            # Send notification telegram
            message_body = f"{count} cabai busuk. \nMohon untuk segera dibuang! \n Link Pembelian Cabai : https://shopee.co.id/search?keyword=cabai%20hijau&locations=Kota%2520Bandung&noCorrection=true&page=0 "
            send_telegram_message(message_body)

        # elif class_name == "fresh-collardgreen" and average_confidence > 0.50:
        #     print(f"sawisegar : {count} Confidence: {average_confidence:.2f}")
        #     # Kirim data ke Pyrebase
        #     firebase = pyrebase.initialize_app(config)
        #     db = firebase.database()
        #     sensor_to_upload = {
        #         'sawisegar': count,
        #         'akurasi': f"{average_confidence}",
        #         }
        #     db.child('sawisegar').set(sensor_to_upload)
        #     print("Data sent to Pyrebase.")
        # elif class_name == "unfresh-collardgreen" and average_confidence > 0.50:
        #     print(f"sawitidaksegar : {count} Confidence: {average_confidence:.2f}")
        #     # Kirim data ke Pyrebase
        #     firebase = pyrebase.initialize_app(config)
        #     db = firebase.database()
        #     sensor_to_upload = {
        #         'sawitidaksegar': count,
        #         'akurasi': f"{average_confidence}",
        #         }
        #     db.child('sawitidaksegar').set(sensor_to_upload)
        #     print("Data sent to Pyrebase.")
        #     # Send notification telegram
        #     message_body = f"{count} sawi sudah tidak segar. \n Mohon untuk segera dikonsumsi!"
        #     send_telegram_message(message_body)
        # elif class_name == "rotten-collardgreen" and average_confidence > 0.50:
        #     print(f"sawibusuk : {count} Confidence: {average_confidence:.2f}")
        #     # Kirim data ke Pyrebase
        #     firebase = pyrebase.initialize_app(config)
        #     db = firebase.database()
        #     sensor_to_upload = {
        #         'sawibusuk': count,
        #         'akurasi': f"{average_confidence}",
        #         }
        #     db.child('sawibusuk').set(sensor_to_upload)
        #     print("Data sent to Pyrebase.")
        #     # Send notification telegram
        #     message_body = f"{count} sawi busuk. \n Mohon untuk segera dibuang! \n Link Pembelian Sawi : https://shopee.co.id/search?keyword=sayur%20sawi&locations=Kota%2520Bandung&noCorrection=true&page=0 "
        #     send_telegram_message(message_body)



def read_sensor_data_and_send():
    # Inisialisasi Firebase
    firebase = pyrebase.initialize_app(config)
    # Inisialisasi Realtime Database
    db = firebase.database()

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    # Gunakan variabel boolean untuk melacak apakah data sudah dikirim
    data_sent = False

    while not data_sent:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            # Upload data ke Firebase
            sensor_to_upload = {
                'sensor_data': line,
            }

            db.child('sensor_readings').set(sensor_to_upload)
            print("Data sent to Pyrebase.")
            if float(line) > 10.03:
                message_body = "Terdeteksi Bau Busuk. \nKulkas anda terdapat bahan makanan yang sudah busuk, segera periksa kulkas anda"
                send_telegram_message(message_body)
            
            # Set variabel boolean menjadi True setelah data dikirim
            data_sent = True
    return

# Fungsi untuk mengirim pesan
def send_telegram_message(message):
    try:
        bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
        bot.sendMessage(chat_id, message)
        print("Pesan berhasil dikirim!")
    except Exception as e:
        print(f"Error: {e}")

def send_data_to_firebase(node, value):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    sensor_to_upload = {node: value}
    db.child(node).set(sensor_to_upload)
    print(f"Data sent to Pyrebase for node: {node}")

def reset_data():
    nodes_to_reset = [
        'semangkasegar',
        'semangkatidaksegar',
        'semangkabusuk',
        'apelsegar',
        'apeltidaksegar',
        'apelbusuk',
        'nagasegar',
        'nagatidaksegar',
        'nagabusuk',
        'tomatsegar',
        'tomattidaksegar',
        'tomatbusuk',
        'cabaisegar',
        'cabaitidaksegar',
        'cabaibusuk',
        'sawisegar',
        'sawitidaksegar',
        'sawibusuk'
    ]

    for node in nodes_to_reset:
        send_data_to_firebase(node, 0)

def main_loop():
    while True:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flush()
        line = ser.readline().decode('utf-8').rstrip()
        print(line)


        current_time = time.localtime()
        timenow = current_time.tm_hour, current_time.tm_min

        # Bandingkan jam dan menit saat ini dengan reset data
        if timenow in [(7,13),(7, 9),(6, 56),(19, 13),(19, 17), (18, 47),(18, 25),(18, 5),(18, 9),(9, 3),(9, 18),(9, 33),(9, 48),(4, 58), (9, 58), (14, 58), (19, 58)]:
            reset_data()

        elif timenow in [(7, 14),(7, 10),(6, 57),(19, 14),(19, 18),(18, 48),(18, 26),(18, 6),(18, 10),(9, 4),(9, 19),(9, 34),(9, 49),(22, 44),(4, 59), (9, 59), (14, 59), (19, 59)]:
            led()

        # Bandingkan jam dan menit saat ini dengan jadwal capture dan deteksi
        elif timenow in [(7, 15),(7, 11),(6, 58),(19, 15), (19, 19) ,(18, 49),(18, 27),(18, 7),(18, 11),(9, 5),(9, 20),(9, 35),(9, 50),(5, 0), (10, 0), (15, 0), (20, 0)]:
           capture_and_detect()

        elif timenow in [(7, 16),(7, 12),(6, 59),(19, 16),(19, 20),(18, 50),(18, 4),(18, 28),(18, 12),(17, 31),(9, 6),(9, 21),(9,36),(9, 51),(5, 1), (10, 1), (15, 1), (20, 1)]:
            led_off()

        # Bandingkan jam dan menit saat ini dengan jadwal sensor
        elif timenow in [(21, 0), (22, 0), (23, 0), (0, 0), 
                         (1, 0), (2, 0), (3, 0), (4, 0), 
                         (6, 0), (7, 0), (8, 0), (9, 0), (9, 30),
                         (11, 0), (12, 0), (13, 0),(14, 0),
                         (16, 0), (17, 0), (18, 0),(19, 0)]:
            read_sensor_data_and_send()

        # Tunggu selama 5 detik sebelum memeriksa waktu lagi
        time.sleep(2)



if __name__ == '__main__':
    message_body = "Selamat Datang di MAGER (sMArt refriGERator)."
    send_telegram_message(message_body)
    main_loop()
