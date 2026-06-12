import json
from data import BankDatabase 
import tietkiem as TK

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

from giao_dich import nap_tien, rut_tien, chuyen_khoan
from truyxuatGD import menu_truy_xuat_giao_dich

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
                print("4. Gui tich kiem")
                print("5. Truy xuat giao dich")     
                print("6. Dang xuat")
                try:
                    lua_chon = input("Nhap lua chon: ")
                except:
                    print("Lua chon khong hop le!")
                    continue
                
                if lua_chon == "1":
                    try:
                        tien_nap = int(input("Nhap so tien muon nap (VND): "))
                        if tien_nap <= 0:
                            print("So tien phai lon hon 0!")
                            continue
                        nap_tien(db, danh_sach_tk, tai_khoan.so_tai_khoan, tien_nap)
                        danh_sach_tk = db._doc_file()
                        for tk in danh_sach_tk:
                            if tk.so_dien_thoai == sdt:
                                tai_khoan = tk
                                break
                    except ValueError:
                        print("So tien phai la so nguyen!")
                    except Exception as e:
                        print("Loi:", str(e))
                        
                elif lua_chon == "2":
                    try:
                        tien_rut = int(input("Nhap so tien muon rut (VND): "))
                        if tien_rut <= 0:
                            print("So tien phai lon hon 0!")
                            continue
                        rut_tien(db, danh_sach_tk, tai_khoan.so_tai_khoan, tien_rut)
                        danh_sach_tk = db._doc_file()
                        for tk in danh_sach_tk:
                            if tk.so_dien_thoai == sdt:
                                tai_khoan = tk
                                break
                    except ValueError:
                        print("So tien phai la so nguyen!")
                    except Exception as e:
                        print("Loi:", str(e))
                        
                elif lua_chon == "3":
                    try:
                        tk_nhan = input("Nhap so tai khoan nguoi nhan: ")
                        if not tk_nhan or len(tk_nhan) != 8:
                            print("So tai khoan phai la 8 chu so!")
                            continue
                        tien_chuyen = int(input("Nhap so tien muon chuyen (VND): "))
                        if tien_chuyen <= 0:
                            print("So tien phai lon hon 0!")
                            continue
                        chuyen_khoan(db, danh_sach_tk, tai_khoan.so_tai_khoan, tk_nhan, tien_chuyen)
                        danh_sach_tk = db._doc_file()
                        for tk in danh_sach_tk:
                            if tk.so_dien_thoai == sdt:
                                tai_khoan = tk
                                break
                    except ValueError:
                        print("So tien phai la so nguyen!")
                    except Exception as e:
                        print("Loi:", str(e))
                        
                elif lua_chon == "4":
                    try:
                        db_bank = BankDatabase()
                        tk_obj = db_bank.lay_thong_tin_user(sdt)
                        if tk_obj:
                            TK.menu_tich_kiem(tk_obj)
                            danh_sach_tk = db._doc_file()
                            for tk in danh_sach_tk:
                                if tk.so_dien_thoai == sdt:
                                    tai_khoan = tk
                                    break
                        else:
                            print("Khong tim thay tai khoan!")
                    except Exception as e:
                        print("Loi khi truy cap tiet kiem:", str(e))
                        
                elif lua_chon == "5":
                    try:
                        menu_truy_xuat_giao_dich(sdt)
                    except Exception as e:
                        print("Loi khi truy xuat giao dich:", str(e))
                        
                elif lua_chon == "6":
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
