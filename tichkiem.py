import os
import random
import json
import datetime
from data import BankDatabase
from luulichsugiaodich import LichSuGiaoDich

class SoTietKiem:
    def __init__(self, ma_so, so_dien_thoai, so_tien_gui, ky_han, ngay_gui, lai_suat, trang_thai):
        self.ma_so = ma_so
        self.so_dien_thoai = str(so_dien_thoai)
        self.so_tien_gui = int(so_tien_gui)
        self.ky_han = int(ky_han)          
        self.ngay_gui = ngay_gui            
        self.lai_suat = float(lai_suat)    
        self.trang_thai = int(trang_thai)  
class QuanLyTichKiem:
    def __init__(self, db_file="tichkiem.json"):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _doc_file(self):
        """Đọc danh sách sổ tiết kiếm từ file JSON"""
        danh_sach_so = []
        if not os.path.exists(self.db_file):
            return danh_sach_so
        
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Chuyển đổi từ dict thành SoTietKiem objects
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
                danh_sach_so.append(so)
        except (json.JSONDecodeError, IOError):
            pass
        
        return danh_sach_so

    def _ghi_file(self, danh_sach_so):
        """Ghi danh sách sổ tiết kiếm vào file JSON"""
        data = []
        for so in danh_sach_so:
            data.append({
                "ma_so": so.ma_so,
                "so_dien_thoai": so.so_dien_thoai,
                "so_tien_gui": so.so_tien_gui,
                "ky_han": so.ky_han,
                "ngay_gui": so.ngay_gui,
                "lai_suat": so.lai_suat,
                "trang_thai": so.trang_thai
            })
        
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def tinh_lai_suat(self, so_tien_gui, ngay_gui_str):
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
        tien_lai = so_tien_gui * (lai_suat_thang / 100) * so_thang
        return int(tien_lai)


def mo_so_tiet_kiem(tai_khoan_dang_nhap):
    print("Lai suat hien hanh: 0.1% / thang")
    print("So du tai khoan goc hien tai cua ban:", tai_khoan_dang_nhap.so_du, "VND")    
    try:
        so_tien_gui = int(input("Nhap so tien muon gui tiet kiem (VND): "))
    except:
        print("So tien phai la so nguyen!")
        return
    if so_tien_gui <= 0:
        print("So tien gui phai lon hon 0!")
        return
    if so_tien_gui > tai_khoan_dang_nhap.so_du:
        print("So du tai khoan khong du de thuc hien giao dich nay!")
        return
    db_bank = BankDatabase()
    danh_sach_tk = db_bank._doc_file()
    tim_thay = False
    for i in range(len(danh_sach_tk)):
        if danh_sach_tk[i].so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai:
            danh_sach_tk[i].so_du -= so_tien_gui
            tai_khoan_dang_nhap.so_du = danh_sach_tk[i].so_du
            tim_thay = True
            break            
    if not tim_thay:
        print("Loi: Khong tim thay thong tin tai khoan dong bo!")
        return
    db_bank._ghi_file(danh_sach_tk)
    ql_tk = QuanLyTichKiem()
    danh_sach_so = ql_tk._doc_file() 
    ma_so_stk = "STK" + str(random.randint(100000, 999999))
    ngay_hom_nay = datetime.date.today().strftime("%Y-%m-%d")
    so_moi = SoTietKiem(ma_so_stk, tai_khoan_dang_nhap.so_dien_thoai, so_tien_gui, 0, ngay_hom_nay, 0.1, 1)
    danh_sach_so.append(so_moi)
    ql_tk._ghi_file(danh_sach_so)
    try:
        ls = LichSuGiaoDich()
        ls.ghi_nhan_giao_dich(tai_khoan_dang_nhap.so_dien_thoai, "SO_TIET_KIEM", so_tien_gui, "Mo so tiet kiem khong ky han " + ma_so_stk)
    except:
        pass
    print("Mo so tiet kiem thanh cong! Ma so:", ma_so_stk)
    print("So du con lai trong tai khoan chinh:", tai_khoan_dang_nhap.so_du, "VND")


def xem_danh_sach_so(tai_khoan_dang_nhap):
    ql_tk = QuanLyTichKiem()
    danh_sach_so = ql_tk._doc_file()  
    dem_so = 0
    for so in danh_sach_so:
        if so.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai and so.trang_thai == 1:
            dem_so += 1
            lai_tam_tinh = ql_tk.tinh_lai_suat(so.so_tien_gui, so.ngay_gui)
            print(str(dem_so) + ". Ma so: " + so.ma_so + " | Tien gui: " + str(so.so_tien_gui) + " VND | Loai: Khong ky han | Ngay gui: " + so.ngay_gui + " | Lai suat: 0.1%/thang | Lai tam tinh: " + str(lai_tam_tinh) + " VND")           
    if dem_so == 0:
        print("Ban khong co so tiet kiem nao dang hoat dong.")
    return dem_so


def tat_toan_so_tiet_kiem(tai_khoan_dang_nhap):
    ql_tk = QuanLyTichKiem()
    danh_sach_so = ql_tk._doc_file()   
    dem_so = xem_danh_sach_so(tai_khoan_dang_nhap)
    if dem_so == 0:
        return       
    ma_so_nhap = input("Nhap Ma so tiet kiem muon tat toan: ")
    tim_thay_so = False
    for so in danh_sach_so:
        if so.ma_so == ma_so_nhap and so.so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai and so.trang_thai == 1:
            tim_thay_so = True
            tien_goc = so.so_tien_gui
            tien_lai = ql_tk.tinh_lai_suat(tien_goc, so.ngay_gui)
            tong_nhan = tien_goc + tien_lai        
            so.trang_thai = 0
            ql_tk._ghi_file(danh_sach_so)           
            db_bank = BankDatabase()
            danh_sach_tk = db_bank._doc_file()
            for j in range(len(danh_sach_tk)):
                if danh_sach_tk[j].so_dien_thoai == tai_khoan_dang_nhap.so_dien_thoai:
                    danh_sach_tk[j].so_du += tong_nhan
                    tai_khoan_dang_nhap.so_du = danh_sach_tk[j].so_du
                    break
            db_bank._ghi_file(danh_sach_tk)          
            try:
                ls = LichSuGiaoDich()
                ls.ghi_nhan_giao_dich("SO_TIET_KIEM", tai_khoan_dang_nhap.so_dien_thoai, tong_nhan, "Tat toan so tiet kiem khong ky han " + ma_so_nhap + " (Goc: " + str(tien_goc) + ", Lai: " + str(tien_lai) + ")")
            except:
                pass               
            print("Tat toan thanh cong so tiet kiem " + ma_so_nhap)
            print("Tien goc nhan: " + str(tien_goc) + " VND")
            print("Tien lai nhan: " + str(tien_lai) + " VND")
            print("Tong so tien da duoc cong vao tai khoan chinh. So du moi: " + str(tai_khoan_dang_nhap.so_du) + " VND")
            break           
    if not tim_thay_so:
        print("Khong tim thay so tiet kiem hop le hop voi ma so tren!")
def menu_tich_kiem(tai_khoan_dang_nhap):
    while True:
        print("1. Mo so tiet kiem moi (Khong ky han)")
        print("2. Xem danh sach so tiet kiem")
        print("3. Tat toan so tiet kiem (Rut tien)")
        print("4. Quay lai menu truoc")
        
        lua_chon = input("Nhap lua chon cua ban (1-4): ")
        if lua_chon == "1":
            mo_so_tiet_kiem(tai_khoan_dang_nhap)
        elif lua_chon == "2":
            xem_danh_sach_so(tai_khoan_dang_nhap)
        elif lua_chon == "3":
            tat_toan_so_tiet_kiem(tai_khoan_dang_nhap)
        elif lua_chon == "4":
            break
        else:
            print("Lua chon khong hop le, vui long nhap lai!")