

## Daftar Isi
* [Tentang Aplikasi](#tentang-aplikasi)
  * [Definisi](#definisi)
  * [Sistem Pembangun](#sistem-pembangun)
* [Petunjuk Instalasi](#petunjuk-instalasi)
* [Petunjuk Penggunaan](#petunjuk-penggunaan)
* [Informasi Lainnya](informasi-lainnya)
  * [Anggota Proyek](#anggota-proyek)
  * [Kontak](#kontak)

<!-- TENTANG APLIKASI -->
## Tentang Aplikasi
### Definisi
Aplikasi BPMN to User Stories (BPMNtoUS) merupakan sebuah aplikasi berbasis web dimana aplikasi ini dapat melakukan translasi dari BPMN menjadi User Stories. 
<br>
User dapat mengupload file BPMN (tanpa login) dengan tipe file BPMN yaitu (.XML atau .XPDL), kemudian user dapat melakukan generate dari file BPMN tadi menjadi User Stories dengan menekan tombol generate. (Project Aplikasi BPMNtoUS ini dikerjakan oleh kelompok 3 kelas I2).
<br/>
>- **BPMN** merupakan standar notasi grafis yang mendeskripsikan langkah logis dari proses bisnis.
>- **User story** merupakan deskripsi mengenai kebutuhan sistem dalam bentuk bahasa natural yang dapat dengan mudah dipahami oleh end user yang tidak memiliki background TI.

Secara garis besar, aspek-aspek pembentuk dari User Stories sebagai output yang dihasilkan terbentuk melalui komponen input, yaitu :
1. Aspect of Who : Mewakili peran pengguna
2. Aspect of What : Mewakili tujuan 
3. Aspect of Why : Mewakili alasan untuk mencapai tujuan

### Sistem Pembangun
Aplikasi CDG dibangun dengan memanfaatkan *software*, *framework*, dan beberapa bahasa pemrograman, diantaranya adalah sebagai berikut :
- [VsCode Editor](https://code.visualstudio.com/)
- [SQLite Database](https://www.sqlite.org/index.html)
- [GitHub](https://github.com/)
- [Django Framework](https://www.djangoproject.com/) 
- [Bootstrap Framework](https://getbootstrap.com/)
- [Python](https://www.python.org/)
- [Javascript](javascript.com)

## Petunjuk Instalasi 
Petunjuk mengenai prosedur instalasi untuk aplikasi BPMNtoUserStories dilakukan pada sesi terminal, berikut prosedur yang dapat dilakukan :
1. Install Python 3.9.2 (Pastikan untuk mencentang add to PATH)
2. Buka Command Prompt
3. Lakukan pembuatan directori
   ```sh
   mkdir AgileRE-2021 (untuk membuat direktori baru [tidak harus pada disk C:])
   ```
4. Masuk ke directori AgileRE-2021
   ```sh
   cd AgileRE-2021
   ```
5. Membuat *virtual environment* pada *python*
   ```sh
   python -m venv env
   ```
6. Lakukan *clone* pada repositori
   ```sh
   git clone https://github.com/AgileRE-2021/BPMNtoUserStories.git
   ```
7. Masuk ke dalam *virtual environment* 
   ```sh
   env\scripts\activate.bat
   ```
8. Masuk ke directori BPMNtoUserStories
   ```sh
   cd BPMNtoUserStories
   ```
9. Lakukan instalasi django
   ```sh
   pip install django
   ```
10. Lakukan instalasi mysqlclient
    ```sh
    pip install mysqlclient
    ```
11. Setelah itu nyalakan Aplikasi XAMPP Control Panel dan sambungkan pada Apache dan MySQL.
12. Kembali ke cmd
13. Lakukan migrate
    ```sh
    python manage.py migrate
    ```
14. Jalankan aplikasi pada *localhost*
    ```sh
    python manage.py runserver
    ```
15. Menuju browser dengan alamat http://127.0.0.1:8000/

> [Video Panduan Cara Instalasi](***link youtube***)


## Petunjuk Penggunaan
Cara Kerja Translasi BPMN to User Stories
1. Masuk halaman home, kemudian klik “Start BPMN2US”
2. Setelah itu tekan “Choose File” dan kemudian pilih file BPMN yang ingin anda Translasikan ke User Stories (filetype harus .XML / .XPDL)
3. Jika sudah selesai upload file yang telah diinginkan, kemudian tekan “Submit”
4. Setelah klik Submit, maka file BPMN anda sudah terlihat berubah menjadi User Stories
5. Untuk mengetahui lebih detail, tekan tombol "Show detail of components"

> [Video Panduan Penggunaan](***link youtube***)

## Informasi Lainnya
### Anggota Proyek
Anggota pada proyek pengerjaan aplikasi *BPMNtoUserStories* terdiri dari 7 orang, meliputi :

1. Nesa Giarfina         (081811633007)
2. Tanvi Azmia Fathoni   (081811633013)
3. M. Dani Rahmatulloh   (081811633029)
4. M. Roziq Syarwan E.   (081811633031)
5. M. Reza Zulfikarsyah  (081811633033)
6. Hisyam Fariqi         (081811633039)
7. Kinara Al Ghiffari    (081811633049)

### Kontak 
Informasi kontak setiap anggota lebih detail dapat dilihat di bawah ini. 
1. Nesa Giarfina         : nesagiarfina@gmail.com
2. Tanvi Azmia Fathoni   : tanviazmia15@gmail.com
3. M. Dani Rahmatullah   : muhammad.dani.rahmatulloh-2018@fst.unair.ac.id
4. M. Roziq Syarwan E.   : mroziq6@gmail.com
5. M. Reza Zulfikarsyah  : rezazulfff@gmail.com
6. Hisyam Fariqi         : hisyamfariqi@gmail.com
7. Kinara Al Ghiffari    : kinaraalghifari17@gmail.com

<h2 align="center"> -------S1 Sistem Informasi - Universitas Airlangga - 2021------- </h2>
