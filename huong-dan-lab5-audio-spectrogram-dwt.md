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

Moi task yeu cau sua file code de dien ten file dau vao roi moi chay. Sau moi task, chay `checkwork` de thay muc tuong ung chuyen sang `Y`.

## Task 1: Tao audio goc

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav
checkwork
```

Can thay:

```text
Y - cover_created
```

## Task 2: Tao hoac chuan bi anh bi mat

```bash
python3 generate_secret_image.py --out secret.png
./view_secret.sh
checkwork
```

Neu da co anh san, copy anh do thanh `~/stego/secret.png` thay cho lenh generate. Anh se mo bang cua so xem anh binh thuong.

Can thay:

```text
Y - secret_image_created
Y - secret_image_viewed
```

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
checkwork
```

Script nay doc anh, chuyen ve gray-scale, hoan vi pixel bang key va luu `processed_image.json`.

Can thay:

```text
Y - image_processed
```

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
checkwork
```

Script nay xem `processed_image.json` nhu spectrogram va tao `hidden_signal.json`.

Can thay:

```text
Y - istft_signal_created
```

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
checkwork
```

Script nay phan ra `cover.wav` bang DWT, ghi tin hieu bi mat vao he so chi tiet tan so cao va IDWT de tao `stego.wav`.

Can thay:

```text
Y - dwt_highfreq_embedded
Y - stego_created
```

## Task 6: Nghe va kiem tra audio

```bash
./play_cover.sh
./play_stego.sh
python3 analyze_audio.py --cover cover.wav --stego stego.wav
checkwork
```

Can thay:

```text
Y - audio_modified
```

## Ket qua cuoi cung

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
