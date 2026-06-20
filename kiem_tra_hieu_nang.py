import time
from Giao_dich import Nap_tien, Rut_tien, Chuyen_khoan
from Luu_du_lieu import BankDatabase
from Luu_lich_su_giao_dich import LichSuGiaoDich
from Truy_xuat_giao_dich import BoTimKiemGiaoDich
from Tiet_kiem import QuanLyTietKiem


class PerformanceTest:
    def __init__(self):
        self.db = BankDatabase()
        self.results = {}

    def do_thoi_gian(self, func, *args, **kwargs):
        """Đo thời gian thực thi của một hàm (giây)"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, end - start

    def tim_theo_sdt(self, danh_sach_tk, sdt):
        for tk in danh_sach_tk:
            if tk.so_dien_thoai == sdt:
                return tk
        return None

    def test_doc_file(self):
        print("\n=== KIEM TRA DOC FILE ===")

        _, t1 = self.do_thoi_gian(self.db.Doc_file)
        print(f"Doc Du_lieu.json       : {t1:.6f} giay")

        lich_su = LichSuGiaoDich()
        _, t2 = self.do_thoi_gian(lich_su.Doc_file)
        print(f"Doc Lich_su.json       : {t2:.6f} giay")

        ql = QuanLyTietKiem()
        _, t3 = self.do_thoi_gian(ql.Doc_file)
        print(f"Doc Tiet_kiem.json     : {t3:.6f} giay")

        return {'doc_tai_khoan': t1, 'doc_lich_su': t2, 'doc_tiet_kiem': t3}

    def test_tim_kiem_tai_khoan(self):
        print("\n=== KIEM TRA TIM KIEM TAI KHOAN ===")

        danh_sach_tk = self.db.Doc_file()
        if not danh_sach_tk:
            print("Khong co du lieu!")
            return {}

        sdt_dau  = danh_sach_tk[0].so_dien_thoai
        sdt_cuoi = danh_sach_tk[-1].so_dien_thoai

        _, t1 = self.do_thoi_gian(self.tim_theo_sdt, danh_sach_tk, sdt_dau)
        print(f"Tim SDT dau danh sach  : {t1:.6f} giay")

        _, t2 = self.do_thoi_gian(self.tim_theo_sdt, danh_sach_tk, sdt_cuoi)
        print(f"Tim SDT cuoi danh sach : {t2:.6f} giay")

        _, t3 = self.do_thoi_gian(self.tim_theo_sdt, danh_sach_tk, "0999999999")
        print(f"Tim SDT khong ton tai  : {t3:.6f} giay")

        return {'tim_dau': t1, 'tim_cuoi': t2, 'tim_khong_ton_tai': t3}

    def test_giao_dich(self):
        print("\n=== KIEM TRA GIAO DICH ===")

        danh_sach_tk = self.db.Doc_file()
        if len(danh_sach_tk) < 2:
            print("Can it nhat 2 tai khoan!")
            return {}

        tk1 = danh_sach_tk[0]
        tk2 = danh_sach_tk[1]
        so_tien = 10000

        _, t1 = self.do_thoi_gian(
            Nap_tien, self.db, danh_sach_tk, tk1.so_tai_khoan, so_tien
        )
        print(f"Nap tien               : {t1:.6f} giay")

        danh_sach_tk = self.db.Doc_file()
        _, t2 = self.do_thoi_gian(
            Rut_tien, self.db, danh_sach_tk, tk1.so_tai_khoan, so_tien
        )
        print(f"Rut tien               : {t2:.6f} giay")

        danh_sach_tk = self.db.Doc_file()
        _, t3 = self.do_thoi_gian(
            Chuyen_khoan, self.db, danh_sach_tk,
            tk1.so_tai_khoan, tk2.so_tai_khoan, so_tien, "Test chuyen khoan"
        )
        print(f"Chuyen khoan           : {t3:.6f} giay")

        return {'nap_tien': t1, 'rut_tien': t2, 'chuyen_khoan': t3}

    def test_lich_su_giao_dich(self):
        print("\n=== KIEM TRA LICH SU GIAO DICH ===")

        danh_sach_tk = self.db.Doc_file()
        if not danh_sach_tk:
            print("Khong co du lieu!")
            return {}

        sdt = danh_sach_tk[0].so_dien_thoai
        bo_tim = BoTimKiemGiaoDich()

        _, t1 = self.do_thoi_gian(bo_tim.bo_gd.Lay_lich_su, sdt)
        print(f"Lay toan bo lich su    : {t1:.6f} giay")

        lich_su = bo_tim.bo_gd.Lay_lich_su(sdt)
        t2 = 0.0
        if lich_su:
            ma_gd = lich_su[0].ma_gd
            _, t2 = self.do_thoi_gian(
                bo_tim.Tim_kiem_giao_dich, sdt, ma_gd_can_tim=ma_gd
            )
            print(f"Tim theo ma GD         : {t2:.6f} giay")
        else:
            print(f"Tim theo ma GD         : (khong co du lieu)")

        _, t3 = self.do_thoi_gian(
            bo_tim.Tim_kiem_giao_dich, sdt, tu_khoa_nd="NAP"
        )
        print(f"Tim theo tu khoa       : {t3:.6f} giay")

        return {'lay_lich_su': t1, 'tim_ma_gd': t2, 'tim_tu_khoa': t3}

    def test_tiet_kiem(self):
        print("\n=== KIEM TRA TIET KIEM ===")

        ql = QuanLyTietKiem()

        ds_so, t1 = self.do_thoi_gian(ql.Doc_file)
        print(f"Doc Tiet_kiem.json     : {t1:.6f} giay")

        dem_hoat_dong = 0
        dem_tat_toan  = 0
        cur = ds_so.get_head()
        while cur:
            if cur.du_lieu.trang_thai == 1:
                dem_hoat_dong += 1
            else:
                dem_tat_toan += 1
            cur = cur.next
        tong_so = dem_hoat_dong + dem_tat_toan
        print(f"  Tong so: {tong_so}  |  Hoat dong: {dem_hoat_dong}  |  Tat toan: {dem_tat_toan}")

        sdt_muc_tieu = None
        cur = ds_so.get_head()
        while cur:
            if cur.du_lieu.trang_thai == 1:
                sdt_muc_tieu = cur.du_lieu.so_dien_thoai
                break
            cur = cur.next

        t2 = 0.0
        if sdt_muc_tieu:
            def tim_so_theo_sdt(sdt):
                ds = ql.Doc_file()
                ket_qua = []
                cur = ds.get_head()
                while cur:
                    if cur.du_lieu.so_dien_thoai == sdt and cur.du_lieu.trang_thai == 1:
                        ket_qua.append(cur.du_lieu)
                    cur = cur.next
                return ket_qua

            _, t2 = self.do_thoi_gian(tim_so_theo_sdt, sdt_muc_tieu)
            print(f"Tim so theo SDT        : {t2:.6f} giay")
        else:
            print(f"Tim so theo SDT        : (khong co so hoat dong)")

        def tinh_lai_hang_loat():
            ds = ql.Doc_file()
            cur = ds.get_head()
            while cur:
                if cur.du_lieu.trang_thai == 1:
                    ql.Tinh_lai_suat(cur.du_lieu.so_tien_gui, cur.du_lieu.ngay_gui)
                cur = cur.next

        _, t3 = self.do_thoi_gian(tinh_lai_hang_loat)
        print(f"Tinh lai hang loat     : {t3:.6f} giay  ({dem_hoat_dong} so)")

        _, t4 = self.do_thoi_gian(ql.Ghi_file, ds_so)
        print(f"Ghi Tiet_kiem.json     : {t4:.6f} giay")

        return {
            'doc_tiet_kiem': t1,
            'tim_so_theo_sdt': t2,
            'tinh_lai_hang_loat': t3,
            'ghi_tiet_kiem': t4,
        }

    def test_ghi_file(self):
        print("\n=== KIEM TRA GHI FILE ===")

        danh_sach_tk = self.db.Doc_file()
        _, t1 = self.do_thoi_gian(self.db.Ghi_file, danh_sach_tk)
        print(f"Ghi Du_lieu.json       : {t1:.6f} giay")

        return {'ghi_tai_khoan': t1}

    def chay_kiem_tra_toan_bo(self):
        print("=" * 60)
        print("BAT DAU KIEM TRA HIEU NANG")
        print("=" * 60)

        danh_sach_tk = self.db.Doc_file()
        ql = QuanLyTietKiem()
        ds_so = ql.Doc_file()
        dem_so = sum(1 for _ in ds_so.iterate())
        print(f"\nSo tai khoan   : {len(danh_sach_tk)}")
        print(f"So tiet kiem   : {dem_so}")

        self.results['doc_file']  = self.test_doc_file()
        self.results['tim_kiem']  = self.test_tim_kiem_tai_khoan()
        self.results['giao_dich'] = self.test_giao_dich()
        self.results['lich_su']   = self.test_lich_su_giao_dich()
        self.results['tiet_kiem'] = self.test_tiet_kiem()
        self.results['ghi_file']  = self.test_ghi_file()

        self.in_ket_qua()
        return self.results

    def in_ket_qua(self):
        print("\n" + "=" * 60)
        print("KET QUA KIEM TRA HIEU NANG")
        print("=" * 60)

        all_times = []
        for category in self.results.values():
            if isinstance(category, dict):
                all_times.extend(v for v in category.values() if v > 0)

        if all_times:
            print(f"\nNgan nhat  : {min(all_times):.6f} giay")
            print(f"Dai nhat   : {max(all_times):.6f} giay")
            print(f"Trung binh : {sum(all_times)/len(all_times):.6f} giay")

        print("\nCHI TIET:")
        for category, values in self.results.items():
            if isinstance(values, dict):
                print(f"\n  {category.upper()}:")
                for key, value in values.items():
                    print(f"    {key:<30}: {value:.6f} giay")


def phan_tich_tang_truong(cac_so_luong=(100, 500, 1000)):
    print("\n" + "=" * 60)
    print("PHAN TICH TOC DO TANG TRUONG")
    print("=" * 60)

    ket_qua = []
    for so_luong in cac_so_luong:
        db = BankDatabase()
        ql = QuanLyTietKiem()

        t0 = time.perf_counter()
        ds = db.Doc_file()
        t_doc_tk = time.perf_counter() - t0

        t0 = time.perf_counter()
        ql.Doc_file()
        t_doc_stk = time.perf_counter() - t0

        t_tim = 0.0
        if ds:
            sdt_cuoi = ds[-1].so_dien_thoai
            t0 = time.perf_counter()
            for tk in ds:
                if tk.so_dien_thoai == sdt_cuoi:
                    break
            t_tim = time.perf_counter() - t0

        ket_qua.append((so_luong, t_doc_tk, t_doc_stk, t_tim))
        print(f"\n  {so_luong:>5} tai khoan | "
              f"doc TK {t_doc_tk:.6f}s | "
              f"doc STK {t_doc_stk:.6f}s | "
              f"tim {t_tim:.6f}s")

    if len(ket_qua) >= 2:
        print("\n  TANG TRUONG GIUA CAC MUC:")
        for i in range(1, len(ket_qua)):
            prev, cur = ket_qua[i-1], ket_qua[i]
            delta = cur[0] - prev[0]
            print(f"  {prev[0]} -> {cur[0]} (+{delta} TK): "
                  f"doc TK +{cur[1]-prev[1]:.6f}s | "
                  f"doc STK +{cur[2]-prev[2]:.6f}s | "
                  f"tim +{cur[3]-prev[3]:.6f}s")


if __name__ == "__main__":
    test = PerformanceTest()
    test.chay_kiem_tra_toan_bo()
    phan_tich_tang_truong()
