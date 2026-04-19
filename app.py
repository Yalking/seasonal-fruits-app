import json
import random
from datetime import datetime
from pathlib import Path

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
html, body, [data-testid="stAppViewContainer"] {
    background: #EEF1F4;
}

[data-testid="stAppViewContainer"] > .main {
    display: flex;
    justify-content: center;
}

.main .block-container {
    width: min(100%, 390px);
    max-width: 390px;
    min-height: 100vh;
    padding: 0.5rem;
    padding-top: 1rem;
    padding-bottom: 0;
    background: #FFFFFF;
    box-shadow: 0 0 0 1px rgba(22, 28, 45, 0.06), 0 18px 60px rgba(22, 28, 45, 0.12);
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

div[class*="st-key-view_"] button {
    min-height: 42px !important;
    font-size: 14px !important;
    padding: 0 16px !important;
    border-radius: 10px !important;
}

div.st-key-refresh_today_recommendations button {
    min-height: 36px !important;
    padding: 0 14px !important;
    border-radius: 999px !important;
    background: #FFFFFF !important;
    color: #4A4F57 !important;
    border: 1px solid #E5E7EB !important;
    box-shadow: none !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

div.st-key-refresh_today_recommendations button:hover {
    background: #F8F9FB !important;
    color: #343A40 !important;
    border-color: #D9DDE3 !important;
    transform: none !important;
    box-shadow: none !important;
}

div[class*="st-key-card_action_row_"] [data-testid="stHorizontalBlock"] {
    display: grid !important;
    grid-template-columns: minmax(0, 1fr) 44px !important;
    gap: 12px !important;
    align-items: center !important;
}

div[class*="st-key-card_action_row_"] [data-testid="column"] {
    display: flex;
    align-items: center;
    min-width: 0;
}

div[class*="st-key-card_action_row_"] [data-testid="column"]:last-child {
    justify-content: flex-end;
}
div[class*="st-key-card_action_row_"] [data-testid="column"]:last-child div[data-testid="stButton"] > button {
    width: 38px;
    min-width: 38px;
    height: 38px;
    min-height: 38px;
    padding: 0 !important;
    border-radius: 12px !important;
    background: #F3F4F7 !important;
    border: 1px solid #E1E4EA !important;
    color: #C7CDD8 !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #C7CDD8 !important;
    text-align: center !important;
}

div[class*="st-key-card_action_row_"] [data-testid="column"]:last-child div[data-testid="stButton"] > button p,
div[data-testid="stButton"][class*="st-key-detail_fav_btn"] > button p,
div[class*="st-key-favwrap_detail_"] button p,
div[class*="st-key-favwrap_on_detail_"] button p,
div[class*="st-key-fav_"] button p,
div[class*="st-key-fav_on_"] button p {
    margin: 0 !important;
    width: 100% !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
}

div[class*="st-key-card_action_row_"] [data-testid="column"]:last-child div[data-testid="stButton"] > button:hover {
    background: #ECEFF4 !important;
    border-color: #D5DAE3 !important;
    color: #AEB6C2 !important;
    box-shadow: none !important;
    transform: none !important;
}

div[class*="st-key-fav_"] button {
    background: #F3F4F7 !important;
    border: 1px solid #E1E4EA !important;
    color: #C7CDD8 !important;
}

div[class*="st-key-fav_"] button:hover {
    background: #ECEFF4 !important;
    border-color: #D5DAE3 !important;
    color: #AEB6C2 !important;
}

div[class*="st-key-fav_on_"] button {
    background: #F3F4F7 !important;
    border: 1px solid #DCE7DA !important;
    color: #9FD39A !important;
}

div[data-testid="stButton"][class*="st-key-detail_fav_btn"] > button,
div[class*="st-key-favwrap_detail_"] button,
div[class*="st-key-favwrap_on_detail_"] button {
    color: #C7CDD8 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

div[data-testid="stButton"][class*="st-key-detail_fav_btn"] > button:hover,
div[class*="st-key-favwrap_detail_"] button:hover,
div[class*="st-key-favwrap_on_detail_"] button:hover {
    color: #AEB6C2 !important;
}

div[class*="st-key-favwrap_on_detail_"] button {
    color: #9FD39A !important;
}

/* 分类按钮 */
div[class*="st-key-cat_"] button {
    min-height: 44px;
    border-radius: 999px;
    margin: 6px 0;
    background: #F3F4F7 !important;
    color: #555B66 !important;
    border: none !important;
    box-shadow: none !important;
    transition: all 0.2s ease;
    font-weight: 500 !important;
    padding: 0 14px !important;
}

div[class*="st-key-cat_"] button:hover {
    background: #EBEDF2 !important;
    color: #3F4652 !important;
    transform: none !important;
    box-shadow: none !important;
}

div[class*="st-key-cat_active_"] button {
    background: #FF6B4A !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
}

/* 标签按钮 */
div[class*="st-key-tag2_"] button {
    width: auto;
    min-height: 40px;
    border-radius: 999px;
    padding: 6px 16px;
    background: #F3F4F7 !important;
    color: #555B66 !important;
    border: none !important;
    font-size: 14px;
    box-shadow: none !important;
    transition: all 0.2s ease;
    font-weight: 500 !important;
    padding: 0 14px !important;
}

div[class*="st-key-tag2_"] button:hover {
    background: #EBEDF2 !important;
    color: #3F4652 !important;
    transform: none !important;
    box-shadow: none !important;
}

div[class*="st-key-tag2_active_"] button {
    background: #FF6B4A !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
}

div.st-key-discover_category_wrap [data-testid="stHorizontalBlock"],
div.st-key-discover_tag_wrap [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    align-items: flex-start !important;
}

div.st-key-discover_category_wrap [data-testid="column"],
div.st-key-discover_tag_wrap [data-testid="column"] {
    width: auto !important;
    flex: 0 0 auto !important;
    min-width: fit-content !important;
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
        width: 100%;
        max-width: 100%;
        box-shadow: none;
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

@media (min-width: 769px) {
    .main .block-container {
        border-radius: 28px 28px 0 0;
        margin-top: 12px;
    }
}

div.st-key-top_header_shell {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: min(100%, 390px);
    z-index: 1001;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid #EEF1F4;
    padding: 8px 12px 6px;
}

div.st-key-top_header_shell [data-testid="stHorizontalBlock"] {
    align-items: center;
}

@media (max-width: 768px) {
    div.st-key-top_header_shell {
        left: 0;
        right: 0;
        width: 100%;
        transform: none;
        padding-left: 8px;
        padding-right: 8px;
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
    "selected_item": None,
    "favorites": [],
    "last_main_page": "home",
    "home_month": default_month,
    "discover_month": default_month,
    "discover_category": "all",
    "discover_tag": "all",
    "discover_search_input": "",
    "discover_search_input_pending": None,
    "discover_keyword": "",
    "discover_search_suggestions": [],
    "favorites_month_filter": "全部月份",
    "favorites_confirm_clear": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 工具函数
def normalize_key(text):
    return str(text).replace(" ", "_").replace("/", "_")

def make_item_ref(item_name, month=None):
    return f"{month}::{item_name}" if month else item_name

def parse_item_ref(item_ref):
    if isinstance(item_ref, str) and "::" in item_ref:
        month, item_name = item_ref.split("::", 1)
        return item_name, month
    return item_ref, None

def is_favorite(item_name, month=None):
    favorites = st.session_state.favorites
    item_ref = make_item_ref(item_name, month)
    return item_ref in favorites or item_name in favorites

def get_image_path(item: dict):
    configured_path = item.get("image")
    if configured_path:
        configured = BASE_DIR / configured_path
        if configured.exists():
            return configured

    item_name = item["name"]
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

def get_item_by_name(name, month=None):
    if not name:
        return None, None
    if month:
        for item in get_month_items(month):
            if item["name"] == name:
                return item, month
    for month in months:
        for item in get_month_items(month):
            if item["name"] == name:
                return item, month
    return None, None

def get_item_by_ref(item_ref):
    item_name, month = parse_item_ref(item_ref)
    return get_item_by_name(item_name, month)

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

def show_toast(message):
    if hasattr(st, "toast"):
        st.toast(message)
    else:
        st.info(message)

def render_responsive_image(image_path):
    try:
        st.image(str(image_path), width="stretch")
    except TypeError:
        st.image(str(image_path), use_column_width=True)

def get_search_suggestions(query, limit=5):
    suggestions = []
    seen = set()
    query = query.strip().lower()
    if not query:
        return suggestions

    for month in months:
        for item in get_month_items(month):
            item_name = item["name"]
            if query in item_name.lower() and item_name not in seen:
                seen.add(item_name)
                suggestions.append(item["name"])
                if len(suggestions) >= limit:
                    break
        if len(suggestions) >= limit:
            break
    return suggestions

def get_random_recommendations(month):
    fruits = data.get(month, {}).get("fruits", [])
    vegetables = data.get(month, {}).get("vegetables", [])
    picks = []

    if fruits:
        fruit_pick = st.session_state.get(f"_today_fruit_{month}")
        if fruit_pick not in [item["name"] for item in fruits]:
            fruit_pick = random.choice(fruits)["name"]
            st.session_state[f"_today_fruit_{month}"] = fruit_pick
        picks.append(fruit_pick)
        if picks[0] not in [item["name"] for item in fruits]:
            picks[0] = fruits[0]["name"]
    if vegetables:
        veg_pick = st.session_state.get(f"_today_veg_{month}")
        if veg_pick not in [item["name"] for item in vegetables]:
            veg_pick = random.choice(vegetables)["name"]
            st.session_state[f"_today_veg_{month}"] = veg_pick
        picks.append(veg_pick)

    items = []
    for item_name in picks:
        item, item_month = get_item_by_name(item_name, month)
        if item:
            items.append((item, item_month))
    return items

def refresh_today_recommendations(month):
    fruits = data.get(month, {}).get("fruits", [])
    vegetables = data.get(month, {}).get("vegetables", [])
    if fruits:
        st.session_state[f"_today_fruit_{month}"] = random.choice(fruits)["name"]
    if vegetables:
        st.session_state[f"_today_veg_{month}"] = random.choice(vegetables)["name"]

def get_favorite_entries(month_filter="全部月份"):
    entries = []
    for item_ref in st.session_state.favorites:
        item, month = get_item_by_ref(item_ref)
        if not item:
            continue
        if month_filter != "全部月份" and month != month_filter:
            continue
        entries.append({
            "ref": item_ref,
            "item": item,
            "month": month,
        })
    return entries

def get_display_favorites(month_filter="全部月份"):
    entries = get_favorite_entries(month_filter)
    if month_filter != "全部月份":
        return entries

    merged = {}
    for entry in entries:
        name = entry["item"]["name"]
        if name not in merged:
            merged[name] = entry
            continue

        current_month_idx = months.index(entry["month"])
        saved_month_idx = months.index(merged[name]["month"])
        if current_month_idx >= saved_month_idx:
            merged[name] = entry

    return list(merged.values())

def get_related_items(item, month, limit=2):
    current_tags = set(item.get("tags", []))
    current_is_fruit = is_fruit(item, month)
    candidates = []

    for candidate in get_month_items(month):
        if candidate["name"] == item["name"]:
            continue
        same_category = is_fruit(candidate, month) == current_is_fruit
        common_tags = len(current_tags & set(candidate.get("tags", [])))
        score = (
            2 if same_category else 0,
            common_tags,
            candidate["name"],
        )
        candidates.append((score, candidate))

    candidates.sort(key=lambda x: (-x[0][0], -x[0][1], x[0][2]))
    return [candidate for _, candidate in candidates[:limit]]

# 状态管理函数
def apply_pending_discover_search_input():
    pending_value = st.session_state.discover_search_input_pending
    if pending_value is not None:
        st.session_state.discover_search_input = pending_value
        st.session_state.discover_search_input_pending = None

def sync_search_state():
    query = st.session_state.discover_search_input.strip()
    st.session_state.discover_keyword = query
    st.session_state.discover_search_suggestions = get_search_suggestions(query)

def submit_discover_search(query=None, sync_input=False):
    final_query = (query if query is not None else st.session_state.discover_search_input).strip()
    st.session_state.page = "search"
    st.session_state.discover_keyword = final_query
    st.session_state.discover_search_suggestions = get_search_suggestions(final_query)
    if sync_input:
        st.session_state.discover_search_input_pending = final_query

def toggle_favorite(item_name, month=None, remove_all_same_name=False):
    favorites = list(st.session_state.favorites)
    item_ref = make_item_ref(item_name, month)

    if remove_all_same_name:
        favorites = [fav for fav in favorites if parse_item_ref(fav)[0] != item_name]
    elif item_ref in favorites or item_name in favorites:
        favorites = [fav for fav in favorites if fav not in {item_ref, item_name}]
    else:
        favorites.append(item_ref)

    st.session_state.favorites = favorites

def open_detail(item_name, month=None):
    st.session_state.selected_item = make_item_ref(item_name, month)
    if st.session_state.page != "detail":
        st.session_state.last_main_page = st.session_state.page
    st.session_state.page = "detail"

def go_to_page(page, month=None, keyword=None, category=None, tag=None):
    st.session_state.page = page
    if keyword is not None:
        clean_keyword = keyword.strip()
        st.session_state.discover_keyword = clean_keyword
        st.session_state.discover_search_input_pending = clean_keyword
        st.session_state.discover_search_suggestions = get_search_suggestions(clean_keyword)
    if category is not None:
        st.session_state.discover_category = category
    if tag is not None:
        st.session_state.discover_tag = tag



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
    main_pages = ["home", "search", "favorites"]
    header_container = st.container(key="top_header_shell") if st.session_state.page in main_pages else st.container()

    with header_container:
        header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

        with header_col1:
            # 返回按钮（仅在非首页显示）
            if st.session_state.page not in main_pages:
                if st.button("←", key="back_btn", help="返回"):
                    go_to_page(st.session_state.last_main_page)
                    st.rerun()

        with header_col2:
            # 标题
            if st.session_state.page == "home":
                st.title("🥬 应季果蔬")
            elif st.session_state.page == "search":
                st.title("🔍 发现")
            elif st.session_state.page == "favorites":
                st.title("⭐ 我的收藏")
            elif st.session_state.page == "detail":
                item, _ = get_item_by_ref(st.session_state.selected_item)
                if item:
                    st.title(item["name"])

        with header_col3:
            # 收藏按钮（仅在详情页显示）
            if st.session_state.page == "detail":
                item, month = get_item_by_ref(st.session_state.selected_item)
                if item:
                    active_fav = is_favorite(item["name"], month)
                    icon = "★"
                    wrap_key = f"favwrap_on_detail_{normalize_key(item['name'])}_{month}" if active_fav else f"favwrap_detail_{normalize_key(item['name'])}_{month}"
                    with st.container(key=wrap_key):
                        if st.button(icon, key="detail_fav_btn", help="收藏/取消收藏"):
                            toggle_favorite(item["name"], month)
                            st.rerun()

def render_search_bar():
    apply_pending_discover_search_input()

    input_col, action_col = st.columns([5, 1])
    with input_col:
        # 搜索框
        st.text_input(
            "搜索果蔬",
            placeholder="搜索名称或关键词...",
            key="discover_search_input",
            on_change=sync_search_state
        )
    with action_col:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("搜索", key=f"search_page_btn_{st.session_state.page}", use_container_width=True):
            submit_discover_search()
            st.rerun()

def render_card(item, month, compact=True, source="default", show_view=True, remove_all_same_name_on_unfavorite=False):
    image_path = get_image_path(item)

    with st.container(border=True):
        # 图片
        if image_path:
            render_responsive_image(image_path)
        else:
            st.caption(f"📷 未找到图片：{item['name']}")

        # 标题
        st.markdown(f"### {item['name']}")

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

        # 底部操作区
        row_key = f"card_action_row_{source}_{normalize_key(item['name'])}_{month}_{compact}"
        with st.container(key=row_key):
            action_col1, action_col2 = st.columns([5, 1], vertical_alignment="center")
            with action_col1:
                if show_view:
                    if st.button("查看详情", key=f"view_{source}_{normalize_key(item['name'])}_{month}_{compact}"):
                        open_detail(item["name"], month)
                        st.rerun()
            with action_col2:
                active_fav = is_favorite(item["name"], month)
                icon = "★"
                fav_key_prefix = "fav_on" if active_fav else "fav"
                if st.button(icon, key=f"{fav_key_prefix}_{source}_{normalize_key(item['name'])}_{month}_{compact}"):
                    toggle_favorite(item["name"], month, remove_all_same_name=remove_all_same_name_on_unfavorite and active_fav)
                    st.rerun()

def render_home():
    selected_month = st.selectbox(
        "📅 选择月份",
        months,
        index=months.index(st.session_state.home_month),
        key="home_month_select",
        format_func=lambda x: f"{x}"
    )
    st.session_state.home_month = selected_month

    title_col, action_col = st.columns([4, 1])
    with title_col:
        st.markdown("## 今日推荐")
    with action_col:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("换一换", key="refresh_today_recommendations", use_container_width=True):
            refresh_today_recommendations(selected_month)
            st.rerun()

    today_items = get_random_recommendations(selected_month)
    if today_items:
        cols = st.columns(2)
        for idx, (item, month) in enumerate(today_items):
            with cols[idx % 2]:
                render_card(item, month, compact=True, source="home_today")
    else:
        st.info("这个月份暂时没有可展示的推荐内容。")

    st.markdown("## 🔥 本月热门")
    hot_items = get_month_items(selected_month)[:6]
    if hot_items:
        cols = st.columns(2)
        for idx, item in enumerate(hot_items):
            with cols[idx % 2]:
                render_card(item, selected_month, compact=True, source="home_hot")
    else:
        st.info("这个月份暂时没有可展示的热门果蔬。")

def render_search():
    selected_month = st.selectbox(
        "📅 发现月份",
        months,
        index=months.index(st.session_state.discover_month),
        key="discover_month_select",
        format_func=lambda x: f"{x}"
    )
    month_changed = selected_month != st.session_state.discover_month
    st.session_state.discover_month = selected_month
    available_tags = get_secondary_tags(selected_month)
    if month_changed and st.session_state.discover_tag != "all" and st.session_state.discover_tag not in available_tags:
        st.session_state.discover_tag = "all"
        show_toast("月份已切换，不适用的标签已重置为“全部”。")

    render_search_bar()

    st.markdown("### 🔽 快速筛选")
    category_label_map = {"全部": "all", "水果": "fruit", "蔬菜": "vegetable"}
    current_category_label = next(
        (label for label, value in category_label_map.items() if value == st.session_state.discover_category),
        "全部",
    )

    selected_category_label = st.pills(
        "快速筛选",
        options=list(category_label_map.keys()),
        default=current_category_label,
        label_visibility="collapsed",
    )
    selected_category_value = category_label_map.get(selected_category_label or "全部", "all")
    if selected_category_value != st.session_state.discover_category:
        st.session_state.discover_category = selected_category_value
        st.rerun()

    st.markdown("### 🏷️ 标签筛选")
    tag_items = ["全部"] + available_tags
    current_tag_label = "全部" if st.session_state.discover_tag == "all" else st.session_state.discover_tag
    if current_tag_label not in tag_items:
        current_tag_label = "全部"
        st.session_state.discover_tag = "all"

    selected_tag_label = st.pills(
        "标签筛选",
        options=tag_items,
        default=current_tag_label,
        label_visibility="collapsed",
    )
    selected_tag_value = "all" if (selected_tag_label or "全部") == "全部" else selected_tag_label
    if selected_tag_value != st.session_state.discover_tag:
        st.session_state.discover_tag = selected_tag_value
        st.rerun()

    items = get_month_items(selected_month)
    filtered_items = filter_items(
        items,
        keyword=st.session_state.discover_keyword,
        category=st.session_state.discover_category,
        tag=st.session_state.discover_tag,
        month=selected_month
    )

    st.caption(f"📊 共找到 {len(filtered_items)} 个结果")

    if filtered_items:
        cols = st.columns(2)
        for idx, item in enumerate(filtered_items):
            with cols[idx % 2]:
                render_card(item, selected_month, compact=True, source="search")
    else:
        st.info("😔 没有找到匹配的内容，试试换个关键词或筛选条件吧！")

def render_favorites():
    month_options = ["全部月份"] + months
    selected_filter = st.selectbox(
        "📅 收藏月份",
        month_options,
        index=month_options.index(st.session_state.favorites_month_filter),
        key="favorites_month_select",
    )
    st.session_state.favorites_month_filter = selected_filter

    display_entries = get_display_favorites(selected_filter)

    if not st.session_state.favorites:
        st.markdown("## ⭐ 我的收藏")
        st.info("你还没有收藏任何果蔬\n\n💡 点击果蔬卡片上的星号来收藏喜欢的果蔬")
        return

    st.markdown(f"## ⭐ 我的收藏 ({len(display_entries)})")

    if not display_entries:
        st.info("当前月份筛选下还没有收藏内容。")
    else:
        for entry in display_entries:
            render_card(
                entry["item"],
                entry["month"],
                compact=False,
                source=f"favorites_{selected_filter}",
                show_view=True,
                remove_all_same_name_on_unfavorite=(selected_filter == "全部月份"),
            )

    action_col1, action_col2 = st.columns([3, 2])
    with action_col2:
        if st.button("清空收藏", key="clear_favorites", help="清空所有收藏", use_container_width=True):
            st.session_state.favorites_confirm_clear = True

    if st.session_state.favorites_confirm_clear:
        st.warning("确认清空全部收藏吗？这个操作会移除所有月份的收藏记录。")
        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
            if st.button("确认清空", key="confirm_clear_favorites", use_container_width=True):
                st.session_state.favorites = []
                st.session_state.favorites_confirm_clear = False
                st.rerun()
        with confirm_col2:
            if st.button("取消", key="cancel_clear_favorites", use_container_width=True):
                st.session_state.favorites_confirm_clear = False
                st.rerun()

def render_detail():
    item, month = get_item_by_ref(st.session_state.selected_item)

    if not item:
        st.warning("❌ 未找到该果蔬信息")
        return

    # 显示所有信息
    st.markdown(f"## {item['name']}")
    st.caption(f"📅 {month} · {'🍎 水果' if is_fruit(item, month) else '🥬 蔬菜'}")

    # 大图
    image_path = get_image_path(item)
    if image_path:
        render_responsive_image(image_path)

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

    related_items = get_related_items(item, month)
    st.markdown("### 🌟 相关推荐")
    if related_items:
        cols = st.columns(2)
        for idx, related_item in enumerate(related_items):
            with cols[idx % 2]:
                render_card(related_item, month, compact=True, source=f"related_{normalize_key(item['name'])}")
    else:
        st.info("暂时没有更多相关推荐。")

# 主页面渲染
render_header()

if st.session_state.page in ["home", "search", "favorites"]:
    st.markdown("<div style='height: 86px;'></div>", unsafe_allow_html=True)

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
    div.st-key-bottom_nav_shell {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: min(100%, 390px);
        background: white;
        border-top: 1px solid #EAEAEA;
        padding: 8px 12px calc(8px + env(safe-area-inset-bottom));
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    div.st-key-bottom_nav_shell [data-testid="stHorizontalBlock"] {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 8px;
        align-items: stretch;
    }
    div.st-key-bottom_nav_shell [data-testid="column"] {
        width: 100% !important;
    }
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_home button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_home_active button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_search button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_search_active button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_favorites button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_favorites_active button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        min-height: 52px !important;
        width: 100% !important;
        color: #9E9E9E !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 6px 8px !important;
    }
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_home button:hover,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_home_active button:hover,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_search button:hover,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_search_active button:hover,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_favorites button:hover,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_favorites_active button:hover {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_home_active button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_search_active button,
    div.st-key-bottom_nav_shell div.st-key-bottom_nav_favorites_active button {
        color: #222222 !important;
        font-weight: 600 !important;
    }
    @media (max-width: 768px) {
        div.st-key-bottom_nav_shell {
            left: 0;
            right: 0;
            width: 100%;
            transform: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="bottom_nav_shell"):
        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            home_key = "bottom_nav_home_active" if current_page == "home" else "bottom_nav_home"
            if st.button("🏠 首页", key=home_key, use_container_width=True):
                go_to_page("home")
                st.rerun()
        with nav2:
            search_key = "bottom_nav_search_active" if current_page == "search" else "bottom_nav_search"
            if st.button("🔍 发现", key=search_key, use_container_width=True):
                go_to_page("search")
                st.rerun()
        with nav3:
            fav_key = "bottom_nav_favorites_active" if current_page == "favorites" else "bottom_nav_favorites"
            if st.button("⭐ 收藏", key=fav_key, use_container_width=True):
                go_to_page("favorites")
                st.rerun()
