import streamlit as st
import pandas as pd
import joblib
import os
from io import BytesIO

# 页面配置
st.set_page_config(page_title="RF V-in-olivine Oxybarometry", page_icon="🧪", layout="centered")

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
    st.title("🧪 RF V-in-olivine Oxybarometry")

    st.markdown("""
### 🌋 Overview
This web-based platform predicts **oxygen fugacity (ΔFMQ)** using a **Random Forest (RF)** model calibrated on olivine–melt datasets. It implements the **V-in-olivine oxybarometer**, which relates the partitioning of vanadium between olivine and melt to redox state.

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

    st.divider()

    with st.expander("📘 Detailed User Guide and Input Specifications"):
        st.markdown("""
### 1. Purpose
Predict **oxygen fugacity (ΔFMQ)** from olivine–melt equilibrium chemistry using the RF V-in-olivine oxybarometer.

### 2. System Requirements
- Modern browser (Chrome / Firefox)
- Stable internet connection
- No installation or login required

### 3. Input File Requirements
- Format: .xlsx (Excel), ≤200 MB  
- Use the downloadable **template** to ensure correct column headers  
- All values must be **numeric**, in **wt%**, using decimal points (e.g., 49.23 not 49,23)

### 4. Input Parameter Definitions

| Group | Prefix | Parameter | Description |
|--------|---------|------------|--------------|
| **Temperature** | — | T (℃) | Temperature in Celsius |
| **Equilibrium Melt Composition** | M- | SiO2, TiO2, Al2O3, FeO, MnO, MgO, CaO, Na2O | Major oxides (wt%) in melt |
| **Olivine Composition** | Ol- | SiO2, FeO, MnO, MgO | Major oxides (wt%) in olivine |
| **Partition Coefficient** | — | DV | Vanadium partition coefficient between olivine and melt |

### 5. Workflow
1. 📥 Download the template  
2. ✍️ Fill in your data  
3. 📤 Upload .xlsx file  
4. ⚙️ The model predicts ΔFMQ automatically  
5. 💾 Download the results

### 6. Output
- All input columns  
- New column: **Predicted ΔFMQ**

### 7. Troubleshooting
| Issue | Solution |
|--------|-----------|
| Upload fails | Check file format (.xlsx) and headers |
| Missing predictions | Ensure all fields are numeric |
| Unrealistic values | Confirm units are wt%, not ppm |
| Browser problems | Use Chrome / Firefox without blockers |

---
**Reference:**  
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025). A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts. Earth and Planetary Science Letters, 671, 119692. [https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
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
本网页工具基于橄榄石及其平衡熔体实验岩石学数据库，利用**随机森林 (Random Forest, RF)** 建立的机器学习模型，预测岩浆体系的**氧逸度 (ΔFMQ)**。

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

    st.divider()

    with st.expander("📘 使用说明与输入参数定义"):
        st.markdown("""
### 1. 工具简介
本工具通过**橄榄石–熔体平衡组成**预测氧逸度 (ΔFMQ)，基于随机森林 (RF) 算法的 V-in-olivine 氧逸度计。

### 2. 系统要求
- 现代浏览器（推荐 Chrome 或 Firefox）  
- 稳定网络连接  
- 无需安装或注册

### 3. 输入文件要求
- 格式：.xlsx (Excel)，最大 200 MB  
- 请使用提供的模板以确保列名正确  
- 所有数值需为**数字**、以 **wt%** 表示，使用小数点（如 49.23）

### 4. 输入参数定义

| 参数组 | 前缀 | 参数 | 说明 |
|--------|------|------|------|
| **温度** | — | T (℃) | 温度（摄氏度） |
| **平衡熔体成分** | M- | SiO2, TiO2, Al2O3, FeO, MnO, MgO, CaO, Na2O | 熔体主要氧化物组成 (wt%) |
| **橄榄石成分** | Ol- | SiO2, FeO, MnO, MgO | 橄榄石主要氧化物组成 (wt%) |
| **分配系数** | — | DV | 橄榄石–熔体间钒的分配系数 |

### 5. 使用流程
1. 📥 下载 Excel 模板  
2. ✍️ 填写样品数据  
3. 📤 上传 .xlsx 文件  
4. ⚙️ 模型自动计算 ΔFMQ  
5. 💾 下载预测结果

### 6. 输出说明
输出文件包含：
- 原始输入列  
- 新增列：**Predicted ΔFMQ**

### 7. 常见问题
| 问题 | 解决方法 |
|------|----------|
| 无法上传 | 检查文件格式与列名是否正确 |
| 无预测结果 | 确认输入中无空值或非数字项 |
| 预测异常 | 确认输入单位为 wt%，而非 ppm |
| 浏览器异常 | 使用 Chrome / Firefox 并关闭脚本拦截 |

---
**参考文献：**  
Wang, G.-S., Bai, Z.-J., Hu, W.-J., Gao, J.-F., Zhu, W.-G., & Bai, Y.-X. (2025). A machine learning-based V-in-olivine oxybarometer for characterizing oxygen fugacity in lunar and terrestrial basalts. Earth and Planetary Science Letters, 671, 119692. [https://doi.org/10.1016/j.epsl.2025.119692](https://doi.org/10.1016/j.epsl.2025.119692)
""")

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
# 侧边栏：模板下载与文件上传
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

# -----------------------------
# 主内容：预测逻辑
# -----------------------------
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
