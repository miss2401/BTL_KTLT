from data import GiaoDich
from luulichsugiaodich import LichSuGiaoDich

def tim_tai_khoan(danh_sach_tk, so_tk):
    for tk in danh_sach_tk:
        if str(tk.so_tai_khoan) == str(so_tk):
            return tk
    return None

def nap_tien(db, danh_sach_tk, so_tk, so_tien):
    if so_tien <= 0:
        print("So tien nap phai lon hon 0!")
        return False        
    tk = tim_tai_khoan(danh_sach_tk, so_tk)
    if tk is None:
        print("Khong tim thay so tai khoan!")
        return False
    tk.so_du += int(so_tien)    
    gd_moi = GiaoDich("NAP TIEN", so_tien, tk.so_du, "KHONG CO")
    tk.lich_su_giao_dich.them_giao_dich(gd_moi)    
    db._ghi_file(danh_sach_tk)
    
    # Lưu lịch sử giao dịch vào history.json
    lich_su = LichSuGiaoDich("history.json")
    lich_su.ghi_nhan_giao_dich(tk.so_dien_thoai, "NAP_TIEN", so_tien, "Nap tien")
    
    print("NAP TIEN THANH CONG! So du hien tai:", tk.so_du, "VND")
    return True

def rut_tien(db, danh_sach_tk, so_tk, so_tien):
    if so_tien <= 0:
        print("So tien rut phai lon hon 0!")
        return False        
    tk = tim_tai_khoan(danh_sach_tk, so_tk)
    if tk is None:
        print("Khong tim thay so tai khoan!")
        return False
    if tk.so_du < so_tien:
        print("So du khong du de thuc hien giao dich!")
        return False        
    tk.so_du -= int(so_tien)    
    gd_moi = GiaoDich("RUT TIEN", so_tien, tk.so_du, "KHONG CO")
    tk.lich_su_giao_dich.them_giao_dich(gd_moi)    
    db._ghi_file(danh_sach_tk)
    
    # Lưu lịch sử giao dịch vào history.json
    lich_su = LichSuGiaoDich("history.json")
    lich_su.ghi_nhan_giao_dich(tk.so_dien_thoai, "RUT_TIEN", so_tien, "Rut tien")
    
    print("RUT TIEN THANH CONG! So du hien tai:", tk.so_du, "VND")
    return True

def chuyen_khoan(db, danh_sach_tk, nguon, dich, so_tien):
    if so_tien <= 0:
        print("So tien chuyen phai lon hon 0!")
        return False        
    tk_nguon = tim_tai_khoan(danh_sach_tk, nguon)
    tk_dich = tim_tai_khoan(danh_sach_tk, dich)    
    if tk_nguon is None:
        print("Tai khoan NGUON khong ton tai!")
        return False
    if tk_dich is None:
        print("Tai khoan DICH khong ton tai!")
        return False
    if tk_nguon.so_du < int(so_tien):
        print("So du khong du de chuyen khoan!")
        return False        
    tk_nguon.so_du -= int(so_tien)
    tk_dich.so_du += int(so_tien)    
    gd_gui = GiaoDich("CHUYEN KHOAN", so_tien, tk_nguon.so_du, tk_dich.so_tai_khoan)
    gd_nhan = GiaoDich("NHAN TIEN", so_tien, tk_dich.so_du, tk_nguon.so_tai_khoan)    
    tk_nguon.lich_su_giao_dich.them_giao_dich(gd_gui)
    tk_dich.lich_su_giao_dich.them_giao_dich(gd_nhan)    
    db._ghi_file(danh_sach_tk)
    
    # Lưu lịch sử giao dịch vào history.json
    lich_su = LichSuGiaoDich("history.json")
    lich_su.ghi_nhan_giao_dich(tk_nguon.so_dien_thoai, tk_dich.so_dien_thoai, so_tien, "Chuyen khoan")
    
    print("CHUYEN KHOAN THANH CONG!")
    print("So du hien tai cua ban:", tk_nguon.so_du, "VND")
    return True