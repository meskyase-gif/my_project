import streamlit as st
import pandas as pd
import psycopg2


# 1. የገጽ አቀማመጥ ማስተካከል
#st.set_page_config(page_title="TEST", layout="centered")

# 2. የPostgreSQL ማገናኛ መረጃ (በ pgAdmin ላይ ባለው መሠረት)
DB_CONFIG = {
    "host": "localhost",
    "database": "TEST",
    "user": "postgres",
    "password": "654321",
    "port": 5432
}
# ------------------ ክፍል 1፦ አዲስ ተማሪ መመዝገቢያ ------------------
tab, = st.tabs([""])

with tab:
    st.subheader("የመረጃ ማስገቢያ")
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


# ------------------ የታችኛው ክፍል፦ ሙሉ የተማሪዎች መረጃ ሰንጠረዥ ------------------
st.write("---")
st.subheader("📋 የአጠቃላይ መረጃ መዝገብ ")

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