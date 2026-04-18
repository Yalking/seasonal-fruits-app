import json
from datetime import datetime
from pathlib import Path
import time

import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="应季果蔬",
    page_icon="🥬",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': '应季果蔬指南 - 帮助您了解当季新鲜果蔬',
    }
)

# 自定义CSS - 优化移动端体验
st.markdown("""
<style>
/* 全局样式优化 */
* {
    -webkit-tap-highlight-color: transparent;
}

/* 主容器样式 */
.main .block-container {
    max-width: 100%;
    padding: 0.5rem;
    padding-top: 1rem;
    padding-bottom: 0;
}

/* 标题样式 */
h1 {
    font-size: 24px !important;
    line-height: 1.3 !important;
    margin-bottom: 0.5rem !important;
    margin-top: 0.5rem !important;
    text-align: center;
    color: #2F3640;
}

h2 {
    font-size: 20px !important;
    line-height: 1.3 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
    color: #2F3640;
}

h3 {
    font-size: 18px !important;
    line-height: 1.3 !important;
    margin-top: 0.8rem !important;
    margin-bottom: 0.4rem !important;
    color: #2F3640;
}

/* 输入框样式 - 移动端友好 */
div[data-testid="stTextInput"] input {
    height: 48px;
    border-radius: 12px;
    font-size: 16px;
    padding: 0 16px;
    border: 1px solid #E0E0E0;
    background: #FFFFFF;
    transition: all 0.3s ease;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

/* 选择框样式 */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 48px;
    border-radius: 12px;
    font-size: 16px;
    border: 1px solid #E0E0E0;
    background: #FFFFFF;
}

/* 按钮样式 - 移动端优化 */
div[data-testid="stButton"] > button {
    border-radius: 12px;
    font-size: 16px;
    white-space: nowrap;
    min-height: 48px;
    padding: 0 20px;
    border: none;
    background: #4CAF50;
    color: white;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

div[data-testid="stButton"] > button:hover {
    background: #45a049;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

div[data-testid="stButton"] > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
}

/* 次要按钮样式 */
div.st-key-home_search_btn > button,
div.st-key-search_page_btn > button,
div[class*="st-key-view_"] > button {
    background: #E8F5E9;
    color: #2E7D32;
}

/* 收藏按钮 */
div[class*="st-key-fav_"] > button {
    width: 48px;
    min-width: 48px;
    height: 48px;
    min-height: 48px;
    padding: 0;
    border-radius: 50%;
    background: #FFFFFF;
    border: 2px solid #E0E0E0;
    color: #757575;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

div[class*="st-key-fav_"] > button:hover {
    background: #E8F5E9;
    border-color: #4CAF50;
    color: #2E7D32;
    transform: scale(1.1);
}

div[class*="st-key-fav_on_"] > button {
    background: #4CAF50;
    border-color: #4CAF50;
    color: white;
}

/* 分类按钮 */
div[class*="st-key-cat_"] > button {
    min-height: 44px;
    border-radius: 12px;
    margin: 4px;
    background: #F7FBF5 !important;
    color: #7A8A7A !important;
    border: 1px solid #E4EFE0 !important;
    box-shadow: none !important;
    transition: all 0.2s ease;
}

div[class*="st-key-cat_"] > button:hover {
    background: #EDF7E8 !important;
    color: #4F6F4F !important;
    border-color: #D7E8D1 !important;
    transform: none !important;
    box-shadow: none !important;
}

div[class*="st-key-cat_active_"] > button {
    background: #DFF2DD !important;
    color: #2E7D32 !important;
    border-color: #B9DEB6 !important;
    font-weight: 600 !important;
}

/* 标签按钮 */
div[class*="st-key-tag2_"] > button {
    width: auto;
    min-height: 36px;
    border-radius: 20px;
    padding: 6px 16px;
    background: #F7FBF5 !important;
    color: #7A8A7A !important;
    border: 1px solid #E4EFE0 !important;
    font-size: 14px;
    box-shadow: none !important;
    transition: all 0.2s ease;
}

div[class*="st-key-tag2_"] > button:hover {
    background: #EDF7E8 !important;
    color: #4F6F4F !important;
    border-color: #D7E8D1 !important;
    transform: none !important;
    box-shadow: none !important;
}

div[class*="st-key-tag2_active_"] > button {
    background: #DFF2DD !important;
    color: #2E7D32 !important;
    border-color: #B9DEB6 !important;
    font-weight: 600 !important;
}

/* 底部导航栏 - 移动端优化 */
div.st-key-bottom_nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    border-top: 1px solid #E0E0E0;
    padding: 8px 0;
    z-index: 1000;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
}

div.st-key-bottom_nav [role="radiogroup"] {
    display: flex;
    justify-content: space-around;
    gap: 0;
    max-width: 500px;
    margin: 0 auto;
}

div.st-key-bottom_nav label[data-baseweb="radio"] {
    flex: 1;
    margin: 0;
    padding: 8px;
    border: none;
    background: transparent;
    justify-content: center;
    border-radius: 0;
    min-height: auto;
}

div.st-key-bottom_nav label[data-baseweb="radio"] div {
    font-size: 12px !important;
    color: #757575;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

div.st-key-bottom_nav label[data-baseweb="radio"][aria-checked="true"] div {
    color: #4CAF50;
}

/* 卡片样式 */
div[data-testid="stVerticalBlockBorder"] {
    border-radius: 16px;
    border: 1px solid #E0E0E0;
    overflow: hidden;
    transition: all 0.3s ease;
    background: white;
}

div[data-testid="stVerticalBlockBorder"]:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

/* 图片容器 */
div[data-testid="stImage"] > div > img {
    border-radius: 12px 12px 0 0;
    width: 100%;
    height: auto;
    object-fit: cover;
}

/* 标签样式 */
.tag-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 16px;
    background: #E8F5E9;
    color: #2E7D32;
    font-size: 12px;
    margin: 2px;
    white-space: nowrap;
}

/* 加载动画 */
.loading-spinner {
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
}

/* 搜索下拉建议 */
.search-suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #E0E0E0;
    border-radius: 0 0 12px 12px;
    max-height: 300px;
    overflow-y: auto;
    z-index: 1000;
    display: none;
}

/* 返回按钮 */
.back-button {
    position: fixed;
    top: 12px;
    left: 12px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #E0E0E0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    transition: all 0.3s ease;
}

.back-button:hover {
    background: white;
    transform: scale(1.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 8px;
        padding-right: 8px;
    }

    h1 {
        font-size: 22px !important;
    }

    h2 {
        font-size: 18px !important;
    }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
    .main .block-container {
        background: #121212;
        color: #ffffff;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    div[data-testid="stTextInput"] input {
        background: #1E1E1E;
        border-color: #333333;
        color: #ffffff;
    }
}
</style>
""", unsafe_allow_html=True)

# 初始化配置
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "seasonal_produce.json"
IMAGES_DIR = BASE_DIR / "images"

# 加载数据
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

months = list(data.keys())
current_month = f"{datetime.now().month}月"
default_month = current_month if current_month in months else months[0]

# 初始化session state
defaults = {
    "page": "home",
    "selected_month": default_month,
    "selected_item": None,
    "selected_category": "all",
    "selected_tag": "all",
    "favorites": [],
    "search_input": "",
    "search_history": [],
    "keyword": "",
    "last_main_page": "home",
    "loading": False,
    "search_suggestions": [],
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 工具函数
def normalize_key(text):
    return str(text).replace(" ", "_").replace("/", "_")

def get_image_path(item_name: str):
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        path = IMAGES_DIR / f"{item_name}{ext}"
        if path.exists():
            return path
    return None

def get_month_items(month):
    month_data = data.get(month, {})
    return month_data.get("fruits", []) + month_data.get("vegetables", [])

def is_fruit(item, month):
    return any(x["name"] == item["name"] for x in data[month].get("fruits", []))

def get_item_by_name(name):
    if not name:
        return None, None
    for month in months:
        for item in get_month_items(month):
            if item["name"] == name:
                return item, month
    return None, None

def get_all_tags(month):
    tags = set()
    for item in get_month_items(month):
        for tag in item.get("tags", []):
            tags.add(tag)
    priority = [
        "水果", "蔬菜", "补维C", "膳食纤维", "清爽", "低负担", "家常常见",
        "适合早餐", "适合凉拌", "适合炖煮", "春季推荐", "夏季推荐", "容易买到",
        "开胃", "时令感强"
    ]
    ordered = [x for x in priority if x in tags] + sorted([x for x in tags if x not in priority])
    return ["全部"] + ordered

def get_secondary_tags(month):
    return [t for t in get_all_tags(month) if t not in ["全部", "水果", "蔬菜"]]

def get_search_suggestions(query, limit=5):
    suggestions = []
    query = query.lower()
    for month in months:
        for item in get_month_items(month):
            if query in item["name"].lower():
                suggestions.append(item["name"])
                if len(suggestions) >= limit:
                    break
        if len(suggestions) >= limit:
            break
    return suggestions

# 状态管理函数
def toggle_favorite(item_name):
    favorites = set(st.session_state.favorites)
    if item_name in favorites:
        favorites.remove(item_name)
    else:
        favorites.add(item_name)
    st.session_state.favorites = list(favorites)

def open_detail(item_name):
    st.session_state.selected_item = item_name
    if st.session_state.page != "detail":
        st.session_state.last_main_page = st.session_state.page
    st.session_state.page = "detail"

def go_to_page(page, month=None, keyword=None, category=None, tag=None):
    st.session_state.page = page
    if month is not None:
        st.session_state.selected_month = month
    if keyword is not None:
        st.session_state.keyword = keyword
        st.session_state.search_input = keyword
    if category is not None:
        st.session_state.selected_category = category
    if tag is not None:
        st.session_state.selected_tag = tag



def get_category_button_key(category_name, active=False):
    return f"cat_active_{category_name}" if active else f"cat_{category_name}"

def get_tag_button_key(tag_name, active=False):
    base = normalize_key(tag_name)
    return f"tag2_active_{base}" if active else f"tag2_{base}"

def filter_items(items, keyword="", category="all", tag="all", month=None):
    result = items
    if keyword:
        kw = keyword.strip().lower()
        result = [
            item for item in result
            if kw in item["name"].lower()
            or kw in item.get("desc", "").lower()
            or kw in item.get("nutrition", "").lower()
        ]
    if category == "fruit":
        result = [item for item in result if month and is_fruit(item, month)]
    elif category == "vegetable":
        result = [item for item in result if month and not is_fruit(item, month)]
    if tag != "all":
        result = [item for item in result if tag in item.get("tags", [])]
    return result

# UI组件函数
def render_header():
    header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

    with header_col1:
        # 返回按钮（仅在非首页显示）
        if st.session_state.page not in ["home", "search", "favorites"]:
            if st.button("←", key="back_btn", help="返回"):
                go_to_page(st.session_state.last_main_page)
                st.rerun()

    with header_col2:
        # 标题
        if st.session_state.page == "home":
            st.title("🥬 应季果蔬")
        elif st.session_state.page == "search":
            st.title("🔍 搜索")
        elif st.session_state.page == "favorites":
            st.title("⭐ 我的收藏")
        elif st.session_state.page == "detail":
            item, _ = get_item_by_name(st.session_state.selected_item)
            if item:
                st.title(item["name"])

    with header_col3:
        # 收藏按钮（仅在详情页显示）
        if st.session_state.page == "detail":
            item, _ = get_item_by_name(st.session_state.selected_item)
            if item:
                active_fav = item["name"] in st.session_state.favorites
                icon = "★" if active_fav else "☆"
                if st.button(icon, key="detail_fav_btn", help="收藏/取消收藏"):
                    toggle_favorite(item["name"])
                    st.rerun()

def render_search_bar():
    search_col = st.columns([1])[0]
    with search_col:
        # 搜索框
        search_input = st.text_input(
            "搜索果蔬",
            value=st.session_state.search_input,
            placeholder="搜索名称或关键词...",
            key="search_input_field",
            on_change=lambda: setattr(st.session_state, 'search_suggestions',
                                     get_search_suggestions(st.session_state.search_input))
        )

        # 搜索建议
        if st.session_state.search_suggestions and st.session_state.search_input:
            st.markdown("""
            <div class="search-suggestions">
            """, unsafe_allow_html=True)
            for suggestion in st.session_state.search_suggestions:
                if st.button(suggestion, key=f"suggestion_{normalize_key(suggestion)}", help=f"搜索{suggestion}"):
                    go_to_page("search", keyword=suggestion)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

def render_card(item, month, compact=True, source="default"):
    image_path = get_image_path(item["name"])

    with st.container(border=True):
        # 图片
        if image_path:
            # 添加图片加载延迟优化
            with st.spinner("加载中..."):
                st.image(str(image_path), use_container_width=True)
        else:
            st.caption(f"📷 未找到图片：{item['name']}")

        # 标题和收藏
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"### {item['name']}")
        with col2:
            active_fav = item["name"] in st.session_state.favorites
            icon = "★" if active_fav else "☆"
            if st.button(icon, key=f"fav_{source}_{normalize_key(item['name'])}_{month}_{compact}"):
                toggle_favorite(item["name"])
                st.rerun()

        # 标签
        tags = item.get("tags", [])[:3 if compact else 6]
        if tags:
            tag_html = " ".join([f'<span class="tag-pill">{tag}</span>' for tag in tags])
            st.markdown(tag_html, unsafe_allow_html=True)

        # 描述
        desc = item.get("desc", "")
        if compact and len(desc) > 50:
            desc = desc[:50] + "..."
        st.write(desc)

        # 营养信息（非紧凑模式）
        if not compact:
            st.caption(f"💪 营养：{item.get('nutrition', '暂无信息')}")

        # 查看详情按钮
        if compact:
            if st.button("查看详情", key=f"view_{source}_{normalize_key(item['name'])}_{month}_{compact}"):
                open_detail(item["name"])
                st.rerun()

def render_home():

    # 月份选择器
    month_col = st.columns([1])[0]
    with month_col:
        selected_month = st.selectbox(
            "📅 选择月份",
            months,
            index=months.index(st.session_state.selected_month),
            key="month_select",
            format_func=lambda x: f"{x}"
        )
        st.session_state.selected_month = selected_month

    # 搜索框
    render_search_bar()

    # 本月热门
    st.markdown("## 🔥 本月热门")
    hot_items = get_month_items(selected_month)[:6]  # 增加到6个
    cols = st.columns(2 or None)
    for idx, item in enumerate(hot_items):
        with cols[idx % 2]:
            render_card(item, selected_month, compact=True, source="home_hot")

    # 分类浏览
    st.markdown("## 📚 分类浏览")
    fruit_items = [item for item in get_month_items(selected_month) if is_fruit(item, selected_month)]
    vegetable_items = [item for item in get_month_items(selected_month) if not is_fruit(item, selected_month)]

    if fruit_items:
        st.markdown("### 🍎 水果")
        fruit_cols = st.columns(2 or None)
        for idx, item in enumerate(fruit_items[:4]):  # 每类最多显示4个
            with fruit_cols[idx % 2]:
                render_card(item, selected_month, compact=True, source="home_fruit")

    if vegetable_items:
        st.markdown("### 🥬 蔬菜")
        veg_cols = st.columns(2 or None)
        for idx, item in enumerate(vegetable_items[:4]):
            with veg_cols[idx % 2]:
                render_card(item, selected_month, compact=True, source="home_veg")

def render_search():

    # 搜索框
    render_search_bar()

    st.markdown("### 🔽 快速筛选")
    current_category = st.session_state.selected_category
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("全部", key=get_category_button_key("all", current_category == "all"), use_container_width=True):
            go_to_page("search", category="all", tag="all")
            st.rerun()
    with col2:
        if st.button("水果", key=get_category_button_key("fruit", current_category == "fruit"), use_container_width=True):
            go_to_page("search", category="fruit", tag="all")
            st.rerun()
    with col3:
        if st.button("蔬菜", key=get_category_button_key("vegetable", current_category == "vegetable"), use_container_width=True):
            go_to_page("search", category="vegetable", tag="all")
            st.rerun()

    st.markdown("### 🏷️ 标签筛选")
    current_tag = st.session_state.selected_tag
    tags = get_secondary_tags(st.session_state.selected_month)
    if tags:
        tag_cols = st.columns(4)
        for idx, tag in enumerate(tags[:8]):
            with tag_cols[idx % 4]:
                is_active = current_tag == tag
                if st.button(tag, key=get_tag_button_key(tag, is_active), use_container_width=True):
                    go_to_page("search", tag=tag)
                    st.rerun()

    items = get_month_items(st.session_state.selected_month)
    filtered_items = filter_items(
        items,
        keyword=st.session_state.keyword,
        category=st.session_state.selected_category,
        tag=st.session_state.selected_tag,
        month=st.session_state.selected_month
    )

    st.caption(f"📊 共找到 {len(filtered_items)} 个结果")

    if filtered_items:
        cols = st.columns(2)
        for idx, item in enumerate(filtered_items):
            with cols[idx % 2]:
                render_card(item, st.session_state.selected_month, compact=True, source="search")
    else:
        st.info("😔 没有找到匹配的内容，试试换个关键词或筛选条件吧！")

def render_favorites():

    if not st.session_state.favorites:
        st.markdown("## ⭐ 我的收藏")
        st.info("你还没有收藏任何果蔬\n\n💡 点击果蔬卡片上的星号来收藏喜欢的果蔬")
        return

    st.markdown(f"## ⭐ 我的收藏 ({len(st.session_state.favorites)})")

    # 收藏列表
    for name in st.session_state.favorites:
        item, month = get_item_by_name(name)
        if item:
            render_card(item, month, compact=False, source="favorites")

    # 清空收藏按钮
    if len(st.session_state.favorites) > 0:
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("清空收藏", key="clear_favorites", help="清空所有收藏"):
                st.session_state.favorites = []
                st.rerun()

def render_detail():
    item_name = st.session_state.selected_item
    item, month = get_item_by_name(item_name)

    if not item:
        st.warning("❌ 未找到该果蔬信息")
        return

    # 显示所有信息
    st.markdown(f"## {item['name']}")
    st.caption(f"📅 {month} · {'🍎 水果' if is_fruit(item, month) else '🥬 蔬菜'}")

    # 大图
    image_path = get_image_path(item["name"])
    if image_path:
        st.image(str(image_path), use_container_width=True)

    # 标签
    tags = item.get("tags", [])
    if tags:
        tag_html = " ".join([f'<span class="tag-pill">{tag}</span>' for tag in tags])
        st.markdown("### 🏷️ 标签")
        st.markdown(tag_html, unsafe_allow_html=True)

    # 详细信息
    st.markdown("### 📝 为什么现在推荐吃")
    st.write(item.get("desc", ""))

    st.markdown("### 💪 营养亮点")
    st.write(item.get("nutrition", ""))

    st.markdown("### 👀 挑选建议")
    st.write(item.get("tips", ""))

    st.markdown("### 🧊 保存建议")
    st.write(item.get("storage", "建议按成熟度冷藏或常温短放，尽快食用。"))

    st.markdown("### 🍳 常见吃法")
    st.write(item.get("recipe", "适合直接食用或做简单家常搭配。"))

# 主页面渲染
render_header()

# 根据页面状态渲染内容
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "search":
    render_search()
elif st.session_state.page == "favorites":
    render_favorites()
elif st.session_state.page == "detail":
    render_detail()

# 底部导航（仅在某些页面显示）
if st.session_state.page in ["home", "search", "favorites"]:
    current_page = st.session_state.page
    st.markdown("<div style='height: 88px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .bottom-nav-wrap {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #EAEAEA;
        padding: 8px 12px calc(8px + env(safe-area-inset-bottom));
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    div.st-key-bottom_nav_home button,
    div.st-key-bottom_nav_home_active button,
    div.st-key-bottom_nav_search button,
    div.st-key-bottom_nav_search_active button,
    div.st-key-bottom_nav_favorites button,
    div.st-key-bottom_nav_favorites_active button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        min-height: 52px !important;
        color: #9E9E9E !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        padding: 6px 8px !important;
    }
    div.st-key-bottom_nav_home button:hover,
    div.st-key-bottom_nav_home_active button:hover,
    div.st-key-bottom_nav_search button:hover,
    div.st-key-bottom_nav_search_active button:hover,
    div.st-key-bottom_nav_favorites button:hover,
    div.st-key-bottom_nav_favorites_active button:hover {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    div.st-key-bottom_nav_home_active button,
    div.st-key-bottom_nav_search_active button,
    div.st-key-bottom_nav_favorites_active button {
        color: #222222 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='bottom-nav-wrap'>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        home_key = "bottom_nav_home_active" if current_page == "home" else "bottom_nav_home"
        if st.button("🏠 首页", key=home_key, use_container_width=True):
            go_to_page("home")
            st.rerun()
    with nav2:
        search_key = "bottom_nav_search_active" if current_page == "search" else "bottom_nav_search"
        if st.button("🔍 搜索", key=search_key, use_container_width=True):
            go_to_page("search")
            st.rerun()
    with nav3:
        fav_key = "bottom_nav_favorites_active" if current_page == "favorites" else "bottom_nav_favorites"
        if st.button("⭐ 收藏", key=fav_key, use_container_width=True):
            go_to_page("favorites")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
