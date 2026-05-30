import json

def doc_du_lieu():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            danh_sach_tai_khoan = json.load(file)
            return danh_sach_tai_khoan            
    except FileNotFoundError:
        print("Loi: Khong tim thay file du lieu data.json")
        return {}
    except json.JSONDecodeError:
        print("Loi: File data.json bi sai dinh dang")
        return {}

def dang_nhap():
    danh_sach_tai_khoan = doc_du_lieu()
    so_lan_sai = 0
    while so_lan_sai < 5:
        sdt = input("Nhap so dien thoai: ")
        mat_khau = input("Nhap mat khau: ")
        if sdt in danh_sach_tai_khoan and danh_sach_tai_khoan[sdt]["mat_khau"] == mat_khau:            
            tai_khoan = danh_sach_tai_khoan[sdt]            
            print("\nDANG NHAP THANH CONG")
            print("Xin chao", tai_khoan["ho_ten"])
            print("\nBAN DANG CAN DICH VU GI?")
            print("1. Xem so du")
            print("2. Xem lich su giao dich")
            print("3. Dang xuat")
            lua_chon = input("Nhap lua chon: ")
            if lua_chon == "1":
                print("So du hien tai:", tai_khoan["so_du"], "VND")
            elif lua_chon == "2":
                print("Chua co lich su giao dich")
            elif lua_chon == "3":
                print("Da dang xuat")                
            return
        so_lan_sai = so_lan_sai + 1
        print("\nDANG NHAP THAT BAI")
        print("Ban da nhap sai tai khoan hoac mat khau")
        print("So lan con lai:", 5 - so_lan_sai)
    print("\nBan da nhap sai qua 5 lan. Tai khoan tam thoi bi khoa, vui long den chi nhanh ngan hang gan nhat de duoc giai quyet!")

if __name__ == "__main__":
    dang_nhap()