# Quản Lý Tài Khoản Ngân Hàng

Chương trình quản lý tài khoản ngân hàng chạy trên giao diện dòng lệnh (CLI), viết bằng Python. Hỗ trợ tạo tài khoản, đăng nhập, nạp/rút/chuyển tiền, gửi tiết kiệm và tra cứu lịch sử giao dịch. Dữ liệu được lưu bền vững dưới dạng file JSON, đọc/ghi bằng parser tự cài đặt (không dùng thư viện `json` của Python).

## Yêu cầu

- Python 3.10 trở lên (chương trình dùng cú pháp `match/case`).
- Không cần cài thêm thư viện ngoài — toàn bộ chỉ dùng thư viện chuẩn của Python.

## Cách chạy

```bash
python3 main.py
```

(Trên Windows dùng `python main.py`.)

## Cấu trúc dự án

```
main.py                     Điểm khởi đầu, menu chính
Kiem_tra.py                 Các hàm xác thực đầu vào (SĐT, mật khẩu, email, tên...)
Tao_tai_khoan.py            Luồng tạo tài khoản mới
Dang_nhap.py                Đăng nhập và menu dịch vụ sau đăng nhập
Giao_dich.py                Nạp tiền, rút tiền, chuyển khoản
Tiet_kiem.py                Gửi/tất toán sổ tiết kiệm
Luu_du_lieu.py              Cấu trúc dữ liệu tài khoản & BankDatabase
Luu_lich_su_giao_dich.py    Ghi và đọc lịch sử giao dịch
Truy_xuat_giao_dich.py      Tra cứu lịch sử giao dịch
Du_lieu.json                Dữ liệu tài khoản (tự tạo khi chạy lần đầu)
Lich_su.json                Lịch sử giao dịch (tự tạo khi chạy lần đầu)
Tiet_kiem.json              Danh sách sổ tiết kiệm (tự tạo khi chạy lần đầu)
```

Ba file `.json` không cần tạo sẵn — chương trình tự sinh file rỗng khi chạy lần đầu nếu chưa tồn tại.

## Hướng dẫn sử dụng

Khi khởi động, chương trình hiện menu chính:

```
1. Dang nhap
2. Tao tai khoan
3. Thoat
```

**1. Tạo tài khoản** — nhập theo thứ tự: số điện thoại (10 số, bắt đầu bằng 0), mật khẩu (≥ 8 ký tự, có chữ hoa/thường/số/ký tự đặc biệt), xác nhận mật khẩu, CCCD/CMND (12 số), họ tên (chỉ chữ và dấu cách), mã PIN (6 số), phần đầu email (trước `@gmail.com`). Nếu số điện thoại đã tồn tại, chương trình báo lỗi và dừng ngay, không hỏi tiếp các trường khác.

**2. Đăng nhập** — nhập số điện thoại và mật khẩu. Sai liên tiếp 5 lần trong cùng một phiên đăng nhập sẽ bị tạm ngừng cho thử tiếp (không phải khóa vĩnh viễn — gọi lại chức năng đăng nhập sẽ được thử lại từ đầu).

Sau khi đăng nhập thành công, menu dịch vụ hiện ra:

```
1. Nap tien
2. Rut tien
3. Chuyen khoan
4. Gui tiet kiem
5. Truy xuat giao dich
6. Dang xuat
```

- **Nạp/Rút tiền**: nhập số tiền (số nguyên dương). Rút tiền sẽ kiểm tra số dư trước khi thực hiện.
- **Chuyển khoản**: nhập số tài khoản người nhận (8 số), số tiền và nội dung chuyển khoản.
- **Gửi tiết kiệm**: cần xác thực mã PIN (tối đa 3 lần thử) trước khi mở sổ, xem danh sách sổ hoặc tất toán. Lãi suất áp dụng: 0,1%/tháng, không kỳ hạn.
- **Truy xuất giao dịch**: xem toàn bộ lịch sử, hoặc tìm theo mã giao dịch / khoảng ngày / từ khóa nội dung / kết hợp nhiều tiêu chí.

Mọi thay đổi được ghi xuống file ngay sau khi giao dịch hoàn tất, nên không cần thao tác lưu thủ công.

## Kiểm tra hiệu năng (tuỳ chọn)

Repo có thêm 3 file phục vụ đo hiệu năng với dữ liệu lớn, không cần thiết để chạy chương trình chính:

```bash
python3 chay_kiem_tra_toan_bo.py
```

Script này tự sinh dữ liệu giả ở 3 mức (100 / 500 / 1000 tài khoản), đo thời gian đọc file, tìm kiếm, giao dịch, tính lãi tiết kiệm..., rồi **tự động khôi phục lại `Du_lieu.json`, `Lich_su.json`, `Tiet_kiem.json` ban đầu** sau khi chạy xong (kể cả khi có lỗi xảy ra giữa lúc test), nên có thể chạy an toàn mà không lo mất dữ liệu thật đang có.

Có thể chạy riêng từng phần nếu cần:
- `tao_du_lieu_lon.py` — chỉ sinh dữ liệu giả.
- `kiem_tra_hieu_nang.py` — chỉ đo hiệu năng trên dữ liệu hiện có.
