import os
from luulichsugiaodich import LichSuGiaoDich

class BoTimKiemGiaoDich:
    def __init__(self, db_file="history.json"):
        # Tự khởi tạo kết nối database lịch sử
        self.bo_gd = LichSuGiaoDich(db_file)

    def _cat_chuoi(self, chuoi, vi_tri_dau, vi_tri_cuoi):
        chuoi_cat = ""
        idx = 0
        for char in chuoi:
            if idx >= vi_tri_dau and idx < vi_tri_cuoi:
                chuoi_cat = chuoi_cat + char
            idx += 1
        return chuoi_cat

    def _kiem_tra_chua_chuoi(self, chuoi_lon, chuoi_con):

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
    #Tìm kiếm giao dịch dựa trên nhiều tiêu chí đồng thời (mã giao dịch, khoảng ngày, từ khóa nội dung), nếu có tiêu chí nào không được cung cấp thì sẽ bỏ qua tiêu chí đó.

        lich_su_goc = self.bo_gd.lay_lich_su_user(so_dien_thoai)
        mang_ket_qua = []
        
        so_luong_gd = self.bo_gd._dem_phan_tu(lich_su_goc)
        
        for i in range(so_luong_gd):
            gd = lich_su_goc[i]
            hop_le = True
            
            #Kiểm tra mã giao dịch
            if ma_gd_can_tim is not None:
                ma_tim_str = self.bo_gd._bien_doi_thanh_chuoi(ma_gd_can_tim)
                if gd.ma_gd != ma_tim_str:
                    hop_le = False
            
            #Kiểm tra khoảng ngày
            if hop_le and (ngay_bat_dau is not None or ngay_ket_thuc is not None):
                ngay_cua_gd = self._cat_chuoi(gd.ma_gd, 2, 10)
                
                #Kiểm tra biên ngày bắt đầu
                if ngay_bat_dau is not None:
                    ngay_bd_str = self.bo_gd._bien_doi_thanh_chuoi(ngay_bat_dau)
                    if ngay_cua_gd < ngay_bd_str:
                        hop_le = False
                        
                #Kiểm tra biên ngày kết thúc
                if hop_le and ngay_ket_thuc is not None:
                    ngay_kt_str = self.bo_gd._bien_doi_thanh_chuoi(ngay_ket_thuc)
                    if ngay_cua_gd > ngay_kt_str:
                        hop_le = False
                    
            #Kiểm tra từ khóa nội dung
            if hop_le and tu_khoa_nd is not None:
                tk_str = self.bo_gd._bien_doi_thanh_chuoi(tu_khoa_nd)
                if not self._kiem_tra_chua_chuoi(gd.noi_dung, tk_str):
                    hop_le = False
            
            if hop_le:
                mang_ket_qua = mang_ket_qua + [gd]
                
        return mang_ket_qua