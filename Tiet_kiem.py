import os
import random
import datetime
from Kiem_tra import Kiem_tra_so
from Luu_lich_su_giao_dich import LichSuGiaoDich
class Node:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, du_lieu):
        node = Node(du_lieu)
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
            yield cur.du_lieu
            cur = cur.next

    def find_first(self, condition_func):
        cur = self.head
        while cur:
            if condition_func(cur.du_lieu):
                return cur.du_lieu
            cur = cur.next
        return None

    def update_first(self, condition_func, new_du_lieu):
        cur = self.head
        while cur:
            if condition_func(cur.du_lieu):
                cur.du_lieu = new_du_lieu
                return True
            cur = cur.next
        return False


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
    def __init__(self, db_file="Tiet_kiem.json"):
        self.db_file = db_file
        if not os.path.exists(self.db_file) or os.path.getsize(self.db_file) == 0:
            with open(self.db_file, "w", encoding="utf-8") as f:
                f.write("[]")

    def Doc_file(self):
        danh_sach_so = LinkedList()
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                chuoi_json = f.read()
        except Exception:
            return danh_sach_so
        chuois = []
        i = 0
        while i < len(chuoi_json):
            char = chuoi_json[i]
            if char == '"':
                chuoi_str = ""
                i += 1
                while i < len(chuoi_json) and chuoi_json[i] != '"':
                    chuoi_str = chuoi_str + chuoi_json[i]
                    i += 1
                chuois = chuois + [chuoi_str]
            elif char in (':', '{', '}', '[', ']', ','):
                chuois = chuois + [char]
            elif char in ('0','1','2','3','4','5','6','7','8','9','.'):
                num_str = ""
                while i < len(chuoi_json) and chuoi_json[i] in ('0','1','2','3','4','5','6','7','8','9','.'):
                    num_str = num_str + chuoi_json[i]
                    i += 1
                chuois = chuois + [num_str]
                continue
            i += 1

        t = 0
        while t < len(chuois):
            if chuois[t] == '{':
                # Khởi tạo giá trị mặc định
                ma_so = so_dien_thoai = ngay_gui = ""
                so_tien_gui = ky_han = trang_thai = 0
                lai_suat = 0.0

                t += 1
                while t < len(chuois) and chuois[t] != '}':
                    if t + 2 < len(chuois) and chuois[t+1] == ':':
                        key = chuois[t]
                        val = chuois[t+2]
                        if key == "ma_so":         ma_so        = val
                        elif key == "so_dien_thoai": so_dien_thoai = val
                        elif key == "ngay_gui":    ngay_gui     = val
                        elif key == "so_tien_gui": so_tien_gui  = int(val)
                        elif key == "ky_han":      ky_han       = int(val)
                        elif key == "trang_thai":  trang_thai   = int(val)
                        elif key == "lai_suat":    lai_suat     = float(val)
                        t += 3
                    else:
                        t += 1

                so_moi = SoTietKiem(ma_so, so_dien_thoai, so_tien_gui,
                                    ky_han, ngay_gui, lai_suat, trang_thai)
                danh_sach_so.append(so_moi)
            t += 1

        return danh_sach_so

    def Ghi_file(self, danh_sach_so):
        # Lắp ráp thủ công chuỗi JSON mảng
        chuoi_json = "[\n"
        cur = danh_sach_so.get_head()
        first = True
        while cur:
            so = cur.du_lieu
            item_str = (
                f'  {{\n'
                f'    "ma_so": "{so.ma_so}",\n'
                f'    "so_dien_thoai": "{so.so_dien_thoai}",\n'
                f'    "so_tien_gui": {so.so_tien_gui},\n'
                f'    "ky_han": {so.ky_han},\n'
                f'    "ngay_gui": "{so.ngay_gui}",\n'
                f'    "lai_suat": {so.lai_suat},\n'
                f'    "trang_thai": {so.trang_thai}\n'
                f'  }}'
            )
            if first:
                chuoi_json = chuoi_json + item_str
                first = False
            else:
                chuoi_json = chuoi_json + ",\n" + item_str
            cur = cur.next
        chuoi_json = chuoi_json + "\n]"
        with open(self.db_file, "w", encoding="utf-8") as f:
            f.write(chuoi_json)

    def Tinh_lai_suat(self, so_tien_gui, ngay_gui_str):
        # Tinh lai suat khong ky han (0.1%/thang)
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


def Doc_tai_khoan_tu_du_lieu():
    danh_sach_tk = LinkedList()
    if not os.path.exists("Du_lieu.json"):
        return danh_sach_tk
    try:
        with open("Du_lieu.json", "r", encoding="utf-8") as f:
            chuoi_json = f.read()
    except Exception:
        return danh_sach_tk

    chuois = []
    i = 0
    while i < len(chuoi_json):
        char = chuoi_json[i]
        if char == '"':
            chuoi_str = ""
            i += 1
            while i < len(chuoi_json) and chuoi_json[i] != '"':
                chuoi_str = chuoi_str + chuoi_json[i]
                i += 1
            chuois = chuois + [chuoi_str]
        elif char in (':', '{', '}', ','):
            chuois = chuois + [char]
        elif char in ('0','1','2','3','4','5','6','7','8','9'):
            num_str = ""
            while i < len(chuoi_json) and chuoi_json[i] in ('0','1','2','3','4','5','6','7','8','9'):
                num_str = num_str + chuoi_json[i]
                i += 1
            chuois = chuois + [num_str]
            continue
        i += 1

    t = 0
    while t < len(chuois):
        is_sdt = len(chuois[t]) == 10
        if is_sdt:
            for char in chuois[t]:
                if char not in ('0','1','2','3','4','5','6','7','8','9'):
                    is_sdt = False
                    break

        if is_sdt and (t + 2 < len(chuois)) and chuois[t+1] == ':' and chuois[t+2] == '{':
            sdt = chuois[t]
            ho_ten = mat_khau = email = cccd = so_tai_khoan = ma_pin = ""
            so_du = 0
            t += 3
            while t < len(chuois) and chuois[t] != '}':
                if t + 2 < len(chuois) and chuois[t+1] == ':':
                    key = chuois[t]
                    val = chuois[t+2]
                    if key == "ho_ten":       ho_ten       = val
                    elif key == "mat_khau":   mat_khau     = val
                    elif key == "email":      email        = val
                    elif key == "cccd":       cccd         = val
                    elif key == "so_tai_khoan": so_tai_khoan = val
                    elif key == "ma_pin":     ma_pin       = val
                    elif key == "so_du":      so_du        = int(val)
                    t += 3
                else:
                    t += 1
            tk = TaiKhoan(ho_ten, sdt, mat_khau, email, cccd,
                          so_tai_khoan, so_du, ma_pin)
            danh_sach_tk.append(tk)
        else:
            t += 1

    return danh_sach_tk


def Ghi_tai_khoan_vao_du_lieu(danh_sach_tk):
    chuoi_json = "{\n"
    cur = danh_sach_tk.get_head()
    first = True
    while cur:
        tk = cur.du_lieu
        user_str = (
            f'    "{tk.so_dien_thoai}": {{\n'
            f'        "ho_ten": "{tk.ho_ten}",\n'
            f'        "mat_khau": "{tk.mat_khau}",\n'
            f'        "email": "{tk.email}",\n'
            f'        "cccd": "{tk.cccd}",\n'
            f'        "so_tai_khoan": "{tk.so_tai_khoan}",\n'
            f'        "so_du": {tk.so_du},\n'
            f'        "ma_pin": "{tk.ma_pin}"\n'
            f'    }}'
        )
        if first:
            chuoi_json = chuoi_json + user_str
            first = False
        else:
            chuoi_json = chuoi_json + ",\n" + user_str
        cur = cur.next
    chuoi_json = chuoi_json + "\n}"
    with open("Du_lieu.json", "w", encoding="utf-8") as f:
        f.write(chuoi_json)


def Xac_thuc_pin(tai_khoan, so_lan_toi_da=3):
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
                print("Sai PIN qua 3 lan. Giao dich bi huy!")
    return False

def Ghi_lich_su_giao_dich(sdt_gui, sdt_nhan, so_tien, noi_dung):
    lich_su = LichSuGiaoDich()
    lich_su.Ghi_giao_dich(sdt_gui, sdt_nhan, so_tien, noi_dung)

def Mo_so_tiet_kiem(tai_khoan_dang_nhap):
    if not Xac_thuc_pin(tai_khoan_dang_nhap):
        return
    print("\nMO SO TIET KIEM MOI")
    print("Lai suat: 0.1%/thang (khong ky han)")
    print(f"So du hien tai: {tai_khoan_dang_nhap.so_du} VND\n")
    so_tien = input("Nhap so tien gui: ")
    while Kiem_tra_so(so_tien) or so_tien == "":
        so_tien = input("Nhap so tien gui: ")
    so_tien = int(so_tien)
    if so_tien <= 0:
        print(" So tien phai > 0!")
        return
    if so_tien > tai_khoan_dang_nhap.so_du:
        print(" So du khong du!")
        return

    # Cap nhat so du tai khoan
    ds_tk = Doc_tai_khoan_tu_du_lieu()
    cap_nhat = False
    cur = ds_tk.get_head()
    while cur:
        if cur.du_lieu.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai:
            cur.du_lieu.so_du -= so_tien
            tai_khoan_dang_nhap.so_du = cur.du_lieu.so_du
            cap_nhat = True
            break
        cur = cur.next
    if not cap_nhat:
        print("Khong tim thay tai khoan!")
        return
    Ghi_tai_khoan_vao_du_lieu(ds_tk)

    # Tao so tiet kiem
    ql = QuanLyTietKiem()
    ds_so = ql.Doc_file()
    ma_so = "STK" + str(random.randint(100000, 999999))
    ngay_gui = datetime.date.today().strftime("%Y-%m-%d")
    so_moi = SoTietKiem(ma_so, tai_khoan_dang_nhap.so_dien_thoai,
                        so_tien, 0, ngay_gui, 0.1, 1)
    ds_so.append(so_moi)
    ql.Ghi_file(ds_so)

    noi_dung = f"Mo so tiet kiem - Ma so: {ma_so} - So tien: {so_tien} VND"
    Ghi_lich_su_giao_dich(tai_khoan_dang_nhap.so_dien_thoai, "TIETKIEM", so_tien, noi_dung)
    print("\n Mo so tiet kiem thanh cong!")
    print(f"  Ma so: {ma_so}")
    print(f"  So tien: {so_tien} VND")
    print(f"  Ngay gui: {ngay_gui}")
    print(f"  So du con lai: {tai_khoan_dang_nhap.so_du} VND\n")


def Xem_danh_sach_so(tai_khoan_dang_nhap):
    ql = QuanLyTietKiem()
    ds_so = ql.Doc_file()
    dem = 0
    print("\nDANH SACH SO TIET KIEM\n")
    cur = ds_so.get_head()
    while cur:
        so = cur.du_lieu
        if so.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai and so.trang_thai == 1:
            dem += 1
            lai = ql.Tinh_lai_suat(so.so_tien_gui, so.ngay_gui)
            print(f"{dem}. Ma so: {so.ma_so}")
            print(f"   Tien gui: {so.so_tien_gui} VND")
            print(f"   Ngay gui: {so.ngay_gui}")
            print(f"   Lai tam tinh: {lai} VND\n")
        cur = cur.next
    if dem == 0:
        print("Ban chua co so tiet kiem nao.\n")
    return dem

def Tat_toan_so_tiet_kiem(tai_khoan_dang_nhap):
    if not Xac_thuc_pin(tai_khoan_dang_nhap):
        return
    ql = QuanLyTietKiem()
    ds_so = ql.Doc_file()
    dem = Xem_danh_sach_so(tai_khoan_dang_nhap)
    if dem == 0:
        return
    ma_so = input("Nhap ma so so muon tat toan: ")
    kiem_tra = False
    cur = ds_so.get_head()
    while cur:
        so = cur.du_lieu
        if (so.ma_so == ma_so and
                so.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai and
                so.trang_thai == 1):
            kiem_tra = True
            tien_goc = so.so_tien_gui
            tien_lai = ql.Tinh_lai_suat(tien_goc, so.ngay_gui)
            tong = tien_goc + tien_lai
            so.trang_thai = 0
            break
        cur = cur.next
    if not kiem_tra:
        print("Khong tim thay so tiet kiem hop le!\n")
        return
    ql.Ghi_file(ds_so)
    ds_tk = Doc_tai_khoan_tu_du_lieu()
    cur = ds_tk.get_head()
    while cur:
        if cur.du_lieu.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai:
            cur.du_lieu.so_du += tong
            tai_khoan_dang_nhap.so_du = cur.du_lieu.so_du
            break
        cur = cur.next
    Ghi_tai_khoan_vao_du_lieu(ds_tk)

    noi_dung = (f"Tat toan so tiet kiem - Ma so: {ma_so} - "
                f"Tien goc: {tien_goc} VND - Tien lai: {tien_lai} VND - "
                f"Tong: {tong} VND")
    Ghi_lich_su_giao_dich(tai_khoan_dang_nhap.so_dien_thoai, "TIETKIEM", tong, noi_dung)
    print("\n Tat toan thanh cong!")
    print(f"  Tien goc: {tien_goc} VND")
    print(f"  Tien lai: {tien_lai} VND")
    print(f"  Tong nhan: {tong} VND")
    print(f"  So du moi: {tai_khoan_dang_nhap.so_du} VND\n")

def Menu(tai_khoan_dang_nhap):
    while True:
        print("1. Mo so tiet kiem moi")
        print("2. Xem danh sach so")
        print("3. Tat toan so")
        print("4. Quay lai")
        chon = input("Nhap lua chon (1-4): ")
        if chon == "1":
            Mo_so_tiet_kiem(tai_khoan_dang_nhap)
        elif chon == "2":
            Xem_danh_sach_so(tai_khoan_dang_nhap)
        elif chon == "3":
            Tat_toan_so_tiet_kiem(tai_khoan_dang_nhap)
        elif chon == "4":
            break
        else:
            print("Lua chon khong hop le!\n")
