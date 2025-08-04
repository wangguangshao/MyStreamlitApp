import streamlit as st
import pandas as pd
import joblib
import os
from io import BytesIO

# 加载模型，使用相对路径
model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
best_model = joblib.load(model_path)

# 定义模型需要的特征
features = [
    'T (℃)', 'M-SiO2','M-TiO2','M-Al2O3', 'M-FeO', 'M-MnO', 'M-MgO',
    'M-CaO', 'M-Na2O','Ol-SiO2', 'Ol-FeO', 'Ol-MnO', 'Ol-MgO', 
    'DV'
]

# 标题
st.title("RF V-in-olivine oxybarometry")

# 添加模板下载功能
template_df = pd.DataFrame(columns=features)
template_io = BytesIO()
with pd.ExcelWriter(template_io, engine='xlsxwriter') as writer:
    template_df.to_excel(writer, index=False)
template_io.seek(0)

st.download_button(
    label="Download Prediction Template",
    data=template_io,
    file_name="templates.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# 文件上传
uploaded_file = st.file_uploader("Upload an Excel file with feature columns for predictions", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 读取上传的文件
        input_data = pd.read_excel(uploaded_file)

        # 检查文件是否包含所有必要特征
        missing_cols = [col for col in features if col not in input_data.columns]
        if missing_cols:
            st.error(f"The input file is missing the following columns: {', '.join(missing_cols)}")
        else:
            # 进行预测
            new_X = input_data[features]
            input_data["Predicted Oxygen fugacity"] = best_model.predict(new_X)

            # 显示结果
            st.success("Prediction complete! Here are the predictions:")
            st.dataframe(input_data)

            # 提供下载
            output_path = "predicted_results.xlsx"
            input_data.to_excel(output_path, index=False)
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download the forecast",
                    data=f,
                    file_name="predicted_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"File processing failed: {e}")
