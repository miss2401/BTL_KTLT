import json
import os
import random
from datetime import datetime

class BankDatabase:
    def __init__(self, db_file="data.json"):
        self.db_file = db_file
        #Tạo file json nếu không tồn tại
        if not os.path.exists(self.db_file) or os.path.getsize(self.db_file) == 0:
            self._ghi_file({})

    def _doc_file(self):
        #Đọc dữ liệu
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _ghi_file(self, data):
        #Ghi dữ liệu
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _tao_stk_ngau_nhien(self, data):
        #Tạo stk không trùng lặp
        stk_da_co = {user["so_tai_khoan"] for user in data.values() if "so_tai_khoan" in user}
        while True:
            stk_goi_y = str(random.randint(10000000, 99999999))
            if stk_goi_y not in stk_da_co:
                return stk_goi_y


    def them_tai_khoan_moi(self, ho_ten, so_dien_thoai, mat_khau, email, cccd, ma_pin):
        
        data = self._doc_file()
        
        #Ktr trùng sđt
        if so_dien_thoai in data:
            return False
            
        so_tai_khoan = self._tao_stk_ngau_nhien(data)
        
        #Ghi info vào json
        data[so_dien_thoai] = {
            "ho_ten": ho_ten,
            "mat_khau": mat_khau,
            "email": email,
            "cccd": cccd,
            "so_tai_khoan": so_tai_khoan,
            "so_du": 0, 
            "ma_pin": ma_pin
        }
        
        self._ghi_file(data)
        return so_tai_khoan

    def lay_thong_tin_user(self, so_dien_thoai):
        
        #Xuất thông tin

        data = self._doc_file()
        return data.get(so_dien_thoai, None)