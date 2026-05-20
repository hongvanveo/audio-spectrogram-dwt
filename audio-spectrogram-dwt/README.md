# audio-spectrogram-dwt

Lab nay yeu cau sinh vien nhung mot anh bi mat vao audio goc bang quy trinh:

```text
secret.png -> hoan vi ngau nhien bang key -> xem nhu spectrogram
-> Inverse STFT -> tin hieu mien thoi gian
-> DWT nhieu muc audio goc -> ghi de vao detail coefficients muc sau cung
-> IDWT -> stego.wav
```

Cau truc lab:

- Lab dung 1 container duy nhat ten `student`.
- Sinh vien thao tac trong thu muc `~/stego`.
- File `embed_task.py` la file can sua de dien ten `cover.wav` va `secret.png`.
- Sender va receiver chia se cung mot `PERMUTATION_KEY` dung cho buoc hoan vi anh truoc khi nhung.
- Khi `labtainer` hoi e-mail/student id, sinh vien nhap ma cua minh. He thong se chuan hoa ma do thanh chu IN HOA va ghi nho ID gan nhat cho lan mo lab sau.
- `checkwork` chi hien va cham ket qua cua dung ID dang duoc su dung cho lab hien tai, khong tron voi cac file `.lab` cu cua ID khac.

Luong thuc hanh:

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav
python3 generate_secret_image.py --out secret.png
nano embed_task.py
python3 embed_task.py
python3 analyze_audio.py --cover cover.wav --stego stego.wav
cmp cover.wav stego.wav
```

Checkwork co cac muc:

- `cover_created`
- `secret_image_created`
- `image_processed`
- `istft_signal_created`
- `dwt_highfreq_embedded`
- `stego_created`
- `audio_modified`
