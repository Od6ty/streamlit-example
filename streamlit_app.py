import streamlit as st
from streamlit import session_state

st.set_page_config(
    page_title="Vipira.ly",
    page_icon="Vipira(logo).png",
    layout="centered"
)

if 'data_perpulau' not in session_state:
    session_state.data_perpulau = {
        'Sumatera dan sekitarnya': {'Jokowi-Maruf Amin': 14673821, 'Prabowo-Sandi': 18036007},
        'Jawa dan sekitarnya': {'Jokowi-Maruf Amin': 53630049, 'Prabowo-Sandi': 37544287},
        'Kalimantan dan sekitarnya': {'Jokowi-Maruf Amin': 3613022, 'Prabowo-Sandi': 3377220},
        'Sulawesi dan sekitarnya': {'Jokowi-Maruf Amin': 5653482, 'Prabowo-Sandi': 4326598},
        'Papua dan sekitarnya': {'Jokowi-Maruf Amin': 4440715, 'Prabowo-Sandi': 1178847},
    }

# Akun admin
admin_username = "kelompok10"
admin_password = "politik"

# Membuat pie chart
def create_image(daerah):
    labels = list(session_state.data_perpulau[daerah].keys())
    sizes = [session_state.data_perpulau[daerah][label] for label in labels]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    image_path = f"{daerah.replace(' ', '_')}_pie_chart.png"
    fig.savefig(image_path)
    plt.close(fig)
    return image_path

# Centang jika ingin menampilkan box login
is_logged_in = st.sidebar.checkbox("Admin Login")
if is_logged_in:

    # Kode menginputkan username dan password
    username = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type="password")

    # Jika username dan password benar, akan muncul selectbox yang berisi 5 pulau besar Indonesia
    if username == admin_username and password == admin_password:
        st.success("Login Berhasil! Anda sekarang bisa menambahkan proporsi suara baru.")

        menu = st.sidebar.radio("Menu", ["Tambah Suara", "Hanya Lihat"], key="menu")

        if menu == "Tambah Suara":
            st.sidebar.header("Tambah Suara")

            # Memilih data mana yang akan ditambahkan
            selected_region = st.sidebar.selectbox('Pilih Daerah:', list(session_state.data_perpulau.keys()), key="add_portions")

            # Menginputkan jumlah penambahan suara
            additional_percentage_jokowi = st.sidebar.number_input("Tambah Suara Jokowi-Maruf Amin", 0, 999999999, 0)
            additional_percentage_prabowo = st.sidebar.number_input("Tambah Suara Prabowo-Sandi", 0, 999999999, 0)

            # Akan berjalan jika menekan tombol "Simpan Proporsi"
            if st.sidebar.button("Simpan"):

                # Mengupdate data
                session_state.data_perpulau[selected_region]['Jokowi-Maruf Amin'] += additional_percentage_jokowi
                session_state.data_perpulau[selected_region]['Prabowo-Sandi'] += additional_percentage_prabowo

                # Mengupdate pie chart sesuai data
                image_path = create_image(selected_region)
                st.image(image_path, caption=f"Hasil Pemilihan di {selected_region}", use_column_width=True)

                # Menampilkan hasil suara setelah update data
                st.write(f"Suara Pasangan 1 (Jokowi-Maruf Amin): {session_state.data_perpulau[selected_region]['Jokowi-Maruf Amin']}")
                st.write(f"Suara Pasangan 2 (Prabowo-Sandi): {session_state.data_perpulau[selected_region]['Prabowo-Sandi']}")

        elif menu == "Hanya Lihat":
            pass

    # Tampil jika username atau password ada yang salah
    else:
        st.warning("Username atau password yang anda coba masukkan salah. Silahkan coba lagi.")
else:
    st.sidebar.warning("Silakan login untuk mengakses opsi admin.")

# Mendefinisikan total suara masing-masing paslon dan suara total yang masuk
totalsuara_jokowi = sum(session_state.data_perpulau[daerah]['Jokowi-Maruf Amin'] for daerah in session_state.data_perpulau)
totalsuara_prabowo = sum(session_state.data_perpulau[daerah]['Prabowo-Sandi'] for daerah in session_state.data_perpulau)
totalsuara_indonesia = totalsuara_jokowi + totalsuara_prabowo
persentase_jokowi = totalsuara_jokowi*100/totalsuara_indonesia
persentase_prabowo = totalsuara_prabowo*100/totalsuara_indonesia

st.sidebar.write("---")
st.title('Vipira.ly')
st.write("Vipira atau Visualisasi Pilihan Rakyat hadir untuk memberikan visualisasi Quick Count pemilihan presiden di Indonesia. Admin dapat menambah besarnya perolehan suara untuk setiap calon pasangan dan melihat grafik hasil pemilihan secara langsung.")
selected_daerah = st.selectbox('Pilih Daerah:', list(session_state.data_perpulau.keys()), key="add_proportions")
image_path = create_image(selected_daerah)
st.write(f"Suara Pasangan 1 (Jokowi-Maruf Amin): {session_state.data_perpulau[selected_daerah]['Jokowi-Maruf Amin']}")
st.write(f"Suara Pasangan 2 (Prabowo-Sandi): {session_state.data_perpulau[selected_daerah]['Prabowo-Sandi']}")
st.image(image_path, caption=f"Hasil Pemilihan di {selected_daerah}", use_column_width=True)
st.sidebar.write(f"Total Suara Pasangan 1 (Jokowi-Maruf Amin): {totalsuara_jokowi}")
st.sidebar.write(f"Persentase suara Jokowi-Maruf Amin: {persentase_jokowi}%")
st.sidebar.write(f"Total Suara Pasangan 2 (Prabowo-Sandi): {totalsuara_prabowo}")
st.sidebar.write(f"Persentase suara Prabowo-Sandi: {persentase_prabowo}%")
st.sidebar.write(f"Total Suara yang Masuk: {totalsuara_indonesia}")
