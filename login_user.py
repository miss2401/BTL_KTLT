import json
from data import BankDatabase as BD
import tichkiem as TK

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
def luu_du_lieu(danh_sach_tai_khoan):
    try:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(danh_sach_tai_khoan, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Loi khi luu du lieu:", e)

def dang_nhap():
    danh_sach_tai_khoan = doc_du_lieu()
    so_lan_sai = 0    
    while so_lan_sai < 5:
        sdt = input("Nhap so dien thoai: ")
        mat_khau = input("Nhap mat khau: ")
        if sdt in danh_sach_tai_khoan and danh_sach_tai_khoan[sdt]["mat_khau"] == mat_khau:            
            tai_khoan = danh_sach_tai_khoan[sdt]            
            if "lich_su" not in tai_khoan:
                tai_khoan["lich_su"] = []
            print("DANG NHAP THANH CONG")           
            print("Xin chao    :", tai_khoan.get('ho_ten', 'Chua cap nhat'))
            print("So tai khoan:", tai_khoan.get('stk', sdt))
            print("So du       :", tai_khoan.get('so_du', 0), "VND")
            while True:
                print("\nBAN DANG CAN DICH VU GI?")
                print("1. Nap tien")
                print("2. Rut tien")
                print("3. Gui tich kiem")
                print("4. Xem lich su giao dich")
                print("5. Dang xuat")                
                lua_chon = input("Nhap lua chon: ")                
                if lua_chon == "1":
                    tien_nap = int(input("Nhap so tien muon nap (VND): "))
                    if tien_nap > 0:
                        tai_khoan["so_du"] += tien_nap
                        chuoi_lich_su = "Nap tien: +" + str(tien_nap) + " VND"
                        tai_khoan["lich_su"].append(chuoi_lich_su)                        
                        luu_du_lieu(danh_sach_tai_khoan)
                        print("Giao dich thanh cong! So du hien tai:", tai_khoan['so_du'], "VND")
                    else:
                        print("So tien nap phai lon hon 0")                        
                elif lua_chon == "2":
                    tien_rut = int(input("Nhap so tien muon rut (VND): "))
                    if 0 < tien_rut <= tai_khoan["so_du"]:
                        tai_khoan["so_du"] -= tien_rut
                        chuoi_lich_su = "Rut tien: -" + str(tien_rut) + " VND"
                        tai_khoan["lich_su"].append(chuoi_lich_su)                        
                        luu_du_lieu(danh_sach_tai_khoan)
                        print("Giao dich thanh cong! So du hien tai:", tai_khoan['so_du'], "VND")
                    else:
                        print("So tien rut khong hop le hoac vuot qua so du")
                elif lua_chon == "3":
                    db_bank = BD()
                    tk_obj = db_bank.lay_thong_tin_user(sdt)
                    if tk_obj:
                        TK.menu_tich_kiem(tk_obj)
                        danh_sach_tai_khoan = doc_du_lieu()
                        tai_khoan = danh_sach_tai_khoan[sdt]  
                elif lua_chon == "4":
                    print("\nLICH SU GIAO DICH")
                    if len(tai_khoan["lich_su"]) == 0:
                        print("Chua co lich su giao dich.")
                    else:
                        for gd in tai_khoan["lich_su"]:
                            print("-", gd)                            
                elif lua_chon == "5":
                    print("Da dang xuat tai khoan")
                    return                    
                else:
                    print("Lua chon khong hop le, vui long nhap lai")                    
            return
        so_lan_sai += 1
        print("\nDANG NHAP THAT BAI")
        print("Ban da nhap sai tai khoan hoac mat khau")
        print("So lan con lai:", 5 - so_lan_sai)        
    print("\nBan da nhap sai qua 5 lan. Tai khoan tam thoi bi khoa, vui long den chi nhanh ngan hang gan nhat de duoc giai quyet!")

if __name__ == "__main__":
    dang_nhap()