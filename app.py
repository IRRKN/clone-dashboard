"""
Серіал "Клон": Аналіз даних
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import base64
import os

st.set_page_config(
    page_title='Серіал "Клон": Аналіз даних',
    page_icon="🌙",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv("oclone_final.csv")
    df["ep_index"] = range(1, len(df) + 1)
    return df

df = load_data()

@st.cache_data
def get_image_data_url(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = path.split(".")[-1].lower()
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{encoded}"

# Загружаем картинки персонажей (положи их в папку проекта)
jade_img = get_image_data_url("jade.jpg")        # фото Жади
leo_img = get_image_data_url("leo.jpeg")          # фото Лео
zoraide_img = get_image_data_url("zoraide.jpg")  # фото Зораиде
cup_img = get_image_data_url("cup.jpg")          # картинка чашки
silomer_img = get_image_data_url("silomer.png")

st.title('🌙 Серіал "Клон": Аналіз даних')
st.markdown(
    "Аналіз бразильської теленовели **«Клон»** (2001-2002, 221 серія). "
    "Усі метрики зібрані вручну за переказами серій."
)
st.divider()

# === СЕКЦИЯ 1: ЖАДИ vs ЛЕО ===
st.header("1. Жаді VS Лео: їх втечі протягом серіалу")
st.markdown(
    """
    Жаді весь серіал тікає до Лукаса. Лео, його клон, народжений через 20 років, 
    теж тікає: спочатку дитиною від Деузи до Альб’єрі, потім юнаком у Марокко 
до тієї ж Жаді. Дві історії втеч, розділені поколінням.
    """
)

df["jade_cum"] = df["jade_escapes"].cumsum()
df["leo_cum"] = df["leo_escapes"].cumsum()

# Маленькие фото персонажей рядом с легендой (через колонки)
col_legend, col_chart = st.columns([1, 5])

with col_legend:
    if jade_img:
        st.markdown(
            f'<div style="text-align:center;"><img src="{jade_img}" '
            f'style="width:80px;height:80px;border-radius:50%;object-fit:cover;'
            f'border:3px solid #D2691E;"/><br>'
            f'<b style="color:#D2691E;">Жаді</b></div>',
            unsafe_allow_html=True,
        )
    st.write("")
    if leo_img:
        st.markdown(
            f'<div style="text-align:center;"><img src="{leo_img}" '
            f'style="width:80px;height:80px;border-radius:50%;object-fit:cover;'
            f'border:3px solid #4682B4;"/><br>'
            f'<b style="color:#4682B4;">Лео</b></div>',
            unsafe_allow_html=True,
        )

with col_chart:
    chart_placeholder = st.empty()

    if st.button("▶ Запуск", type="primary", key="start_jade_leo"):
        step = 3
        for i in range(1, len(df) + 1, step):
            sub = df.iloc[:i]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sub["ep_index"], y=sub["jade_cum"],
                mode="lines+markers", name="Жаді",
                line=dict(color="#D2691E", width=3),
                marker=dict(size=4),
            ))
            fig.add_trace(go.Scatter(
                x=sub["ep_index"], y=sub["leo_cum"],
                mode="lines+markers", name="Лео",
                line=dict(color="#4682B4", width=3),
                marker=dict(size=4),
            ))
            fig.update_layout(
                xaxis=dict(title="Эпізод", range=[0, len(df) + 5]),
                yaxis=dict(title="Накопичені втечі", range=[0, max(df["jade_cum"].max(), df["leo_cum"].max()) + 3]),
                height=450, margin=dict(l=40, r=40, t=20, b=40),
                legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
                template="simple_white",
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)
        st.success(
            f"Финал: **Жаді втікла {df['jade_escapes'].sum()} разів**, "
            f"**Лео — {df['leo_escapes'].sum()} разів**."
        )
    else:
        fig_empty = go.Figure()
        fig_empty.update_layout(
            xaxis=dict(title="Эпізод", range=[0, len(df) + 5]),
            yaxis=dict(title="Накопичені втечі", range=[0, max(df["jade_cum"].max(), df["leo_cum"].max()) + 3]),
            height=450, margin=dict(l=40, r=40, t=20, b=40),
            template="simple_white",
        )
        chart_placeholder.plotly_chart(fig_empty, use_container_width=True)
        st.info("Натисни ▶ Запуск, щоб побачити гонку втеч.")

st.divider()

# === СЕКЦИЯ 2: СИЛОМЕР АЛИ ===

st.header("2. Барометр Алі: тиск дяди-диктатора на Жаді")
st.markdown(
    """
    Дядя Алі — головний носій патриархального контролю в родині. Кожен раз,
    коли він погрожує прокляттям, забороняє Жаді виходити, тягне її з руїн
    або свариться за непослухання, «барометр» отримує оцінку.
    Всього за серіал — **30 балів тиску.**
    """
)

total_ali = int(df["ali_meter"].sum())

# Координаты шкалы на картинке силомера (1024×1536)
IMG_W, IMG_H = 1024, 1500
SCALE_BOTTOM_Y = 1205
SCALE_TOP_Y = 500
SCALE_CENTER_X = 500
SCALE_WIDTH = 165

def render_silomer(fill_value, max_value=30):
    fill_frac = fill_value / max_value if max_value > 0 else 0
    fill_y_top = SCALE_BOTTOM_Y - (SCALE_BOTTOM_Y - SCALE_TOP_Y) * fill_frac

    fig = go.Figure()
    if silomer_img:
        fig.add_layout_image(
            dict(
                source=silomer_img,
                xref="x", yref="y",
                x=0, y=0,
                sizex=IMG_W, sizey=IMG_H,
                sizing="stretch",
                opacity=1.0,
                layer="below",
            )
        )
    fig.add_shape(
        type="rect",
        x0=SCALE_CENTER_X - SCALE_WIDTH/2,
        y0=fill_y_top,
        x1=SCALE_CENTER_X + SCALE_WIDTH/2,
        y1=SCALE_BOTTOM_Y,
        fillcolor="rgba(220, 50, 50, 0.7)",
        line=dict(width=0),
        layer="above",
    )
    fig.update_xaxes(visible=False, range=[0, IMG_W])
    fig.update_yaxes(visible=False, range=[IMG_H, 0], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        height=400,
        width=270,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig

if "ali_hit" not in st.session_state:
    st.session_state.ali_hit = False

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    placeholder_ali = st.empty()
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        if st.button("🔨 УДАР!", type="primary", key="hit_ali", use_container_width=True):
            st.session_state.ali_hit = True

if st.session_state.ali_hit:
    for v in range(0, total_ali + 1, 3):
        fig = render_silomer(v, max_value=total_ali)
        placeholder_ali.plotly_chart(fig, use_container_width=False)
        time.sleep(0.01)
    with col2:
        st.success(f"Всього: **{total_ali} балів** за {len(df)} серій.")
        if st.button("↺ Заново", key="reset_ali"):
            st.session_state.ali_hit = False
            st.rerun()
else:
    fig = render_silomer(0, max_value=total_ali)
    placeholder_ali.plotly_chart(fig, use_container_width=False)

# === СЕКЦИЯ 3: ГАДАНИЯ ЗОРАИДЕ ===
st.header("3. Зораїде і її 5 передбачень на кофейній гущі")

col_z_img, col_z_text = st.columns([1, 4])
with col_z_img:
    if zoraide_img:
        st.markdown(
            f'<div style="text-align:center;"><img src="{zoraide_img}" '
            f'style="width:120px;height:120px;border-radius:50%;object-fit:cover;'
            f'border:3px solid #8B4513;"/><br>'
            f'<b>Зораиде</b></div>',
            unsafe_allow_html=True,
        )
with col_z_text:
   st.markdown(
    """
    Служниця Зораїде ворожить Жаді на кавовій гущі п’ять разів за весь серіал.
    Кожне передбачення звучить туманно — про "дві зустрічі з долею",
    "тінь, що відділиться від людини", "камінь, який повернеться".
    До фіналу **усі п’ять передбачень здійснилися**. Точність — **100%**.

    *Натисни на чашку, щоб побачити ворожіння.*
    """
)
# Дані про ворожіння
predictions = [
    {"ep": 8, "text": "Ти зустрінеш двох: один — твоя доля, інший — її тінь"},
    {"ep": 24, "text": "Дзеркало покаже тобі твоє минуле і твоє майбутнє в одному обличчі"},
    {"ep": 49, "text": "Камінь повернеться до тебе, коли минуле зустріне майбутнє"},
    {"ep": 95, "text": "Тінь відділиться від людини, і ти не розрізниш, хто з них справжній"},
    {"ep": 167, "text": "Минуле і майбутнє зіллються, як дві ріки, і тобі доведеться обирати"},
]
# CSS для переворота чашек
flip_css = """
<style>
.cup-container {
    perspective: 1000px;
    width: 100%;
    margin: 10px 0;
}
.cup-card {
    width: 100%;
    aspect-ratio: 1 / 1;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.8s;
    cursor: pointer;
}
.cup-card.flipped {
    transform: rotateY(180deg);
}
.cup-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 10px;
    box-sizing: border-box;
    text-align: center;
}
.cup-front {
    background: #f5e6d3;
    border: 2px solid #8B4513;
}
.cup-front img {
    width: 80%;
    height: 80%;
    object-fit: contain;
}
.cup-front .ep-label {
    position: absolute;
    top: 6px;
    left: 50%;
    transform: translateX(-50%);
    background: #8B4513;
    color: white;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}
.cup-back {
    background: #fff8e7;
    border: 2px solid #8B4513;
    transform: rotateY(180deg);
}
.cup-back .prediction-text {
    font-size: 13px;
    font-style: italic;
    color: #3d2817;
    line-height: 1.3;
}
.cup-back .check {
    margin-top: 8px;
    color: #2e7d32;
    font-weight: bold;
    font-size: 14px;
}
</style>
"""

# JS для клика по чашке (переворот)
flip_js = """
<script>
document.addEventListener('click', function(e) {
    var card = e.target.closest('.cup-card');
    if (card) {
        card.classList.toggle('flipped');
    }
});
</script>
"""

# Строим HTML для 5 чашек в ряд
cups_html = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;">'
for p in predictions:
    cup_face_img = f'<img src="{cup_img}"/>' if cup_img else '<div style="font-size:60px;">☕</div>'
    cups_html += f"""
    <div class="cup-container">
        <div class="cup-card">
            <div class="cup-face cup-front">
                <span class="ep-label">Епізод {p['ep']}</span>
                {cup_face_img}
            </div>
            <div class="cup-face cup-back">
                <div class="prediction-text">«{p['text']}»</div>
                <div class="check">✓ збулось</div>
            </div>
        </div>
    </div>
    """
cups_html += '</div>'

st.components.v1.html(flip_css + cups_html + flip_js, height=280)

st.markdown(
    """
    <div style="text-align:center; padding:20px; background:#fff8e7;
                border-radius:12px; margin-top:20px; border:2px solid #8B4513;">
        <h2 style="margin:0; color:#3d2817;">Точність гадалки: <b>100%</b></h2>
        <p style="margin:8px 0 0; color:#3d2817;">
            5 передбачень із 5 збулися к фіналу серіала.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
