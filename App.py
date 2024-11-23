import streamlit as st
import pandas as pd
import joblib
import os

# 加载模型，使用相对路径
model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
best_model = joblib.load(model_path)

# 定义模型需要的特征
features = [
    'T (℃)', 'M-TiO2', 'M-FeO', 'M-MnO', 'M-MgO',
    'M-CaO', 'Ol-SiO2', 'Ol-FeO', 'Ol-MnO', 'Ol-MgO', 'Ol-CaO',
    'DV'
]

# 标题
st.title("Oxygen Fugacity Prediction Model")

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
