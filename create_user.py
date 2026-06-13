from data import BankDatabase as BD
from check import Kiem_tra_email, Kiem_tra_sdt_ton_tai, Kiem_tra_so, Kiem_tra_ten, check_mat_khau
class User:
    def __init__(self, sdt,  ho_ten, email, cccd, ma_pin, mat_khau):
        self.ho_ten = ho_ten
        self.sdt = sdt
        self.email = email
        self.cccd = cccd
        self.ma_pin = ma_pin
        self.mat_khau = mat_khau
def Create_user():
    sdt = input("So dien thoai: ")
    while(len(sdt) != 10 or sdt[0] != '0' or Kiem_tra_so(sdt)):
        sdt = input("Nhap lai so dien thoai: ")
    if Kiem_tra_sdt_ton_tai(sdt):
        print("So dien thoai nay da ton tai trong he thong! Vui long nhap so khac.")
        return
    mat_khau1 = input("Mat khau: ")
    while(len(mat_khau1) < 8 or check_mat_khau(mat_khau1)):
        print("Mat khau phai co it nhat 8 ki tu, co ket hop giua chu cai in hoa, chu so va ki tu dac biet")
        mat_khau1 = input("Nhap lai mat khau: ")
    mat_khau2 = input("Nhap lai mat khau: ")
    while(mat_khau1 != mat_khau2):
        print("Mat khau khong khop")
        mat_khau2 = input("Nhap lai mat khau: ")
    cccd = input("Nhap so CMND/CCCD: ")
    while(len(cccd) != 12 or cccd[0] != '0' or Kiem_tra_so(cccd)):
        cccd = input("Nhap lai CMND/CCCD: ")
    ten = input("Nhap ho va ten: ").title()
    while(len(ten) == 0 or Kiem_tra_ten(ten)):
        ten = input("Nhap lai ho va ten: ").title()
    ma_pin = input("Nhap ma pin: ")
    while(len(ma_pin) != 6 or Kiem_tra_so(ma_pin)):
        ma_pin = input("Nhap lai ma pin: ")
    email = input("Nhap email: ")
    while(Kiem_tra_email(email)):
        print("Email khong hop le! Khong duoc chua @, dau Viet, dau cach, hoac ky tu dac biet. Chi dung a-z, 0-9, . _ -")
        email = input("Nhap lai email: ")
    email = email + "@gmail.com"
    database = BD()
    database.them_tai_khoan_moi(ten, sdt, mat_khau2, email, cccd, ma_pin)
    print("Tao tai khoan thanh cong")
    
    