import pandas as pd
import streamlit as st
import datetime
import os

st.set_page_config(page_title="Task Management System", page_icon="📅", layout="wide")

st.markdown("""
    <div style='background-color: #1B365D; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='text-align: center; color: white; margin: 0; font-family: sans-serif;'>📅 Meski Daily Task Management System</h1>
    </div>
""", unsafe_allow_html=True)

# 🔗 External URL for application references
LOCAL_APP_BASE_URL = "http://localhost:8080/ticket-console?id="

# 💾 CSV Data Storage Files
DEPT_FILE = "departments_storage.csv"
OWNER_FILE = "owners_storage.csv"
CREDENTIALS_FILE = "owners_credentials.csv"
ADMINS_CREDENTIALS_FILE = "admins_credentials.csv"
DELETED_LOG_FILE = "deleted_tasks_log.csv"
REASSIGN_LOG_FILE = "reassignment_history_log.csv"

def load_stored_data():
    if os.path.exists(DEPT_FILE):
        depts = pd.read_csv(DEPT_FILE)['Department'].dropna().tolist()
    else:
        depts = ["Operations", "Marketing", "Sales", "Finance", "HR", "IT Support", "Customer Success"]
        pd.DataFrame({'Department': depts}).to_csv(DEPT_FILE, index=False)
        
    if os.path.exists(OWNER_FILE):
        owners = pd.read_csv(OWNER_FILE)['Assigned To'].dropna().tolist()
    else:
        owners = ["Evan Wright", "George Clark", "Bob Jones", "Abebe Kebede", "Aster Lemma", "Abebe Wondwosen", "Kalkidan Abiyu"]
        pd.DataFrame({'Assigned To': owners}).to_csv(OWNER_FILE, index=False)
        
    if os.path.exists(CREDENTIALS_FILE):
        creds_df = pd.read_csv(CREDENTIALS_FILE)
        creds = dict(zip(creds_df['Username'], creds_df['Password']))
    else:
        creds = {owner: "staff123" for owner in owners}
        pd.DataFrame({'Username': list(creds.keys()), 'Password': list(creds.values())}).to_csv(CREDENTIALS_FILE, index=False)
        
    # 👥 Multi-Admin Setup Logic
    if os.path.exists(ADMINS_CREDENTIALS_FILE):
        admin_creds_df = pd.read_csv(ADMINS_CREDENTIALS_FILE)
        admin_creds = dict(zip(admin_creds_df['AdminName'], admin_creds_df['Password']))
    else:
        admin_creds = {"Admin_1": "admin123", "Admin_2": "admin123", "Admin_3": "admin123"}
        pd.DataFrame({'AdminName': list(admin_creds.keys()), 'Password': list(admin_creds.values())}).to_csv(ADMINS_CREDENTIALS_FILE, index=False)
        
    return sorted(list(set(depts))), sorted(list(set(owners))), creds, admin_creds

stored_depts, stored_owners, stored_creds, stored_admin_creds = load_stored_data()

if 'departments_list' not in st.session_state:
    st.session_state.departments_list = stored_depts

if 'owners_list' not in st.session_state:
    st.session_state.owners_list = stored_owners

if 'user_credentials' not in st.session_state:
    st.session_state.user_credentials = stored_creds

if 'admin_credentials' not in st.session_state:
    st.session_state.admin_credentials = stored_admin_creds

# 🌟 Core Schema Definitions
COLUMNS_NAME = [
    "Task ID", "Task Description", "Department", "Assigned To", "Priority", 
    "Status", "Estimated Hours", "Assign Date", "Started Date", "Completed Date", 
    "Reference ID", "Verification Status", "EOD Report"
]

if 'department_tasks_master' not in st.session_state:
    st.session_state.department_tasks_master = []

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_role = None
    st.session_state.current_user_identity = None

# ---- 🚪 Sidebar System Access ----
st.sidebar.markdown("<h2 style='color: #1B365D;'>🔐 System Access</h2>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    user_role = st.sidebar.selectbox("Select Your Role:", ["User Staff", "Administrator (Admin)"])
    if user_role == "Administrator (Admin)":
        chosen_admin = st.sidebar.text_input("Enter Admin Username:", value="Admin_1")
        admin_password = st.sidebar.text_input("Enter Admin Password:", type="password")
        if st.sidebar.button("🔓 Login as Admin", use_container_width=True):
            correct_admin_pass = st.session_state.admin_credentials.get(chosen_admin.strip())
            if correct_admin_pass and admin_password == correct_admin_pass:
                st.session_state.logged_in = True
                st.session_state.current_role = "Admin"
                st.session_state.current_user_identity = chosen_admin.strip()
                st.rerun()
            else:
                st.sidebar.error("❌ Incorrect Admin Username or Password!")
    else:
        chosen_user = st.sidebar.text_input("Enter Staff Username:")
        user_password = st.sidebar.text_input("Enter Staff Password:", type="password")
        
        if st.sidebar.button("🔓 Login as User", use_container_width=True):
            if not chosen_user.strip():
                st.sidebar.error("❌ Username cannot be empty!")
            else:
                correct_password = st.session_state.user_credentials.get(chosen_user.strip())
                if correct_password and user_password == correct_password:
                    st.session_state.logged_in = True
                    st.session_state.current_role = "User"
                    st.session_state.current_user_identity = chosen_user.strip()
                    st.rerun()
                else:
                    st.sidebar.error("❌ Incorrect Username or Password!")

else:
    is_admin = st.session_state.current_role == "Admin"
    current_identity = st.session_state.current_user_identity
    
    st.sidebar.markdown("---")
    if is_admin:
        st.sidebar.success(f"👑 Admin Session: **{current_identity}**")
        
        with st.sidebar.expander("🏢 Excel Data & Manual Admin Management"):
            st.markdown("**📂 Upload Department & Staff Excel**")
            uploaded_file = st.file_uploader("Choose Excel File (.xlsx, .xls):", type=["xlsx", "xls"])
            
            if uploaded_file is not None:
                try:
                    df_excel = pd.read_excel(uploaded_file, engine='openpyxl')
                    has_dept = 'Department' in df_excel.columns
                    has_owner = 'Assigned To' in df_excel.columns
                    
                    if has_dept or has_owner:
                        if st.button("🔄 Sync Excel Data with System", use_container_width=True):
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
                                
                                for staff in final_owners:
                                    if staff not in st.session_state.user_credentials:
                                        st.session_state.user_credentials[staff] = "staff123"
                                pd.DataFrame({'Username': list(st.session_state.user_credentials.keys()), 'Password': list(st.session_state.user_credentials.values())}).to_csv(CREDENTIALS_FILE, index=False)
                                
                            st.success("✅ Data synced and saved permanently!")
                            st.rerun()
                    else:
                        st.error("❌ Error: Excel sheet must contain 'Department' or 'Assigned To' columns!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            
            st.markdown("---")
            st.markdown("**➕ Add Record Manually**")
            new_dept = st.text_input("Add New Department:")
            if st.button("Save Department", use_container_width=True):
                if new_dept.strip() != "" and new_dept.strip() not in st.session_state.departments_list:
                    st.session_state.departments_list.append(new_dept.strip())
                    st.session_state.departments_list = sorted(st.session_state.departments_list)
                    pd.DataFrame({'Department': st.session_state.departments_list}).to_csv(DEPT_FILE, index=False)
                    st.success("🏢 Department added successfully!")
                    st.rerun()
                    
            new_owner = st.text_input("Add New Staff Member:")
            if st.button("Save Staff Member", use_container_width=True):
                if new_owner.strip() != "" and new_owner.strip() not in st.session_state.owners_list:
                    st.session_state.owners_list.append(new_owner.strip())
                    st.session_state.owners_list = sorted(st.session_state.owners_list)
                    pd.DataFrame({'Assigned To': st.session_state.owners_list}).to_csv(OWNER_FILE, index=False)
                    
                    st.session_state.user_credentials[new_owner.strip()] = "staff123"
                    pd.DataFrame({'Username': list(st.session_state.user_credentials.keys()), 'Password': list(st.session_state.user_credentials.values())}).to_csv(CREDENTIALS_FILE, index=False)
                    st.success("🧑‍💼 Staff member added!")
                    st.rerun()

            # 👥 Add New Admin Configuration
            st.markdown("---")
            st.markdown("**👑 Add New Admin User**")
            new_admin_name = st.text_input("New Admin Username:")
            if st.button("Save Admin User", use_container_width=True):
                if new_admin_name.strip() != "" and new_admin_name.strip() not in st.session_state.admin_credentials:
                    st.session_state.admin_credentials[new_admin_name.strip()] = "admin123"
                    pd.DataFrame({'AdminName': list(st.session_state.admin_credentials.keys()), 'Password': list(st.session_state.admin_credentials.values())}).to_csv(ADMINS_CREDENTIALS_FILE, index=False)
                    st.success(f"👑 Admin user '{new_admin_name.strip()}' created successfully!")
                    st.rerun()
        
        with st.sidebar.expander("🛠️ Security Settings"):
            new_pass = st.text_input("Update My Admin Password:", type="password")
            if st.button("Save Password"):
                if new_pass.strip() != "":
                    st.session_state.admin_credentials[current_identity] = new_pass.strip()
                    pd.DataFrame({'AdminName': list(st.session_state.admin_credentials.keys()), 'Password': list(st.session_state.admin_credentials.values())}).to_csv(ADMINS_CREDENTIALS_FILE, index=False)
                    st.success("🔒 Password updated successfully!")
    else:
        st.sidebar.info(f"🧑‍💼 Active Staff User: **{current_identity}**")
        with st.sidebar.expander("🔐 Change My Password"):
            old_staff_pass = st.text_input("Current Password:", type="password")
            new_staff_pass = st.text_input("New Password:", type="password")
            if st.button("Update Password", use_container_width=True):
                if st.session_state.user_credentials[current_identity] == old_staff_pass:
                    if new_staff_pass.strip() != "":
                        st.session_state.user_credentials[current_identity] = new_staff_pass.strip()
                        pd.DataFrame({'Username': list(st.session_state.user_credentials.keys()), 'Password': list(st.session_state.user_credentials.values())}).to_csv(CREDENTIALS_FILE, index=False)
                        st.success("✅ Password updated successfully!")
                    else:
                        st.error("New password cannot be blank!")
                else:
                    st.error("Incorrect current password!")
        
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Log Out", type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_role = None
        st.session_state.current_user_identity = None
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📋 Daily Task Master", "📅 Historical Logs & Audits", "📊 Dashboard Metrics"])

    # ==========================================
    # 📋 TAB 1: DAILY TASK MASTER
    # ==========================================
    with tab1:
        st.markdown(f"<h2 style='color: #1B365D;'>📋 Daily Task Control Hub <span style='font-size:16px; color:gray;'>[Session: {current_identity}]</span></h2>", unsafe_allow_html=True)
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔄 Status Updates & Action Controls", "📊 Live Task Preview Grid", "📥 Export Daily Report"])
        
        with sub_tab1:
            if is_admin:
                col_u1, col_u2 = st.columns(2)
            else:
                col_u1 = st.container()
            
            with col_u1:
                st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>🔄 Manage My Assigned Tasks & Reports</h3>", unsafe_allow_html=True)
                
                if is_admin:
                    my_tasks = [t for t in st.session_state.department_tasks_master]
                else:
                    my_tasks = [t for t in st.session_state.department_tasks_master if t[3] == current_identity]
                
                if my_tasks:
                    task_options = [t[0] for t in my_tasks]
                    selected_user_task = st.selectbox("Select Target Task ID:", task_options, key="user_task_select")
                    target_user_task = next(t for t in st.session_state.department_tasks_master if t[0] == selected_user_task)
                    
                    st.info(f"📌 **Description:** {target_user_task[1]} | **Owner:** `{target_user_task[3]}` | **Status:** `{target_user_task[5]}`")
                    
                    new_status_selection = st.selectbox("Choose Status Status:", ["Not Started", "In Progress", "Completed"], 
                                                         index=["Not Started", "In Progress", "Completed"].index(target_user_task[5]), key="status_select_user")
                    
                    current_eod_val = target_user_task[12] if target_user_task[12] != "No report yet." and target_user_task[12] != "Directly added as Completed" else ""
                    user_report_text = st.text_area("📝 End of Day (EOD) Summary Report (Editable):", value=current_eod_val, placeholder="Provide or modify your brief summary here...")
                    
                    if st.button("💾 Save Changes & Update Task", use_container_width=True, type="primary"):
                        if new_status_selection == "Completed" and not user_report_text.strip():
                            st.error("❌ Error: You must complete the End of Day summary report before marking a task as Completed!")
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
                                    
                                    task[12] = user_report_text.strip() if user_report_text.strip() else "No report yet."
                                        
                            st.success(f"🎯 Task {selected_user_task} updated successfully!")
                            st.rerun()
                else:
                    st.info("🎉 There are no tasks assigned right now for your profile queue.")
            
            # 👑 ADMIN REGISTER NEW TASK
            if is_admin:
                with col_u2:
                    st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>➕ Register & Assign New Task</h3>", unsafe_allow_html=True)
                    existing_ids = [task[0] for task in st.session_state.department_tasks_master]
                    counter = 1
                    while True:
                        check_id = f"TSK-{counter:03d}"
                        if check_id not in existing_ids:
                            next_id = check_id
                            break
                        counter += 1
                        
                    st.text_input("🔒 Task ID (Auto-Generated):", value=next_id, disabled=True, key="main_task_id")
                    t_desc = st.text_input("Task Description * :")
                    t_dept = st.selectbox("Department Context Location:", st.session_state.departments_list)
                    t_owner = st.selectbox("Assigned To Staff Member:", st.session_state.owners_list)
                    t_priority = st.selectbox("Priority Level Category:", ["Low", "Medium", "High", "Critical"])
                    t_status = st.selectbox("Initial Status state:", ["Not Started", "In Progress", "Completed"])
                    t_hours = st.number_input("Estimated Hours:", min_value=0.5, max_value=24.0, value=2.0)
                    
                    today = datetime.date.today()
                    t_assign_date = st.date_input("Assign Date Target (Today or Future Only) * :", value=today, min_value=today)
                    t_ref_id = st.text_input("External Reference Link ID (Optional):")
                    
                    if st.button("➕ Register & Route Task", use_container_width=True):
                        if not t_desc.strip():
                            st.error("❌ Error: The 'Task Description' field cannot be left blank!")
                        else:
                            today_str = str(t_assign_date)
                            start_log = today_str if t_status == "In Progress" else "-"
                            comp_log = today_str if t_status == "Completed" else "-"
                            default_rep = "No report yet." if t_status != "Completed" else "Directly added as Completed"
                            
                            st.session_state.department_tasks_master.append([
                                next_id, t_desc, t_dept, t_owner, t_priority, t_status, t_hours, 
                                today_str, start_log, comp_log, t_ref_id.strip(), "Pending ⏳", default_rep
                            ])
                            st.success(f"🎯 Task record {next_id} registered and allocated to {t_owner}!")
                            st.rerun()

            # 🛠️ 1. NEW COMPREHENSIVE EDIT PANEL FOR ADMIN
            if is_admin and st.session_state.department_tasks_master:
                st.write("---")
                st.markdown("<h3 style='color: #1B365D;'>📝 Admin Comprehensive Task Modification Panel</h3>", unsafe_allow_html=True)
                
                edit_task_id = st.selectbox("Select Any Existing Task ID to Edit/Modify:", [t[0] for t in st.session_state.department_tasks_master], key="admin_edit_select")
                target_edit_task = next(t for t in st.session_state.department_tasks_master if t[0] == edit_task_id)
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    updated_desc = st.text_input("Modify Task Description:", value=target_edit_task[1])
                    updated_dept = st.selectbox("Modify Department Context:", st.session_state.departments_list, index=st.session_state.departments_list.index(target_edit_task[2]) if target_edit_task[2] in st.session_state.departments_list else 0)
                    updated_owner = st.selectbox("Modify Assigned Staff Member:", st.session_state.owners_list, index=st.session_state.owners_list.index(target_edit_task[3]) if target_edit_task[3] in st.session_state.owners_list else 0)
                    updated_priority = st.selectbox("Modify Priority Category:", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(target_edit_task[4]))
                
                with col_e2:
                    updated_status = st.selectbox("Modify Task Status State:", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(target_edit_task[5]))
                    updated_hours = st.number_input("Modify Estimated Hours:", min_value=0.5, max_value=24.0, value=float(target_edit_task[6]))
                    
                    # Convert string date back to datetime object safely
                    try:
                        curr_date_obj = datetime.datetime.strptime(target_edit_task[7], "%Y-%m-%d").date()
                    except:
                        curr_date_obj = datetime.date.today()
                        
                    updated_assign_date = st.date_input("Modify Target Assignment Date:", value=curr_date_obj)
                    updated_ref_id = st.text_input("Modify External Reference ID:", value=target_edit_task[10])
                
                if st.button("💾 Apply & Save Master Modifications", use_container_width=True):
                    if not updated_desc.strip():
                        st.error("❌ Task description cannot be left blank!")
                    else:
                        old_owner_check = target_edit_task[3]
                        action_date_str = str(datetime.date.today())
                        
                        # 🔄 Audit log if owner changes during editing
                        if old_owner_check != updated_owner:
                            log_entry = pd.DataFrame([{
                                "Task ID": edit_task_id,
                                "Task Description": updated_desc,
                                "Previous Owner": old_owner_check,
                                "New Owner": updated_owner,
                                "Reassigned By Admin": current_identity,
                                "Reassignment Date": action_date_str
                            }])
                            if not os.path.exists(REASSIGN_LOG_FILE):
                                log_entry.to_csv(REASSIGN_LOG_FILE, index=False)
                            else:
                                log_entry.to_csv(REASSIGN_LOG_FILE, mode='a', header=False, index=False)
                        
                        # Save changes back to session state list
                        for t in st.session_state.department_tasks_master:
                            if t[0] == edit_task_id:
                                t[1] = updated_desc.strip()
                                t[2] = updated_dept
                                t[3] = updated_owner
                                t[4] = updated_priority
                                t[5] = updated_status
                                t[6] = updated_hours
                                t[7] = str(updated_assign_date)
                                t[10] = updated_ref_id.strip()
                                
                        st.success(f"✅ Task {edit_task_id} details have been successfully modified by {current_identity}!")
                        st.rerun()

            # ADMIN LOGICAL VERIFICATION PANEL & DELETION AUDITING
            if is_admin:
                st.write("---")
                col_adm1, col_adm2 = st.columns(2)
                
                with col_adm1:
                    st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>👑 Admin Verification Panel</h3>", unsafe_allow_html=True)
                    pending_tasks = [task for task in st.session_state.department_tasks_master if task[11] == "Pending ⏳"]
                    
                    if pending_tasks:
                        pending_ids = [t[0] for t in pending_tasks]
                        verify_target = st.selectbox("Select Task to Verify:", pending_ids, key="verify_box")
                        target_verify_task = next(t for t in pending_tasks if t[0] == verify_target)
                        
                        st.warning(f"🧑‍💼 **Submitted EOD Report by ({target_verify_task[3]}):** {target_verify_task[12]}")
                        if st.button("✔️ Approve Task & EOD Log", use_container_width=True, type="primary"):
                            for task in st.session_state.department_tasks_master:
                                if task[0] == verify_target:
                                    task[11] = "Verified ✔️"
                            st.success(f"🎉 Task record {verify_target} approved!")
                            st.rerun()
                    else:
                        st.info("👍 Clean sheet! No reports awaiting validation.")
                
                with col_adm2:
                    st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>🗑️ Danger Zone (With Audited Logs)</h3>", unsafe_allow_html=True)
                    all_ids = [task[0] for task in st.session_state.department_tasks_master]
                    if all_ids:
                        delete_target = st.selectbox("Select Task to Delete:", all_ids, key="admin_del")
                        if st.button("❌ Terminate Task Record", use_container_width=True):
                            target_del_task = next(t for t in st.session_state.department_tasks_master if t[0] == delete_target)
                            
                            del_entry = pd.DataFrame([{
                                "Task ID": target_del_task[0],
                                "Task Description": target_del_task[1],
                                "Assigned To": target_del_task[3],
                                "Deleted By User": current_identity,
                                "Deletion Timestamp": str(datetime.datetime.now())
                            }])
                            if not os.path.exists(DELETED_LOG_FILE):
                                del_entry.to_csv(DELETED_LOG_FILE, index=False)
                            else:
                                del_entry.to_csv(DELETED_LOG_FILE, mode='a', header=False, index=False)
                                
                            st.session_state.department_tasks_master = [t for t in st.session_state.department_tasks_master if t[0] != delete_target]
                            st.warning(f"🗑️ Task entry {delete_target} deleted and archived to security logs!")
                            st.rerun()

        with sub_tab2:
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>📊 Live Consolidated Task Master Grid</h3>", unsafe_allow_html=True)
            if st.session_state.department_tasks_master:
                st.session_state.department_tasks_master.sort(key=lambda x: x[0])
                df_tasks = pd.DataFrame(st.session_state.department_tasks_master, columns=COLUMNS_NAME)
                
                if is_admin:
                    df_display_final = df_tasks.copy()
                else:
                    df_display_final = df_tasks[df_tasks["Assigned To"] == current_identity].copy()
                
                def make_clickable(ref_id):
                    if ref_id and str(ref_id).strip() != "":
                        return f'<a href="{LOCAL_APP_BASE_URL}{ref_id}" target="_blank" style="color: #1B365D; font-weight: bold;">🔗 View {ref_id}</a>'
                    return "-"
                
                df_display_final["Reference ID"] = df_display_final["Reference ID"].apply(make_clickable)
                if not is_admin:
                    df_display_final = df_display_final.drop(columns=["Verification Status"])
                    
                st.write(df_display_final.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.info("📊 No tasks registered yet.")

        with sub_tab3:
            st.markdown("<h3 style='color: #1B365D; border-bottom: 2px solid #1B365D;'>💾 Report Export Storage Engine</h3>", unsafe_allow_html=True)
            if st.session_state.department_tasks_master:
                df_tasks_dl = pd.DataFrame(st.session_state.department_tasks_master, columns=COLUMNS_NAME)
                if not is_admin:
                    df_tasks_dl = df_tasks_dl[df_tasks_dl["Assigned To"] == current_identity]
                html_data = f"<h3>Daily Task Schedule Master Logs</h3>{df_tasks_dl.to_html(index=False)}"
                st.download_button(label="📥 Download Approved Excel Report File", data=html_data.encode('utf-8'), file_name="Department_Daily_Task_Schedule_System.xls", mime="application/vnd.ms-excel", use_container_width=True, key="dl_main")

    # ==========================================
    # 📅 TAB 2: HISTORICAL LOGS & AUDITS
    # ==========================================
    with tab2:
        st.markdown("<h2 style='color: #1B365D;'>📅 Historical Activity Filter & Security Logs</h2>", unsafe_allow_html=True)
        
        st.write("### 📅 Filter Active Records Grid View Mode")
        col_start, col_end = st.columns(2)
        with col_start:
            filter_start = st.date_input("Start Date Filter:", value=datetime.date.today() - datetime.timedelta(days=30)) 
        with col_end:
            filter_end = st.date_input("End Date Filter:", value=datetime.date.today())
            
        if st.session_state.department_tasks_master:
            df_all = pd.DataFrame(st.session_state.department_tasks_master, columns=COLUMNS_NAME)
            df_all["Assign Date DT"] = pd.to_datetime(df_all["Assign Date"])
            start_dt = pd.to_datetime(filter_start)
            end_dt = pd.to_datetime(filter_end)
            
            df_filtered = df_all[(df_all["Assign Date DT"] >= start_dt) & (df_all["Assign Date DT"] <= end_dt)]
            if not is_admin:
                df_filtered = df_filtered[df_filtered["Assigned To"] == current_identity]
                
            columns_to_show = ["Task ID", "Task Description", "Department", "Assigned To", "Assign Date", "Started Date", "Completed Date", "Status", "EOD Report"]
            df_weekly_view = df_filtered[columns_to_show]
        else:
            df_weekly_view = pd.DataFrame(columns=["Task ID", "Task Description", "Department", "Assigned To", "Assign Date", "Started Date", "Completed Date", "Status", "EOD Report"])
            
        st.write(f"📊 Query Results: Found **{len(df_weekly_view)}** records matching range:")
        st.dataframe(df_weekly_view, use_container_width=True)
        
        if is_admin:
            st.write("---")
            st.markdown("<h3 style='color: #CC0000;'>🛡️ Security Audit Logs Panel (Admin Only)</h3>", unsafe_allow_html=True)
            aud_t1, aud_t2 = st.tabs(["🗑️ Permanently Deleted Tasks History Records", "🔄 Reassignment & Redirection Audit Logs"])
            
            with aud_t1:
                if os.path.exists(DELETED_LOG_FILE):
                    df_del_log = pd.read_csv(DELETED_LOG_FILE)
                    st.dataframe(df_del_log, use_container_width=True)
                else:
                    st.info("No deleted tasks archived in history yet.")
                    
            with aud_t2:
                if os.path.exists(REASSIGN_LOG_FILE):
                    df_re_log = pd.read_csv(REASSIGN_LOG_FILE)
                    st.dataframe(df_re_log, use_container_width=True)
                else:
                    st.info("No task reassignment shifts executed yet.")

    # ==========================================
    # 📊 TAB 3: DASHBOARD METRICS
    # ==========================================
    with tab3:
        st.markdown("<h2 style='color: #1B365D;'>📊 Live Dashboard Operational Metrics</h2>", unsafe_allow_html=True)
        
        if is_admin:
            user_tasks_metrics = st.session_state.department_tasks_master
        else:
            user_tasks_metrics = [t for t in st.session_state.department_tasks_master if t[3] == current_identity]
            
        total_tasks = len(user_tasks_metrics)
        completed_tasks = len([t for t in user_tasks_metrics if t[5] == "Completed"])
        pending_verify = len([t for t in user_tasks_metrics if t[11] == "Pending ⏳"])
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="📈 Total Tasks Tracked", value=total_tasks)
        with m_col2:
            st.metric(label="✅ Completed Successfully", value=completed_tasks)
        with m_col3:
            st.metric(label="⏳ Awaiting Verification (Pending)", value=pending_verify)
            
        st.write("---")
        st.subheader("💡 Departmental Overall Task Status Analytics Chart")
        if user_tasks_metrics:
            df_metrics = pd.DataFrame(user_tasks_metrics, columns=COLUMNS_NAME)
            status_counts = df_metrics["Status"].value_counts()
            st.bar_chart(status_counts)
        else:
            st.info("📊 No live chart metrics available yet.")