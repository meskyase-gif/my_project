import streamlit as st
import pandas as pd
import os

# 1. የድረ-ገጹን መሰረታዊ ገጽታ ማስተካከል (Page Configuration)
st.set_page_config(page_title="FreshMart - Supermarket", page_icon="🛒", layout="wide")

# 2. የምርት መረጃዎችን ሴቭ ማድረጊያ ፋይል ማዘጋጀት
DATA_FILE = "supermarket_inventory.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["የምርት ስም", "ምድብ (Category)", "ዋጋ (ETB)", "የክምችት መጠን (Qty)"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df_inventory = load_data()

# 3. የድረ-ገጹ የላይኛው ክፍል (Header & Logo)
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🛒 FreshMart Supermarket</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Your Favorite Groceries, Delivered Fresh</h3>", unsafe_allow_html=True)
st.write("---")

# 4. ገጹን በሁለት ዓምድ መክፈል (Layout Split)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 አዲስ ምርት መመዝገቢያ (Product Registration)")
    
    # የፎርም መጻፊያ ሳጥኖች
    prod_name = st.text_input("የምርት ስም (Product Name):")
    category = st.selectbox("የምርት ምድብ (Category):", ["አትክልትና ፍራፍሬ", "የታሸጉ ምግቦች", "ቅመማ ቅመም", "የቤት ውስጥ ሳሙናዎች", "ሌሎች"])
    price = st.number_input("ዋጋ በብር (Price in ETB):", min_value=0.0, step=0.5)
    quantity = st.number_input("የክምችት መጠን (Quantity):", min_value=0, step=1)
    
    submit_btn = st.button("💾 ምርቱን መዝግብ", use_container_width=True)
    
    if submit_btn:
        if prod_name:
            # አዲስ መረጃ ማዘጋጀት
            new_item = pd.DataFrame([[prod_name, category, price, quantity]], 
                                    columns=["የምርት ስም", "ምድብ (Category)", "ዋጋ (ETB)", "የክምችት መጠን (Qty)"])
            # መረጃውን ቀላቅሎ ሴቭ ማድረግ
            df_inventory = pd.concat([df_inventory, new_item], ignore_index=True)
            save_data(df_inventory)
            st.success(f"🎉 ምርት '{prod_name}' በተሳካ ሁኔታ ተመዝግቧል!")
            st.rerun()
        else:
            st.error("⚠️ እባክዎ መጀመሪያ የምርቱን ስም ያስገቡ!")

with col2:
    st.subheader("📊 በሱቁ ውስጥ ያሉ ምርቶች ዝርዝር (Inventory)")
    
    if df_inventory.empty:
        st.info("📉 እስካሁን ምንም የተመዘገበ ምርት የገበያ ክምችት ውስጥ የለም።")
    else:
        # ሰንጠረዡን ውብ አድርጎ ማሳየት
        st.dataframe(df_inventory, use_container_width=True)
        
        # አጠቃላይ ስታቲስቲክስ
        st.write("---")
        st.markdown(f"**🔹 አጠቃላይ የተመዘገቡ የምርት አይነቶች:** {len(df_inventory)}")