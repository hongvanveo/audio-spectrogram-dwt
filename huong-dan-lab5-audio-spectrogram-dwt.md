# Huong dan thuc hanh Lab 5: audio-spectrogram-dwt

Lab 5 dung mot container `student`. Sinh vien tao audio goc, chuan bi anh bi mat, xu ly anh thanh spectrogram, dung Inverse STFT tao tin hieu mien thoi gian, sau do nhung tin hieu nay vao he so tan so cao cua audio bang DWT.

## Tai bai lab

```bash
imodule https://github.com/hongvanveo/audio-spectrogram-dwt/raw/refs/heads/main/imodule_audio-spectrogram-dwt.tar
```

## Khoi dong

```bash
labtainer -r audio-spectrogram-dwt
```

Khi duoc hoi email/student id, nhap ma sinh vien. Lab se chuan hoa ID sang chu IN HOA va checkwork chi cham ket qua cua ID dang dung.

## Quy trinh

```text
secret.png
-> process_image.py: doc anh, hoan vi bang key, tao processed_image.json
-> istft.py: xem ma tran anh nhu spectrogram, tao hidden_signal.json
-> dwt_embed.py: DWT cover.wav, ghi hidden_signal vao detail coefficients
-> IDWT
-> stego.wav
```

Moi task yeu cau sua file code de dien ten file dau vao roi moi chay. Sinh vien chi can kiem tra lenh tao dung file dau ra cua task do; khong can chay `checkwork` sau tung task.

## Task 1: Tao audio goc

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav
ls -l cover.wav
```

Ket qua can co: file `cover.wav`.

## Task 2: Tao hoac chuan bi anh bi mat

```bash
python3 generate_secret_image.py --out secret.png
./view_secret.sh
ls -l secret.png
```

Neu da co anh san, copy anh do thanh `~/stego/secret.png` thay cho lenh generate. Anh se mo bang cua so xem anh binh thuong.

Ket qua can co: file `secret.png` va cua so xem anh da mo duoc.

## Task 3: Xu ly anh thanh ma tran spectrogram

Mo file:

```bash
nano process_image.py
```

Sua TODO:

```python
SECRET_IMAGE = "secret.png"
PERMUTATION_KEY = 3101
```

Chay:

```bash
python3 process_image.py
ls -l processed_image.json
```

Script nay doc anh, chuyen ve gray-scale, hoan vi pixel bang key va luu `processed_image.json`.

## Task 4: Tao tin hieu mien thoi gian bang Inverse STFT

Mo file:

```bash
nano istft.py
```

Sua TODO:

```python
COVER_FILE = "cover.wav"
PROCESSED_IMAGE = "processed_image.json"
```

Chay:

```bash
python3 istft.py
ls -l hidden_signal.json
```

Script nay xem `processed_image.json` nhu spectrogram va tao `hidden_signal.json`.

## Task 5: Nhung tin hieu vao audio bang DWT

Mo file:

```bash
nano dwt_embed.py
```

Sua TODO:

```python
COVER_FILE = "cover.wav"
HIDDEN_SIGNAL = "hidden_signal.json"
```

Chay:

```bash
python3 dwt_embed.py
ls -l stego.wav
```

Script nay phan ra `cover.wav` bang DWT, ghi tin hieu bi mat vao he so chi tiet tan so cao va IDWT de tao `stego.wav`.

## Task 6: Nghe va kiem tra audio

```bash
./play_cover.sh
./play_stego.sh
python3 analyze_audio.py --cover cover.wav --stego stego.wav
```

Lenh phan tich can in ra so mau audio bi thay doi va gia tri `snr_db`.

## Ket qua cuoi cung

Sau khi lam xong tat ca task, chay:

```bash
checkwork
```

Ket qua dung:

```text
Y - cover_created
Y - secret_image_created
Y - secret_image_viewed
Y - image_processed
Y - istft_signal_created
Y - dwt_highfreq_embedded
Y - stego_created
Y - audio_modified
```

Ket thuc:

```bash
stoplab audio-spectrogram-dwt
```
