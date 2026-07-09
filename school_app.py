import streamlit as st
import pandas as pd
import psycopg2


# 1. የገጽ አቀማመጥ ማስተካከል
st.set_page_config(page_title="School System", layout="centered")

# 2. የPostgreSQL ማገናኛ መረጃ (በ pgAdmin ላይ ባለው መሠረት)
DB_CONFIG = {
    "host": "localhost",
    "database": "school_py_db",
    "user": "postgres",
    "password": "654321",
    "port": 5432
}

# 3. የሰንጠረዥ መዋቅርን በራስ-ሰር ማረጋገጫ (Database Setup)
def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS public.students (
                id SERIAL PRIMARY KEY,
                student_name VARCHAR(100) NOT NULL,
                grade_level VARCHAR(50) NOT NULL,
                parent_phone VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'NOT PAID',
                paid_bank VARCHAR(50) DEFAULT 'NONE'
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"ከዳታቤዝ ጋር መገናኘት አልተቻለም: {e}")

# አፑ ሲነሳ ሰንጠረዡ መኖሩን ያረጋግጥ
init_db()

# 4. የፊት ገጽ ዲዛይን ራስጌ
st.markdown("<h2 style='text-align: center; color: #1E88E5;'>🏫 የትምህርት ቤት ተማሪዎች መመዝገቢያና ክፍያ ሲስተም</h2>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 አዲስ ተማሪ መመዝገቢያ", "💳 የባንክ ክፍያ ማረጋገጫ"])

# ------------------ ክፍል 1፦ አዲስ ተማሪ መመዝገቢያ ------------------
with tab1:
    st.subheader("የተማሪ መረጃ ማስገቢያ")
    s_name = st.text_input("የተማሪ ሙሉ ስም (Student Name) *")
    s_grade = st.selectbox("የክፍል ደረጃ (Grade)", [f"ክፍል {i}" for i in range(1, 13)])
    s_phone = st.text_input("የወላጅ ስልክ ቁጥር (Parent Phone)")
    
    register_btn = st.button("💾 ተማሪውን መዝግብ", type="primary")
    
    if register_btn:
        if s_name.strip():
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO public.students (student_name, grade_level, parent_phone)
                    VALUES (%s, %s, %s)
                ''', (s_name.strip().upper(), s_grade, s_phone.strip()))
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"🎉 ተማሪ {s_name.upper()} በተሳካ ሁኔታ በ PostgreSQL ላይ ተመዝግቧል!")
                st.rerun()
            except Exception as e:
                st.error(f"መዝገቡ ላይ ስህተት አጋጥሟል: {e}")
        else:
            st.error("⚠️ እባክዎ የተማሪውን ስም ያስገቡ!")

# ------------------ ክፍል 2፦ የባንክ ክፍያ ማረጋገጫ ------------------
with tab2:
    st.subheader("የክፍያ ማስተካከያ (ኮር ባንኪንግ ዲፖዚት)")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df_names = pd.read_sql("SELECT student_name FROM public.students WHERE payment_status = 'NOT PAID'", conn)
        conn.close()
    except:
        df_names = pd.DataFrame()
    
    if not df_names.empty:
        student_list = df_names["student_name"].tolist()
        selected_student = st.selectbox("ክፍያ የፈጸመውን ተማሪ ይምረጡ፦", student_list)
        
        select_bank = st.selectbox("የተከፈለበት ባንክ (Settlement Bank)፦", [
            "የኢትዮጵያ ንግድ ባንክ (CBE)", 
            "አዋሽ ባንክ (Awash)", 
            "አቢሲኒያ ባንክ (Abyssinia)", 
            "ዳሸን ባንክ (Dashen)", 
            "ቴሌብር (telebirr)"
        ])
        pay_btn = st.button("✅ ክፍያን አረጋግጥ (Confirm Payment)", type="secondary")
        
        if pay_btn:
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE public.students 
                    SET payment_status = 'PAID', paid_bank = %s 
                    WHERE student_name = %s
                ''', (select_bank, selected_student))
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"💰 ለተማሪ '{selected_student}' በ '{select_bank}' የተደረገ ክፍያ በዳታቤዝ ላይ ጸድቋል!")
                st.rerun()
            except Exception as e:
                st.error(f"ክፍያውን ማጽደቅ አልተቻለም: {e}")
    else:
        st.info("📉 ክፍያ የሚጠባበቅ ያልከፈለ ተማሪ በአሁን ሰዓት የለም።")

# ------------------ የታችኛው ክፍል፦ ሙሉ የተማሪዎች መረጃ ሰንጠረዥ ------------------
st.write("---")
st.subheader("📋 የተማሪዎች አጠቃላይ መረጃ መዝገብ (Live PostgreSQL Ledger)")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    query = '''
        SELECT id AS "መለያ ቁጥር",
               student_name AS "የተማሪ ስም", 
               grade_level AS "ክፍል", 
               parent_phone AS "የወላጅ ስልክ", 
               payment_status AS "የክፍያ ሁኔታ", 
               paid_bank AS "የከፈለበት ባንክ" 
        FROM public.students
        ORDER BY id DESC
    '''
    df_students = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    df_students = pd.DataFrame()

if df_students.empty:
    st.info("📉 በአሁን ሰዓት በዳታቤዙ ላይ ምንም የተመዘገበ ተማሪ የለም።")
else:
    st.dataframe(df_students, use_container_width=True, hide_index=True)