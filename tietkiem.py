import os
import random
import json
import datetime
from check import Kiem_tra_email, Kiem_tra_sdt_ton_tai, Kiem_tra_so, Kiem_tra_ten, check_mat_khau
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.size += 1

    def get_head(self):
        return self.head

    def iterate(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next
    def find_first(self, condition_func):
        cur = self.head
        while cur:
            if condition_func(cur.data):
                return cur.data
            cur = cur.next
        return None

    def update_first(self, condition_func, new_data):
        cur = self.head
        while cur:
            if condition_func(cur.data):
                cur.data = new_data
                return True
            cur = cur.next
        return False

    def to_json_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    @staticmethod
    def from_json_list(lst):
        ll = LinkedList()
        for item in lst:
            ll.append(item)
        return ll
class SoTietKiem:
    def __init__(self, ma_so, so_dien_thoai, so_tien_gui, ky_han, ngay_gui, lai_suat, trang_thai):
        self.ma_so = ma_so
        self.so_dien_thoai = str(so_dien_thoai)
        self.so_tien_gui = int(so_tien_gui)
        self.ky_han = int(ky_han)
        self.ngay_gui = ngay_gui
        self.lai_suat = float(lai_suat)
        self.trang_thai = int(trang_thai)
class TaiKhoan:
    def __init__(self, ho_ten, so_dien_thoai, mat_khau, email, cccd, so_tai_khoan, so_du, ma_pin):
        self.ho_ten = ho_ten
        self.so_dien_thoai = str(so_dien_thoai)
        self.mat_khau = mat_khau
        self.email = email
        self.cccd = cccd
        self.so_tai_khoan = so_tai_khoan
        self.so_du = int(so_du)
        self.ma_pin = str(ma_pin)
class QuanLyTietKiem:
    def __init__(self, db_file="tichkiem.json"):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    def _doc_file(self):
        if not os.path.exists(self.db_file):
            return LinkedList()
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)   
            ll = LinkedList()
            for item in data:
                so = SoTietKiem(
                    item.get("ma_so"),
                    item.get("so_dien_thoai"),
                    item.get("so_tien_gui"),
                    item.get("ky_han"),
                    item.get("ngay_gui"),
                    item.get("lai_suat"),
                    item.get("trang_thai")
                )
                ll.append(so)
            return ll
        except:
            return LinkedList()
    def _ghi_file(self, danh_sach_so):
        data = []
        cur = danh_sach_so.get_head()
        while cur:
            so = cur.data
            data.append({
                "ma_so": so.ma_so,
                "so_dien_thoai": so.so_dien_thoai,
                "so_tien_gui": so.so_tien_gui,
                "ky_han": so.ky_han,
                "ngay_gui": so.ngay_gui,
                "lai_suat": so.lai_suat,
                "trang_thai": so.trang_thai
            })
            cur = cur.next
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def tinh_lai_suat(self, so_tien_gui, ngay_gui_str):
        """Tính lãi suất không kỳ hạn (0.1%/thang)"""
        try:
            ngay_gui = datetime.datetime.strptime(ngay_gui_str, "%Y-%m-%d").date()
        except:
            ngay_gui = datetime.date.today()
        ngay_hien_tai = datetime.date.today()
        so_ngay = (ngay_hien_tai - ngay_gui).days
        if so_ngay < 0:
            so_ngay = 0
        so_thang = so_ngay // 30
        lai_suat_thang = 0.1
        return int(so_tien_gui * (lai_suat_thang / 100) * so_thang)

def doc_tai_khoan_tu_data():
    if not os.path.exists("data.json"):
        return LinkedList()
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            du_lieu = json.load(f)   # du_lieu là dict {sdt: {...}}
        ll = LinkedList()
        for sdt, info in du_lieu.items():
            tk = TaiKhoan(
                ho_ten=info.get("ho_ten", ""),
                so_dien_thoai=sdt,
                mat_khau=info.get("mat_khau", ""),
                email=info.get("email", ""),
                cccd=info.get("cccd", ""),
                so_tai_khoan=info.get("so_tai_khoan", ""),
                so_du=info.get("so_du", 0),
                ma_pin=info.get("ma_pin", "")
            )
            ll.append(tk)
        return ll
    except:
        return LinkedList()

def ghi_tai_khoan_vao_data(danh_sach_tk):
    du_lieu = {}
    cur = danh_sach_tk.get_head()
    while cur:
        tk = cur.data
        du_lieu[tk.so_dien_thoai] = {
            "ho_ten": tk.ho_ten,
            "mat_khau": tk.mat_khau,
            "email": tk.email,
            "cccd": tk.cccd,
            "so_tai_khoan": tk.so_tai_khoan,
            "so_du": tk.so_du,
            "ma_pin": tk.ma_pin
        }
        cur = cur.next
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=4)
def xac_thuc_pin(tai_khoan, so_lan_toi_da=3):
    pin_he_thong = tai_khoan.ma_pin
    if not pin_he_thong:
        print("Khong tim thay ma PIN!")
        return False
    so_lan = 0
    while so_lan < so_lan_toi_da:
        pin_nhap = input(f"Nhap PIN giao dich (con {so_lan_toi_da - so_lan} lan thu): ").strip()
        if pin_nhap == pin_he_thong:
            print("Xac thuc thanh cong\n")
            return True
        else:
            so_lan += 1
            if so_lan < so_lan_toi_da:
                print(f"PIN sai! Con {so_lan_toi_da - so_lan} lan thu.")
            else:
                print("Sai PIN qua 3 lan. Giao dịch bi huy!")
    return False

def ghi_lich_su_giao_dich(sdt_gui, sdt_nhan, so_tien, noi_dung):
    now = datetime.datetime.now()
    timestamp = f"{now.year}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}{now.second:02d}_{now.microsecond//1000:03d}"
    ma_gd = f"GD{timestamp}_{random.randint(0,999):03d}"

    # Đọc history.json hiện tại
    if os.path.exists("history.json"):
        with open("history.json", "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = {}
    else:
        history = {}

    gd_str = f"{ma_gd}|{sdt_gui}|{sdt_nhan}|{so_tien}|{noi_dung}"

    # Thêm vào lịch sử của người gửi
    if sdt_gui not in history:
        history[sdt_gui] = {"lich_su": []}
    history[sdt_gui]["lich_su"].append(gd_str)

    # Thêm vào lịch sử của người nhận (nếu không phải tài khoản hệ thống)
    if sdt_nhan not in ("TIETKIEM", "NAP_TIEN", "RUT_TIEN") and sdt_nhan != sdt_gui:
        if sdt_nhan not in history:
            history[sdt_nhan] = {"lich_su": []}
        history[sdt_nhan]["lich_su"].append(gd_str)

    # Ghi lại vào history.json
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

    return ma_gd
def mo_so_tiet_kiem(tai_khoan_dang_nhap):
    if not xac_thuc_pin(tai_khoan_dang_nhap):
        return
    print("\nMO SO TIET KIEM MOI")
    print("Lai suat: 0.1%/thang (không ky han)")
    print(f"So du hien tai: {tai_khoan_dang_nhap.so_du} VND\n")
    try:
        so_tien = input("Nhap so tien gui: ")
        while(Kiem_tra_so(so_tien)):
            so_tien = input("Nhap so tien gui: ")
        so_tien = int(so_tien)
    except:
        print(" So tien không hop le!")
        return
    if so_tien <= 0:
        print(" So tien phai > 0!")
        return
    if so_tien > tai_khoan_dang_nhap.so_du:
        print(" So du khong đu!")
        return
    # Cập nhật số dư tài khoản (từ file data.json)
    ds_tk = doc_tai_khoan_tu_data()
    cap_nhat = False
    cur = ds_tk.get_head()
    while cur:
        if cur.data.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai:
            cur.data.so_du -= so_tien
            tai_khoan_dang_nhap.so_du = cur.data.so_du
            cap_nhat = True
            break
        cur = cur.next
    if not cap_nhat:
        print("Khong tim thay tai khoan!")
        return
    ghi_tai_khoan_vao_data(ds_tk)

    # Tạo sổ tiết kiệm
    ql = QuanLyTietKiem()
    ds_so = ql._doc_file()
    ma_so = "STK" + str(random.randint(100000, 999999))
    ngay_gui = datetime.date.today().strftime("%Y-%m-%d")
    so_moi = SoTietKiem(ma_so, tai_khoan_dang_nhap.so_dien_thoai, so_tien, 0, ngay_gui, 0.1, 1)
    ds_so.append(so_moi)
    ql._ghi_file(ds_so)

    # Ghi lịch sử giao dịch
    noi_dung = f"Mo so tiet kiem - Ma so: {ma_so} - So tien: {so_tien} VND"
    ghi_lich_su_giao_dich(tai_khoan_dang_nhap.so_dien_thoai, "TIETKIEM", so_tien, noi_dung)
    print("\n Mo so tiet kiem thanh cong!")
    print(f"  Ma so: {ma_so}")
    print(f"  So tien: {so_tien} VND")
    print(f"  Ngay gui: {ngay_gui}")
    print(f"  So du con lại: {tai_khoan_dang_nhap.so_du} VND\n")

def xem_danh_sach_so(tai_khoan_dang_nhap):
    ql = QuanLyTietKiem()
    ds_so = ql._doc_file()
    dem = 0
    print("\nDANH SACH SO TIET KIEM\n")
    cur = ds_so.get_head()
    while cur:
        so = cur.data
        if so.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai and so.trang_thai == 1:
            dem += 1
            lai = ql.tinh_lai_suat(so.so_tien_gui, so.ngay_gui)
            print(f"{dem}. Ma so: {so.ma_so}")
            print(f"   Tien gui: {so.so_tien_gui} VND")
            print(f"   Ngay gui: {so.ngay_gui}")
            print(f"   Lai tam tinh: {lai} VND\n")
        cur = cur.next
    if dem == 0:
        print("Ban chua co so tiet kiem nào.\n")
    return dem
def tat_toan_so_tiet_kiem(tai_khoan_dang_nhap):
    if not xac_thuc_pin(tai_khoan_dang_nhap):
        return
    ql = QuanLyTietKiem()
    ds_so = ql._doc_file()
    dem = xem_danh_sach_so(tai_khoan_dang_nhap)
    if dem == 0:
        return
    ma_so = input("Nhap ma so so muon tat toan: ")
    found = False
    cur = ds_so.get_head()
    while cur:
        so = cur.data
        if so.ma_so == ma_so and so.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai and so.trang_thai == 1:
            found = True
            tien_goc = so.so_tien_gui
            tien_lai = ql.tinh_lai_suat(tien_goc, so.ngay_gui)
            tong = tien_goc + tien_lai
            so.trang_thai = 0
            break
        cur = cur.next
    if not found:
        print("Khong tim thay so tiet kiem hop le!\n")
        return
    # Ghi lại danh sách sổ đã cập nhật
    ql._ghi_file(ds_so)
    # Cập nhật số dư tài khoản
    ds_tk = doc_tai_khoan_tu_data()
    cur = ds_tk.get_head()
    while cur:
        if cur.data.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai:
            cur.data.so_du += tong
            tai_khoan_dang_nhap.so_du = cur.data.so_du
            break
        cur = cur.next
    ghi_tai_khoan_vao_data(ds_tk)
    noi_dung = f"Tat toan so tiet kiem - Ma so: {ma_so} - Tien goc: {tien_goc} VND - Tien lai: {tien_lai} VND - Tong: {tong} VND"
    ghi_lich_su_giao_dich(tai_khoan_dang_nhap.so_dien_thoai, "TIETKIEM", tong, noi_dung)
    print("\n Tat toan thanh cong!")
    print(f"  Tien goc: {tien_goc} VND")
    print(f"  Tien lai: {tien_lai} VND")
    print(f"  Tong nhan: {tong} VND")
    print(f"  So du moi: {tai_khoan_dang_nhap.so_du} VND\n")
def menu_tich_kiem(tai_khoan_dang_nhap):
    while True:
        print("1. Mo so tiet kiem moi")
        print("2. Xem danh sách so")
        print("3. Tat toan so")
        print("4. Quay lại")
        chon = input("Nhap lua chon (1-4): ")
        if chon == "1":
            mo_so_tiet_kiem(tai_khoan_dang_nhap)
        elif chon == "2":
            xem_danh_sach_so(tai_khoan_dang_nhap)
        elif chon == "3":
            tat_toan_so_tiet_kiem(tai_khoan_dang_nhap)
        elif chon == "4":
            break
        else:
            print("Lua chon khong hop le!\n")