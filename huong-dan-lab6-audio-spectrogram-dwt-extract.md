# Hướng dẫn thực hành Lab 6: audio-spectrogram-dwt-extract

Tài liệu này áp dụng cho:

- Lab 6: `audio-spectrogram-dwt-extract`

Lưu ý chung:

- Bài lab dùng hai container: `sender` và `receiver`.
- Sender có sẵn `stego.wav` và `secret.key`.
- Receiver nhận hai file này, dùng DWT để lấy lại tín hiệu bí mật từ phần tần số cao của audio, sau đó dùng key để đảo hoán vị và khôi phục ảnh.
- Nếu sinh viên muốn làm lại từ đầu, dùng:

```bash
labtainer -r audio-spectrogram-dwt-extract
```

## Tải bài lab

```bash
imodule https://raw.githubusercontent.com/hongvanveo/audio-spectrogram-dwt/main/imodule_audio-spectrogram-dwt-extract.tar
```

## Khởi động bài lab

```bash
labtainer -r audio-spectrogram-dwt-extract
```

Khi được hỏi email, sinh viên nhập mã sinh viên của mình. Hệ thống sẽ tự chuẩn hoá mã đó sang dạng IN HOA và ghi nhớ ID gần nhất.

`checkwork` chỉ hiển thị và chấm kết quả của đúng ID đang được dùng cho bài lab hiện tại, không trộn với các file `.lab` cũ của ID khác.

## Mục tiêu bài lab

Sinh viên cần:

1. Kiểm tra sender có `stego.wav` và `secret.key`.
2. Bật SSH trên receiver.
3. Có thể nghe trực tiếp `stego.wav` ở sender.
4. Gửi `stego.wav` và `secret.key` từ sender sang receiver.
5. Sửa `extract_task.py` để điền đúng tên file đầu vào.
6. Chạy chương trình tách ảnh để tạo `recovered_secret.png`.
7. Mở trực tiếp `recovered_secret.png`.
8. Chạy `checkwork` để kiểm tra kết quả.

## Nội dung kỹ thuật

Quy trình tách tin:

```text
stego.wav + secret.key
→ DWT nhiều mức trên audio stego
→ lấy detail coefficients ở mức phân rã cuối
→ nhân lại với scaled để lấy tín hiệu bí mật
→ dùng key để đảo hoán vị
→ dựng lại recovered_secret.png
```

Quy trình này bám theo phần retrieving/decryption của repo `haoyuhsu/Image-in-Audio-Steganography`: lấy high-frequency DWT coefficients, khôi phục tín hiệu đã nhúng bằng hệ số scale, rồi dùng key làm seed để đảo permutation.

## Task 1: Kiểm tra file ở sender

Trong terminal `sender`:

```bash
cd ~/stego
ls -l
cat README_sender.txt
```

Sender cần có:

```text
stego.wav
secret.key
```

## Task 2: Bật SSH trên receiver

Trong terminal `receiver`:

```bash
sudo service ssh start
```

## Task 3: Nghe trực tiếp audio stego ở sender

Trong terminal `sender`:

```bash
./play_stego.sh
```

## Task 4: Gửi file từ sender sang receiver

Trong terminal `sender`:

```bash
scp ~/stego/stego.wav ~/stego/secret.key ubuntu@receiver:~/stego/
```

Sau đó kiểm tra ở terminal `receiver`:

```bash
cd ~/stego
ls -l stego.wav secret.key
```

## Task 5: Sửa file extract_task.py

Trong terminal `receiver`:

```bash
cd ~/stego
nano extract_task.py
```

Tìm hai dòng TODO:

```python
STEGO_FILE = "TODO_STEGO_FILENAME"
KEY_FILE = "TODO_KEY_FILENAME"
```

Sửa thành:

```python
STEGO_FILE = "stego.wav"
KEY_FILE = "secret.key"
```

Lưu file và thoát khỏi `nano`.

## Task 6: Tách ảnh bí mật

Trong terminal `receiver`:

```bash
python3 extract_task.py
ls -l recovered_secret.png
```

Nếu chạy đúng, chương trình sẽ tạo file:

```text
recovered_secret.png
```

Mở trực tiếp ảnh trong terminal `receiver`:

```bash
./view_recovered.sh
```

## Task 7: Kiểm tra kết quả

Trên terminal chính của Labtainer:

```bash
checkwork
```

Kết quả đúng cần có:

```text
Y - audio_received
Y - key_received
Y - dwt_signal_extracted
Y - key_permutation_used
Y - secret_image_recovered
Y - recovered_image_viewed
Y - recovered_image_valid
```

Ý nghĩa các mục chấm:

- `audio_received`: receiver đã nhận `stego.wav`.
- `key_received`: receiver đã nhận `secret.key`.
- `dwt_signal_extracted`: receiver đã lấy tín hiệu bí mật từ detail coefficients của DWT.
- `key_permutation_used`: receiver đã dùng key để đảo hoán vị dữ liệu ảnh.
- `secret_image_recovered`: đã tạo `recovered_secret.png`.
- `recovered_image_viewed`: đã mở trực tiếp `recovered_secret.png` trong lab.
- `recovered_image_valid`: ảnh khôi phục đúng với ảnh bí mật ban đầu.

## Kết thúc bài lab

```bash
stoplab audio-spectrogram-dwt-extract
```

Kết quả sẽ được lưu tại:

```bash
/home/student/labtainer_xfer/audio-spectrogram-dwt-extract
```

Tên file bài làm có dạng:

```text
B22DCAT311.audio-spectrogram-dwt-extract.lab
```
