import pandas as pd
import streamlit as st
import datetime
import os

st.set_page_config(page_title="Task Management System", page_icon="📅", layout="wide")

st.markdown("""
    <div style='background-color: #1B365D; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='text-align: center; color: white; margin: 0; font-family: sans-serif;'>📅 የዲፓርትመንት ዕለታዊ ስራዎች መቆጣጠሪያ ሲስተም</h1>
    </div>
""", unsafe_allow_html=True)

# 🔗 የሌላኛው መተግበሪያዎ ሎካል URL
LOCAL_APP_BASE_URL = "http://localhost:8080/ticket-console?id="

# 💾 የዳታ ማከማቻ ፋይሎች
DEPT_FILE = "departments_storage.csv"
OWNER_FILE = "owners_storage.csv"

def load_stored_data():
    if os.path.exists(DEPT_FILE):
        depts = pd.read_csv(DEPT_FILE)['Department'].dropna().tolist()
    else:
        depts = ["Operations", "Marketing", "Sales", "Finance", "HR", "IT Support", "Customer Success"]
        pd.DataFrame({'Department': depts}).to_csv(DEPT_FILE, index=False)
        
    if os.path.exists(OWNER_FILE):
        owners = pd.read_csv(OWNER_FILE)['Assigned To'].dropna().tolist()
    else:
        owners = ["Evan Wright", "George Clark", "Bob Jones", "Abebe Kebede", "Aster Lemma"]
        pd.DataFrame({'Assigned To': owners}).to_csv(OWNER_FILE, index=False)
        
    return sorted(list(set(depts))), sorted(list(set(owners)))

stored_depts, stored_owners = load_stored_data()

if 'departments_list' not in st.session_state:
    st.session_state.departments_list = stored_depts

if 'owners_list' not in st.session_state:
    st.session_state.owners_list = stored_owners

# 🌟 13 አምዶች ያሉት ሙሉ የዳታ መዋቅር
if 'department_tasks_master' not in st.session_state:
    st.session_state.department_tasks_master = [
        ["TSK-001", "Review quarterly budget reports", "Finance", "Evan Wright", "High", "In Progress", 4.0, "2026-06-22", "2026-06-22", "-", "REF-9921", "Verified ✔️", "Checked all sheets."],
        ["TSK-002", "Deploy security patch to server", "IT Support", "George Clark", "Critical", "Not Started", 2.0, "2026-06-23", "-", "-", "REF-4812", "Pending ⏳", "No report yet."],
        ["TSK-003", "Social media campaign scheduling", "Marketing", "Bob Jones", "Medium", "Completed", 3.0, "2026-06-23", "2026-06-24", "2026-06-25", "", "Pending ⏳", "All posts are scheduled successfully."]
    ]

if 'admin_password_key' not in st.session_state:
    st.session_state.admin_password_key = "admin123"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_role = None

# ---- 🚪 የግራ ጎን ሳጥን መግቢያ ----
st.sidebar.markdown("<h2 style='color: #1B365D;'>🔐 System Access</h2>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    user_role = st.sidebar.selectbox("የእርስዎን የስራ ድርሻ ይምረጡ:", ["ሰራተኛ (User)", "አስተዳዳሪ (Admin)"])
    if user_role == "አስተዳዳሪ (Admin)":
        admin_password = st.sidebar.text_input("የአስተዳዳሪ ይለፍ ቃል:", type="password")
        if st.sidebar.button("🔓 ግባ (Login as Admin)", use_container_width=True):
            if admin_password == st.session_state.admin_password_key:
                st.session_state.logged_in = True
                st.session_state.current_role = "Admin"
                st.rerun()
            else:
                st.sidebar.error("❌ የተሳሳተ የይለፍ ቃል ነው!")
    else:
        if st.sidebar.button("🔓 ግባ (Login as User)", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.current_role = "User"
            st.rerun()
    st.info("👋 | እባክዎ ለመቀጠል በስተግራ በኩል ያለውን ሳጥን ተጠቅመው ይግቡ።")

else:
    is_admin = st.session_state.current_role == "Admin"
    
    st.sidebar.markdown("---")
    if is_admin:
        st.sidebar.success("👑 አስተዳዳሪ (Admin Account)")
        
        with st.sidebar.expander("🏢 የዳታ ማስተዳደሪያ (Excel Upload)"):
            st.markdown("**📂 የዲፓርትመንት እና ሰራተኞች ኤክሴል ጫን**")
            uploaded_file = st.file_uploader("የኤክሴል ፋይል ይምረጡ (.xlsx ወይም .xls):", type=["xlsx", "xls"])
            
            if uploaded_file is not None:
                try:
                    df_excel = pd.read_excel(uploaded_file, engine='openpyxl')
                    has_dept = 'Department' in df_excel.columns
                    has_owner = 'Assigned To' in df_excel.columns
                    
                    if has_dept or has_owner:
                        if st.button("🔄 የኤክሴል ዳታዎችን በሲስተሙ ላይ ተካ", use_container_width=True):
                            if has_dept:
                                excel_depts = df_excel['Department'].dropna().astype(str).str.strip().tolist()
                                final_depts = sorted(list(set(excel_depts)))
                                st.session_state.departments_list = final_depts
                                pd.DataFrame({'Department': final_depts}).to_csv(DEPT_FILE, index=False)
                            
                            if has_owner:
                                excel_owners = df_excel['Assigned To'].dropna().astype(str).str.strip().tolist()
                                final_owners = sorted(list(set(excel_owners)))
                                st.session_state.owners_list = final_owners
                                pd.DataFrame({'Assigned To': final_owners}).to_csv(OWNER_FILE, index=False)
                                
                            st.success("✅ ዳታው በቋሚነት ተቀምጧል!")
                            st.rerun()
                    else:
                        st.error("❌ ስህተት፡ የኤክሴል ፋይሉ 'Department' ወይም 'Assigned To' አርዕስት ሊኖረው ይገባል!")
                except Exception as e:
                    st.error(f"ፋይሉን በማንበብ ላይ ስህተት ተፈጥሯል: {e}")
            
            st.markdown("---")
            st.markdown("**➕ በእጅ አዲስ ለመጨመር**")
            new_dept = st.text_input("አዲስ ዲፓርትመንት ጨምር:")
            if st.button("ዲፓርትመንት መዝግብ", use_container_width=True):
                if new_dept.strip() != "" and new_dept.strip() not in st.session_state.departments_list:
                    st.session_state.departments_list.append(new_dept.strip())
                    st.session_state.departments_list = sorted(st.session_state.departments_list)
                    pd.DataFrame({'Department': st.session_state.departments_list}).to_csv(DEPT_FILE, index=False)
                    st.success("🏢 ዲፓርትመንት ተጨምሯል!")
                    st.rerun()
                    
            new_owner = st.text_input("አዲስ የስራ ባለቤት (Staff) ጨምር:")
            if st.button("ሰራተኛ መዝግብ", use_container_width=True):
                if new_owner.strip() != "" and new_owner.strip() not in st.session_state.owners_list:
                    st.session_state.owners_list.append(new_owner.strip())
                    st.session_state.owners_list = sorted(st.session_state.owners_list)
                    pd.DataFrame({'Assigned To': st.session_state.owners_list}).to_csv(OWNER_FILE, index=False)
                    st.success("🧑‍💼 ሰራተኛ ተጨምሯል!")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**📥 የዝርዝር ማውጫዎች**")
            df_depts_dl = pd.DataFrame({'Department': st.session_state.departments_list})
            html_depts = f"<h3>Department List</h3>{df_depts_dl.to_html(index=False)}"
            st.download_button(label="🏢 የዲፓርትመንቶችን ዝርዝር አውርድ", data=html_depts.encode('utf-8'), file_name="System_Department_List.xls", mime="application/vnd.ms-excel", use_container_width=True, key="dl_depts")
            
            df_owners_dl = pd.DataFrame({'Assigned To': st.session_state.owners_list})
            html_owners = f"<h3>Assigned To Staff List</h3>{df_owners_dl.to_html(index=False)}"
            st.download_button(label="🧑‍💼 የሰራተኞችን ዝርዝር አውርድ", data=html_owners.encode('utf-8'), file_name="System_Assigned_To_List.xls", mime="application/vnd.ms-excel", use_container_width=True, key="dl_owners")
                    
        with st.sidebar.expander("🛠️ ፓስወርድ መቀየሪያ"):
            new_pass = st.text_input("አዲስ ይለፍ ቃል:", type="password")
            if st.button("አዲስ ፓስወርድ ሴቭ አድርግ"):
                if new_pass.strip() != "":
                    st.session_state.admin_password_key = new_pass
                    st.success("🔒 ፓስወርድ ተቀይሯል!")
                else:
                    st.error("ባዶ መሆን አይችልም!")
    else:
        st.sidebar.info("🧑‍💼 ሰራተኛ (User Account)")
        
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 ውጣ (Log Out)", type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_role = None
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📋 Daily Task Master", "📅 Weekly & Historical Schedule", "📊 Dashboard Metrics"])

    # ==========================================
    # 📋 TAB 1: DAILY TASK MASTER (በንዑስ ታቦች የተከፋፈለ)
    # ==========================================
    with tab1:
        st.markdown("<h2 style='color: #1B365D;'>📋 ዕለታዊ ስራዎች ማስተዳደሪያ (Daily Task Master)</h2>", unsafe_allow_html=True)
        
        # 🟢 እዚህ ጋር ነው ለዩዘሩ እንዲቀልለው በንዑስ ታብ (Sub-tabs) የከፈልነው!
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔄 ማሻሻያ እና አዲስ መመዝገቢያ", "📊 የተመዘገቡ ስራዎች (Live Preview)", "📥 ፋይል ማውጫ"])
        
        # --- ንዑስ ታብ 1: ማሻሻያ እና አዲስ መመዝገቢያ ---
        with sub_tab1:
            col_u1, col_u2 = st.columns(2)
            
            with col_u1:
                st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>🔄 የስራ ሁኔታ ማሻሻያ (Update Task Status)</h3>", unsafe_allow_html=True)
                active_tasks_ids = [t[0] for t in st.session_state.department_tasks_master if t[5] != "Completed"]
                
                if active_tasks_ids:
                    selected_user_task = st.selectbox("የሚሰሩበትን የስራ መታወቂያ (Task ID) ይምረጡ፦", active_tasks_ids, key="user_task_select")
                    target_user_task = next(t for t in st.session_state.department_tasks_master if t[0] == selected_user_task)
                    
                    st.info(f"📌 **ስራ፦** {target_user_task[1]} | **ያሁኑ ሁኔታ፦** `{target_user_task[5]}`")
                    
                    new_status_selection = st.selectbox("አዲስ የስራ ሁኔታ ይምረጡ፦", ["Not Started", "In Progress", "Completed"], 
                                                         index=["Not Started", "In Progress", "Completed"].index(target_user_task[5]), key="status_select_user")
                    
                    user_report_text = ""
                    if new_status_selection == "Completed":
                        user_report_text = st.text_area("📝 የቀኑ ስራ ማጠቃለያ ሪፖርት (End of Day Report) * ፦", placeholder="ዛሬ የሰሩትን ስራ አጭር ማጠቃለያ እዚህ ይጻፉ...")
                    
                    if st.button("💾 ማሻሻያውን መዝግብ", use_container_width=True, type="primary"):
                        if new_status_selection == "Completed" and not user_report_text.strip():
                            st.error("❌ እባክዎ ስራውን ከማጠናቀቅዎ በፊት የቀኑን ስራ ማጠቃለያ ሪፖርት ይጻፉ!")
                        else:
                            today_str = str(datetime.date.today())
                            for task in st.session_state.department_tasks_master:
                                if task[0] == selected_user_task:
                                    task[5] = new_status_selection
                                    
                                    if new_status_selection == "In Progress" and task[8] == "-":
                                        task[8] = today_str  
                                    elif new_status_selection == "Completed":
                                        if task[8] == "-": 
                                            task[8] = today_str 
                                        task[9] = today_str  
                                        task[12] = user_report_text.strip()
                                        
                            st.success(f"🎯 ስራ {selected_user_task} በተሳካ ሁኔታ ተሻሽሏል!")
                            st.rerun()
                else:
                    st.info("🎉 በአሁኑ ሰዓት ያልተጠናቀቀ ክፍት ስራ የለም።")
            
            with col_u2:
                st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>➕ አዲስ ስራ መመዝገቢያ</h3>", unsafe_allow_html=True)
                existing_ids = [task[0] for task in st.session_state.department_tasks_master]
                counter = 1
                while True:
                    check_id = f"TSK-{counter:03d}"
                    if check_id not in existing_ids:
                        next_id = check_id
                        break
                    counter += 1
                    
                st.text_input("🔒 Task ID (ራስ-ሰር የሚሞላ):", value=next_id, disabled=True, key="main_task_id")
                t_desc = st.text_input("የስራው ዝርዝር መግለጫ (Task Description) * :")
                t_dept = st.selectbox("ዲፓርትመንት (Department):", st.session_state.departments_list)
                t_owner = st.selectbox("የስራው ባለቤት (Assigned To):", st.session_state.owners_list)
                t_priority = st.selectbox("ቅድሚያ ደረጃ (Priority):", ["Low", "Medium", "High", "Critical"])
                t_status = st.selectbox("ሁኔታ (Status):", ["Not Started", "In Progress", "Completed"])
                t_hours = st.number_input("የፈጀው ሰአት (Estimated Hours):", min_value=0.5, max_value=24.0, value=2.0)
                
                today = datetime.date.today()
                t_assign_date = st.date_input("ስራው የተሰጠበት ቀን (Assign Date):", value=today)
                t_ref_id = st.text_input("የሌላኛው መተግበሪያ መታወቂያ (External Reference ID):", placeholder="ምሳሌ፦ REF-4812")
                
                if st.button("➕ ስራውን አስመዝግብ", use_container_width=True):
                    if not t_desc.strip():
                        st.error("❌ እባክዎ 'የስራው ዝርዝር መግለጫ' ሳጥንን ይሙሉ!")
                    else:
                        today_str = str(t_assign_date)
                        start_log = today_str if t_status == "In Progress" else "-"
                        comp_log = today_str if t_status == "Completed" else "-"
                        default_rep = "No report yet." if t_status != "Completed" else "Directly added as Completed"
                        
                        st.session_state.department_tasks_master.append([
                            next_id, t_desc, t_dept, t_owner, t_priority, t_status, t_hours, 
                            today_str, start_log, comp_log, t_ref_id.strip(), "Pending ⏳", default_rep
                        ])
                        st.success(f"🎯 ስራ {next_id} በተሳካ ሁኔታ ተመዝግቧል!")
                        st.rerun()

            # የአስተዳዳሪ ማረጋገጫ እና መሰረዣ
            if is_admin or any(task[11] == "Pending ⏳" for task in st.session_state.department_tasks_master):
                st.write("---")
                col_adm1, col_adm2 = st.columns(2)
                
                with col_adm1:
                    if is_admin:
                        st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>👑 የአስተዳዳሪ ማረጋገጫ (Admin Verify)</h3>", unsafe_allow_html=True)
                        pending_tasks = [task for task in st.session_state.department_tasks_master if task[11] == "Pending ⏳"]
                        
                        if pending_tasks:
                            pending_ids = [t[0] for t in pending_tasks]
                            verify_target = st.selectbox("ለማጽደቅ ይምረጡ:", pending_ids, key="verify_box")
                            target_verify_task = next(t for t in pending_tasks if t[0] == verify_target)
                            
                            st.warning(f"🧑‍💼 **የሰራተኛው ሪፖርት ({target_verify_task[3]})፦** {target_verify_task[12]}")
                            if st.button("✔️ የቀኑን ሪፖርት አረጋግጥ", use_container_width=True, type="primary"):
                                for task in st.session_state.department_tasks_master:
                                    if task[0] == verify_target:
                                        task[11] = "Verified ✔️"
                                st.success(f"🎉 {verify_target} በተሳካ ሁኔታ ተረጋግጧል!")
                                st.rerun()
                        else:
                            st.info("👍 አዲስ ማረጋገጫ የሚጠብቅ ስራ የለም።")
                
                with col_adm2:
                    st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>🗑️ ስራ መሰረዣ ሳጥን</h3>", unsafe_allow_html=True)
                    if is_admin:
                        all_ids = [task[0] for task in st.session_state.department_tasks_master]
                        if all_ids:
                            delete_target = st.selectbox("የሚሰረዝ ስራ ይምረጡ (Admin):", all_ids, key="admin_del")
                            if st.button("❌ አስወግድ/ሰርዝ (Admin Delete)", use_container_width=True):
                                st.session_state.department_tasks_master = [t for t in st.session_state.department_tasks_master if t[0] != delete_target]
                                st.warning(f"🗑️ {delete_target} ተሰርዟል!")
                                st.rerun()
                    else:
                        user_deletable = [task[0] for task in st.session_state.department_tasks_master if task[11] == "Pending ⏳"]
                        if user_deletable:
                            delete_target = st.selectbox("የተሳሳተውን ለመሰረዝ ይምረጡ (User Delete):", user_deletable, key="user_del")
                            if st.button("❌ የተሳሳተ መስመር ሰርዝ (User Delete)", use_container_width=True):
                                st.session_state.department_tasks_master = [t for t in st.session_state.department_tasks_master if t[0] != delete_target]
                                st.warning(f"🗑️ {delete_target} ተሰርዟል!")
                                r.rerun()

        # --- ንዑስ ታብ 2: የተመዘገቡ ስራዎች ቅድመ-ዕይታ (Live Preview) ---
        with sub_tab2:
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>📊 የተመዘገቡ ስራዎች ሙሉ ሰንጠረዥ ቅድመ-ዕይታ</h3>", unsafe_allow_html=True)
            st.session_state.department_tasks_master.sort(key=lambda x: x[0])
            columns_name = ["Task ID", "Task Description", "Department", "Assigned To", "Priority", "Status", "Estimated Hours", "Assign Date", "Started Date", "Completed Date", "Reference ID", "Verification Status", "EOD Report"]
            df_tasks = pd.DataFrame(st.session_state.department_tasks_master, columns=columns_name)
            
            df_display = df_tasks.copy()
            def make_clickable(ref_id):
                if ref_id and str(ref_id).strip() != "":
                    return f'<a href="{LOCAL_APP_BASE_URL}{ref_id}" target="_blank" style="color: #1B365D; font-weight: bold;">🔗 {ref_id} እይ</a>'
                return "-"
            df_display["Reference ID"] = df_display["Reference ID"].apply(make_clickable)
            if not is_admin:
                df_display = df_display.drop(columns=["Verification Status"])
                
            st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

        # --- ንዑስ ታብ 3: ፋይል ማውጫ ---
        with sub_tab3:
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>💾 የሪፖርት ፋይል ማውጫ ሳጥን</h3>", unsafe_allow_html=True)
            columns_name = ["Task ID", "Task Description", "Department", "Assigned To", "Priority", "Status", "Estimated Hours", "Assign Date", "Started Date", "Completed Date", "Reference ID", "Verification Status", "EOD Report"]
            df_tasks_dl = pd.DataFrame(st.session_state.department_tasks_master, columns=columns_name)
            html_data = f"<h3>Daily Task Master</h3>{df_tasks_dl.to_html(index=False)}"
            st.download_button(label="📥 የጸደቀውን የኤክሴል ፋይል አውርድ", data=html_data.encode('utf-8'), file_name="Department_Daily_Task_Schedule_System.xls", mime="application/vnd.ms-excel", use_container_width=True, key="dl_main")

    # ==========================================
    # 📅 TAB 2: WEEKLY & HISTORICAL SCHEDULE
    # ==========================================
    with tab2:
        st.markdown("<h2 style='color: #1B365D;'>📅 ሳምንታዊ እና የረጅም ጊዜ ስራዎች ሪፖርት መፈለጊያ</h2>", unsafe_allow_html=True)
        
        df_all = pd.DataFrame(st.session_state.department_tasks_master, columns=columns_name)
        
        st.write("### 📅 የሪፖርት ቀናትን መርጠው ይፈልጉ (የ1 ወር ወይም ከዚያ በላይ ድሮ ዳታ)")
        col_start, col_end = st.columns(2)
        with col_start:
            filter_start = st.date_input("ከቀን (Start Date)፦", value=datetime.date.today() - datetime.timedelta(days=30)) 
        with col_end:
            filter_end = st.date_input("እስከ ቀን (End Date)፦", value=datetime.date.today())
            
        df_all["Assign Date DT"] = pd.to_datetime(df_all["Assign Date"])
        start_dt = pd.to_datetime(filter_start)
        end_dt = pd.to_datetime(filter_end)
        
        df_filtered = df_all[(df_all["Assign Date DT"] >= start_dt) & (df_all["Assign Date DT"] <= end_dt)]
        df_weekly_view = df_filtered[["Task ID", "Task Description", "Department", "Assigned To", "Assign Date", "Started Date", "Completed Date", "Status", "EOD Report"]]
        
        st.write(f"📊 ከ **{filter_start}** እስከ **{filter_end}** ባለው ጊዜ ውስጥ **{len(df_weekly_view)}** ስራዎች ተገኝተዋል፦")
        st.dataframe(df_weekly_view, use_container_width=True)

    # ==========================================
    # 📊 TAB 3: DASHBOARD METRICS
    # ==========================================
    with tab3:
        st.markdown("<h2 style='color: #1B365D;'>📊 የአፈፃፀም መቆጣጠሪያ ዳሽቦርድ (Dashboard Metrics)</h2>", unsafe_allow_html=True)
        total_tasks = len(st.session_state.department_tasks_master)
        completed_tasks = len([t for t in st.session_state.department_tasks_master if t[5] == "Completed"])
        pending_verify = len([t for t in st.session_state.department_tasks_master if t[11] == "Pending ⏳"])
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="📈 ጠቅላላ የተመዘገቡ ስራዎች", value=total_tasks)
        with m_col2:
            st.metric(label="✅ በተሳካ ሁኔታ የተጠናቀቁ", value=completed_tasks)
        with m_col3:
            st.metric(label="⏳ ማረጋገጫ የሚጠብቁ (Pending)", value=pending_verify)
            
        st.write("---")
        st.subheader("💡 የዲፓርትመንት አጠቃላይ የሥራ ሁኔታ ግራፍ")
        df_metrics = pd.DataFrame(st.session_state.department_tasks_master, columns=columns_name)
        status_counts = df_metrics["Status"].value_counts()
        st.bar_chart(status_counts)