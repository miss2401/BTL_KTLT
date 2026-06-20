import random
import os
from datetime import datetime, timedelta, date

def tao_so_dien_thoai():
    return '0' + ''.join([str(random.randint(0, 9)) for _ in range(9)])

def tao_ho_ten():
    ho      = ['Nguyen', 'Tran', 'Le', 'Pham', 'Hoang', 'Vu', 'Dang', 'Bui', 'Do', 'Ho']
    ten_dem = ['Van', 'Thi', 'Duc', 'Minh', 'Thanh', 'Thu', 'Quang', 'Tuan', 'Anh', 'Hai']
    ten     = ['An', 'Binh', 'Cuong', 'Dung', 'Hoa', 'Khang', 'Linh', 'Mai', 'Nam', 'Phuc']
    return f"{random.choice(ho)} {random.choice(ten_dem)} {random.choice(ten)}"

def tao_email(sdt):
    return f"user_{sdt}@gmail.com"

def tao_mat_khau():
    # Mật khẩu gồm 1 chữ thường, 1 chữ hoa, 1 số, 1 ký tự đặc biệt, và 4 ký tự ngẫu nhiên khác
    chu_thuong = random.choice('abcdefghijklmnopqrstuvwxyz')
    chu_hoa    = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    so         = random.choice('0123456789')
    dac_biet   = random.choice('!#$%&@')
    them = ''.join([random.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ) for _ in range(4)])
    mk = list(chu_thuong + chu_hoa + so + dac_biet + them)
    random.shuffle(mk)
    return ''.join(mk)

def tao_cccd(sdt):
    return sdt + ''.join([str(random.randint(0, 9)) for _ in range(2)])

def tao_ma_pin():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def tao_so_tai_khoan(existing):
    while True:
        stk = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        if stk not in existing:
            existing.add(stk)
            return stk

def tao_ngay_ngau_nhien(ngay_truoc=365):
    #Tạo ngày ngẫu nhiên
    d = date.today() - timedelta(days=random.randint(0, ngay_truoc))
    return d.strftime("%Y-%m-%d")

def tao_du_lieu_tai_khoan(so_luong):

    existing_stk = set()
    existing_sdt = set()
    dong = []

    for i in range(so_luong):
        while True:
            sdt = tao_so_dien_thoai()
            if sdt not in existing_sdt:
                existing_sdt.add(sdt)
                break
        stk = tao_so_tai_khoan(existing_stk)
        so_du = random.randint(100000, 100000000)

        user_str = (
            f'    "{sdt}": {{\n'
            f'        "ho_ten": "{tao_ho_ten()}",\n'
            f'        "mat_khau": "{tao_mat_khau()}",\n'
            f'        "email": "{tao_email(sdt)}",\n'
            f'        "cccd": "{tao_cccd(sdt)}",\n'
            f'        "so_tai_khoan": "{stk}",\n'
            f'        "so_du": {so_du},\n'
            f'        "ma_pin": "{tao_ma_pin()}"\n'
            f'    }}'
        )
        dong.append(user_str)

        if (i + 1) % 100 == 0:
            print(f"  Du_lieu: {i+1}/{so_luong} tai khoan...")

    chuoi_json = "{\n" + ",\n".join(dong) + "\n}"
    with open("Du_lieu.json", "w", encoding="utf-8") as f:
        f.write(chuoi_json)

    print(f"  => Da ghi Du_lieu.json ({so_luong} tai khoan)")
    return existing_sdt

# --------------------------------------------------------------- Lich_su.json --

def tao_lich_su_giao_dich(danh_sach_sdt, so_tk_co_ls=None):

    sdt_list = list(danh_sach_sdt)
    if so_tk_co_ls is None:
        so_tk_co_ls = min(100, len(sdt_list))

    loai_gd = ['NAP TIEN', 'RUT TIEN', 'CHUYEN KHOAN', 'TIETKIEM']
    dong = []

    for i, sdt in enumerate(sdt_list[:so_tk_co_ls]):
        so_gd = random.randint(10, 50)
        entries = []
        for j in range(so_gd):
            ngay = datetime.now() - timedelta(days=random.randint(0, 365))
            ts = ngay.strftime('%Y%m%d_%H%M%S')
            ma_gd = f"GD{ts}_{str(j).zfill(3)}"
            so_tien = random.randint(10000, 5000000)
            loai = random.choice(loai_gd)
            if loai == 'CHUYEN KHOAN' and len(sdt_list) > 1:
                sdt_nhan = random.choice([s for s in sdt_list if s != sdt])
            else:
                sdt_nhan = loai  # NAP TIEN, RUT TIEN, TIETKIEM
            entries.append(f"{ma_gd}|{sdt}|{sdt_nhan}|{so_tien}|{loai}")

        lich_su_str = ',\n            '.join([f'"{e}"' for e in entries])
        user_str = (
            f'    "{sdt}": {{\n'
            f'        "lich_su": [\n'
            f'            {lich_su_str}\n'
            f'        ]\n'
            f'    }}'
        )
        dong.append(user_str)

        if (i + 1) % 20 == 0:
            print(f"  Lich_su: {i+1}/{so_tk_co_ls} tai khoan...")

    chuoi_json = "{\n" + ",\n".join(dong) + "\n}"
    with open("Lich_su.json", "w", encoding="utf-8") as f:
        f.write(chuoi_json)

    print(f"  => Da ghi Lich_su.json ({so_tk_co_ls} tai khoan co lich su)")

def tao_tiet_kiem(danh_sach_sdt, so_tk_co_so=None):
    
    sdt_list = list(danh_sach_sdt)
    if so_tk_co_so is None:
        so_tk_co_so = min(200, len(sdt_list))

    ma_so_da_dung = set()
    items = []

    for sdt in sdt_list[:so_tk_co_so]:
        # Mỗi tài khoản có 1–3 sổ, một số đã tất toán
        so_so = random.randint(1, 3)
        for _ in range(so_so):
            while True:
                ma_so = "STK" + str(random.randint(100000, 999999))
                if ma_so not in ma_so_da_dung:
                    ma_so_da_dung.add(ma_so)
                    break
            so_tien = random.randint(100000, 10000000)
            ngay_gui = tao_ngay_ngau_nhien(ngay_truoc=500)
            trang_thai = random.choice([1, 1, 1, 0])  # ~75% còn hoạt động

            item_str = (
                f'  {{\n'
                f'    "ma_so": "{ma_so}",\n'
                f'    "so_dien_thoai": "{sdt}",\n'
                f'    "so_tien_gui": {so_tien},\n'
                f'    "ky_han": 0,\n'
                f'    "ngay_gui": "{ngay_gui}",\n'
                f'    "lai_suat": 0.1,\n'
                f'    "trang_thai": {trang_thai}\n'
                f'  }}'
            )
            items.append(item_str)

    chuoi_json = "[\n" + ",\n".join(items) + "\n]"
    with open("Tiet_kiem.json", "w", encoding="utf-8") as f:
        f.write(chuoi_json)

    print(f"  => Da ghi Tiet_kiem.json ({len(items)} so, {so_tk_co_so} tai khoan)")

def tao_du_lieu_lon(so_luong_tai_khoan=1000):
    """Tạo đồng bộ cả 3 file: Du_lieu.json, Lich_su.json, Tiet_kiem.json"""
    print(f"Dang tao {so_luong_tai_khoan} tai khoan...")

    danh_sach_sdt = tao_du_lieu_tai_khoan(so_luong_tai_khoan)

    print("Dang tao lich su giao dich...")
    tao_lich_su_giao_dich(danh_sach_sdt)

    print("Dang tao so tiet kiem...")
    tao_tiet_kiem(danh_sach_sdt)

    print(f"Hoan thanh! {so_luong_tai_khoan} tai khoan, lich su, va so tiet kiem da san sang.\n")
    return danh_sach_sdt


if __name__ == "__main__":
    for so_luong in [100, 500, 1000]:
        print(f"\n{'='*50}")
        print(f"Tao {so_luong} tai khoan...")
        tao_du_lieu_lon(so_luong)
