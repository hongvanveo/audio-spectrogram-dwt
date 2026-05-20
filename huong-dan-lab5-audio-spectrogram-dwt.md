# Hướng dẫn thực hành Lab 5: audio-spectrogram-dwt

Tài liệu này áp dụng cho:

- Lab 5: `audio-spectrogram-dwt`

Lưu ý chung:

- Bài lab dùng một container duy nhất.
- Sinh viên tạo audio gốc `cover.wav`, tạo ảnh bí mật `secret.png`, sau đó nhúng ảnh vào audio.
- Ảnh bí mật được hoán vị ngẫu nhiên bằng một khóa chia sẻ, sau đó được xem như một spectrogram và dùng Inverse STFT để biến thành tín hiệu miền thời gian.
- Audio gốc được phân rã bằng DWT nhiều mức, rồi tín hiệu bí mật được ghi đè trực tiếp vào nhóm hệ số chi tiết ở mức phân rã cuối.
- Sau khi nhúng, chương trình dùng IDWT để tạo audio stego `stego.wav`.
- Nếu sinh viên muốn làm lại từ đầu, dùng:

```bash
labtainer -r audio-spectrogram-dwt
```

## Lab 5: audio-spectrogram-dwt

### Tải bài lab

```bash
imodule https://github.com/hongvanveo/audio-spectrogram-dwt/raw/refs/heads/main/imodule_audio-spectrogram-dwt.tar
```

### Khởi động bài lab

Vào terminal, gõ:

```bash
labtainer -r audio-spectrogram-dwt
```

Chú ý: sinh viên sử dụng mã sinh viên của mình để nhập thông tin email/người thực hiện bài lab khi có yêu cầu. Hệ thống sẽ tự chuẩn hoá mã đó sang dạng IN HOA và ghi nhớ ID gần nhất.

`checkwork` chỉ hiển thị và chấm kết quả của đúng ID đang được dùng cho bài lab hiện tại, không trộn với các file `.lab` cũ của ID khác.

Sau khi khởi động xong, trong thư mục `~/stego` có các file hỗ trợ thực hành, ví dụ:

```text
generate_cover.py
generate_secret_image.py
spectrogram_dwt_stego.py
embed_task.py
analyze_audio.py
refresh_status.py
```

### Mục tiêu bài lab

Sinh viên cần:

1. Tạo file audio gốc `cover.wav`.
2. Tạo ảnh bí mật `secret.png`.
3. Sửa file `embed_task.py`, điền đúng tên file audio gốc và ảnh bí mật.
4. Chạy chương trình nhúng tin để tạo `stego.wav`.
5. Kiểm tra `stego.wav` đã được tạo và khác `cover.wav`.
6. Chạy `checkwork` để kiểm tra kết quả.

### Nội dung kỹ thuật

Quy trình nhúng tin của bài lab:

```text
Ảnh bí mật
→ hoán vị ngẫu nhiên bằng key
→ xem như spectrogram
→ Inverse STFT
→ tín hiệu miền thời gian
→ DWT audio gốc
→ nhúng vào hệ số tần số cao
→ IDWT
→ audio stego
```

Ý nghĩa các bước:

- `secret.png`: ảnh bí mật cần nhúng.
- Hoán vị bằng key: trộn vị trí các điểm ảnh bằng khóa dùng chung giữa bên gửi và bên nhận.
- Spectrogram: biểu diễn ảnh như một ma trận biên độ tần số-thời gian.
- Inverse STFT: biến spectrogram thành tín hiệu miền thời gian.
- DWT nhiều mức: phân rã audio gốc thành hệ số xấp xỉ và các hệ số chi tiết qua nhiều mức.
- Ghi đè hệ số chi tiết: dùng tín hiệu bí mật để thay trực tiếp hệ số chi tiết ở mức phân rã cuối.
- IDWT: tái tạo lại audio sau khi đã nhúng tin.

### Task 1: Tạo file audio gốc

Trong terminal của lab, gõ:

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav
```

Kiểm tra file đã được tạo:

```bash
ls -l cover.wav
```

### Task 2: Tạo ảnh bí mật

Trong terminal của lab, gõ:

```bash
python3 generate_secret_image.py --out secret.png
```

Kiểm tra file ảnh đã được tạo:

```bash
ls -l secret.png
```

Nếu muốn xem nhanh thông tin file ảnh, có thể dùng:

```bash
file secret.png
```

### Task 3: Sửa code để điền tên file audio, ảnh bí mật và kiểm tra khóa

Mở file `embed_task.py`:

```bash
nano embed_task.py
```

Tìm các dòng TODO:

```python
COVER_FILE = "TODO_COVER_FILENAME"
SECRET_IMAGE = "TODO_SECRET_IMAGE_FILENAME"
```

Sửa thành:

```python
COVER_FILE = "cover.wav"
SECRET_IMAGE = "secret.png"
```

Trong file cũng có sẵn:

```python
PERMUTATION_KEY = 3101
```

Sinh viên giữ nguyên khóa này để dùng cho bước hoán vị ảnh trước khi nhúng.

Lưu file và thoát khỏi `nano`.

### Task 4: Chạy chương trình nhúng tin

Trong terminal của lab, gõ:

```bash
python3 embed_task.py
```

Lệnh này sẽ gọi `spectrogram_dwt_stego.py` để:

1. Đọc ảnh `secret.png`.
2. Hoán vị ảnh bằng khóa chia sẻ.
3. Chuẩn hóa ảnh thành ma trận spectrogram.
4. Dùng Inverse STFT để tạo tín hiệu miền thời gian từ ảnh.
5. Dùng DWT nhiều mức để tách `cover.wav` thành hệ số xấp xỉ và các hệ số chi tiết.
6. Ghi đè hệ số chi tiết ở mức cuối bằng tín hiệu bí mật đã scale.
7. Dùng IDWT để tạo file `stego.wav`.

Kiểm tra file kết quả:

```bash
ls -l stego.wav
```

### Task 5: Kiểm tra sự thay đổi giữa cover và stego

Gõ lệnh:

```bash
python3 analyze_audio.py --cover cover.wav --stego stego.wav
```

Có thể kiểm tra thêm bằng lệnh:

```bash
cmp cover.wav stego.wav
```

Nếu hai file khác nhau, điều đó chứng tỏ ảnh bí mật đã được nhúng vào audio.

### Task 6: Nghe thử audio stego

Nếu môi trường hỗ trợ phát âm thanh, sinh viên có thể nghe thử:

```bash
aplay stego.wav
```

Nếu môi trường không hỗ trợ phát âm thanh, chỉ cần kiểm tra file bằng `ls`, `file` và `analyze_audio.py`.

### Kiểm tra kết quả

Trên terminal chính của lab, gõ:

```bash
checkwork
```

Kết quả đúng cần có:

```text
Y - cover_created
Y - secret_image_created
Y - image_processed
Y - istft_signal_created
Y - dwt_highfreq_embedded
Y - stego_created
Y - audio_modified
```

Ý nghĩa các mục chấm:

- `cover_created`: đã tạo file audio gốc `cover.wav`.
- `secret_image_created`: đã tạo file ảnh bí mật `secret.png`.
- `image_processed`: ảnh bí mật đã được đọc, hoán vị bằng khóa và chuẩn hóa để dùng như spectrogram.
- `istft_signal_created`: đã dùng Inverse STFT để biến spectrogram từ ảnh thành tín hiệu miền thời gian.
- `dwt_highfreq_embedded`: đã dùng DWT nhiều mức trên audio gốc và ghi đè tín hiệu bí mật vào hệ số chi tiết của mức phân rã cuối.
- `stego_created`: đã chạy chương trình nhúng tin và tạo `stego.wav`.
- `audio_modified`: `stego.wav` khác `cover.wav`, chứng tỏ quá trình nhúng đã làm thay đổi tín hiệu audio.

### Kết thúc bài lab

Trên terminal chính, gõ:

```bash
stoplab audio-spectrogram-dwt
```

Kết quả sẽ được lưu tại:

```bash
/home/student/labtainer_xfer/audio-spectrogram-dwt
```

Tên file bài làm sẽ có dạng:

```text
B22DCAT311.audio-spectrogram-dwt.lab
```
