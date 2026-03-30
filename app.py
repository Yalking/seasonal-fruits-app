import json
import streamlit as st

st.set_page_config(
    page_title="应季果蔬小助手",
    page_icon="🥬",
    layout="centered"
)

# 读取数据
with open("seasonal_produce.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("🥬 应季果蔬小助手")
st.caption("按月份查看当季水果和蔬菜")

months = list(data.keys())
selected_month = st.selectbox("请选择月份", months)

month_data = data[selected_month]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍓 当季水果")
    for item in month_data["fruits"]:
        st.markdown(
            f"""
**{item["name"]}**  
- 简介：{item["desc"]}
- 营养价值：{item["nutrition"]}
- 挑选建议：{item["tips"]}
"""
        )

with col2:
    st.subheader("🥦 当季蔬菜")
    for item in month_data["vegetables"]:
        st.markdown(
            f"""
**{item["name"]}**  
- 简介：{item["desc"]}
- 营养价值：{item["nutrition"]}
- 挑选建议：{item["tips"]}
"""
        )

st.divider()
st.info("这是第一版原型，后续可以继续加：搜索、城市筛选、收藏、图片、每日推荐。")