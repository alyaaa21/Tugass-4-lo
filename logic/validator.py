def validate_input(judul, sutradara, durasi):
    if not judul or not sutradara or not durasi:
        return False, "Semua field wajib diisi!"

    if not durasi.isdigit():
        return False, "Durasi harus berupa angka!"

    return True, ""