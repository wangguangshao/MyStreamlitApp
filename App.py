import streamlit as st 
import pandas as pd
import joblib
import os
from io import BytesIO

# 页面配置
st.set_page_config(page_title="A CatBoost-based model for scandium (Sc) partitioning between clinopyroxene and its equilibrium melt.", page_icon="🧪", layout="centered")

# 加载模型
model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
best_model = joblib.load(model_path)

# 特征定义
features = [
    'Melt-Si', 'Melt-Ti', 'Melt-Al', 'Melt-Fe', 'Melt-Mn', 'Melt-Mg', 'Melt-Ca', 'Melt-Na',
    'Melt-K', 'Melt-P', 'Cpx-Si', 'Cpx-Ti', 'Cpx-Fe', 'Cpx-Mn', 'Cpx-Mg',
    'Cpx-Ca', 'Cpx-Na', 'Cpx-K', 'Cpx-Cr', 'Cpx-IVAl', 'Cpx-VIAl', 'P (GPa)', 'T (K)'
]

# -----------------------------
# 语言选择
# -----------------------------
lang = st.sidebar.selectbox("🌐 Language / 语言", ["English", "中文"])

# -----------------------------
# 英文界面内容
# -----------------------------
if lang == "English":
    st.title("🧪 A CatBoost-based model for scandium (Sc) partitioning between clinopyroxene and its equilibrium melt.")

    st.markdown("""
### 🌋 Overview
This web-based platform predicts the **scandium partition coefficient (DSc)** between **clinopyroxene (cpx)** and its **equilibrium melt** using a **CatBoost** regression model trained on clinopyroxene–melt datasets.

**Scientific Background**  
Mineral–melt partitioning captures how trace elements (e.g., Sc) distribute between crystalline phases and coexisting liquids, governed by **temperature (T)**, **pressure (P)**, **melt composition/structure**, and **crystal-chemical parameters** (e.g., IVAl, VIAl) in clinopyroxene. Data-driven models offer flexible, non-linear mappings from composition and P–T to **DSc**.

**What this tool does**  
- Input: melt and clinopyroxene compositions (as given by the template), with **P (GPa)** and **T (K)**.  
- Output: **Predicted DSc** (clinopyroxene–melt scandium partition coefficient).
""")

    st.info("💡 Prefix **Melt-** denotes the composition of the equilibrium melt; prefix **Cpx-** denotes the composition of clinopyroxene.")

    st.divider()

    with st.expander("📘 Detailed User Guide and Input Specifications"):
        st.markdown("""
### 1. Purpose
Predict the **clinopyroxene–melt scandium partition coefficient (DSc)** from melt/cpx chemistry and **P–T** using a **CatBoost** model.

### 2. System Requirements
- Modern browser (Chrome / Firefox)  
- Stable internet connection  
- No installation or login required

### 3. Input File Requirements
- Format: .xlsx (Excel), ≤200 MB  
- Use the downloadable **template** to ensure correct column headers  
- All values must be **numeric**; units must be consistent with the template headers

### 4. Input Parameter Definitions

| Group | Prefix | Parameters | Description |
|------|--------|------------|-------------|
| **Pressure** | — | P (GPa) | Pressure in gigapascals |
| **Temperature** | — | T (K) | Temperature in Kelvin |
| **Equilibrium Melt Composition** | Melt- | Si, Ti, Al, Fe, Mn, Mg, Ca, Na, K, P | Melt compositional variables (as required by the model) |
| **Clinopyroxene Composition** | Cpx- | Si, Ti, Fe, Mn, Mg, Ca, Na, K, Cr, IVAl, VIAl | Clinopyroxene crystal-chemical parameters |
| **Target** | — | DSc | Sc partition coefficient (cpx/melt) |

### 5. Workflow
1. 📥 Download the template  
2. ✍️ Fill in your data  
3. 📤 Upload the .xlsx file  
4. ⚙️ The model predicts **DSc** automatically  
5. 💾 Download the results

### 6. Output
- All input columns  
- New column: **Predicted DSc**

### 7. Troubleshooting
| Issue | Solution |
|------|----------|
| Upload fails | Check file format (.xlsx) and headers |
| Missing predictions | Ensure all fields are numeric |
| Odd results | Verify units and header names match the template |
| Browser problems | Use Chrome / Firefox without blockers |
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
    st.title("🧪 基于CatBoost的单斜辉石—熔体钪分配系数（DSc）预测模型")

    st.markdown("""
### 🌋 概述
本网页工具使用 **CatBoost** 回归模型，根据**单斜辉石（Cpx）**与**平衡熔体（Melt）**的组成以及 **P–T 条件**，预测二者之间的**钪分配系数（DSc）**。

**科学背景**  
矿物—熔体分配系数反映微量元素（如 Sc）在晶体与熔体间的分配行为，受**温度（T）**、**压力（P）**、**熔体成分/结构**以及**晶体化学参量**（如 IVAl、VIAl）共同控制。数据驱动模型可在复杂的成分与 P–T 空间中，对 **DSc** 进行稳健的非线性预测。

**工具功能**  
- 输入：模板规定的熔体与单斜辉石组成变量，以及 **P (GPa)** 与 **T (K)**；  
- 输出：**Predicted DSc**（单斜辉石—熔体钪分配系数）。
""")

    st.info("💡 **Melt-** 前缀表示平衡熔体组成；**Cpx-** 前缀表示单斜辉石组成（含 IVAl、VIAl 等晶体化学参量）。")

    st.divider()

    with st.expander("📘 使用说明与输入参数定义"):
        st.markdown("""
### 1. 工具简介
基于 **CatBoost** 的数据驱动模型，从熔体/单斜辉石组成与 **P–T** 条件预测**钪分配系数 DSc（cpx/melt）**。

### 2. 系统要求
- 现代浏览器（Chrome / Firefox）  
- 稳定网络连接  
- 无需安装或登录

### 3. 输入文件要求
- 格式：.xlsx（Excel），≤200 MB  
- 请使用提供的**模板**以确保列名一致  
- 所有取值需为**数值型**；单位与模板保持一致

### 4. 输入参数定义

| 参数组 | 前缀 | 参数 | 说明 |
|------|------|------|------|
| **压力** | — | P (GPa) | 压力（GPa） |
| **温度** | — | T (K) | 温度（K） |
| **平衡熔体成分** | Melt- | Si, Ti, Al, Fe, Mn, Mg, Ca, Na, K, P | 熔体组成变量（按模板提供） |
| **单斜辉石成分** | Cpx- | Si, Ti, Fe, Mn, Mg, Ca, Na, K, Cr, IVAl, VIAl | 单斜辉石晶体化学参量 |
| **预测目标** | — | DSc | 钪分配系数（cpx/melt） |

### 5. 使用流程
1. 📥 下载模板  
2. ✍️ 填写样品数据  
3. 📤 上传 .xlsx 文件  
4. ⚙️ 自动计算 **DSc**  
5. 💾 下载结果

### 6. 输出说明
- 原始输入列  
- 新增列：**Predicted DSc**

### 7. 常见问题
| 问题 | 解决方法 |
|------|----------|
| 上传失败 | 检查文件格式与列名是否正确 |
| 无预测结果 | 确认所有字段为数值型 |
| 结果异常 | 核对单位与列名是否与模板一致 |
| 浏览器问题 | 使用 Chrome / Firefox 并关闭脚本拦截 |
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
                # ⬇⬇⬇ 输出列名改为 Predicted DSc（其余逻辑不变）
                input_data["Predicted DSc"] = best_model.predict(new_X)

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
