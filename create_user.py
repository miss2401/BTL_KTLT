from data import BankDatabase as BD
class User:
    def __init__(self, sdt,  ho_ten, email, cccd, ma_pin, mat_khau):
        self.ho_ten = ho_ten
        self.sdt = sdt
        self.email = email
        self.cccd = cccd
        self.ma_pin = ma_pin
        self.mat_khau = mat_khau
def Kiem_tra_so(arr):
    for i in arr:
        if(i < '0' or i > '9'):
            return 1
    return 0

def Kiem_tra_ten(arr):
    for i in arr:
        is_lowercase = (i >= 'a' and i <= 'z')
        is_uppercase = (i >= 'A' and i <= 'Z')
        is_space = (i == ' ')
        if not (is_lowercase or is_uppercase or is_space):
            return 1
    return 0

def Kiem_tra_email(email):
    if not email or len(email) == 0:
        return 1
    if "@" in email:
        return 1
    for i in email:
        is_lowercase = (i >= 'a' and i <= 'z')
        is_uppercase = (i >= 'A' and i <= 'Z')
        is_digit = (i >= '0' and i <= '9')
        is_valid_char = (i in '._-')
        if not (is_lowercase or is_uppercase or is_digit or is_valid_char):
            return 1
    return 0

def Kiem_tra_sdt_ton_tai(sdt):
    try:
        database = BD()
        danh_sach_tk = database._doc_file()
        for tk in danh_sach_tk:
            if tk.so_dien_thoai == sdt:
                return 1
        return 0
    except:
        return 0

def check_mat_khau(arr):
    co_chu_thuong = False
    co_chu_hoa = False
    co_so = False
    co_ky_tu_dac_biet = False
    for i in arr:
        if(i >= 'a' and i <= 'z'):
            co_chu_thuong = True
        elif(i >= '0' and i <= '9'):
            co_so = True
        elif(i >= 'A' and i <= 'Z'):
            co_chu_hoa = True
        elif(i >= '!' and i <= '@'):
            co_ky_tu_dac_biet = True
    if(co_chu_thuong and co_chu_hoa and co_so and co_ky_tu_dac_biet):
        return 0
    else:
        return 1
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
    
    