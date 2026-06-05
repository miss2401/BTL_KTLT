from data import BankDatabase

from giao_dich import nap_tien, rut_tien, chuyen_khoan

def dang_nhap():
    db = BankDatabase("data.json")
    danh_sach_tk = db._doc_file()
    so_lan_sai = 0    
    while so_lan_sai < 5:
        sdt = input("Nhap so dien thoai: ")
        mat_khau = input("Nhap mat khau: ")
        tai_khoan = None       
        for tk in danh_sach_tk:
            if tk.so_dien_thoai == sdt:
                tai_khoan = tk
                break               
        if tai_khoan is not None and tai_khoan.mat_khau == mat_khau:
            print("DANG NHAP THANH CONG")
            print("Xin chao    :", tai_khoan.ho_ten)
            print("So tai khoan:", tai_khoan.so_tai_khoan if tai_khoan.so_tai_khoan != "" else sdt)
            print("So du       :", tai_khoan.so_du, "VND")
            while True:
                print("\nBAN DANG CAN DICH VU GI?")
                print("1. Nap tien")
                print("2. Rut tien")
                print("3. Chuyen khoan")
                print("4. Dang xuat")               
                lua_chon = input("Nhap lua chon: ")               
                if lua_chon == "1":
                    tien_nap = int(input("Nhap so tien muon nap (VND): "))
                    nap_tien(db, danh_sach_tk, tai_khoan.so_tai_khoan, tien_nap)                  
                elif lua_chon == "2":
                    tien_rut = int(input("Nhap so tien muon rut (VND): "))
                    rut_tien(db, danh_sach_tk, tai_khoan.so_tai_khoan, tien_rut)                   
                elif lua_chon == "3":
                    tk_nhan = input("Nhap so tai khoan nguoi nhan: ")
                    tien_chuyen = int(input("Nhap so tien muon chuyen (VND): "))
                    chuyen_khoan(db, danh_sach_tk, tai_khoan.so_tai_khoan, tk_nhan, tien_chuyen)                    
                elif lua_chon == "4":
                    print("Da dang xuat tai khoan!")
                    return
                else:
                    print("Lua chon khong hop le, vui long nhap lai!")
            return        
        so_lan_sai += 1
        print("\nDANG NHAP THAT BAI")
        print("Ban da nhap sai tai khoan hoac mat khau")
        print("So lan con lai:", 5 - so_lan_sai)       
    print("\nBan da nhap sai qua 5 lan. Tai khoan tam thoi bi khoa. Vui long den chi nhanh ngan hang gan nhat de duoc ho tro.")

if __name__ == "__main__":
    dang_nhap()