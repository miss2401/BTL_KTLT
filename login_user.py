from data import BankDatabase

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
                print("3. Dang xuat")                
                lua_chon = input("Nhap lua chon: ")                
                if lua_chon == "1":
                    tien_nap = int(input("Nhap so tien muon nap (VND): "))
                    if tien_nap > 0:
                        tai_khoan.so_du += tien_nap
                        db._ghi_file(danh_sach_tk) 
                        print("Giao dich thanh cong! So du hien tai:", tai_khoan.so_du, "VND")
                    else:
                        print("So tien nap phai lon hon 0!")                        
                elif lua_chon == "2":
                    tien_rut = int(input("Nhap so tien muon rut (VND): "))
                    if 0 < tien_rut <= tai_khoan.so_du:
                        tai_khoan.so_du -= tien_rut
                        db._ghi_file(danh_sach_tk)
                        print("Giao dich thanh cong! So du hien tai:", tai_khoan.so_du, "VND")
                    else:
                        print("So tien rut khong hop le hoac vuot qua so du!")                        
                elif lua_chon == "3":
                    print("Da dang xuat tai khoan!")
                    return                    
                else:
                    print("Khong hop le, vui long nhap lai!")                    
            return
        so_lan_sai += 1
        print("\nDANG NHAP THAT BAI")
        print("Ban da nhap sai tai khoan hoac mat khau")
        print("So lan con lai:", 5 - so_lan_sai)        
    print("\nBan da nhap sai qua 5 lan. Tai khoan tam thoi bi khoa. Vui long den chi nhanh ngan hang gan nhat de duoc ho tro.")

if __name__ == "__main__":
    dang_nhap()