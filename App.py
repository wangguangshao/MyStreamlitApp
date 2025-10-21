import streamlit as st
import pandas as pd
import joblib
import os
from io import BytesIO

# 页面设置
st.set_page_config(page_title="RF V-in-olivine Oxybarometry", page_icon="🧪", layout="centered")

# 加载模型
model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
best_model = joblib.load(model_path)

# 定义特征
features = [
    'T (℃)', 'M-SiO2','M-TiO2','M-Al2O3', 'M-FeO', 'M-MnO', 'M-MgO',
    'M-CaO', 'M-Na2O','Ol-SiO2', 'Ol-FeO', 'Ol-MnO', 'Ol-MgO', 'DV'
]

# -----------------------------------
# 主标题与详细介绍
# -----------------------------------
st.title("🧪 RF V-in-olivine Oxybarometry")

st.markdown("""
### 🌋 Overview
This web-based tool provides **oxygen fugacity (ΔFMQ)** predictions using **Random Forest (RF) regression** based on **V-in-olivine oxybarometry**.  
It estimates the redox state of magmatic systems through combined chemical compositions of **olivine** and its **coexisting melt**.

**Scientific background:**  
Oxygen fugacity (fO₂) is a key variable controlling redox-sensitive element behavior (e.g., Fe, V, Cr, S) during magmatic differentiation.  
This tool applies a machine-learning calibration to predict ΔFMQ from compositional data, supporting research in mantle melting, magma storage, and volcanic degassing.

**Applicable range:**  
- ΔFMQ: -6.8 → +6.5  
- Temperature: 1025°C → 1530°C  
- Melt MgO: 3.5 → 27.5 wt%  
- Melt SiO₂: 35 → 60 wt%

""")

st.info("💡 *‘M-’ prefix denotes the composition of the equilibrium melt, while ‘Ol-’ prefix denotes the composition of the olivine phase.*")

st.divider()

# -----------------------------------
# 折叠式详细使用指南
# -----------------------------------
with st.expander("📘 Detailed User Guide and Input Specifications"):
    st.markdown("""
### 1. Introduction
This platform predicts **oxygen fugacity (ΔFMQ)** from experimental or natural olivine–melt compositions.  
The model was trained on a diverse dataset covering basaltic to evolved magmatic systems, ensuring robust performance across geological settings:contentReference[oaicite:1]{index=1}.

### 2. Required Environment
- Any modern browser (Chrome / Firefox)
- Stable internet connection
- No installation or login required

### 3. Input File Requirements
- Format: `.xlsx` (Excel)  
- Maximum file size: **200 MB**  
- Use the downloadable **template** to ensure correct column headers.  
- All values must be **numeric** and expressed in **wt%**.  
- Use decimal points (e.g., `49.23` not `49,23`).

### 4. Input Parameter Definitions

| Group | Prefix | Parameter | Description |
|--------|---------|------------|--------------|
| **Temperature** | — | `T (℃)` | Temperature in Celsius |
| **Equilibrium Melt Composition** | `M-` | `SiO2`, `TiO2`, `Al2O3`, `FeO`, `MnO`, `MgO`, `CaO`, `Na2O` | Major element oxides (wt%) in the coexisting melt |
| **Olivine Composition** | `Ol-` | `SiO2`, `FeO`, `MnO`, `MgO` | Major element oxides (wt%) in the olivine phase |
| **Partition Coefficient** | — | `DV` | Vanadium partition coefficient between olivine and melt |

### 5. Typical Workflow
1. 📥 **Download the template**  
2. ✍️ **Fill in your experimental or natural sample data**  
3. 📤 **Upload the `.xlsx` file**  
4. ⚙️ **The model automatically predicts ΔFMQ**  
5. 💾 **Download the result file**

### 6. Output Description
The result file includes:
- All original input columns  
- An additional column: **Predicted ΔFMQ**

### 7. Troubleshooting
| Issue | Solution |
|--------|-----------|
| File upload fails | Ensure `.xlsx` format, ≤200MB, correct headers |
| Missing predictions | Check for missing or non-numeric cells |
| Unexpected values | Verify inputs are in wt% |
| Display problems | Try Chrome or Firefox without blocking extensions |

---
*Reference:*  
RF V-in-olivine Oxybarometry – Web Tool User Guide (2025):contentReference[oaicite:2]{index=2}  
""")

# -----------------------------------
# 侧边栏：下载模板与上传数据
# -----------------------------------
st.sidebar.header("🔧 Workflow Steps")

template_df = pd.DataFrame(columns=features)
template_io = BytesIO()
with pd.ExcelWriter(template_io, engine='xlsxwriter') as writer:
    template_df.to_excel(writer, index=False)
template_io.seek(0)

st.sidebar.download_button(
    label="⬇️ Download Excel Template",
    data=template_io,
    file_name="prediction_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader("📂 Upload Your Excel File", type=["xlsx"])

# -----------------------------------
# 主内容：模型预测部分
# -----------------------------------
if uploaded_file is not None:
    try:
        with st.spinner("🔍 Processing your data..."):
            input_data = pd.read_excel(uploaded_file)
            missing_cols = [col for col in features if col not in input_data.columns]
            if missing_cols:
                st.error(f"⚠️ Missing columns: {', '.join(missing_cols)}")
            else:
                new_X = input_data[features]
                input_data["Predicted ΔFMQ"] = best_model.predict(new_X)

                st.success("✅ Prediction complete! Here are the results:")
                st.dataframe(input_data.head(10))

                # 生成可下载文件
                output_io = BytesIO()
                with pd.ExcelWriter(output_io, engine='xlsxwriter') as writer:
                    input_data.to_excel(writer, index=False)
                output_io.seek(0)

                st.download_button(
                    label="💾 Download Predicted Results",
                    data=output_io,
                    file_name="predicted_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"❌ File processing failed: {e}")
else:
    st.info("👈 Please upload your Excel file in the sidebar to begin.")

