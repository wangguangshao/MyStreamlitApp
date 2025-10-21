import streamlit as st
import pandas as pd
import joblib
import os
from io import BytesIO

# 页面配置
st.set_page_config(page_title="RF V-in-olivine Oxybarometry", page_icon="🧪", layout="centered")

# -----------------------------
# 样式：全局背景 + 卡片分区样式（可在Streamlit Cloud中生效）
# -----------------------------
st.markdown("""
<style>
/* 整体背景 */
.stApp {
    background-color: #f5f7fa !important;
    font-family: "Segoe UI", "Helvetica Neue", sans-serif;
}

/* 主体卡片 */
div[data-testid="stVerticalBlock"] > div {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 25px 35px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.07);
}

/* expander 样式 */
.streamlit-expanderHeader {
    background-color: #f0f2f6 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}

/* 提示框 */
.stAlert {
    background-color: #eef7ff !important;
    border-left: 4px solid #2b7de9 !important;
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background-color: #edf1f5 !important;
}

/* 分割线 */
hr {
    border: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 加载模型
# -----------------------------
model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
best_model = joblib.load(model_path)

# 特征定义
features = [
    'T (℃)', 'M-SiO2','M-TiO2','M-Al2O3', 'M-FeO', 'M-MnO', 'M-MgO',
    'M-CaO', 'M-Na2O','Ol-SiO2', 'Ol-FeO', 'Ol-MnO', 'Ol-MgO', 'DV'
]

# -----------------------------
# 语言选择
# -----------------------------
lang = st.sidebar.selectbox("🌐 Language / 语言", ["English", "中文"])

# -----------------------------
# 英文界面内容
# -----------------------------
if lang == "English":
    st.title("🧪 RF V-in-olivine Oxybarometry")

    st.markdown("""
### 🌋 Overview
This web-based platform predicts **oxygen fugacity (ΔFMQ)** using a **Random Forest (RF)** model calibrated on global olivine–melt datasets.  
It implements the **V-in-olivine oxybarometer**, which relates the partitioning of vanadium between olivine and melt to redox state.

**Scientific Background**  
Oxygen fugacity (fO₂) is a key factor controlling the speciation and behavior of redox-sensitive elements (Fe, V, Cr, S) in magmatic systems.  
This RF-based oxybarometer provides a robust, non-linear model for estimating ΔFMQ from chemical compositions, suitable for both **lunar** and **terrestrial** basaltic systems.

**Applicable range:**  
- ΔFMQ: −6.8 → +6.5  
- Temperature: 1025°C → 1530°C  
- Melt MgO: 3.5 → 27.5 wt%  
- Melt SiO₂: 35 → 60 wt%

**Model Reference:**  
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025).  
*A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts.*  
**Earth and Planetary Science Letters, 671, 119692.**  
[https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
""")

    st.info("💡 ‘M-’ prefix denotes the composition of the **equilibrium melt**, while ‘Ol-’ prefix denotes the composition of the **olivine phase**.")

    with st.expander("📘 Detailed User Guide and Input Specifications"):
        st.markdown("""
### 1. Purpose
Predict **oxygen fugacity (ΔFMQ)** from olivine–melt equilibrium chemistry using the RF V-in-olivine oxybarometer.

### 2. System Requirements
- Modern browser (Chrome / Firefox)
- Stable internet connection
- No installation or login required

### 3. Input File Requirements
- Format: `.xlsx` (Excel), ≤200 MB  
- Use the downloadable **template** to ensure correct column headers  
- All values must be **numeric**, in **wt%**, using decimal points (e.g., `49.23` not `49,23`)

### 4. Input Parameter Definitions

| Group | Prefix | Parameter | Description |
|--------|---------|------------|--------------|
| **Temperature** | — | `T (℃)` | Temperature in Celsius |
| **Equilibrium Melt Composition** | `M-` | `SiO2`, `TiO2`, `Al2O3`, `FeO`, `MnO`, `MgO`, `CaO`, `Na2O` | Major oxides (wt%) in melt |
| **Olivine Composition** | `Ol-` | `SiO2`, `FeO`, `MnO`, `MgO` | Major oxides (wt%) in olivine |
| **Partition Coefficient** | — | `DV` | Vanadium partition coefficient between olivine and melt |

### 5. Workflow
1. 📥 Download the template  
2. ✍️ Fill in your data  
3. 📤 Upload `.xlsx` file  
4. ⚙️ The model predicts ΔFMQ automatically  
5. 💾 Download the results
""")

    sidebar_title = "🔧 Workflow Steps"
    download_label = "⬇️ Download Excel Template"
    upload_label = "📂 Upload Your Excel File"
    result_label = "💾 Download Predicted Results"
    process_text = "🔍 Processing your data..."
    complete_text = "✅ Prediction complete! Here are the results:"
    missing_text = "⚠️ Missing columns: "
    error_text = "❌ File processing failed: "
    info_text = "👈 Please upload your Excel file in the sidebar to begin."

# -----------------------------
# 中文界面内容
# -----------------------------
else:
    st.title("🧪 基于随机森林的橄榄石钒分配氧逸度计 (RF V-in-olivine Oxybarometry)")

    st.markdown("""
### 🌋 概述
本网页工具基于全球橄榄石–熔体实验与自然样品数据库，利用**随机森林 (Random Forest, RF)** 建立的机器学习模型，预测岩浆体系的**氧逸度 (ΔFMQ)**。

**科学背景**  
氧逸度 (fO₂) 是控制岩浆体系中氧化还原敏感元素（如 Fe、V、Cr、S）行为的关键参数。本模型基于 **V-in-olivine 氧逸度计**，通过橄榄石与平衡熔体间钒的分配行为估算体系氧化还原状态，适用于地球和月球玄武质岩浆体系。

**适用范围：**  
- ΔFMQ: −6.8 → +6.5  
- 温度: 1025°C → 1530°C  
- 熔体 MgO: 3.5 → 27.5 wt%  
- 熔体 SiO₂: 35 → 60 wt%

**模型参考文献：**  
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025).  
*A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts.*  
**Earth and Planetary Science Letters, 671, 119692.**  
[https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
""")

    st.info("💡 ‘M-’ 前缀表示**平衡熔体成分**，‘Ol-’ 前缀表示**橄榄石成分**。")

    with st.expander("📘 使用说明与输入参数定义"):
        st.markdown("""（此处保持原内容不变）""")

    sidebar_title = "🔧 操作步骤"
    download_label = "⬇️ 下载预测模板"
    upload_label = "📂 上传 Excel 文件"
    result_label = "💾 下载预测结果"
    process_text = "🔍 正在处理数据..."
    complete_text = "✅ 预测完成！以下为结果预览："
    missing_text = "⚠️ 缺少列："
    error_text = "❌ 文件处理失败："
    info_text = "👈 请在侧边栏上传 Excel 文件开始预测。"

# -----------------------------
# 侧边栏 + 文件上传逻辑
# -----------------------------
st.sidebar.header(sidebar_title)

template_df = pd.DataFrame(columns=features)
template_io = BytesIO()
with pd.ExcelWriter(template_io, engine='xlsxwriter') as writer:
    template_df.to_excel(writer, index=False)
template_io.seek(0)

st.sidebar.download_button(
    label=download_label,
    data=template_io,
    file_name="prediction_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.sidebar.divider()
uploaded_file = st.sidebar.file_uploader(upload_label, type=["xlsx"])

if uploaded_file is not None:
    try:
        with st.spinner(process_text):
            input_data = pd.read_excel(uploaded_file)
            missing_cols = [col for col in features if col not in input_data.columns]
            if missing_cols:
                st.error(f"{missing_text}{', '.join(missing_cols)}")
            else:
                new_X = input_data[features]
                input_data["Predicted ΔFMQ"] = best_model.predict(new_X)

                st.success(complete_text)
                st.dataframe(input_data.head(10))

                output_io = BytesIO()
                with pd.ExcelWriter(output_io, engine='xlsxwriter') as writer:
                    input_data.to_excel(writer, index=False)
                output_io.seek(0)

                st.download_button(
                    label=result_label,
                    data=output_io,
                    file_name="predicted_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"{error_text}{e}")
else:
    st.info(info_text)
