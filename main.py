import create_user as CS
import login_user as LS
answer = int(input("1.Dang nhap \n2.Tao tai khoan \n3.Thoat \nNhập lựa chọn: "))
match answer:
    case 1:
        LS.dang_nhap()
    case 2:
        CS.Create_user()
    case _:
        pass