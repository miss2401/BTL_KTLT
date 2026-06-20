import os
import time

from tao_du_lieu_lon import tao_du_lieu_lon
from kiem_tra_hieu_nang import PerformanceTest, phan_tich_tang_truong

CAC_CAP_DO = [
    (100,  "Nho   -  100 tai khoan"),
    (500,  "Vua   -  500 tai khoan"),
    (1000, "Lon   - 1000 tai khoan"),
]

FILES_DU_LIEU = ["Du_lieu.json", "Lich_su.json", "Tiet_kiem.json"]


def backup_files():
    for f in FILES_DU_LIEU:
        if os.path.exists(f):
            os.rename(f, f + ".backup")

def restore_files():
    for f in FILES_DU_LIEU:
        bak = f + ".backup"
        if os.path.exists(bak):
            os.replace(bak, f)

def xoa_files_hien_tai():
    for f in FILES_DU_LIEU:
        if os.path.exists(f):
            os.remove(f)

def chay_mot_cap_do(so_luong, mo_ta):
    print(f"\n{'#'*60}")
    print(f"# {mo_ta.upper()}")
    print(f"{'#'*60}")

    #Xóa file cũ của lần chạy trước
    xoa_files_hien_tai()

    #tạo dữ liệu
    print("\n[1/2] TAO DU LIEU...")
    t0 = time.perf_counter()
    tao_du_lieu_lon(so_luong)
    t_tao = time.perf_counter() - t0
    print(f"  => Tao xong trong {t_tao:.3f} giay")

    #kiểm tra hiệu năng
    print("\n[2/2] KIEM TRA HIEU NANG...")
    test = PerformanceTest()
    results = test.chay_kiem_tra_toan_bo()

    return results

def main():
    print("=" * 60)
    print("CHUONG TRINH KIEM TRA HIEU NANG NGAN HANG")
    print("=" * 60)
    print(f"Se chay {len(CAC_CAP_DO)} cap do: "
          + ", ".join(str(n) for n, _ in CAC_CAP_DO) + " tai khoan")

    #Backup file gốc của người dùng
    backup_files()

    tat_ca_ket_qua = {}

    try:
        for so_luong, mo_ta in CAC_CAP_DO:
            tat_ca_ket_qua[so_luong] = chay_mot_cap_do(so_luong, mo_ta)

        #Phân tích tăng trưởng dựa trên lần chạy cuối cùng
        print("\n")
        phan_tich_tang_truong([n for n, _ in CAC_CAP_DO])

        #Tổng kết
        print("\n" + "=" * 60)
        print("TONG KET")
        print("=" * 60)
        for so_luong, mo_ta in CAC_CAP_DO:
            print(f"\n  {mo_ta}:")
            r = tat_ca_ket_qua.get(so_luong, {})
            #In thời gian đọc 3 file
            doc = r.get('doc_file', {})
            print(f"    doc Du_lieu.json  : {doc.get('doc_tai_khoan', 0):.6f}s")
            print(f"    doc Lich_su.json  : {doc.get('doc_lich_su', 0):.6f}s")
            print(f"    doc Tiet_kiem.json: {doc.get('doc_tiet_kiem', 0):.6f}s")
            tk_test = r.get('tiet_kiem', {})
            print(f"    tinh lai hang loat: {tk_test.get('tinh_lai_hang_loat', 0):.6f}s")

    finally:
        #khôi phục file gốc dù có lỗi
        xoa_files_hien_tai()
        restore_files()
        print("\n=> Da khoi phuc file du lieu goc.")


if __name__ == "__main__":
    main()
