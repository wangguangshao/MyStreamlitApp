import os
import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

# 加载模型，使用相对路径
model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
if not os.path.exists(model_path):
    st.error("Model file not found! Ensure 'best_model.joblib' is in the same directory as this script.")
    st.stop()

try:
    best_model = joblib.load(model_path)
except Exception as e:
    st.error(f"Failed to load the model: {e}")
    st.stop()

# 定义模型需要的特征
features = [
    'T (℃)', 'M-TiO2', 'M-FeO', 'M-MnO', 'M-MgO',
    'M-CaO', 'Ol-SiO2', 'Ol-FeO', 'Ol-MnO', 'Ol-MgO', 'Ol-CaO',
    'DV'
]

# 标题
st.title("Oxygen Fugacity Prediction Model")

# 提供模板文件下载
if st.button("Download template file"):
    template_df = pd.DataFrame(columns=features)
    output = BytesIO()
    template_df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    st.download_button(
        label="Download Template",
        data=output,
        file_name="template.xlsx",
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
            # 填充空值
            if input_data.isnull().values.any():
                st.warning("The input file contains missing values. These will be filled with 0 for prediction.")
                input_data = input_data.fillna(0)

            # 进行预测
            try:
                new_X = input_data[features]
                input_data["Predicted Oxygen Fugacity"] = best_model.predict(new_X)

                # 显示结果
                st.success("Prediction complete! Here are the predictions:")
                st.dataframe(input_data)

                # 提供下载
                output = BytesIO()
                input_data.to_excel(output, index=False, engine="openpyxl")
                output.seek(0)

                st.download_button(
                    label="Download the forecast",
                    data=output,
                    file_name="predicted_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Prediction failed: {e}")
    except Exception as e:
        st.error(f"File processing failed: {e}")
