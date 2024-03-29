## Sistem Pendeteksi Bahan Makanan Tidak Layak Konsumsi Menggunakan YOLOv5 Berbasis IoT pada Kulkas
##### Sistem ini merupakan sebuah sistem ekstensi yang dapat mendeteksi citra dan bau dari buah-buahan dan sayur-sayuran untuk menentukan tingkat kesegaran pada buah-buahan dan sayur-sayuran pada kulkas yang akan terhubung pada aplikasi untuk.
![alt text](https://github.com/fahiraq/SmartFridge/blob/main/alat.jpg?raw=true)
### Komponen yang digunakan:
1. Raspberry Pi 4
2. Arduino Nano
3. Webcam
4. Sensor Gas (MQ-135)
5. Led
6. Relay
7. Battery Li-Ion
### Cara Menjalankan Sistem:
#### 1. Install Package/Library
Sebelum codingan dapat dijalankan, kita perlu mempersiapkan raspberry pi dengan library-library yang akan dibutuhkan untuk object detection dan komunikasi IoT seperti:
- opencv
- cv2
- torch
- torchvision
- ultralytics
- yolov5
- yaml
- pyrebase
- RPi
- serial
- telepot
Library-library tersebut bisa di install melalui command prompt atau dengan mengunduh file file yang telah disediakan pada repository ini.
#### 2. Buka File Source Code
Jika seluruh library yang dibutuhkan telah diinstal, anda juga dapat melakukan pengecekan dengan menggunakan command "pip list" pada command prompt raspberry pi, kemudian bukan codingan bisa.py, file dapat ditemukan pada repo ini.
#### 3. Auto Run Raspberry Pi
Karena sistem akan dipasangkan pada bagian dalam kulkas, sebelumnya kita perlu mengatur agar raspi dapat menjalankan program secara automatis ketika raspi dinyalakan dengan menggunakan Auto Run.
Untuk memasang Auto Run pada Raspi dapat menggunakan command berikut:
1. crontab -e
2. @reboot python path_file_bisa.py
3. ctrl x
4. pilih y untuk rewrite/save command
5. enter
#### 4. Instalasi Alat
Pasangkan komponen-komponen yang telah dipersiapkan sebelumnya dengan mengikuti gambar rangkaian dibawah ini.
![alt text](https://github.com/fahiraq/SmartFridge/blob/main/Rangkaian%20sensor.jpg?raw=true)
###### Hubungkan kamera dan relay ke raspberry pi, kemudian relay LED dan baterai hubungkan pada relay.
![alt text](https://github.com/fahiraq/SmartFridge/blob/main/rangkaian%20LED.jpg?raw=true)
###### Untuk sensor gas membutuhkan bantuan dari Arduino Nano, hubungkan Arduino Nano ke Raspberry Pi terlebih dahulu. Kemudian sensor gas akan dihubungkan ke Arduino Nano.
#### 5. Sistem siap dijalankan 
Jangan lupa untuk memastikan raspberry pi telah tersambung dengan daya!
