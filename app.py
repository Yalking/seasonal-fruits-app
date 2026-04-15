import json
import random
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="应季果蔬",
    page_icon="🥬",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "seasonal_produce.json"
IMAGES_DIR = BASE_DIR / "images"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

months = list(data.keys())
current_month = f"{datetime.now().month}月"
active_month = current_month if current_month in data else months[0]
default_index = months.index(active_month)

# -------------------------
# session state
# -------------------------
defaults = {
    "page": "首页",
    "keyword": "",
    "selected_month": active_month,
    "selected_category": "全部",
    "selected_tag": "全部",
    "selected_item": None,
    "favorites": [],
    "home_pick_name": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------------
# helpers
# -------------------------
def get_image_path(item_name: str):
    path = IMAGES_DIR / f"{item_name}.png"
    return path if path.exists() else None

def get_month_items(month):
    month_data = data[month]
    fruits = month_data.get("fruits", [])
    vegetables = month_data.get("vegetables", [])
    return fruits + vegetables

def get_all_tags(month):
    tags = set()
    for item in get_month_items(month):
        for tag in item.get("tags", []):
            tags.add(tag)
    priority = ["水果", "蔬菜", "补维C", "膳食纤维", "清爽", "低负担", "家常常见", "适合早餐", "适合凉拌", "适合炖煮", "春季推荐", "夏季推荐", "容易买到", "开胃", "时令感强"]
    ordered = [x for x in priority if x in tags] + sorted([x for x in tags if x not in priority])
    return ["全部"] + ordered

def is_fruit(item, month):
    return any(x["name"] == item["name"] for x in data[month].get("fruits", []))

def filter_items(items, keyword="", category="全部", tag="全部", month=None):
    result = items
    if keyword:
        keyword = keyword.strip().lower()
        result = [item for item in result if keyword in item["name"].lower() or keyword in item.get("desc", "").lower()]
    if category != "全部":
        if category == "水果":
            result = [item for item in result if month and is_fruit(item, month)]
        elif category == "蔬菜":
            result = [item for item in result if month and not is_fruit(item, month)]
    if tag != "全部":
        result = [item for item in result if tag in item.get("tags", [])]
    return result

def get_item_by_name(name):
    if not name:
        return None
    for month in months:
        for item in get_month_items(month):
            if item["name"] == name:
                return item, month
    return None, None

def open_detail(item_name):
    st.session_state.selected_item = item_name
    st.session_state.page = "详情页"

def toggle_favorite(item_name):
    favorites = set(st.session_state.favorites)
    if item_name in favorites:
        favorites.remove(item_name)
    else:
        favorites.add(item_name)
    st.session_state.favorites = list(favorites)

def change_home_pick():
    items = get_month_items(active_month)
    if items:
        current = st.session_state.home_pick_name
        candidates = [x["name"] for x in items if x["name"] != current] or [x["name"] for x in items]
        st.session_state.home_pick_name = random.choice(candidates)

def ensure_home_pick():
    items = get_month_items(active_month)
    names = [x["name"] for x in items]
    if not names:
        st.session_state.home_pick_name = None
        return
    if st.session_state.home_pick_name not in names:
        st.session_state.home_pick_name = random.choice(names)

def pill_html(text):
    return f"""
    <span style="
        display:inline-block;
        padding:4px 10px;
        border-radius:999px;
        background:#F3F8F1;
        color:#4E7A52;
        font-size:12px;
        margin:0 6px 6px 0;
        border:1px solid #E4EFE0;
    ">{text}</span>
    """

def render_card(item, month, compact=False):
    image_path = get_image_path(item["name"])
    with st.container(border=True):
        if image_path:
            st.image(str(image_path), use_container_width=True)
        else:
            st.caption(f"未找到图片：images/{item['name']}.png")

        top_left, top_right = st.columns([4, 1])
        with top_left:
            st.markdown(f"### {item['name']}" if not compact else f"**{item['name']}**")
        with top_right:
            fav = "★" if item["name"] in st.session_state.favorites else "☆"
            if st.button(fav, key=f"fav_{month}_{item['name']}_{'compact' if compact else 'full'}", help="收藏/取消收藏"):
                toggle_favorite(item["name"])
                st.rerun()

        tags = item.get("tags", [])[:3 if compact else 4]
        if tags:
            st.markdown("".join([pill_html(t) for t in tags]), unsafe_allow_html=True)

        st.write(item["desc"])
        if not compact:
            st.caption(f"营养亮点：{item['nutrition']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("查看详情", key=f"detail_{month}_{item['name']}_{'compact' if compact else 'full'}", use_container_width=True):
                open_detail(item["name"])
                st.rerun()
        with col2:
            if st.button("收藏" if item["name"] not in st.session_state.favorites else "已收藏", key=f"save_{month}_{item['name']}_{'compact' if compact else 'full'}", use_container_width=True):
                toggle_favorite(item["name"])
                st.rerun()

def render_detail():
    item_name = st.session_state.selected_item
    item, month = get_item_by_name(item_name)
    if not item:
        st.warning("未找到该果蔬信息。")
        return

    top1, top2 = st.columns([1, 5])
    with top1:
        if st.button("← 返回", use_container_width=True):
            st.session_state.page = "首页"
            st.rerun()
    with top2:
        st.caption(f"{month} · {'水果' if is_fruit(item, month) else '蔬菜'}")

    image_path = get_image_path(item["name"])
    if image_path:
        st.image(str(image_path), use_container_width=True)

    row1, row2 = st.columns([5, 1])
    with row1:
        st.title(item["name"])
    with row2:
        fav = "★ 已收藏" if item["name"] in st.session_state.favorites else "☆ 收藏"
        if st.button(fav, use_container_width=True):
            toggle_favorite(item["name"])
            st.rerun()

    tags = item.get("tags", [])
    if tags:
        st.markdown("".join([pill_html(t) for t in tags]), unsafe_allow_html=True)

    st.markdown("### 为什么现在推荐吃")
    st.write(item["desc"])

    st.markdown("### 营养亮点")
    st.write(item["nutrition"])

    st.markdown("### 挑选建议")
    st.write(item["tips"])

    st.markdown("### 保存建议")
    st.write(item.get("storage", "建议按成熟度冷藏或常温短放，尽快食用。"))

    st.markdown("### 常见吃法")
    st.write(item.get("recipe", "适合直接食用或做简单家常搭配。"))

# -------------------------
# top nav
# -------------------------
left, right = st.columns([4, 2])
with left:
    st.title("应季果蔬")
    st.caption("每天看看今天适合吃什么")
with right:
    page = st.radio(
        "页面",
        ["首页", "查询页", "收藏页", "详情页"],
        index=["首页", "查询页", "收藏页", "详情页"].index(st.session_state.page),
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.page = page

# -------------------------
# home
# -------------------------
if st.session_state.page == "首页":
    ensure_home_pick()
    month_data = data[active_month]
    month_items = get_month_items(active_month)

    top_a, top_b = st.columns([2, 1])
    with top_a:
        st.markdown(f"## {active_month}在吃什么")
        st.caption(month_data.get("season_hint", ""))
    with top_b:
        quick_search = st.text_input("搜索果蔬", placeholder="例如：草莓、菠菜", label_visibility="collapsed")
        if quick_search:
            st.session_state.keyword = quick_search
            st.session_state.page = "查询页"
            st.rerun()

    st.markdown("## 今日推荐")
    pick_item, pick_month = get_item_by_name(st.session_state.home_pick_name)
    c1, c2 = st.columns([5, 1])
    with c1:
        if pick_item:
            render_card(pick_item, pick_month, compact=False)
        else:
            st.info("暂无推荐")
    with c2:
        st.write("")
        st.write("")
        if st.button("换一换", use_container_width=True):
            change_home_pick()
            st.rerun()

    st.markdown("## 本月热门")
    hot_items = month_items[:6]
    cols = st.columns(2)
    for idx, item in enumerate(hot_items):
        with cols[idx % 2]:
            render_card(item, active_month, compact=True)

    st.markdown("## 标签探索")
    tags = get_all_tags(active_month)[1:9]
    if tags:
        cols = st.columns(4)
        for idx, tag in enumerate(tags):
            with cols[idx % 4]:
                if st.button(tag, key=f"home_tag_{tag}", use_container_width=True):
                    st.session_state.selected_month = active_month
                    st.session_state.selected_tag = tag
                    st.session_state.selected_category = "全部"
                    st.session_state.page = "查询页"
                    st.rerun()

    st.markdown("## 分类查看")
    a, b = st.columns(2)
    with a:
        if st.button("看水果", use_container_width=True):
            st.session_state.selected_month = active_month
            st.session_state.selected_category = "水果"
            st.session_state.selected_tag = "全部"
            st.session_state.page = "查询页"
            st.rerun()
    with b:
        if st.button("看蔬菜", use_container_width=True):
            st.session_state.selected_month = active_month
            st.session_state.selected_category = "蔬菜"
            st.session_state.selected_tag = "全部"
            st.session_state.page = "查询页"
            st.rerun()

# -------------------------
# query
# -------------------------
elif st.session_state.page == "查询页":
    st.markdown("## 查询页")

    col1, col2, col3 = st.columns([1.2, 1, 2])
    with col1:
        selected_month = st.selectbox("月份", months, index=months.index(st.session_state.selected_month))
        st.session_state.selected_month = selected_month

    month_tags = get_all_tags(st.session_state.selected_month)

    with col2:
        selected_category = st.selectbox("分类", ["全部", "水果", "蔬菜"], index=["全部", "水果", "蔬菜"].index(st.session_state.selected_category))
        st.session_state.selected_category = selected_category

    with col3:
        input_keyword = st.text_input("搜索", value=st.session_state.keyword, placeholder="搜索果蔬名称或关键词")
        st.session_state.keyword = input_keyword

    tag_cols = st.columns(5)
    for idx, tag in enumerate(month_tags[:10]):
        with tag_cols[idx % 5]:
            active = st.session_state.selected_tag == tag
            label = f"✓ {tag}" if active else tag
            if st.button(label, key=f"filter_{tag}", use_container_width=True):
                st.session_state.selected_tag = tag
                st.rerun()

    selected_data = data[st.session_state.selected_month]
    items = get_month_items(st.session_state.selected_month)
    filtered_items = filter_items(
        items,
        keyword=st.session_state.keyword,
        category=st.session_state.selected_category,
        tag=st.session_state.selected_tag,
        month=st.session_state.selected_month
    )

    st.caption(f"共找到 {len(filtered_items)} 个结果")

    if filtered_items:
        cols = st.columns(2)
        for idx, item in enumerate(filtered_items):
            with cols[idx % 2]:
                render_card(item, st.session_state.selected_month, compact=True)
    else:
        st.info("没有找到匹配内容，试试换关键词或筛选条件。")

# -------------------------
# favorites
# -------------------------
elif st.session_state.page == "收藏页":
    st.markdown("## 收藏页")
    favorites = st.session_state.favorites
    if not favorites:
        st.info("你还没有收藏果蔬，可以先去首页或查询页看看。")
    else:
        cols = st.columns(2)
        for idx, name in enumerate(favorites):
            item, month = get_item_by_name(name)
            if item:
                with cols[idx % 2]:
                    render_card(item, month, compact=True)

# -------------------------
# detail
# -------------------------
else:
    render_detail()
