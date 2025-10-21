import streamlit as st
import pandas as pd
import joblib
import os
from io import BytesIO

# 页面配置
st.set_page_config(page_title="RF V-in-olivine Oxybarometry", page_icon="🧪", layout="centered")

# 自定义样式（仅视觉增强）
st.markdown("""
<style>
/* 全局字体和背景 */
body {
    background-color: #f5f7fa;
    font-family: 'Helvetica', sans-serif;
}

/* 区块容器样式 */
.block {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* 信息提示区 */
.stAlert {
    background-color: #f0f8ff !important;
}

/* 分隔线颜色 */
hr {
    border: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# 加载模型
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
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.title("🧪 RF V-in-olivine Oxybarometry")

    st.markdown("""
### 🌋 Overview
This web-based platform predicts **oxygen fugacity (ΔFMQ)** using a **Random Forest (RF)** model calibrated on global olivine–melt datasets. It implements the **V-in-olivine oxybarometer**, which relates the partitioning of vanadium between olivine and melt to redox state.

**Scientific Background**  
Oxygen fugacity (fO₂) is a key factor controlling the speciation and behavior of redox-sensitive elements (Fe, V, Cr, S) in magmatic systems. This RF-based oxybarometer provides a robust, non-linear model for estimating ΔFMQ from chemical compositions, suitable for both **lunar** and **terrestrial** basaltic systems.

**Applicable range:**  
- ΔFMQ: −6.8 → +6.5  
- Temperature: 1025°C → 1530°C  
- Melt MgO: 3.5 → 27.5 wt%  
- Melt SiO₂: 35 → 60 wt%

**Model Reference:**  
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025). A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts. Earth and Planetary Science Letters, 671, 119692. [https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
""")

    st.info("💡 ‘M-’ prefix denotes the composition of the **equilibrium melt**, while ‘Ol-’ prefix denotes the composition of the **olivine phase**.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='block'>", unsafe_allow_html=True)
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

### 6. Output
- All input columns  
- New column: **Predicted ΔFMQ**

### 7. Troubleshooting
| Issue | Solution |
|--------|-----------|
| Upload fails | Check file format (`.xlsx`) and headers |
| Missing predictions | Ensure all fields are numeric |
| Unrealistic values | Confirm units are wt%, not ppm |
| Browser problems | Use Chrome / Firefox without blockers |

---
**Reference:**  
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025). A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts. Earth and Planetary Science Letters, 671, 119692. [https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
""")
    st.markdown("</div>", unsafe_allow_html=True)

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
    st.markdown("<div class='block'>", unsafe_allow_html=True)
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
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025). A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts. Earth and Planetary Science Letters, 671, 119692. [https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
""")

    st.info("💡 ‘M-’ 前缀表示**平衡熔体成分**，‘Ol-’ 前缀表示**橄榄石成分**。")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='block'>", unsafe_allow_html=True)
    with st.expander("📘 使用说明与输入参数定义"):
        st.markdown("""（此处保持原内容不变）""")
    st.markdown("</div>", unsafe_allow_html=True)

    sidebar_title = "🔧 操作步骤"
    download_label = "⬇️ 下载预测模板"
    upload_label = "📂 上传 Excel 文件"
    result_label = "💾 下载预测结果"
    process_text = "🔍 正在处理数据..."
    complete_text = "✅ 预测完成！以下为结果预览："
    missing_text = "⚠️ 缺少列："
    error_text = "❌ 文件处理失败："
    info_text = "👈 请在侧边栏上传 Excel 文件开始预测。"
