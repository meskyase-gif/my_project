import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="Task Management System", page_icon="📅", layout="wide")

st.markdown("""
    <div style='background-color: #1B365D; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='text-align: center; color: white; margin: 0; font-family: sans-serif;'>📅 የዲፓርትመንት ዕለታዊ ስራዎች መቆጣጠሪያ ሲስተም</h1>
    </div>
""", unsafe_allow_html=True)

# 🔗 የሌላኛው መተግበሪያዎ ሎካል URL
LOCAL_APP_BASE_URL = "http://localhost:8080/ticket-console?id="

# 1. የዲፓርትመንት ዝርዝር በሴሽን
if 'departments_list' not in st.session_state:
    st.session_state.departments_list = ["Operations", "Marketing", "Sales", "Finance", "HR", "IT Support", "Customer Success"]

# 2. ዋና ዳታዎችን ማዘጋጀት
if 'tasks_list' not in st.session_state:
    st.session_state.tasks_list = [
        ["TSK-001", "Review quarterly budget reports", "Finance", "Evan Wright", "High", "In Progress", 4.0, "2026-06-22", "2026-06-24", "REF-9921", "Verified ✔️"],
        ["TSK-002", "Deploy security patch to server", "IT Support", "George Clark", "Critical", "Not Started", 2.0, "2026-06-23", "2026-06-23", "REF-4812", "Pending ⏳"],
        ["TSK-003", "Social media campaign scheduling", "Marketing", "Bob Jones", "Medium", "Completed", 3.0, "2026-06-23", "2026-06-26", "", "Pending ⏳"]
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
    st.info("👋 እባክዎ ለመቀጠል በስተግራ በኩል ያለውን ሳጥን ተጠቅመው ይግቡ።")

else:
    is_admin = st.session_state.current_role == "Admin"
    
    st.sidebar.markdown("---")
    if is_admin:
        st.sidebar.success("👑 አስተዳዳሪ (Admin Account)")
        
        with st.sidebar.expander("🏢 የዲፓርትመንቶች ማስተዳደሪያ"):
            st.markdown("**➕ አዲስ ዲፓርትመንት ጨምር**")
            new_dept = st.text_input("የዲፓርትመንት ስም:", key="add_dept_input")
            if st.button("ዲፓርትመንቱን መዝግብ", use_container_width=True):
                if new_dept.strip() == "":
                    st.error("ስም ባዶ መሆን አይችልም!")
                elif new_dept.strip() in st.session_state.departments_list:
                    st.warning("ይህ ዲፓርትመንት አስቀድሞ አለ!")
                else:
                    st.session_state.departments_list.append(new_dept.strip())
                    st.success(f"🏢 {new_dept} ተጨምሯል!")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**🗑️ ዲፓርትመንት አስወግድ/ሰርዝ**")
            dept_to_delete = st.selectbox("የሚሰረዝ ዲፓርትመንት:", st.session_state.departments_list, key="del_dept_select")
            if st.button("ይህንን ዲፓርትመንት ሰርዝ", type="primary", use_container_width=True):
                if len(st.session_state.departments_list) > 1:
                    st.session_state.departments_list.remove(dept_to_delete)
                    st.warning(f"🗑️ {dept_to_delete} ተሰርዟል!")
                    st.rerun()
                else:
                    st.error("ቢያንስ አንድ ዲፓርትመንት መኖር አለበት!")
                    
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

    tab1, tab2, tab3 = st.tabs(["📋 Daily Task Master", "📅 Weekly Schedule", "📊 Dashboard Metrics"])

    # ==========================================
    # 📋 TAB 1: DAILY TASK MASTER
    # ==========================================
    with tab1:
        col1, col2 = st.columns([1, 1.3])

        with col1:
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>📝 1. አዲስ ስራ መመዝገቢያ (Add Task)</h3>", unsafe_allow_html=True)
            
            existing_ids = [task[0] for task in st.session_state.tasks_list]
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
            t_owner = st.text_input("የስራው ባለቤት (Assigned To) * :")
            t_priority = st.selectbox("ቅድሚያ ደረጃ (Priority):", ["Low", "Medium", "High", "Critical"])
            t_status = st.selectbox("ሁኔታ (Status):", ["Not Started", "In Progress", "Completed"])
            t_hours = st.number_input("የፈጀው ሰአት (Estimated Hours):", min_value=0.5, max_value=24.0, value=2.0)
            
            today = datetime.date.today()
            t_assign_date = st.date_input("ስራው የተሰጠበት ቀን (Assign Date):", value=today)
            t_end_date = st.date_input("ማጠናቀቂያ ቀን (End Date):", value=today)
            
            t_ref_id = st.text_input("የሌላኛው መተግበሪያ መታወቂያ (External Reference ID - Optional):", placeholder="ምሳሌ፦ REF-4812")
            
            if st.button("➕ ስራውን መዝግብ (Add Task)", use_container_width=True):
                if not t_desc.strip() or not t_owner.strip():
                    st.error("❌ እባክዎ 'የስራው ዝርዝር መግለጫ' እና 'የስራው ባለቤት' ሳጥኖችን ይሙሉ!")
                elif t_end_date < t_assign_date:
                    st.error("❌ ማጠናቀቂያ ቀን ስራው ከተሰጠበት ቀን ማነስ አይችልም!")
                else:
                    st.session_state.tasks_list.append([
                        next_id, t_desc, t_dept, t_owner, t_priority, t_status, t_hours, 
                        str(t_assign_date), str(t_end_date), t_ref_id.strip(), "Pending ⏳"
                    ])
                    st.success(f"🎯 ስራ {next_id} በተሳካ ሁኔታ ተመዝግቧል!")
                    st.rerun()

            if is_admin:
                st.write("---")
                st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>✏️ 2. ስራ ማስተካከያ (Admin Amend)</h3>", unsafe_allow_html=True)
                all_ids = [task[0] for task in st.session_state.tasks_list]
                if all_ids:
                    edit_target = st.selectbox("ማስተካከል የሚፈልጉትን Task ID ይምረጡ:", all_ids, key="amend_box")
                    target_task = next(t for t in st.session_state.tasks_list if t[0] == edit_target)
                    
                    edit_desc = st.text_input("መግለጫ አሻሽል:", value=target_task[1], key="edit_desc_key")
                    edit_status = st.selectbox("ሁኔታ አሻሽል:", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(target_task[5]), key="edit_status_key")
                    
                    if st.button("💾 ማሻሻያውን አጽድቅ (Update Task)", use_container_width=True):
                        for task in st.session_state.tasks_list:
                            if task[0] == edit_target:
                                task[1] = edit_desc
                                task[5] = edit_status
                        st.success(f"🔄 {edit_target} በተሳካ ሁኔታ ተሻሽሏል!")
                        st.rerun()
                
                st.write("---")
                st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>👑 3. የአስተዳዳሪ ማረጋገጫ (Admin Verify)</h3>", unsafe_allow_html=True)
                pending_tasks = [task[0] for task in st.session_state.tasks_list if task[10] == "Pending ⏳"]
                if pending_tasks:
                    verify_target = st.selectbox("ለማጽደቅ ይምረጡ:", pending_tasks, key="verify_box")
                    if st.button("✔️ ይህንን ስራ በይፋ አረጋግጥ", use_container_width=True):
                        for task in st.session_state.tasks_list:
                            if task[0] == verify_target:
                                task[10] = "Verified ✔️"
                        st.success(f"🎉 {verify_target} ተረጋግጧል!")
                        st.rerun()
                else:
                    st.info("👍 አዲስ Pending ስራ የለም።")

            st.write("---")
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>🗑️ ስራ መሰረዣ ሳጥን</h3>", unsafe_allow_html=True)
            if is_admin:
                all_ids = [task[0] for task in st.session_state.tasks_list]
                if all_ids:
                    delete_target = st.selectbox("የሚሰረዝ ስራ ይምረጡ (Admin):", all_ids, key="admin_del")
                    if st.button("❌ አስወግድ/ሰርዝ (Admin Delete)", use_container_width=True):
                        st.session_state.tasks_list = [t for t in st.session_state.tasks_list if t[0] != delete_target]
                        st.warning(f"🗑️ {delete_target} ተሰርዟል!")
                        st.rerun()
            else:
                user_deletable = [task[0] for task in st.session_state.tasks_list if task[10] == "Pending ⏳"]
                if user_deletable:
                    delete_target = st.selectbox("የተሳሳተውን ለመሰረዝ ይምረጡ (User Delete):", user_deletable, key="user_del")
                    if st.button("❌ የተሳሳተ መስመር ሰርዝ (User Delete)", use_container_width=True):
                        st.session_state.tasks_list = [t for t in st.session_state.tasks_list if t[0] != delete_target]
                        st.warning(f"🗑️ {delete_target} ተሰርዟል!")
                        st.rerun()
                else:
                    st.info("🔒 በአስተዳዳሪ የጸደቁ ስራዎችን መደበኛ ሰራተኛ መሰረዝ አይችልም!")

            st.write("---")
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>💾 ፋይል ማውጫ</h3>", unsafe_allow_html=True)
            st.session_state.tasks_list.sort(key=lambda x: x[0])
            
            columns_name = ["Task ID", "Task Description", "Department", "Assigned To", "Priority", "Status", "Estimated Hours", "Assign Date", "End Date", "Reference ID", "Verification Status"]
            df_tasks = pd.DataFrame(st.session_state.tasks_list, columns=columns_name)
            
            html_data = f"<h3>Daily Task Master</h3>{df_tasks.to_html(index=False)}"
            st.download_button(
                label="📥 የጸደቀውን የኤክሴል ፋይል አውርድ",
                data=html_data.encode('utf-8'),
                file_name="Department_Daily_Task_Schedule_System.xls",
                mime="application/vnd.ms-excel",
                use_container_width=True,
                key="download_daily"
            )

        with col2:
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>📊 የተመዘገቡ ስራዎች ቅድመ-ዕይታ (Live Preview)</h3>", unsafe_allow_html=True)
            
            df_display = df_tasks.copy()
            def make_clickable(ref_id):
                if ref_id and str(ref_id).strip() != "":
                    return f'<a href="{LOCAL_APP_BASE_URL}{ref_id}" target="_blank" style="color: #1B365D; font-weight: bold;">🔗 {ref_id} እይ</a>'
                return "-"
            
            df_display["Reference ID"] = df_display["Reference ID"].apply(make_clickable)
            
            if not is_admin:
                df_display = df_display.drop(columns=["Verification Status"])
                
            st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

    # ==========================================
    # 📅 TAB 2: WEEKLY SCHEDULE
    # ==========================================
    with tab2:
        st.markdown("<h2 style='color: #1B365D;'>📅 ሳምንታዊ የስራ መርሃ-ግብር (Weekly Schedule)</h2>", unsafe_allow_html=True)
        columns_name = ["Task ID", "Task Description", "Department", "Assigned To", "Priority", "Status", "Estimated Hours", "Assign Date", "End Date", "Reference ID", "Verification Status"]
        df_all = pd.DataFrame(st.session_state.tasks_list, columns=columns_name)
        df_weekly_view = df_all[["Task ID", "Task Description", "Department", "Assigned To", "Assign Date", "End Date", "Reference ID", "Status"]]
        
        # 🛠️ ማስተካከያ፡ እዚህ ጋር የነበረውን index=False ከ st.dataframe() ውስጥ አስወግደነዋል!
        st.dataframe(df_weekly_view, use_container_width=True)

    # ==========================================
    # 📊 TAB 3: DASHBOARD METRICS
    # ==========================================
    with tab3:
        st.markdown("<h2 style='color: #1B365D;'>📊 የአፈፃፀም መቆጣጠሪያ ዳሽቦርድ (Dashboard Metrics)</h2>", unsafe_allow_html=True)
        
        total_tasks = len(st.session_state.tasks_list)
        completed_tasks = len([t for t in st.session_state.tasks_list if t[5] == "Completed"])
        pending_verify = len([t for t in st.session_state.tasks_list if t[10] == "Pending ⏳"])
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="📈 ጠቅላላ የተመዘገቡ ስራዎች", value=total_tasks)
        with m_col2:
            st.metric(label="✅ በተሳካ ሁኔታ የተጠናቀቁ", value=completed_tasks)
        with m_col3:
            st.metric(label="⏳ ማረጋገጫ የሚጠብቁ (Pending)", value=pending_verify)
            
        st.write("---")
        st.subheader("💡 የዲፓርትመንት አጠቃላይ የሥራ ሁኔታ ግራፍ")
        df_metrics = pd.DataFrame(st.session_state.tasks_list, columns=columns_name)
        status_counts = df_metrics["Status"].value_counts()
        st.bar_chart(status_counts)