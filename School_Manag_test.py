import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime
import random

# የገጽታ ማስተካከያ

st.set_page_config(page_title="Meski_School_Management", layout="wide")

# የዳታቤዝ ግንኙነት መረጃ
DB_CONFIG = {
    "host": "localhost",
    "database": "school_register_test",  
    "user": "postgres",
    "password": "654321",           
    "port": 5432
}

# ከPostgreSQL ዳታቤዝ ጋር የሚያገናኝ ዋና ፈንክሽን
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# የተጠቃሚውን ስም እና የይለፍ ቃል ከዳታቤዝ ጋር የሚያገናኝ ፈንክሽን
def check_login(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT username, full_name FROM public.users WHERE username = %s AND password = %s;"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        st.error(f"የዳታቤዝ ስህተት አጋጥሟል: {e}")
        return None

# ==========================================
# 🔐 የሎጊን ቁጥጥር (SESSION STATE & AUTH)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""

# ተጠቃሚው ካልገባ መጀመሪያ የሎጊን ፎርም ብቻ አሳይ
if not st.session_state.logged_in:
    st.title("🌐 Meski_School_Management(MSM)")
    st.subheader("🔑 ወደ MSM አድሚን ሲስተም ይግቡ")
    
    with st.form("login_form"):
        username_input = st.text_input("የተጠቃሚ ስም (Username)")
        password_input = st.text_input("የይለፍ ቃል (Password)", type="password")
        login_submit = st.form_submit_button("ግባ (Login)")
        
        if login_submit:
            user_info = check_login(username_input, password_input)
            if user_info:
                st.session_state.logged_in = True
                st.session_state.user_name = user_info[1]
                ##st.success(f"እንኳን በደህና መጡ {user_info[1]}!")
                st.rerun()
            else:
                st.error("የተሳሳተ የተጠቃሚ ስም ወይም የይለፍ ቃል አስገብተዋል!")

# ==========================================
# 🔓 ተጠቃሚው በትክክል ከገባ በኋላ የሚከፈተው ዋናው ሲስተም
# ==========================================
else:
    # --- ዋና የጎን ማውጫ (Sidebar Dashboard) ---
    st.sidebar.title("🌐 MSM")
    st.sidebar.write(f"👤 አድሚን: **{st.session_state.user_name}**")
    
    if st.sidebar.button("ውጣ (Logout)"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.rerun()
        
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("ማውጫ (Navigation)", ["📊 ዳሽቦርድ (Dashboard)", "👥 የተማሪዎች ምዝገባ", "📜 የክፍያ ዓይነቶች", "💳 የPayten ክፍያ መፈጸሚያ"])

    st.sidebar.markdown("---")
    st.sidebar.success("PostgreSQL: Connected ✅")
    st.sidebar.success("Payten Gateway: Active 🟢")

    # ==========================================
    # 1. ዳሽቦርድ እይታ (DASHBOARD VIEW)
    # ==========================================
    if menu == "📊 ዳሽቦርድ (Dashboard)":
        st.title("📈 አጠቃላይ የMeskiFinance መረጃ መቆጣጠሪያ")
        
        try:
            conn = get_db_connection()
            
            # የዳታ አጠቃላይ ድምር ለማውጣት
            total_students = pd.read_sql("SELECT COUNT(*) FROM public.students;", conn).iloc[0,0]
            total_collected = pd.read_sql("SELECT SUM(amount) FROM public.payments WHERE status='Success';", conn).iloc[0,0] or 0
            total_pending = pd.read_sql("""
                SELECT SUM(f.amount) FROM public.fee_assignments fa 
                JOIN public.fee_types f ON fa.fee_id = f.id WHERE fa.status='Pending';
            """, conn).iloc[0,0] or 0
            
            conn.close()
            
            # የሪፖርት ማሳያ ካርዶች
            col1, col2, col3 = st.columns(3)
            col1.metric("አጠቃላይ የተመዘገቡ ተማሪዎች", f"{total_students} ተማሪዎች")
            col2.metric("በPayten የተሰበሰበ ክፍያ", f"${total_collected:,.2f}", delta="🟢 Live")
            col3.metric("ያልተከፈለ ቀሪ ክፍያ (Pending)", f"${total_pending:,.2f}", delta="⚠️ Urgent", delta_color="inverse")
            
            st.markdown("---")
            st.subheader("🔄 የቅርብ ጊዜ የዳታቤዝ ትራንዛክሽኖች (Recent Activities)")
            
            conn = get_db_connection()
            recent_df = pd.read_sql("""
                SELECT p.payten_ref as "የክፍያ መለያ", s.full_name as "የተማሪ ስም", f.fee_name as "የክፍያ ዓይነት", 
                       p.amount as "የገንዘብ መጠን", p.payment_method as "የክፍያ መንገድ", p.payment_date as "የተከፈለበት ቀን"
                FROM public.payments p
                JOIN public.students s ON p.student_id = s.id
                JOIN public.fee_types f ON p.fee_id = f.id
                ORDER BY p.id DESC LIMIT 5;
            """, conn)
            conn.close()
            
            if not recent_df.empty:
                st.dataframe(recent_df, use_container_width=True)
            else:
                st.info("እስካሁን በዳታቤዙ ላይ የተመዘገበ አዲስ የክፍያ እንቅስቃሴ የለም።")
                
        except Exception as e:
            st.error(f"መረጃውን ከዳታቤዝ ማንበብ አልተቻለም፦ {e}")

    # ==========================================
    # 2. የተማሪዎች ምዝገባ (STUDENT REGISTER)
    # ==========================================
    elif menu == "👥 የተማሪዎች ምዝገባ":
        st.title("👥 የተማሪዎች ማህደር እና አዲስ ምዝገባ")
        
        tab1, tab2 = st.tabs(["📋 የነባር ተማሪዎች ዝርዝር", "➕ አዲስ ተማሪ መመዝገቢያ"])
        
        with tab1:
            st.subheader("በሲስተሙ ላይ ያሉ ተማሪዎች")
            search_query = st.text_input("🔍 ተማሪ በስም ፈልግ...", placeholder="የተማሪውን ስም እዚህ ይጻፉ...")
            
            try:
                conn = get_db_connection()
                if search_query:
                    df = pd.read_sql(f"SELECT id as \"መለያ ቁጥር\", full_name as \"የተማሪ ስም\", email as \"ኢሜይል\", grade as \"ክፍል\", parent_name as \"የወላጅ ስም\", parent_phone as \"ስልክ\", status as \"ሁኔታ\" FROM public.students WHERE full_name ILIKE '%{search_query}%' ORDER BY id DESC;", conn)
                else:
                    df = pd.read_sql("SELECT id as \"መለያ ቁጥር\", full_name as \"የተማሪ ስም\", email as \"ኢሜይል\", grade as \"ክፍል\", parent_name as \"የወላጅ ስም\", parent_phone as \"ስልክ\", status as \"ሁኔታ\" FROM public.students ORDER BY id DESC;", conn)
                conn.close()
                
                if not df.empty:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("ምንም የተመዘገበ ተማሪ አልተገኘም።")
            except Exception as e:
                st.error(f"የተማሪዎችን መረጃ መጫን አልተቻለም፦ {e}")
                
        with tab2:
            st.subheader("የአዲስ ተማሪ መረጃ ማስገቢያ ፎርም")
            with st.form("student_form", clear_on_submit=True):
                s_name = st.text_input("የተማሪው ሙሉ ስም *")
                s_email = st.text_input("ኢሜይል አድራሻ *")
                s_grade = st.selectbox("ክፍል / ደረጃ *", [f"Grade {i}" for i in range(1, 13)])
                s_parent = st.text_input("የወላጅ/አስጋሪ ሙሉ ስም *")
                s_phone = st.text_input("የወላጅ ስልክ ቁጥር *")
                s_status = st.selectbox("የተማሪው ሁኔታ", ["Active", "Pending", "Inactive"])
                
                submitted = st.form_submit_button("💾 ተማሪውን ወደ PostgreSQL መዝግብ")
                if submitted:
                    if s_name.strip() and s_email.strip() and s_parent.strip() and s_phone.strip():
                        try:
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO public.students (full_name, email, grade, parent_name, parent_phone, status)
                                VALUES (%s, %s, %s, %s, %s, %s);
                            """, (s_name.strip().upper(), s_email.strip(), s_grade, s_parent.strip().upper(), s_phone.strip(), s_status))
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.success(f"🎉 ተማሪ '{s_name.upper()}' በተሳካ ሁኔታ ዳታቤዝ ውስጥ ተመዝግቧል!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"ዳታቤዝ ላይ መመዝገብ አልተቻለም፦ {e}")
                    else:
                        st.warning("እባክዎ ምልክት የተደረገባቸውን (*) ቦታዎች በሙሉ ይሙሉ!")

    # ==========================================
    # 3. የክፍያ ዓይነቶች ማስተዳደሪያ (FEE MANAGEMENT)
    # ==========================================
    elif menu == "📜 የክፍያ ዓይነቶች":
        st.title("📜 የትምህርት ቤት ክፍያ ዓይነቶች እና ክፍያ መደብ")
        
        tab1, tab2, tab3 = st.tabs(["💎 ያሉ የክፍያ ዓይነቶች", "➕ አዲስ የክፍያ ዓይነት መፍጠሪያ", "🎯 ክፍያ ለተማሪ መደቢያ (Assign)"])
        
        with tab1:
            try:
                conn = get_db_connection()
                df_fees = pd.read_sql("SELECT id, fee_name as \"የክፍያ ስም\", amount as \"ዋጋ ($)\", category as \"ምድብ\", description as \"ማብራሪያ\" FROM public.fee_types ORDER BY id DESC;", conn)
                conn.close()
                if not df_fees.empty:
                    st.dataframe(df_fees, use_container_width=True, hide_index=True)
                else:
                    st.info("ምንም የተፈጠረ የክፍያ ዓይነት የለም።")
            except Exception as e:
                st.error(f"መረጃውን መጫን አልተቻለም፦ {e}")
                
        with tab2:
            st.subheader("አዲስ የክፍያ መዋቅር መፍጠሪያ")
            with st.form("fee_form", clear_on_submit=True):
                f_name = st.text_input("የክፍያው ስም (e.g., Tuition Fee 2026) *")
                f_amount = st.number_input("የገንዘብ መጠን ($) *", min_value=0.0, step=50.0)
                f_category = st.selectbox("የክፍያ ምድብ", ["Tuition", "Library", "Lab", "Sports", "Transport", "Other"])
                f_desc = st.text_area("ስለ ክፍያው አጭር ማብራሪያ")
                
                fee_submitted = st.form_submit_button("Create Fee Structure")
                if fee_submitted:
                    if f_name.strip() and f_amount > 0:
                        try:
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO public.fee_types (fee_name, amount, category, description)
                                VALUES (%s, %s, %s, %s);
                            """, (f_name.strip(), f_amount, f_category, f_desc.strip()))
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.success(f"✅ የክፍያ ዓይነት '{f_name}' በስኬት ተፈጥሯል!")
                        except Exception as e:
                            st.error(f"ሊፈጠር አልቻለም፦ {e}")
                    else:
                        st.warning("እባክዎ ስምና የገንዘብ መጠን በትክክል ያስገቡ!")

        with tab3:
            st.subheader("የተፈጠረን ክፍያ ለተማሪ መመደብ")
            try:
                conn = get_db_connection()
                students_df = pd.read_sql("SELECT id, full_name, grade FROM public.students;", conn)
                fees_df = pd.read_sql("SELECT id, fee_name, amount FROM public.fee_types;", conn)
                
                assignments_df = pd.read_sql("""
                    SELECT fa.id as "የመዝገብ ቁጥር (ID)", s.full_name as "የተማሪ ስም", f.fee_name as "የክፍያ ዓይነት", f.amount as "መጠን ($)", fa.status as "ሁኔታ"
                    FROM public.fee_assignments fa
                    JOIN public.students s ON fa.student_id = s.id
                    JOIN public.fee_types f ON fa.fee_id = f.id ORDER BY fa.id DESC;
                """, conn)
                conn.close()
                
                student_options = {row['full_name']: row['id'] for _, row in students_df.iterrows()}
                fee_options = {row['fee_name'] + f" (${row['amount']})": row['id'] for _, row in fees_df.iterrows()}
                
                # --- የክፍያ መመደቢያ ፎርም ---
                col1, col2 = st.columns(2)
                with col1:
                    selected_student = st.selectbox("ተማሪ ይምረጡ", list(student_options.keys()) if student_options else ["ተማሪ የለም"])
                with col2:
                    selected_fee = st.selectbox("የክፍያ ዓይነት ይምረጡ", list(fee_options.keys()) if fee_options else ["የክፍያ ዓይነት የለም"])
                    
                if st.button("🎯 ክፍያውን ለተማሪው መድብ"):
                    if student_options and fee_options:
                        s_id = student_options[selected_student]
                        fee_id = fee_options[selected_fee]
                        
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO public.fee_assignments (student_id, fee_id, status)
                            VALUES (%s, %s, 'Pending');
                        """, (s_id, fee_id))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("🎯 ክፍያው ለተማሪው በ-Pending ሁኔታ ተመድቧል!")
                        st.rerun()
                
                # --- 🔥 አዲስ የተጨመረ: የተመደበ ክፍያ ማጥፊያ (Delete Section) ---
                if not assignments_df.empty:
                    st.markdown("---")
                    st.subheader("🗑️ የተመደበ ክፍያን መሰረዣ")
                    
                    # ተጠቃሚው በቀላሉ ማጥፋት የሚፈልገውን የመዝገብ ቁጥር (ID) እንዲመርጥ ማድረግ
                    delete_options = {f"መለያ ID {row['የመዝገብ ቁጥር (ID)']} - {row['የተማሪ ስም']} ({row['የክፍያ ዓይነት']})": row['የመዝገብ ቁጥር (ID)'] for _, row in assignments_df.iterrows()}
                    selected_to_delete = st.selectbox("ማጥፋት የሚፈልጉትን የተመደበ ክፍያ ይምረጡ፦", list(delete_options.keys()))
                    
                    if st.button("❌ የተመደበውን ክፍያ ሰርዝ", type="primary"):
                        assignment_id_to_delete = delete_options[selected_to_delete]
                        try:
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            # መረጃውን ከዳታቤዝ የማጥፋት ኩዌሪ (DELETE QUERY)
                            cursor.execute("DELETE FROM public.fee_assignments WHERE id = %s;", (assignment_id_to_delete,))
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.error(f"💥 መለያ ቁጥር {assignment_id_to_delete} ያለው የክፍያ ምደባ በተሳካ ሁኔታ ተሰርዟል!")
                            st.rerun()
                        except Exception as delete_error:
                            st.error(f"ትዕዛዙን መፈጸም አልተቻለም (ምናልባት ክፍያው ቀድሞ የተከፈለ ሊሆን ይችላል)፦ {delete_error}")

                # --- የዝርዝር ማሳያ ሰንጠረዥ ---
                st.markdown("---")
                st.write("### 📌 ለተማሪዎች የተመደቡ ክፍያዎች ዝርዝር")
                if not assignments_df.empty:
                    st.dataframe(assignments_df, use_container_width=True, hide_index=True)
                else:
                    st.info("እስካሁን ለተማሪ የተመደበ ምንም ክፍያ የለም።")
                    
            except Exception as e:
                st.error(f"የመደብ ስራውን ለመስራት አልተቻለም፦ {e}")
                
    # ==========================================
    # 4. የPAYTEN ክፍያ መፈጸሚያ (PAYMENTS GATEWAY)
    # ==========================================
    elif menu == "💳 የPayten ክፍያ መፈጸሚያ":
        st.title("💳 Payten Payment Gateway Integration")
        st.info("የተማሪዎችን ያልተከፈለ ክፍያ በካርድ፣ በባንክ ወይም በሞባይል ገንዘብ ለመቀበል ያገለግላል።")
        
        tab1, tab2 = st.tabs(["💸 ክፍያ መፈጸሚያ ፎርም", "📜 የክፍያ ታሪክ ማህደር (Payment History)"])
        
        with tab1:
            try:
                conn = get_db_connection()
                pending_list = pd.read_sql("""
                    SELECT fa.id as assign_id, s.id as student_id, s.full_name, f.id as fee_id, f.fee_name, f.amount 
                    FROM public.fee_assignments fa
                    JOIN public.students s ON fa.student_id = s.id
                    JOIN public.fee_types f ON fa.fee_id = f.id
                    WHERE fa.status = 'Pending';
                """, conn)
                conn.close()
                
                if not pending_list.empty:
                    pay_options = {f"{row['full_name']} - {row['fee_name']} (${row['amount']})": row for _, row in pending_list.iterrows()}
                    selected_pay = st.selectbox("ለመክፈል የተማሪውን ስም እና የክፍያውን ዓይነት ይምረጡ", list(pay_options.keys()))
                    method = st.selectbox("የክፍያ መፈጸሚያ መንገድ (Payment Method)", ["Credit/Debit Card", "Bank Transfer", "Mobile Money"])
                    
                    if st.button("🚀 ክፍያውን በPayten ፈጽም"):
                        row_data = pay_options[selected_pay]
                        payten_reference = f"PAY-{datetime.now().year}-{random.randint(10000, 99999)}"
                        current_date = datetime.now().date()
                        
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        cursor.execute("""
                            INSERT INTO public.payments (payten_ref, student_id, fee_id, amount, payment_method, payment_date, status)
                            VALUES (%s, %s, %s, %s, %s, %s, 'Success');
                        """, (payten_reference, int(row_data['student_id']), int(row_data['fee_id']), float(row_data['amount']), method, current_date))
                        
                        cursor.execute("UPDATE public.fee_assignments SET status = 'Paid' WHERE id = %s;", (int(row_data['assign_id']),))
                        
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        st.balloons()
                        st.success(f"🎉 ክፍያው በPayten Gateway በኩል ተፈጽሟል! የትራንዛክሽን መለያ ቁጥር፦ {payten_reference}")
                        st.rerun()
                else:
                    st.info("በአሁኑ ሰዓት መከፈል ያለበት ምንም የPending ክፍያ መዝገብ የለም።")
            except Exception as e:
                st.error(f"የክፍያ ሂደቱን ለመጫን አልተቻለም፦ {e}")
                
        with tab2:
            st.subheader("📜 የተሳኩ የPayten ክፍያዎች ዝርዝር")
            try:
                conn = get_db_connection()
                history_df = pd.read_sql("""
                    SELECT p.payten_ref as "የPayten መለያ", s.full_name as "የተማሪ ስም", f.fee_name as "የክፍያ ዓይነት", 
                           p.amount as "የተከፈለ መጠን ($)", p.payment_method as "የአከፋፈል ዘዴ", p.payment_date as "የተከፈለበት ቀን", p.status as "ሁኔታ"
                    FROM public.payments p
                    JOIN public.students s ON p.student_id = s.id
                    JOIN public.fee_types f ON p.fee_id = f.id ORDER BY p.id DESC;
                """, conn)
                conn.close()
                
                if not history_df.empty:
                    st.dataframe(history_df, use_container_width=True, hide_index=True)
                    csv = history_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📥 የክፍያ ታሪክ ሪፖርት አውርድ (Export CSV)", data=csv, file_name="payten_payment_history.csv", mime="text/csv")
                else:
                    st.info("እስካሁን የተፈጸመ ምንም የክፍያ ታሪክ የለም።")
            except Exception as e:
                st.error(f"ታሪኩን ለማንበብ አልተቻለም፦ {e}")

    # ==========================================
    # 5. የተማሪዎች አጠቃላይ መረጃ መዝገብ (የታችኛው ክፍል)
    # ==========================================
    st.write("---")
    st.subheader("📋 የተማሪዎች አጠቃላይ መረጃ መዝገብ (Live PostgreSQL Ledger)")

    try:
        conn = get_db_connection()
        query = '''
            SELECT id AS "መለያ ቁጥር", full_name AS "የተማሪ ስም", email AS "ኢሜይል", grade AS "ክፍል",
                   parent_name AS "የወላጅ ስም", parent_phone AS "የወላጅ ስልክ", status AS "ሁኔታ"
            FROM public.students ORDER BY id DESC
        '''
        df_students = pd.read_sql(query, conn)
        conn.close()
    except Exception as e:
        df_students = pd.DataFrame()

    if df_students.empty:
        st.info("📉 በአሁን ሰዓት በዳታቤዙ ላይ ምንም የተመዘገበ ተማሪ የለም።")
    else:
        st.dataframe(df_students, use_container_width=True, hide_index=True)


