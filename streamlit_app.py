import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Freelance Fatura Hesaplayıcı", page_icon="📊")

st.title("📊 Fatura Hesaplama Paneli")
st.markdown("Günlük rate ve ek mesai bilgilerinizi girerek toplam hakedişinizi hesaplayın.")

# --- 1. ve 2. ADIM: Günlük Rate ve Çalışma Saati ---
st.header("1. Temel Ücret Bilgileri")
col1, col2 = st.columns(2)

with col1:
    daily_rate = st.number_input("Günlük Rate (Ücret) Giriniz:", min_value=0.0, step=100.0)
with col2:
    working_hours_per_day = st.number_input("Günlük Çalışma Saati:", min_value=1.0, max_value=24.0, value=8.0)

# Saatlik ücret hesabı
hourly_rate = daily_rate / working_hours_per_day if working_hours_per_day > 0 else 0
st.info(f"**Hesaplanan Standart Saatlik Ücret:** {hourly_rate:.2f} £")

st.divider()

# --- 3. ADIM: Overtime (Fazla Mesai) ---
st.header("2. Fazla Mesai (Overtime)")
has_overtime = st.checkbox("Fazla mesai yaptım")

ot_hourly_rate = 0.0
if has_overtime:
    ot_ratio = st.number_input("Overtime Çarpanı (Örn: 1.5):", min_value=1.0, value=1.5, step=0.1)
    ot_hourly_rate = hourly_rate * ot_ratio
    st.write(f"👉 **Overtime Saat Ücreti:** {ot_hourly_rate:.2f} £")

# --- 4. ADIM: Resmi Tatil ---
st.header("3. Resmi Tatil Mesaisi")
has_holiday = st.checkbox("Resmi tatilde çalıştım")

holiday_hourly_rate = 0.0
if has_holiday:
    holiday_ratio = st.number_input("Resmi Tatil Çarpanı (Örn: 2.0):", min_value=1.0, value=2.0, step=0.1)
    holiday_hourly_rate = hourly_rate * holiday_ratio
    st.write(f"👉 **Resmi Tatil Saat Ücreti:** {holiday_hourly_rate:.2f} £")

st.divider()

# --- 5. ADIM: Çalışma Bilgileri ve Hesaplama ---
st.header("4. Toplam Çalışma Verileri")

c1, c2, c3 = st.columns(3)

with c1:
    total_days = st.number_input("Toplam Çalışılan Gün Sayısı:", min_value=0, step=1)
with c2:
    total_ot_hours = st.number_input("Toplam Overtime Saati:", min_value=0.0, step=0.5) if has_overtime else 0.0
with c3:
    total_holiday_hours = st.number_input("Toplam Tatil Mesai Saati:", min_value=0.0, step=0.5) if has_holiday else 0.0

# Hesaplama Motoru
standard_total = total_days * daily_rate
ot_total = total_ot_hours * ot_hourly_rate
holiday_total = total_holiday_hours * holiday_hourly_rate
grand_total = standard_total + ot_total + holiday_total

# SONUÇ EKRANI
if st.button("FATURAYI HESAPLA", type="primary"):
    st.success(f"### Toplam Fatura Tutarı: {grand_total:,.2f} £")
    
    # Detay Tablosu
    st.markdown("#### Hesaplama Detayları")
    data = {
        "Açıklama": ["Standart Çalışma", "Fazla Mesai (OT)", "Resmi Tatil"],
        "Birim Ücret": [f"{daily_rate} £ (Gün)", f"{ot_hourly_rate:.2f} £ (Saat)", f"{holiday_hourly_rate:.2f} £ (Saat)"],
        "Miktar": [f"{total_days} Gün", f"{total_ot_hours} Saat", f"{total_holiday_hours} Saat"],
        "Toplam": [f"{standard_total:,.2f} £", f"{ot_total:,.2f} £", f"{holiday_total:,.2f} £"]
    }
    st.table(data)
