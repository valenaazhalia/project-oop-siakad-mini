# ============================================================
# PROJECT OOP: SIAKAD MINI (SISTEM AKADEMIK KAMPUS)
# Materi yang tercakup:
#   1. Class & Object
#   2. Constructor (__init__) + Validation
#   3. Special Method (__str__, __repr__, __eq__)
#   4. Class Variable & Instance Variable
#   5. @classmethod
#   6. @staticmethod
#   7. @property (getter & setter)
#   8. Method antar objek (seperti serang -> diserang di game)
#
# Cara menjalankan:
#   python siakad_mini.py        -> mode MENU interaktif
#   python siakad_mini.py demo   -> mode DEMO otomatis
# ============================================================
import sys


# ------------------------------------------------------------
# CLASS 1: MataKuliah
# ------------------------------------------------------------
class MataKuliah:
    # CLASS VARIABLE
    jumlah_mk = 0

    # CONSTRUCTOR + VALIDATION
    def __init__(self, kode, nama, sks):
        if kode.strip() == "" or nama.strip() == "":
            raise ValueError("Kode dan nama mata kuliah tidak boleh kosong!")
        if not (1 <= sks <= 6):
            raise ValueError("SKS harus antara 1 sampai 6!")

        # INSTANCE VARIABLE
        self.kode = kode.upper()
        self.nama = nama
        self._sks = sks
        MataKuliah.jumlah_mk += 1

    # PROPERTY sks (getter + setter)
    @property
    def sks(self):
        return self._sks

    @sks.setter
    def sks(self, nilai):
        if not (1 <= nilai <= 6):
            raise ValueError("SKS harus antara 1 sampai 6!")
        self._sks = nilai

    # SPECIAL METHOD
    def __str__(self):
        return f"[{self.kode}] {self.nama:<32} {self._sks} SKS"

    def __repr__(self):
        return f"MataKuliah('{self.kode}', '{self.nama}', {self._sks})"

    def __eq__(self, other):
        return self.kode == other.kode

    # CLASS METHOD
    @classmethod
    def total_mk(cls):
        return cls.jumlah_mk

    # STATIC METHOD: konversi nilai angka -> (huruf, bobot)
    @staticmethod
    def konversi_nilai(angka):
        if angka >= 85:
            return "A", 4.0
        elif angka >= 70:
            return "B", 3.0
        elif angka >= 55:
            return "C", 2.0
        elif angka >= 40:
            return "D", 1.0
        return "E", 0.0


# ------------------------------------------------------------
# CLASS 2: Mahasiswa
# ------------------------------------------------------------
class Mahasiswa:
    BATAS_SKS = 24            # class variable (konstanta)
    jumlah_mahasiswa = 0
    daftar_semua = []         # menyimpan semua objek mahasiswa

    def __init__(self, nama, nim, jurusan):
        if not nim.isdigit() or len(nim) != 10:
            raise ValueError("NIM harus berupa 10 digit angka!")
        self.nama = nama                 # lewat setter property nama
        self.nim = nim
        self.jurusan = jurusan
        self.krs = {}                    # {kode: [objek MataKuliah, nilai]}
        Mahasiswa.jumlah_mahasiswa += 1
        Mahasiswa.daftar_semua.append(self)

    # PROPERTY nama (getter + setter, seperti property_method.py)
    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        if nilai.strip() == "":
            raise ValueError("Nama tidak boleh kosong!")
        self._nama = nilai

    # PROPERTY read-only (dihitung otomatis)
    @property
    def total_sks(self):
        return sum(mk.sks for mk, _ in self.krs.values())

    @property
    def ipk(self):
        total_bobot, total_sks = 0.0, 0
        for mk, nilai in self.krs.values():
            if nilai is not None:
                _, bobot = MataKuliah.konversi_nilai(nilai)   # static method
                total_bobot += bobot * mk.sks
                total_sks += mk.sks
        return total_bobot / total_sks if total_sks else 0.0

    @property
    def predikat(self):
        if self.ipk >= 3.5:
            return "Cum Laude"
        elif self.ipk >= 3.0:
            return "Sangat Memuaskan"
        elif self.ipk >= 2.0:
            return "Memuaskan"
        return "Perlu Peningkatan"

    # METHOD (dipanggil oleh objek lain / pengguna)
    def ambil_mk(self, mk):
        if mk.kode in self.krs:
            raise ValueError(f"{mk.nama} sudah diambil!")
        if self.total_sks + mk.sks > Mahasiswa.BATAS_SKS:
            raise ValueError(f"Melebihi batas {Mahasiswa.BATAS_SKS} SKS!")
        self.krs[mk.kode] = [mk, None]
        print(f"[OK] {self.nama} mengambil {mk.nama}.")

    def terima_nilai(self, mk, angka):          # dipanggil oleh Dosen
        if mk.kode not in self.krs:
            raise ValueError(f"{self.nama} tidak mengambil {mk.nama}!")
        if not (0 <= angka <= 100):
            raise ValueError("Nilai harus antara 0 sampai 100!")
        self.krs[mk.kode][1] = angka

    def cetak_transkrip(self):
        print("\n" + "=" * 56)
        print("                  TRANSKRIP NILAI")
        print("=" * 56)
        print(f"Nama    : {self.nama}")
        print(f"NIM     : {self.nim}")
        print(f"Jurusan : {self.jurusan}")
        print("-" * 56)
        if not self.krs:
            print("(belum mengambil mata kuliah)")
        for mk, nilai in self.krs.values():
            if nilai is None:
                print(f"{mk.nama:<32}{mk.sks} SKS   belum dinilai")
            else:
                huruf, _ = MataKuliah.konversi_nilai(nilai)
                print(f"{mk.nama:<32}{mk.sks} SKS {nilai:>6.1f} ({huruf})")
        print("-" * 56)
        print(f"Total SKS : {self.total_sks}")
        print(f"IPK       : {self.ipk:.2f}  -> {self.predikat}")
        print("=" * 56)

    # SPECIAL METHOD
    def __str__(self):
        return f"{self.nama} ({self.nim}) - {self.jurusan} | IPK {self.ipk:.2f}"

    def __repr__(self):
        return f"Mahasiswa('{self.nama}', '{self.nim}', '{self.jurusan}')"

    def __eq__(self, other):
        return self.nim == other.nim

    # CLASS METHOD
    @classmethod
    def total_mahasiswa(cls):
        return cls.jumlah_mahasiswa

    @classmethod
    def rata_rata_ipk(cls):
        dinilai = [m.ipk for m in cls.daftar_semua if m.ipk > 0]
        return sum(dinilai) / len(dinilai) if dinilai else 0.0

    @classmethod
    def mahasiswa_terbaik(cls):
        if not cls.daftar_semua:
            return None
        return max(cls.daftar_semua, key=lambda m: m.ipk)


# ------------------------------------------------------------
# CLASS 3: Dosen -> berinteraksi dengan Mahasiswa & MataKuliah
# ------------------------------------------------------------
class Dosen:
    jumlah_dosen = 0

    def __init__(self, nama, nidn, mk_diampu):
        if nama.strip() == "":
            raise ValueError("Nama dosen tidak boleh kosong!")
        if not nidn.isdigit() or len(nidn) != 8:
            raise ValueError("NIDN harus berupa 8 digit angka!")
        self.nama = nama
        self.nidn = nidn
        self.mk_diampu = mk_diampu          # objek MataKuliah
        Dosen.jumlah_dosen += 1

    # METHOD antar objek (mirip serang -> diserang)
    def beri_nilai(self, mahasiswa, angka):
        mahasiswa.terima_nilai(self.mk_diampu, angka)
        huruf, _ = MataKuliah.konversi_nilai(angka)
        print(f"[OK] {self.nama} memberi nilai {angka} ({huruf}) "
              f"untuk {mahasiswa.nama} di {self.mk_diampu.nama}.")

    def __str__(self):
        return f"{self.nama} (NIDN {self.nidn}) - mengampu {self.mk_diampu.nama}"

    def __repr__(self):
        return f"Dosen('{self.nama}', '{self.nidn}', {self.mk_diampu!r})"

    @classmethod
    def total_dosen(cls):
        return cls.jumlah_dosen


# ============================================================
# DATA AWAL
# ============================================================
def siapkan_data():
    mk = {
        "PBO": MataKuliah("PBO", "Pemrograman Berorientasi Objek", 3),
        "BDA": MataKuliah("BDA", "Basis Data", 3),
        "ALG": MataKuliah("ALG", "Algoritma & Struktur Data", 4),
        "JKM": MataKuliah("JKM", "Jaringan Komputer", 3),
        "MTK": MataKuliah("MTK", "Matematika Diskrit", 3),
    }
    dosen = {
        "PBO": Dosen("Pak Andika", "12345678", mk["PBO"]),
        "BDA": Dosen("Bu Sari", "23456789", mk["BDA"]),
        "ALG": Dosen("Pak Budi", "34567890", mk["ALG"]),
        "JKM": Dosen("Bu Rina", "45678901", mk["JKM"]),
        "MTK": Dosen("Pak Hendra", "56789012", mk["MTK"]),
    }
    mhs = [
        Mahasiswa("Riko", "2023010001", "Teknik Informatika"),
        Mahasiswa("Dika", "2023010002", "Sistem Informasi"),
    ]
    return mk, dosen, mhs


# ============================================================
# MODE DEMO
# ============================================================
def demo():
    mk, dosen, mhs = siapkan_data()
    riko, dika = mhs

    print("===== 1. OBJEK AWAL =====")
    for m in mk.values():
        print(m)
    print(repr(mk["PBO"]))
    print(dosen["PBO"])
    print(riko)
    print("riko == dika ?", riko == dika)

    print("\n===== 2. VALIDASI =====")
    for aksi in (lambda: MataKuliah("XXX", "Salah", 9),
                 lambda: Mahasiswa("Rina", "123", "TI"),
                 lambda: setattr(riko, "nama", "")):
        try:
            aksi()
        except ValueError as e:
            print("Gagal:", e)

    print("\n===== 3. PENGISIAN KRS =====")
    for kode in ("PBO", "BDA", "ALG"):
        riko.ambil_mk(mk[kode])
    dika.ambil_mk(mk["PBO"])
    try:
        riko.ambil_mk(mk["PBO"])
    except ValueError as e:
        print("Gagal:", e)

    print("\n===== 4. DOSEN MEMBERI NILAI =====")
    dosen["PBO"].beri_nilai(riko, 90)
    dosen["BDA"].beri_nilai(riko, 78)
    dosen["ALG"].beri_nilai(riko, 65)
    dosen["PBO"].beri_nilai(dika, 72)
    try:
        dosen["BDA"].beri_nilai(dika, 80)       # dika tidak ambil BDA
    except ValueError as e:
        print("Gagal:", e)

    riko.cetak_transkrip()
    dika.cetak_transkrip()

    print("\n===== 5. STATISTIK (CLASS METHOD) =====")
    print("Total mata kuliah :", MataKuliah.total_mk())
    print("Total mahasiswa   :", Mahasiswa.total_mahasiswa())
    print("Total dosen       :", Dosen.total_dosen())
    print(f"Rata-rata IPK     : {Mahasiswa.rata_rata_ipk():.2f}")
    print("Mahasiswa terbaik :", Mahasiswa.mahasiswa_terbaik())
    print("Konversi 88       :", MataKuliah.konversi_nilai(88))   # static method


# ============================================================
# MODE MENU INTERAKTIF
# ============================================================
def pilih_mahasiswa(daftar):
    for i, m in enumerate(daftar, 1):
        print(f"  {i}. {m}")
    return daftar[int(input("Pilih nomor mahasiswa: ")) - 1]


def pilih_mk(mk):
    for k, m in mk.items():
        print(f"  {m}")
    kode = input("Masukkan kode MK: ").strip().upper()
    if kode not in mk:
        raise ValueError("Kode mata kuliah tidak ditemukan!")
    return mk[kode]


def menu():
    mk, dosen, mhs = siapkan_data()
    while True:
        print("\n========== SIAKAD MINI ==========")
        print("1. Lihat mata kuliah")
        print("2. Lihat mahasiswa")
        print("3. Daftar mahasiswa baru")
        print("4. Ambil mata kuliah (KRS)")
        print("5. Beri nilai (oleh dosen)")
        print("6. Cetak transkrip")
        print("7. Statistik kampus")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                for m in mk.values():
                    print(m)
            elif pilihan == "2":
                for m in mhs:
                    print(m)
            elif pilihan == "3":
                mhs.append(Mahasiswa(input("Nama: "), input("NIM (10 digit): "),
                                     input("Jurusan: ")))
                print("[OK] Mahasiswa berhasil didaftarkan.")
            elif pilihan == "4":
                pilih_mahasiswa(mhs).ambil_mk(pilih_mk(mk))
            elif pilihan == "5":
                m = pilih_mahasiswa(mhs)
                matkul = pilih_mk(mk)
                dosen[matkul.kode].beri_nilai(m, float(input("Nilai (0-100): ")))
            elif pilihan == "6":
                pilih_mahasiswa(mhs).cetak_transkrip()
            elif pilihan == "7":
                print("Total mahasiswa :", Mahasiswa.total_mahasiswa())
                print("Total mata kuliah:", MataKuliah.total_mk())
                print("Total dosen     :", Dosen.total_dosen())
                print(f"Rata-rata IPK   : {Mahasiswa.rata_rata_ipk():.2f}")
                print("Terbaik         :", Mahasiswa.mahasiswa_terbaik())
            elif pilihan == "0":
                print("Terima kasih!")
                break
            else:
                print("Menu tidak tersedia.")
        except ValueError as e:
            print("[ERROR]", e)
        except IndexError:
            print("[ERROR] Nomor tidak valid.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        menu()