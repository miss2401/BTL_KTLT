class User:
    def __init__(self, ten_dang_nhap, ho_ten, email, sdt = 0, cccd = 0):
        self.ten_dang_nhap = ten_dang_nhap
        self.ho_ten = ho_ten
        self.sdt = sdt
        self.email = email
        self.cccd = cccd
def check_number(arr):
    if(arr[0] != '0'):
        return 1
    for i in arr:
        if(i < '0' or i > '9'):
            return 1
    return 0
co_chu_thuong = False
co_chu_hoa = False
co_so = False
co_ky_tu_dac_biet = False
def check_password(arr):
    for i in arr:
        if(i >= 'a' and i <= 'z'):
            co_chu_thuong = True
        elif(i >= '0' and i <= '9'):
            co_chu_hoa = True
        elif(i >= 'A' and i <= 'Z'):
            co_so = True
        elif(i >= '!' and i <= '@'):
            co_ky_tu_dac_biet = True
    if(co_chu_thuong and co_chu_hoa and co_so and co_ky_tu_dac_biet):
        return 0
    else:
        return 1
def Create_user():
    sdt = input("So dien thoai: ")
    while(len(sdt) != 10 or CS.check_number(sdt)):
        sdt = input("Nhap lai so dien thoai: ")
        password = input("Mat khau: ")
    while(len(password) < 8 or CS.check_password(password)):
        print("Mat khau phai co it nhat 8 ki tu, co ket hop giua chu cai in hoa, chu so va ki tu dac biet")
        password = input("Nhap lai mat khau: ")
    print("Tao tai khoan thanh cong")