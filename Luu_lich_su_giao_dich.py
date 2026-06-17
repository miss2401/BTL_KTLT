import os
import random
import datetime

class GiaoDich:
    def __init__(self, ma_gd, sdt_gui, sdt_nhan, so_tien, noi_dung):
        self.ma_gd = ma_gd
        self.sdt_gui = sdt_gui
        self.sdt_nhan = sdt_nhan
        self.so_tien = int(so_tien)
        self.noi_dung = noi_dung
class LichSuGiaoDich:
    def __init__(self, db_file="Lich_su.json"):
        self.db_file = db_file
        
        # Khởi tạo trạng thái cho bộ đếm chống trùng lặp toàn thời gian trên RAM
        self.counter = 0
        self.last_miligiay = ""
        
        if not os.path.exists(self.db_file) or os.path.getsize(self.db_file) == 0:
            with open(self.db_file, "w", encoding="utf-8") as f:
                f.write("{}")
    def Dem_phan_tu(self, doi_tuong):
        so_luong = 0
        for _ in doi_tuong:
            so_luong += 1
        return so_luong
    def Bien_doi_thanh_chuoi(self, gia_tri):
        if gia_tri.__class__ == str:
            return gia_tri       
        if gia_tri.__class__ == int:
            if gia_tri == 0:
                return "0"  
            am = False
            if gia_tri < 0:
                am = True
                gia_tri = -gia_tri        
            chuoi_so = ""
            bang_chu_so = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")     
            while gia_tri > 0:
                du = gia_tri % 10
                chuoi_so = bang_chu_so[du] + chuoi_so
                gia_tri = gia_tri // 10             
            if am:
                chuoi_so = "-" + chuoi_so
            return chuoi_so     
        return ""

    def Dinh_dang(self, so):
        #Thêm 0 phía trước nếu có một chữ số
        chuoi_so = self.Bien_doi_thanh_chuoi(so)
        if self.Dem_phan_tu(chuoi_so) == 1:
            return "0" + chuoi_so
        return chuoi_so
    def Tao_ma_giao_dich(self):
        #Cấu trúc mã giao dịch: GD + YYYYMMDD_HHMMSS_miligiay + _ + counter
        bay_gio = datetime.datetime.now() 
        #Trích xuất chuỗi thời gian
        nam = self.Bien_doi_thanh_chuoi(bay_gio.year)
        thang = self.Dinh_dang(bay_gio.month)
        ngay = self.Dinh_dang(bay_gio.day)
        gio = self.Dinh_dang(bay_gio.hour)
        phut = self.Dinh_dang(bay_gio.minute)
        giay = self.Dinh_dang(bay_gio.second)
        mili_giay_so = (bay_gio.microsecond // 1000)
        mili_giay = self.Bien_doi_thanh_chuoi(mili_giay_so)
        while self.Dem_phan_tu(mili_giay) < 3:
            mili_giay = "0" + mili_giay      
        thoi_gian_hien_tai = f"{nam}{thang}{ngay}_{gio}{phut}{giay}_{mili_giay}"      
        #Kiểm tra trùng lăp
        if thoi_gian_hien_tai == self.last_miligiay:
            self.counter += 1
        else:
            self.counter = 0
            self.last_miligiay = thoi_gian_hien_tai         
        # Định dạng chuỗi số thứ tự luôn có 3 chữ số
        chuoi_counter = self.Bien_doi_thanh_chuoi(self.counter)
        while self.Dem_phan_tu(chuoi_counter) < 3:
            chuoi_counter = "0" + chuoi_counter       
        return f"GD{thoi_gian_hien_tai}_{chuoi_counter}"
    def Doc_file(self):
        #Đọc và phân tích dữ liệu từ file json
        du_lieu_he_thong = []
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                chuoi_json = f.read()
        except Exception:
            return du_lieu_he_thong
        chuoi = []
        i = 0
        do_dai_json = self.Dem_phan_tu(chuoi_json)
        while i < do_dai_json:
            char = chuoi_json[i]
            if char == '"':
                chuoi_str = ""
                i += 1
                while i < do_dai_json and chuoi_json[i] != '"':
                    chuoi_str = chuoi_str + chuoi_json[i]
                    i += 1
                chuoi = chuoi + [chuoi_str]
            elif char in (':', '{', '}', '[', ']', ','):
                chuoi = chuoi + [char]
            i += 1

        t = 0
        do_dai_chuoi = self.Dem_phan_tu(chuoi)
        while t < do_dai_chuoi:
            is_sdt = self.Dem_phan_tu(chuoi[t]) == 10
            if is_sdt:
                for char in chuoi[t]:
                    if char not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        is_sdt = False
                        break

            if is_sdt and (t + 4 < do_dai_chuoi) and chuoi[t+1] == ':' and chuoi[t+2] == '{' and chuoi[t+3] == "lich_su":
                sdt = chuoi[t]
                mang_gd_cua_user = []
                
                t = t + 6 
                while t < do_dai_chuoi and chuoi[t] != ']':
                    chuoi_gd_tho = chuoi[t]
                    if self.Dem_phan_tu(chuoi_gd_tho) > 5:
                        
                        # Split thủ công chuỗi giao dịch bằng dấu '|'
                        thong_tin = ["", "", "", "", ""]
                        idx_tt = 0
                        for c in chuoi_gd_tho:
                            if c == '|':
                                idx_tt += 1
                            else:
                                thong_tin[idx_tt] = thong_tin[idx_tt] + c
                        
                        gd_obj = GiaoDich(thong_tin[0], thong_tin[1], thong_tin[2], thong_tin[3], thong_tin[4])
                        mang_gd_cua_user = mang_gd_cua_user + [gd_obj]
                    t += 1
                
                du_lieu_he_thong = du_lieu_he_thong + [[sdt, mang_gd_cua_user]]
            t += 1
        return du_lieu_he_thong
    def Ghi_file(self, du_lieu_he_thong):
        chuoi_json = "{\n"
        do_dai_he_thong = self.Dem_phan_tu(du_lieu_he_thong)
        for i in range(do_dai_he_thong):
            sdt = du_lieu_he_thong[i][0]
            mang_gd = du_lieu_he_thong[i][1]     
            user_str = f'    "{sdt}": {{\n        "lich_su": [\n'
            do_dai_mang_gd = self.Dem_phan_tu(mang_gd)
            for j in range(do_dai_mang_gd):
                gd = mang_gd[j]
                
                s_tien = self.Bien_doi_thanh_chuoi(gd.so_tien)
                chuoi_ghep = f"{gd.ma_gd}|{gd.sdt_gui}|{gd.sdt_nhan}|{s_tien}|{gd.noi_dung}"
                
                if j == 0:
                    user_str = user_str + f'            "{chuoi_ghep}"'
                else:
                    user_str = user_str + f',\n            "{chuoi_ghep}"'
            user_str = user_str + "\n        ]\n    }"
            
            if i == 0:
                chuoi_json = chuoi_json + user_str
            else:
                chuoi_json = chuoi_json + ",\n" + user_str
                
        chuoi_json = chuoi_json + "\n}"
        with open(self.db_file, "w", encoding="utf-8") as f:
            f.write(chuoi_json)

    def Them_giao_dich(self, du_lieu, sdt_muc_tieu, gd_obj):
        tim_thay = False
        do_dai_du_lieu = self.Dem_phan_tu(du_lieu)
        for i in range(do_dai_du_lieu):
            if du_lieu[i][0] == sdt_muc_tieu:
                du_lieu[i][1] = du_lieu[i][1] + [gd_obj]
                tim_thay = True
                break
        if not tim_thay:
            du_lieu = du_lieu + [[sdt_muc_tieu, [gd_obj]]]
        return du_lieu

    def Ghi_giao_dich(self, sdt_gui, sdt_nhan, so_tien, noi_dung):
        du_lieu = self.Doc_file()
        ma_gd = self.Tao_ma_giao_dich()
        
        sdt_gui_str = self.Bien_doi_thanh_chuoi(sdt_gui)
        sdt_nhan_str = self.Bien_doi_thanh_chuoi(sdt_nhan)
        
        gd_obj = GiaoDich(ma_gd, sdt_gui_str, sdt_nhan_str, so_tien, noi_dung)
        
        du_lieu = self.Them_giao_dich(du_lieu, sdt_gui_str, gd_obj)
        
        # Chỉ thêm vào sdt_nhan nếu đó là số điện thoại hợp lệ (10 chữ số)
        if len(sdt_nhan_str) == 10 and sdt_nhan_str.isdigit():
            du_lieu = self.Them_giao_dich(du_lieu, sdt_nhan_str, gd_obj)
        
        self.Ghi_file(du_lieu)
        return ma_gd

    def Lay_lich_su(self, so_dien_thoai):
        du_lieu = self.Doc_file()
        sdt_str = self.Bien_doi_thanh_chuoi(so_dien_thoai)
        do_dai_du_lieu = self.Dem_phan_tu(du_lieu)
        for i in range(do_dai_du_lieu):
            if du_lieu[i][0] == sdt_str:
                return du_lieu[i][1]
        return []