import json

# Tên file lưu trữ dữ liệu
ten_file = 'chitieu.json'

def doc_du_lieu():
    """Đọc dữ liệu từ file JSON."""
    try:
        with open(ten_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def luu_du_lieu(du_lieu):
    """Ghi dữ liệu vào file JSON."""
    with open(ten_file, 'w', encoding='utf-8') as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=4)

def them_khoan_chi(du_lieu):
    """Thêm một khoản chi tiêu, tránh trùng lặp danh mục không phân biệt chữ hoa."""
    ten_danh_muc = input("Nhập tên danh mục: ").strip()
    ten_khoan_chi = input("Nhập tên khoản chi: ").strip()
    try:
        so_tien = float(input("Nhập số tiền: "))
    except ValueError:
        print("Số tiền không hợp lệ!")
        return
    ngay = input("Nhập ngày (YYYY-MM-DD): ").strip()

    # Tìm danh mục không phân biệt chữ hoa, chữ thường
    danh_muc = next((dm for dm in du_lieu if dm['ten'].lower() == ten_danh_muc.lower()), None)
    if danh_muc:
        ten_danh_muc = danh_muc['ten']  # Giữ nguyên tên danh mục gốc
        # Kiểm tra trùng lặp khoản chi
        for khoan_chi in danh_muc["Chitiet"]:
            if khoan_chi['ten'].lower() == ten_khoan_chi.lower():
                print(f"Khoản chi '{ten_khoan_chi}' đã tồn tại trong danh mục '{ten_danh_muc}'.")
                return
    else:
        # Tạo danh mục mới nếu không tìm thấy
        danh_muc = {"ten": ten_danh_muc, "Chitiet": []}
        du_lieu.append(danh_muc)

    # Thêm khoản chi vào danh mục
    danh_muc["Chitiet"].append({"ten": ten_khoan_chi, "sotien": so_tien, "date": ngay})
    luu_du_lieu(du_lieu)
    print(f"Đã thêm khoản chi '{ten_khoan_chi}' vào danh mục '{ten_danh_muc}'.")

def hien_thi_chi_tieu(du_lieu):
    """Hiển thị danh sách chi tiêu, phân loại theo ngày, tháng, năm."""
    if not du_lieu:
        print("Chưa có dữ liệu chi tiêu.")
        return

    print("\n1. Xem tất cả chi tiêu")
    print("2. Phân loại chi tiêu theo ngày")
    print("3. Phân loại chi tiêu theo tháng")
    print("4. Phân loại chi tiêu theo năm")
    lua_chon = input("Chọn cách xem chi tiêu (1-4): ")

    if lua_chon == '1':
        # Hiển thị tất cả chi tiêu
        for danh_muc in du_lieu:
            print(f"\nDanh mục: {danh_muc['ten']}")
            for khoan_chi in danh_muc["Chitiet"]:
                print(f"  - {khoan_chi['ten']}: {khoan_chi['sotien']} VND (Ngày: {khoan_chi['date']})")
    elif lua_chon in ['2', '3', '4']:
        # Lọc chi tiêu theo ngày, tháng, hoặc năm
        if lua_chon == '2':
            ngay = input("Nhập ngày (YYYY-MM-DD): ").strip()
            print(f"\nChi tiêu trong ngày {ngay}:")
        elif lua_chon == '3':
            thang = input("Nhập tháng (YYYY-MM): ").strip()
            print(f"\nChi tiêu trong tháng {thang}:")
        elif lua_chon == '4':
            nam = input("Nhập năm (YYYY): ").strip()
            print(f"\nChi tiêu trong năm {nam}:")

        # Hiển thị chi tiêu theo bộ lọc
        for danh_muc in du_lieu:
            for khoan_chi in danh_muc["Chitiet"]:
                if (lua_chon == '2' and khoan_chi['date'] == ngay) or \
                   (lua_chon == '3' and khoan_chi['date'].startswith(thang)) or \
                   (lua_chon == '4' and khoan_chi['date'].startswith(nam)):
                    print(f"- Danh mục: {danh_muc['ten']}, Khoản chi: {khoan_chi['ten']}, Số tiền: {khoan_chi['sotien']} VND, Ngày: {khoan_chi['date']}")
    else:
        print("Lựa chọn không hợp lệ.")

def xoa_khoan_chi(du_lieu):
    """Xóa một khoản chi tiêu."""
    if not du_lieu:
        print("Chưa có dữ liệu chi tiêu.")
        return
    ten_danh_muc = input("Nhập tên danh mục: ")
    for danh_muc in du_lieu:
        if danh_muc['ten'] == ten_danh_muc:
            break
    else:
        print(f"Không tìm thấy danh mục '{ten_danh_muc}'.")
        return

    if not danh_muc["Chitiet"]:
        print(f"Danh mục '{ten_danh_muc}' không có khoản chi nào.")
        return

    print(f"Các khoản chi trong danh mục '{ten_danh_muc}':")
    for i, khoan_chi in enumerate(danh_muc["Chitiet"], start=1):
        print(f"{i}. {khoan_chi['ten']} - {khoan_chi['sotien']} VND (Ngày: {khoan_chi['date']})")

    try:
        lua_chon = int(input("Nhập số thứ tự khoản chi cần xóa: "))
        if 1 <= lua_chon <= len(danh_muc["Chitiet"]):
            da_xoa = danh_muc["Chitiet"].pop(lua_chon - 1)
            luu_du_lieu(du_lieu)
            print(f"Đã xóa khoản chi '{da_xoa['ten']}'.")
        else:
            print("Số thứ tự không hợp lệ.")
    except ValueError:
        print("Giá trị nhập không hợp lệ.")

def tinh_tong_chi_tieu(du_lieu):
    """Tính tổng chi tiêu."""
    tong = 0
    for danh_muc in du_lieu:
        for khoan_chi in danh_muc["Chitiet"]:
            tong += khoan_chi["sotien"]
    print(f"Tổng chi tiêu: {tong} VND")

def chinh_sua_khoan_chi(du_lieu):
    """Chỉnh sửa thông tin của một khoản chi tiêu, không phân biệt chữ hoa."""
    if not du_lieu:
        print("Chưa có dữ liệu chi tiêu.")
        return
    ten_danh_muc = input("Nhập tên danh mục chứa khoản chi cần chỉnh sửa: ").strip()
    danh_muc = next((dm for dm in du_lieu if dm['ten'].lower() == ten_danh_muc.lower()), None)
    if not danh_muc:
        print(f"Không tìm thấy danh mục '{ten_danh_muc}'.")
        return

    if not danh_muc["Chitiet"]:
        print(f"Danh mục '{danh_muc['ten']}' không có khoản chi nào.")
        return

    print(f"Các khoản chi trong danh mục '{danh_muc['ten']}':")
    for i, khoan_chi in enumerate(danh_muc["Chitiet"], start=1):
        print(f"{i}. {khoan_chi['ten']} - {khoan_chi['sotien']} VND (Ngày: {khoan_chi['date']})")

    try:
        lua_chon = int(input("Nhập số thứ tự khoản chi cần chỉnh sửa: "))
        if 1 <= lua_chon <= len(danh_muc["Chitiet"]):
            khoan_chi = danh_muc["Chitiet"][lua_chon - 1]
            print(f"Đang chỉnh sửa khoản chi: {khoan_chi['ten']}")
            khoan_chi['ten'] = input(f"Tên mới (nhấn Enter để giữ nguyên '{khoan_chi['ten']}'): ") or khoan_chi['ten']
            try:
                so_tien_moi = input(f"Số tiền mới (nhấn Enter để giữ nguyên '{khoan_chi['sotien']}'): ")
                if so_tien_moi:
                    khoan_chi['sotien'] = float(so_tien_moi)
            except ValueError:
                print("Số tiền không hợp lệ! Giữ nguyên giá trị cũ.")
            khoan_chi['date'] = input(f"Ngày mới (nhấn Enter để giữ nguyên '{khoan_chi['date']}'): ") or khoan_chi['date']
            luu_du_lieu(du_lieu)
            print("Đã chỉnh sửa khoản chi thành công.")
        else:
            print("Số thứ tự không hợp lệ.")
    except ValueError:
        print("Giá trị nhập không hợp lệ.")

def tim_kiem_khoan_chi(du_lieu):
    """Tìm kiếm khoản chi tiêu hoặc danh mục theo tên."""
    if not du_lieu:
        print("Chưa có dữ liệu chi tiêu.")
        return
    tu_khoa = input("Nhập từ khóa cần tìm (khoản chi hoặc danh mục): ").lower()
    ket_qua_danh_muc = []
    ket_qua_khoan_chi = []

    # Tìm kiếm danh mục
    for danh_muc in du_lieu:
        if tu_khoa in danh_muc['ten'].lower():
            ket_qua_danh_muc.append(danh_muc)

    # Tìm kiếm khoản chi
    for danh_muc in du_lieu:
        for khoan_chi in danh_muc["Chitiet"]:
            if tu_khoa in khoan_chi['ten'].lower():
                ket_qua_khoan_chi.append((danh_muc['ten'], khoan_chi))

    # Hiển thị kết quả
    if not ket_qua_danh_muc and not ket_qua_khoan_chi:
        print("Không tìm thấy kết quả nào phù hợp.")
    else:
        if ket_qua_danh_muc:
            print("\nKết quả tìm kiếm danh mục:")
            for danh_muc in ket_qua_danh_muc:
                print(f"- Danh mục: {danh_muc['ten']}")
                if danh_muc["Chitiet"]:
                    print("Chi tiết:")
                    for khoan_chi in danh_muc["Chitiet"]:
                        print(f"+ {khoan_chi['ten']} - {khoan_chi['sotien']} VND (Ngày: {khoan_chi['date']})")
                else:
                    print("  (Danh mục này chưa có khoản chi nào)")

        if ket_qua_khoan_chi:
            print("\nKết quả tìm kiếm khoản chi:")
            for danh_muc, khoan_chi in ket_qua_khoan_chi:
                print(f"- Danh mục: {danh_muc}, Khoản chi: {khoan_chi['ten']}, Số tiền: {khoan_chi['sotien']} VND, Ngày: {khoan_chi['date']}")

def thong_ke_theo_danh_muc(du_lieu):
    """Thống kê tổng chi tiêu theo từng danh mục."""
    if not du_lieu:
        print("Chưa có dữ liệu chi tiêu.")
        return
    print("\nThống kê chi tiêu theo danh mục:")
    for danh_muc in du_lieu:
        tong = sum(khoan_chi['sotien'] for khoan_chi in danh_muc["Chitiet"])
        print(f"- {danh_muc['ten']}: {tong} VND")

def main():
    """Chương trình chính."""
    du_lieu = doc_du_lieu()
    while True:
        print("\n===== QUẢN LÝ CHI TIÊU =====")
        print("1. Thêm khoản chi")
        print("2. Xem danh sách chi tiêu")
        print("3. Xóa khoản chi")
        print("4. Tính tổng chi tiêu")
        print("5. Chỉnh sửa khoản chi")
        print("6. Tìm kiếm khoản chi")
        print("7. Thống kê chi tiêu theo danh mục")
        print("8. Thoát")
        lua_chon = input("Chọn chức năng (1-8): ")

        if lua_chon == '1':
            them_khoan_chi(du_lieu)
        elif lua_chon == '2':
            hien_thi_chi_tieu(du_lieu)
        elif lua_chon == '3':
            xoa_khoan_chi(du_lieu)
        elif lua_chon == '4':
            tinh_tong_chi_tieu(du_lieu)
        elif lua_chon == '5':
            chinh_sua_khoan_chi(du_lieu)
        elif lua_chon == '6':
            tim_kiem_khoan_chi(du_lieu)
        elif lua_chon == '7':
            thong_ke_theo_danh_muc(du_lieu)
        elif lua_chon == '8':
            print("Thoát chương trình. Cảm ơn đã sử dụng!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
