import streamlit as st
import psycopg2
import pandas as pd
import qrcode
from io import BytesIO

st.set_page_config(page_title="Meski-Flavor Inventory", layout="centered")

st.title("🌶️ የMeski-Flavor ቅመማቅመም ማከማቻ እና ጥራት ቁጥጥር")

# የዳታቤዝ ግንኙነት መረጃ
DB_CONFIG = {
    "host": "localhost",
    "database": "flavor_py_db",
    "user": "postgres",
    "password": "654321",
    "port": 5432
}

# 🔄 አዲስ ሰንጠረዥ በራስ-ሰር መኖሩን ማረጋገጫና መፍጠሪያ ፈንክሽን
def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS public.flavor_products (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                batch_number VARCHAR(50) NOT NULL,
                quantity_kg NUMERIC(10, 2) NOT NULL,
                production_date DATE NOT NULL,
                quality_status VARCHAR(50) DEFAULT 'PENDING',
                qr_code_data TEXT
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"ሰንጠረዡን በዳታቤዙ ላይ መፍጠር አልተቻለም፦ {e}")

# አፑ ሲነሳ መጀመሪያ ዳታቤዙን ያዘጋጃል
init_db()

# 1. አዲስ ምርት በዳታቤዝ ውስጥ መመዝገቢያ ፈንክሽን
def save_product(name, batch, qty, prod_date, status):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # ለQR ኮድ የሚሆን ልዩ መረጃ ማዘጋጀት
        qr_data = f"Product: {name} | Batch: {batch} | Qty: {qty}kg | Date: {prod_date} | Status: {status}"
        
        # ስሙ ወደ public.flavor_products ተስተካክሏል
        query = """
            INSERT INTO public.flavor_products (product_name, batch_number, quantity_kg, production_date, quality_status, qr_code_data)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (name, batch, qty, prod_date, status, qr_data))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"ዳታቤዝ ላይ ለመመዝገብ አልተቻለም፦ {e}")
        return False

# 2. የQR ኮድ ምስል በራስ-ሰር ማመንጫ ፈንክሽን
def generate_qr_image(data_text):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # ምስሉን በሜሞሪ ውስጥ ጊዜያዊ ፋይል አድርጎ መያዣ
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# --- የተጠቃሚ በይነገጽ (UI) ---
tab1, tab2 = st.tabs(["➕ አዲስ ምርት መመዝገቢያ", "📊 የማከማቻ ክምችት ሪፖርት"])

with tab1:
    st.subheader("የቅመም ምርት መረጃ ማስገቢያ")
    
    p_name = st.text_input("የቅመሙ ስም (Product Name) *", placeholder="ምሳሌ፦ የገበታ በርበሬ")
    b_num = st.text_input("የምርት ስብስብ ቁጥር (Batch Number) *", placeholder="ምሳሌ፦ EF-2026-B1")
    p_qty = st.number_input("የምርት መጠን በኪሎግራም (Quantity KG)", min_value=0.0, step=0.5)
    p_date = st.date_input("የተመረተበት ቀን (Production Date)")
    p_status = st.selectbox("የጥራት ደረጃ (Quality Status)", ["PENDING", "APPROVED", "REJECTED"])
    
    if st.button("💾 ምርቱን መዝግብ እና QR ኮድ አውጣ"):
        if p_name.strip() and b_num.strip():
            success = save_product(p_name.strip(), b_num.strip(), p_qty, p_date, p_status)
            if success:
                st.success(f"🎉 '{p_name.upper()}' በተሳካ ሁኔታ ማከማቻው ውስጥ ተመዝግቧል!")
                
                # ለዚህ ምርት የተሰራውን የQR ኮድ ማሳየት
                test_data = f"Flavor\nProduct: {p_name.upper()}\nBatch: {b_num.upper()}\nStatus: {p_status}"
                qr_img_bytes = generate_qr_image(test_data)
                
                st.image(qr_img_bytes, caption=f"ለ {p_name.upper()} የተዘጋጀ ልዩ የQR መለያ", width=200)
                st.download_button("📥 የQR ኮዱን ምስል አውርድ (Download)", data=qr_img_bytes, file_name=f"{b_num}_qr.png", mime="image/png")
        else:
            st.warning("እባክዎ የተኮከቡባቸውን (*) ቦታዎች በሙሉ በትክክል ይሙሉ!")

with tab2:
    st.subheader("በማከማቻ ውስጥ ያሉ የቅመም ምርቶች ዝርዝር")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # ስሙ ወደ public.flavor_products ተስተካክሏል
        df = pd.read_sql("SELECT id, product_name, batch_number, quantity_kg, production_date, quality_status FROM public.flavor_products ORDER BY id DESC;", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("በአሁኑ ሰዓት በማከማቻው ውስጥ ምንም የተመዘገበ የቅመም ምርት የለም።")
    except Exception as e:
        st.error(f"ሪፖርቱን ለማንበብ አልተቻለም፦ {e}")