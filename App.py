from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="V-partitioning Oxybarometry Portal",
    page_icon="🧪",
    layout="centered",
)

BASE_DIR = Path(__file__).resolve().parent


# -----------------------------------------------------------------------------
# Model registry
# Keep every feature name and feature order identical to model training.
# -----------------------------------------------------------------------------
MODELS: dict[str, dict[str, Any]] = {
    "olivine_oxybarometer": {
        "display_name": "V-in-olivine Oxybarometry",
        "file_name": "best_model_olivine.joblib",
        "target": "fO2 (ΔFMQ)",
        "output_column": "Predicted ΔFMQ",
        "model_type": "oxybarometer",
        "features": [
            "T (℃)", "M-SiO2", "M-TiO2", "M-Al2O3", "M-FeO", "M-MnO",
            "M-MgO", "M-CaO", "M-Na2O", "Ol-SiO2", "Ol-FeO", "Ol-MnO",
            "Ol-MgO", "DV",
        ],
        "description_en": (
            "Predicts oxygen fugacity (ΔFMQ) from olivine–melt equilibrium chemistry "
            "and vanadium partitioning."
        ),
        "description_zh": "利用橄榄石—熔体平衡组成及钒分配系数预测氧逸度（ΔFMQ）。",
    },
    "cpx_melt_partitioning": {
        "display_name": "V-in-clinopyroxene partitioning model",
        "file_name": "best_model_cpx_melt.joblib",
        "target": "LOG(Dv)",
        "output_column": "Predicted LOG(Dv)",
        "model_type": "partitioning",
        "features": [
            "Melt-SiO2", "Melt-TiO2", "Melt-Al2O3", "Melt-FeO", "Melt-MnO",
            "Melt-MgO", "Melt-CaO", "Melt-Na2O", "Melt-K2O", "Melt-P2O5",
            "Cpx-SiO2", "Cpx-TiO2", "Cpx-Al2O3", "Cpx-FeO", "Cpx-MnO",
            "Cpx-MgO", "Cpx-CaO", "Cpx-Na2O", "Cpx-K2O", "T (C)",
            "fO2 (ΔFMQ)",
        ],
        "description_en": (
            "Predicts log10 vanadium partitioning between clinopyroxene and melt "
            "from temperature, oxygen fugacity, and phase compositions."
        ),
        "description_zh": "根据温度、氧逸度及相组成预测单斜辉石—熔体钒分配系数的对数值。",
    },
    "cpx_oxybarometer": {
        "display_name": "V-in-clinopyroxene Oxybarometry",
        "file_name": "best_model_cpx_oxybarometer.joblib",
        "target": "fO2 (ΔFMQ)",
        "output_column": "Predicted fO2 (ΔFMQ)",
        "model_type": "oxybarometer",
        "features": [
            "Melt-SiO2", "Melt-TiO2", "Melt-Al2O3", "Melt-FeO", "Melt-MnO",
            "Melt-MgO", "Melt-CaO", "Melt-Na2O", "Melt-K2O", "Melt-P2O5",
            "Cpx-SiO2", "Cpx-TiO2", "Cpx-Al2O3", "Cpx-FeO", "Cpx-MnO",
            "Cpx-MgO", "Cpx-CaO", "Cpx-Na2O", "Cpx-K2O", "T (C)", "Dv",
        ],
        "description_en": (
            "Predicts oxygen fugacity from clinopyroxene–melt chemistry, temperature, "
            "and the measured vanadium partition coefficient."
        ),
        "description_zh": "根据单斜辉石—熔体组成、温度及钒分配系数预测氧逸度。",
    },
    "mt_melt_partitioning": {
        "display_name": "V-in-magnetite partitioning model",
        "file_name": "best_model_mt_melt.joblib",
        "target": "LOG(Dv)",
        "output_column": "Predicted LOG(Dv)",
        "model_type": "partitioning",
        "features": [
            "T(C)", "ΔFMQ", "Melt-SiO2", "Melt-TiO2", "Melt-Al2O3",
            "Melt-FeO", "Melt-MnO", "Melt-MgO", "Melt-CaO", "Melt-Na2O",
            "Melt-K2O", "Mt-SiO2", "Mt-TiO2", "Mt-Al2O3", "Mt-FeO",
            "Mt-MnO", "Mt-MgO",
        ],
        "description_en": (
            "Predicts log10 vanadium partitioning between magnetite and melt from "
            "temperature, oxygen fugacity, and phase compositions."
        ),
        "description_zh": "根据温度、氧逸度及相组成预测磁铁矿—熔体钒分配系数的对数值。",
    },
    "mt_oxybarometer": {
        "display_name": "V-in-magnetite Oxybarometry",
        "file_name": "best_model_mt_oxybarometer.joblib",
        "target": "ΔFMQ",
        "output_column": "Predicted ΔFMQ",
        "model_type": "oxybarometer",
        "features": [
            "T(C)", "Dv", "Melt-SiO2", "Melt-TiO2", "Melt-Al2O3", "Melt-FeO",
            "Melt-MnO", "Melt-MgO", "Melt-CaO", "Melt-Na2O", "Melt-K2O",
            "Mt-SiO2", "Mt-TiO2", "Mt-Al2O3", "Mt-FeO", "Mt-MnO", "Mt-MgO",
            "Mt-Cr2O3",
        ],
        "description_en": (
            "Predicts oxygen fugacity from magnetite–melt chemistry, temperature, "
            "and the measured vanadium partition coefficient."
        ),
        "description_zh": "根据磁铁矿—熔体组成、温度及钒分配系数预测氧逸度。",
    },
    "mt_cpx_oxybarometer": {
        "display_name": "V-in-magnetite-clinopyroxene Oxybarometry",
        "file_name": "best_model_mt_cpx_oxybarometer.joblib",
        "target": "fO2 (ΔFMQ)",
        "output_column": "Predicted fO2 (ΔFMQ)",
        "model_type": "oxybarometer",
        "features": [
            "Mt-SiO2", "Mt-Al₂O₃", "Mt-FeO", "Mt-MnO", "Mt-MgO", "Mt-CaO",
            "Mt-Na2O", "Mt-K2O", "Cpx-SiO2", "Cpx-TiO2", "Cpx-Al2O3",
            "Cpx-MnO", "Cpx-MgO", "Cpx-CaO", "Cpx-Na2O", "Cpx-K2O",
            "T (C)", "Dv",
        ],
        "description_en": (
            "Melt-independent oxygen-fugacity model based on coexisting magnetite–"
            "clinopyroxene compositions, temperature, and inter-mineral V partitioning."
        ),
        "description_zh": "基于共生磁铁矿—单斜辉石组成、温度及矿物间钒分配的无熔体氧逸度计。",
    },
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def resolve_model_path(file_name: str) -> Path:
    """Allow model files either beside app.py or inside ./models/."""
    candidates = [BASE_DIR / file_name, BASE_DIR / "models" / file_name]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


@st.cache_resource(show_spinner=False)
def load_model(file_name: str):
    model_path = resolve_model_path(file_name)
    if not model_path.is_file():
        raise FileNotFoundError(
            f"Model file not found: {file_name}. Place it beside app.py or in the models folder."
        )
    return joblib.load(model_path)


def build_excel_template(features: list[str]) -> bytes:
    template_df = pd.DataFrame(columns=features)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        template_df.to_excel(writer, index=False, sheet_name="Input")
    output.seek(0)
    return output.getvalue()


def dataframe_to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Predictions")
    output.seek(0)
    return output.getvalue()


def validate_model_feature_names(model: Any, expected_features: list[str]) -> list[str]:
    """Return warnings when a fitted sklearn model exposes a different feature schema."""
    warnings: list[str] = []
    trained_features = getattr(model, "feature_names_in_", None)
    if trained_features is not None:
        trained = [str(item) for item in trained_features]
        if trained != expected_features:
            missing_from_registry = [x for x in trained if x not in expected_features]
            extra_in_registry = [x for x in expected_features if x not in trained]
            if set(trained) == set(expected_features):
                warnings.append(
                    "The model contains the same feature names but in a different order. "
                    "The website will use the training order stored in the model."
                )
            else:
                warnings.append(
                    "The website feature list differs from model.feature_names_in_. "
                    f"Only in trained model: {missing_from_registry or 'None'}; "
                    f"only in website registry: {extra_in_registry or 'None'}."
                )
    return warnings


def prediction_features(model: Any, registry_features: list[str]) -> list[str]:
    trained_features = getattr(model, "feature_names_in_", None)
    if trained_features is None:
        return registry_features
    trained = [str(item) for item in trained_features]
    if set(trained) == set(registry_features):
        return trained
    return registry_features


def validate_input(df: pd.DataFrame, required_features: list[str]) -> tuple[list[str], list[str], list[str]]:
    missing = [col for col in required_features if col not in df.columns]
    non_numeric: list[str] = []
    contains_nulls: list[str] = []

    for col in required_features:
        if col not in df.columns:
            continue
        converted = pd.to_numeric(df[col], errors="coerce")
        original_non_null = df[col].notna()
        invalid = original_non_null & converted.isna()
        if invalid.any():
            non_numeric.append(col)
        if converted.isna().any():
            contains_nulls.append(col)

    return missing, non_numeric, contains_nulls


# -----------------------------------------------------------------------------
# Language and model selection
# -----------------------------------------------------------------------------
lang = st.sidebar.selectbox("🌐 Language / 语言", ["English", "中文"])

model_labels = {key: cfg["display_name"] for key, cfg in MODELS.items()}
model_key = st.sidebar.selectbox(
    "🧪 Model" if lang == "English" else "🧪 选择模型",
    options=list(MODELS.keys()),
    format_func=lambda key: model_labels[key],
)
config = MODELS[model_key]
features: list[str] = config["features"]


# -----------------------------------------------------------------------------
# Main page content
# -----------------------------------------------------------------------------
if lang == "English":
    st.title("🧪 V-partitioning Oxybarometry Portal")
    st.subheader(config["display_name"])
    st.markdown(config["description_en"])
    st.info(
        f"**Target:** {config['target']}  |  **Required inputs:** {len(features)} columns"
    )

    with st.expander("📘 User guide and exact input columns"):
        st.markdown(
            """
            1. Select a model in the sidebar.  
            2. Download that model's Excel template.  
            3. Fill one sample per row without changing column names.  
            4. Upload the `.xlsx` file.  
            5. Download the prediction results.

            All compositional inputs must use the same units and definitions as the training data.
            Feature names are case-sensitive and symbol-sensitive.
            """
        )
        st.code("\n".join(features), language="text")

    sidebar_title = "🔧 Workflow"
    download_label = "⬇️ Download model-specific template"
    upload_label = "📂 Upload Excel input"
    result_label = "💾 Download prediction results"
    process_text = "🔍 Validating data and running the selected model..."
    complete_text = "✅ Prediction complete."
    initial_text = "👈 Select a model and upload its completed Excel template."
else:
    st.title("🧪 钒分配模型与氧逸度计平台")
    st.subheader(config["display_name"])
    st.markdown(config["description_zh"])
    st.info(f"**输出参数：** {config['target']}　|　**必需输入列：** {len(features)} 项")

    with st.expander("📘 使用说明与精确输入列名"):
        st.markdown(
            """
            1. 在侧边栏选择模型；  
            2. 下载该模型对应的Excel模板；  
            3. 每行填写一个样品，不要修改列名；  
            4. 上传 `.xlsx` 文件；  
            5. 下载预测结果。

            所有成分数据的单位和定义必须与模型训练数据一致。列名对大小写、空格及特殊符号敏感。
            """
        )
        st.code("\n".join(features), language="text")

    sidebar_title = "🔧 操作步骤"
    download_label = "⬇️ 下载当前模型模板"
    upload_label = "📂 上传Excel输入文件"
    result_label = "💾 下载预测结果"
    process_text = "🔍 正在校验数据并调用所选模型……"
    complete_text = "✅ 预测完成。"
    initial_text = "👈 请选择模型并上传填写完成的Excel模板。"


# -----------------------------------------------------------------------------
# Sidebar input/output
# -----------------------------------------------------------------------------
st.sidebar.header(sidebar_title)
st.sidebar.caption(
    ("Model file: " if lang == "English" else "模型文件：") + config["file_name"]
)

template_bytes = build_excel_template(features)
st.sidebar.download_button(
    label=download_label,
    data=template_bytes,
    file_name=f"{model_key}_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True,
)

st.sidebar.divider()
uploaded_file = st.sidebar.file_uploader(upload_label, type=["xlsx"], key=model_key)


# -----------------------------------------------------------------------------
# Prediction workflow
# -----------------------------------------------------------------------------
if uploaded_file is None:
    st.info(initial_text)
else:
    try:
        with st.spinner(process_text):
            input_data = pd.read_excel(uploaded_file)
            missing_cols, non_numeric_cols, null_cols = validate_input(input_data, features)

            if missing_cols:
                message = (
                    "Missing required columns: " if lang == "English" else "缺少必需列："
                )
                st.error(message + ", ".join(missing_cols))
                st.stop()

            if non_numeric_cols:
                message = (
                    "Non-numeric values were found in: "
                    if lang == "English"
                    else "以下列包含非数字内容："
                )
                st.error(message + ", ".join(non_numeric_cols))
                st.stop()

            if null_cols:
                message = (
                    "Blank or invalid values were found in: "
                    if lang == "English"
                    else "以下列包含空值或无效值："
                )
                st.error(message + ", ".join(null_cols))
                st.stop()

            if input_data.empty:
                st.error("The uploaded file contains no data rows." if lang == "English" else "上传文件没有数据行。")
                st.stop()

            model = load_model(config["file_name"])
            schema_warnings = validate_model_feature_names(model, features)
            for warning in schema_warnings:
                st.warning(warning)

            ordered_features = prediction_features(model, features)
            new_x = input_data[ordered_features].apply(pd.to_numeric, errors="raise")
            predictions = np.asarray(model.predict(new_x)).reshape(-1)

            if len(predictions) != len(input_data):
                raise ValueError(
                    "The model returned a different number of predictions than input rows."
                )

            result_data = input_data.copy()
            result_data[config["output_column"]] = predictions

        st.success(complete_text)
        metric_label = config["target"]
        if len(predictions) == 1:
            st.metric(metric_label, f"{float(predictions[0]):.4f}")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Samples" if lang == "English" else "样品数", len(predictions))
            c2.metric("Mean" if lang == "English" else "平均值", f"{np.mean(predictions):.4f}")
            c3.metric("Std." if lang == "English" else "标准差", f"{np.std(predictions):.4f}")

        st.dataframe(result_data.head(20), use_container_width=True)

        output_bytes = dataframe_to_excel(result_data)
        st.download_button(
            label=result_label,
            data=output_bytes,
            file_name=f"{model_key}_predicted_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    except FileNotFoundError as exc:
        st.error(str(exc))
        st.code(
            f"Expected location:\n{BASE_DIR / config['file_name']}\nor\n{BASE_DIR / 'models' / config['file_name']}",
            language="text",
        )
    except Exception as exc:
        prefix = "File processing or prediction failed: " if lang == "English" else "文件处理或预测失败："
        st.error(prefix + str(exc))
