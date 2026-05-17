# audio-spectrogram-dwt

Lab nay yeu cau sinh vien nhung mot anh bi mat vao audio goc bang quy trinh:

```text
secret.png -> xem nhu spectrogram -> Inverse STFT -> tin hieu mien thoi gian
-> DWT audio goc -> nhung vao he so tan so cao -> IDWT -> stego.wav
```

Cau truc lab:

- Lab dung 1 container duy nhat ten `student`.
- Sinh vien thao tac trong thu muc `~/stego`.
- File `embed_task.py` la file can sua de dien ten `cover.wav` va `secret.png`.

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
