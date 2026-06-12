import os
from luulichsugiaodich import LichSuGiaoDich

class BoTimKiemGiaoDich:
    def __init__(self, db_file="history.json"):
        # Tự khởi tạo kết nối database lịch sử
        self.bo_gd = LichSuGiaoDich(db_file)

    def _cat_chuoi(self, chuoi, vi_tri_dau, vi_tri_cuoi):
        # Cắt chuỗi từ vị trí đầu đến vị trí cuối
        chuoi_cat = ""
        idx = 0
        for char in chuoi:
            if idx >= vi_tri_dau and idx < vi_tri_cuoi:
                chuoi_cat = chuoi_cat + char
            idx += 1
        return chuoi_cat

    def _kiem_tra_chua_chuoi(self, chuoi_lon, chuoi_con):
        # Kiểm tra xem chuỗi con có xuất hiện trong chuỗi lớn hay không
        len_lon = self.bo_gd._dem_phan_tu(chuoi_lon)
        len_con = self.bo_gd._dem_phan_tu(chuoi_con)
        
        if len_con == 0:
            return True
        if len_con > len_lon:
            return False
            
        for i in range(len_lon - len_con + 1):
            doan_cat = self._cat_chuoi(chuoi_lon, i, i + len_con)
            if doan_cat == chuoi_con:
                return True
        return False

    def tim_kiem_giao_dich(self, so_dien_thoai, tu_khoa_nd=None, ma_gd_can_tim=None, ngay_bat_dau=None, ngay_ket_thuc=None):
        # Tìm kiếm giao dịch dựa trên nhiều tiêu chí khác nhau
        lich_su_goc = self.bo_gd.lay_lich_su_user(so_dien_thoai)
        mang_ket_qua = []
        
        so_luong_gd = self.bo_gd._dem_phan_tu(lich_su_goc)
        
        for i in range(so_luong_gd):
            gd = lich_su_goc[i]
            hop_le = True
            
            if ma_gd_can_tim is not None:
                ma_tim_str = self.bo_gd._bien_doi_thanh_chuoi(ma_gd_can_tim)
                if gd.ma_gd != ma_tim_str:
                    hop_le = False
            
            if hop_le and (ngay_bat_dau is not None or ngay_ket_thuc is not None):
                ngay_cua_gd = self._cat_chuoi(gd.ma_gd, 2, 10)
                
                if ngay_bat_dau is not None:
                    ngay_bd_str = self.bo_gd._bien_doi_thanh_chuoi(ngay_bat_dau)
                    if ngay_cua_gd < ngay_bd_str:
                        hop_le = False
                        
                if hop_le and ngay_ket_thuc is not None:
                    ngay_kt_str = self.bo_gd._bien_doi_thanh_chuoi(ngay_ket_thuc)
                    if ngay_cua_gd > ngay_kt_str:
                        hop_le = False
                    
            if hop_le and tu_khoa_nd is not None:
                tk_str = self.bo_gd._bien_doi_thanh_chuoi(tu_khoa_nd)
                if not self._kiem_tra_chua_chuoi(gd.noi_dung, tk_str):
                    hop_le = False
            
            if hop_le:
                mang_ket_qua = mang_ket_qua + [gd]
                
        return mang_ket_qua
    
    def hien_thi_giao_dich(self, danh_sach_gd, tieu_de=""):
        # Hiển thị danh sách giao dịch
        if len(danh_sach_gd) == 0:
            print(f"\n{tieu_de} - Khong tim thay giao dich nao!")
            return
        
        print(f"\n{tieu_de} - Tim thay {len(danh_sach_gd)} giao dịch")
        print(f"{'STT':<5} {'Mã GD':<35} {'Ngày':<10} {'Gio':<10} {'Nguoi gui':<15} {'Nguoi nhan':<15} {'So tien':<15} {'Nội dung':<25}")
        
        for idx, gd in enumerate(danh_sach_gd, 1):
            ngay = self._cat_chuoi(gd.ma_gd, 2, 10)
            gio = self._cat_chuoi(gd.ma_gd, 11, 17)
            
            sdt_gui_display = gd.sdt_gui[:8] + "****" if len(gd.sdt_gui) >= 10 else gd.sdt_gui
            sdt_nhan_display = gd.sdt_nhan[:8] + "****" if len(gd.sdt_nhan) >= 10 else gd.sdt_nhan
            noi_dung_display = gd.noi_dung[:22] + "..." if len(gd.noi_dung) > 22 else gd.noi_dung
            so_tien_display = self.bo_gd._bien_doi_thanh_chuoi(gd.so_tien) + " VND"
            
            print(f"{idx:<5} {gd.ma_gd:<35} {ngay:<10} {gio:<10} {sdt_gui_display:<15} {sdt_nhan_display:<15} {so_tien_display:<15} {noi_dung_display:<25}")
    
    def hien_thi_chi_tiet_gd(self, gd):
        # Hiển thị chi tiết một giao dịch cụ thể
        ngay = self._cat_chuoi(gd.ma_gd, 2, 10)
        gio = self._cat_chuoi(gd.ma_gd, 11, 17)
        ms_giao_dich = self._cat_chuoi(gd.ma_gd, 18, 21)
        
        print(f"\nCHI TIET GAO DICH")
        print(f"Ma giao dich:        {gd.ma_gd}")
        print(f"Ngay:                {ngay}")
        print(f"Gio:                 {gio}")
        print(f"Miligay:             {ms_giao_dich}")
        print(f"Nguoi gui:           {gd.sdt_gui}")
        print(f"Nguoi nhan:          {gd.sdt_nhan}")
        print(f"So tien:             {gd.so_tien:,} VND")
        print(f"Noi dung:            {gd.noi_dung}")

def menu_truy_xuat_giao_dich(so_dien_thoai):
    # Menu truy xuất giao dịch cho người dùng đã đăng nhập
    bo_tim_kiem = BoTimKiemGiaoDich()
    
    while True:
        print(f"MENU TRUY XUAT GIAO DICH - SDT: {so_dien_thoai}")
        print("1. Xem tat ca giao dich")
        print("2. Tim kiem theo ma GD")
        print("3. Tim kiem theo khoang ngay")
        print("4. Tim kiem theo tu khoa noi dung")
        print("5. Tim kiem theo nhieu tieu chi")
        print("0. Quay lai")
        
        try:
            lua_chon = input("Nhap lua chon: ").strip()
            
            if lua_chon == "0":
                print("Quay lai menu chinh...")
                break
            
            elif lua_chon == "1":
                lich_su = bo_tim_kiem.bo_gd.lay_lich_su_user(so_dien_thoai)
                bo_tim_kiem.hien_thi_giao_dich(lich_su, "TAT CA GAO DICH")
            
            elif lua_chon == "2":
                ma_gd = input("Nhap ma giao dich: ").strip()
                ket_qua = bo_tim_kiem.tim_kiem_giao_dich(so_dien_thoai, ma_gd_can_tim=ma_gd)
                bo_tim_kiem.hien_thi_giao_dich(ket_qua, "TIM KIEM THEO MA GD")
                if len(ket_qua) == 1:
                    xem_ct = input("Ban co muon xem chi tiet giao dich nay khong? (y/n): ").strip().lower()
                    if xem_ct == 'y':
                        bo_tim_kiem.hien_thi_chi_tiet_gd(ket_qua[0])
            
            elif lua_chon == "3":
                ngay_bd = input("Nhap ngay bat dau (YYYYMMDD): ").strip()
                ngay_kt = input("Nhap ngay ket thuc (YYYYMMDD): ").strip()
                ket_qua = bo_tim_kiem.tim_kiem_giao_dich(so_dien_thoai, ngay_bat_dau=ngay_bd, ngay_ket_thuc=ngay_kt)
                bo_tim_kiem.hien_thi_giao_dich(ket_qua, "TIM KIEM THEO KHOANG NGAY")
            
            elif lua_chon == "4":
                tu_khoa = input("Nhap tu khoa noi dung: ").strip()
                ket_qua = bo_tim_kiem.tim_kiem_giao_dich(so_dien_thoai, tu_khoa_nd=tu_khoa)
                bo_tim_kiem.hien_thi_giao_dich(ket_qua, "TIM KIEM THEO NOI DUNG")
            
            elif lua_chon == "5":
                print("\n--- Tim kiem theo nhieu tieu chi ---")
                ma_gd = input("Nhap ma giao dich (de trong de bo qua): ").strip() or None
                ngay_bd = input("Nhap ngay bat dau YYYYMMDD (de trong de bo qua): ").strip() or None
                ngay_kt = input("Nhap ngay ket thuc YYYYMMDD (de trong de bo qua): ").strip() or None
                tu_khoa = input("Nhap tu khoa noi dung (de trong de bo qua): ").strip() or None
                
                ket_qua = bo_tim_kiem.tim_kiem_giao_dich(
                    so_dien_thoai,
                    ma_gd_can_tim=ma_gd,
                    ngay_bat_dau=ngay_bd,
                    ngay_ket_thuc=ngay_kt,
                    tu_khoa_nd=tu_khoa
                )
                bo_tim_kiem.hien_thi_giao_dich(ket_qua, "KET QUA TIM KIEM")
            
            else:
                print("Lua chon khong hop le!")
        
        except Exception as e:
            print(f"Loi: {str(e)}")
