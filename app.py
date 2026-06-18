import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import base64
from io import BytesIO

st.set_page_config(page_title="MorphGuard", page_icon="🛡️", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

/* ── App background ── */
.stApp { background: #EEF0F8 !important; }

/* ── Hide chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.1rem 1.3rem 1.5rem !important;
    max-width: 100% !important;
}

/* ════════════════════════════════════════
   TOP HEADER
════════════════════════════════════════ */
.top-header {
    background: #ffffff;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 13px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.brand-wrap { display:flex; align-items:center; gap:10px; }
.brand-icon {
    width:40px; height:40px; border-radius:12px;
    background:linear-gradient(135deg,#5865f2,#818cf8);
    display:flex; align-items:center; justify-content:center;
    font-size:20px;
}
.brand-title { font-size:16px; font-weight:800; color:#1e293b; margin:0; line-height:1.2; }
.brand-sub   { font-size:11px; color:#94a3b8; margin:0; }
.page-title  { font-size:24px; font-weight:800; color:#1e293b; text-align:center; margin:0; }
.page-sub    { font-size:11px; color:#94a3b8; text-align:center; margin:0; }
.status-badge {
    background:#dcfce7; color:#16a34a;
    font-size:12px; font-weight:700;
    padding:7px 16px; border-radius:999px;
    border:1px solid #bbf7d0;
    white-space:nowrap;
}

/* ════════════════════════════════════════
   UNIVERSAL CARD
════════════════════════════════════════ */
.card {
    background: #ffffff;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 16px 20px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.card-title {
    font-size: 10px;
    font-weight: 700;
    color: #9ca3af;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin: 0 0 12px 0;
    line-height: 1;
    position:relative;
    top:-22px;
    left: 22px;        
}

/* ════════════════════════════════════════
   FIXED IMAGE CONTAINER
════════════════════════════════════════ */
.img-frame {
    width: 100%;
    height: 300px;
    border-radius: 14px;
    border: 1.5px solid #e5e7eb;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin-bottom: 12px;
}
.img-frame img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 12px;
}
.img-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: #cbd5e1;
}
.img-placeholder span { font-size: 40px; }
.img-placeholder p    { font-size: 12px; font-weight: 500; color: #94a3b8; margin: 0; }

/* ── File uploader styling ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #c7d2fe !important;
    border-radius: 12px !important;
    background: #f5f7ff !important;
    padding: 6px !important;
    margin-bottom: 10px !important;
}
[data-testid="stFileUploader"] section { padding: 6px 0 !important; }
[data-testid="stFileUploader"] label {
    visibility:hidden !important;
    height:0px !important;
}
[data-testid="stFileUploader"] small {
    display:none !important;
}

.stFileUploader{
    margin-top:-80px;
}                        
[data-testid="stFileUploader"] button {
    background:#5865f2 !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    font-weight:600 !important;
}            
/* ── Analyze Again button ── */
.stButton > button {
    background: linear-gradient(135deg, #5865f2, #818cf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 11px !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    transition: opacity .2s !important;
    box-shadow: 0 3px 10px rgba(88,101,242,0.35) !important;
}
.stButton > button:hover { opacity: .88 !important; }

/* ── Tip box ── */
.tip-box {
    background: #fffbeb; border: 1px solid #fde68a;
    border-radius: 12px; padding: 9px 13px;
    font-size: 12px; color: #92400e; margin-top: 10px;
}

/* ════════════════════════════════════════
   PREDICTION – TOP ROW (equal height)
════════════════════════════════════════ */
.pred-row {
    display: grid;
    grid-template-columns: 1fr 1.5fr 1fr;
    gap: 12px;
    align-items: stretch;
    margin-bottom: 12px;
}

/* Verdict card */
.verdict-card {
    border-radius: 16px;
    padding: 16px 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    gap: 6px;
}
.verdict-real  { background:#f0fdf4; border:1.5px solid #86efac; }
.verdict-morph { background:#fff1f2; border:1.5px solid #fca5a5; }
.verdict-icon  { font-size:28px; line-height:1; }
.verdict-label {
    font-size: 14px; font-weight: 800; text-align: center;
    margin: 0; line-height: 1.3;
}
.verdict-real  .verdict-label { color: #15803d; }
.verdict-morph .verdict-label { color: #b91c1c; }
.verdict-sub {
    font-size: 10px; color: #94a3b8; text-align: center; margin: 0;
}

/* Donut wrapper */
.donut-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    padding: 4px;
}

/* Score card */
.score-card {
    background: linear-gradient(160deg, #5865f2 0%, #818cf8 100%);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    gap: 4px;
    padding: 14px;
}
.score-label { font-size: 11px; color: rgba(255,255,255,.75); font-weight: 600; letter-spacing:.06em; text-transform:uppercase; }
.score-value { font-size: 38px; font-weight: 900; color: #ffffff; line-height:1.1; }
.score-sub   { font-size: 11px; color: rgba(255,255,255,.6); }

/* ── Probability cards ── */
.prob-row { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:10px; }
.prob-card {
    border-radius: 14px; padding: 13px 16px;
}
.prob-card-real  { background:#f0fdf4; border:1px solid #bbf7d0; }
.prob-card-morph { background:#fff1f2; border:1px solid #fecaca; }
.prob-label { font-size:11px; font-weight:600; color:#6b7280; margin-bottom:4px; }
.prob-bar-track {
    height: 5px; border-radius: 99px;
    background: #e5e7eb; margin: 6px 0;
    overflow: hidden;
}
.prob-bar-fill-real  { height:100%; border-radius:99px; background:linear-gradient(90deg,#4ade80,#22c55e); }
.prob-bar-fill-morph { height:100%; border-radius:99px; background:linear-gradient(90deg,#f87171,#ef4444); }
.prob-value-real  { font-size:22px; font-weight:800; color:#16a34a; }
.prob-value-morph { font-size:22px; font-weight:800; color:#dc2626; }

/* ── Raw score strip ── */
.raw-score {
    background:#f8fafc; border:1px solid #e5e7eb;
    border-radius:10px; padding:8px 14px;
    font-size:12px; color:#6b7280;
}

/* ════════════════════════════════════════
   PROCESSING STEPS
════════════════════════════════════════ */
.step-item {
    display:flex; align-items:center; gap:12px;
    background:#f8fafc; border:1px solid #e5e7eb;
    border-radius:14px; padding:11px 13px;
    margin-bottom:9px;
}
.step-icon {
    width:38px; height:38px; border-radius:11px;
    display:flex; align-items:center; justify-content:center;
    font-size:17px; flex-shrink:0;
}
.step-name { font-size:13px; font-weight:700; color:#1e293b; }
.step-desc { font-size:11px; color:#94a3b8; margin-top:1px; }

/* ════════════════════════════════════════
   MODEL DETAIL GRID
════════════════════════════════════════ */
.detail-grid {
    display:grid; grid-template-columns:1fr 1fr;
    gap:10px; margin-top:4px;
}
.detail-cell {
    background:#f8fafc; border:1px solid #e5e7eb;
    border-radius:12px; padding:11px 13px;
}
.detail-key { font-size:10px; color:#9ca3af; font-weight:600; text-transform:uppercase; letter-spacing:.06em; }
.detail-val { font-size:15px; font-weight:800; color:#1e293b; margin-top:3px; }

/* ── Warning strip ── */
.warn-strip {
    background:#fffbeb; border:1px solid #fde68a;
    border-radius:12px; padding:10px 14px;
    font-size:12px; color:#92400e;
    font-weight:500; margin-top:12px;
}

/* ════════════════════════════════════════
   PLOTLY – clean embedded look
════════════════════════════════════════ */
.js-plotly-plot .plotly { border-radius:12px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MODEL LOADER  (unchanged logic)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_my_model():
    try:
        from keras.models import load_model
        return load_model("model/final_deployment_model.keras", compile=False)
    except Exception:
        return None

model = load_my_model()


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER – convert PIL image → base64 data-URI for fixed container
# ─────────────────────────────────────────────────────────────────────────────
def pil_to_b64(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ─────────────────────────────────────────────────────────────────────────────
#  TOP HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-header">
  <div class="brand-wrap">
    <div class="brand-icon">🛡️</div>
    <div>
      <p class="brand-title">MorphGuard</p>
      <p class="brand-sub">AI-Powered Face Morph Detection</p>
    </div>
  </div>
  <div>
    <p class="page-title">Face Morph Detection</p>
    <p class="page-sub">Accurate &bull; Reliable &bull; Intelligent</p>
  </div>
  <div class="status-badge">🟢 System Active</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN 3-COLUMN ROW
# ─────────────────────────────────────────────────────────────────────────────
left, center, right = st.columns([1.15, 1.85, 1.0], gap="medium")


# ══════════════════════════════════════════════════════════════════════════════
#  LEFT – Input Image
# ══════════════════════════════════════════════════════════════════════════════
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📁 Input Image</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    image = None

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        b64 = pil_to_b64(image)
        st.markdown(
            f'<div class="img-frame"><img src="data:image/png;base64,{b64}" /></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("""
        <div class="img-frame">
          <div class="img-placeholder">
            <span>🖼️</span>
            <p>No image uploaded</p>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close card

    st.button("🔄 Analyze Again", use_container_width=True)
    st.markdown(
        '<div class="tip-box">💡 Upload a clear, front-facing image for best results.</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  CENTER – Prediction Result
# ══════════════════════════════════════════════════════════════════════════════
with center:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔍 Prediction Result</div>', unsafe_allow_html=True)

    # ── Run inference ──────────────────────────────────────────────────────
    if uploaded_file and model is not None and image is not None:
        img_arr = np.array(image.resize((224, 224))) / 255.0
        img_arr = np.expand_dims(img_arr, axis=0)
        pred      = float(model.predict(img_arr, verbose=0)[0][0])
        real_pct  = pred * 100
        morph_pct = (1 - pred) * 100
        confidence = max(real_pct, morph_pct)
        is_real    = pred >= 0.5

        # ── Top row: verdict | donut | score ──────────────────────────────
        if is_real:
            verdict_html = f"""
            <div class="verdict-card verdict-real">
              <div class="verdict-icon">✅</div>
              <p class="verdict-label">REAL<br>DETECTED</p>
              <p class="verdict-sub">Face appears genuine</p>
            </div>"""
            c_real, c_morph = "#22c55e", "#d1d5db"
        else:
            verdict_html = f"""
            <div class="verdict-card verdict-morph">
              <div class="verdict-icon">⚠️</div>
              <p class="verdict-label">MORPH<br>DETECTED</p>
              <p class="verdict-sub">Manipulation suspected</p>
            </div>"""
            c_real, c_morph = "#d1d5db", "#ef4444"

        # Donut chart
        fig_donut = go.Figure(data=[go.Pie(
            values=[real_pct, morph_pct],
            labels=["Real", "Morph"],
            hole=0.70,
            marker=dict(colors=[c_real, c_morph], line=dict(color="#ffffff", width=2)),
            textinfo="none",
            hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
            sort=False,
        )])
        fig_donut.update_layout(
            height=210,
            margin=dict(l=8, r=8, t=8, b=30),
            showlegend=True,
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.08,
                font=dict(
                    size=11,
                    family="Inter"
                )
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        score_html = f"""
        <div class="score-card">
          <div class="score-label">Confidence</div>
          <div class="score-value">{confidence:.1f}<span style="font-size:20px">%</span></div>
          <div class="score-sub">Prediction score</div>
        </div>"""

        # Render top row via HTML grid + Streamlit chart injected between
        c1, c2, c3 = st.columns([1,1.5,1])

        with c1:
            st.markdown(verdict_html, unsafe_allow_html=True)

        with c2:
            st.plotly_chart(
                fig_donut,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with c3:
            st.markdown(score_html, unsafe_allow_html=True)
        # Extra spacer so prob cards render below the tallest row element
        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

        # ── Probability cards ──────────────────────────────────────────────
        bar_real  = min(real_pct,  100)
        bar_morph = min(morph_pct, 100)
        st.markdown(f"""
        <div class="prob-row">
          <div class="prob-card prob-card-real">
            <div class="prob-label">Real Face Probability</div>
            <div class="prob-bar-track"><div class="prob-bar-fill-real" style="width:{bar_real:.1f}%"></div></div>
            <div class="prob-value-real">{real_pct:.2f}%</div>
          </div>
          <div class="prob-card prob-card-morph">
            <div class="prob-label">Morph Face Probability</div>
            <div class="prob-bar-track"><div class="prob-bar-fill-morph" style="width:{bar_morph:.1f}%"></div></div>
            <div class="prob-value-morph">{morph_pct:.2f}%</div>
          </div>
        </div>
        <div class="raw-score">🔢 Raw Prediction Score: <strong>{pred:.6f}</strong></div>
        """, unsafe_allow_html=True)

    # ── Empty / no-model state ─────────────────────────────────────────────
    else:
        fig_empty = go.Figure(data=[go.Pie(
            values=[1], hole=0.70,
            marker=dict(colors=["#f1f5f9"]),
            textinfo="none", hoverinfo="none",
        )])
        fig_empty.update_layout(
            height=220,
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            ),
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        )

        st.markdown("""
        <div style="display:grid;grid-template-columns:1fr 1.5fr 1fr;gap:12px;align-items:stretch;margin-bottom:12px;">
          <div class="verdict-card verdict-morph">
            <div class="verdict-icon">✗</div>
            <p class="verdict-label">Prediction<br>Failed</p>
            <p class="verdict-sub">Upload an image<br>to see results</p>
          </div>
          <div class="donut-card" id="donut-slot"></div>
          <div class="score-card">
            <div class="score-label">Confidence</div>
            <div class="score-value">0<span style="font-size:20px">%</span></div>
            <div class="score-sub">Prediction score</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="prob-row">
          <div class="prob-card prob-card-real">
            <div class="prob-label">Real Face Probability</div>
            <div class="prob-bar-track"><div class="prob-bar-fill-real" style="width:0%"></div></div>
            <div class="prob-value-real">--%</div>
          </div>
          <div class="prob-card prob-card-morph">
            <div class="prob-label">Morph Face Probability</div>
            <div class="prob-bar-track"><div class="prob-bar-fill-morph" style="width:0%"></div></div>
            <div class="prob-value-morph">--%</div>
          </div>
        </div>
        <div class="raw-score">🔢 Raw Prediction Score: <strong>--</strong></div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close card


# ══════════════════════════════════════════════════════════════════════════════
#  RIGHT – Processing Steps
# ══════════════════════════════════════════════════════════════════════════════
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ Processing Steps</div>', unsafe_allow_html=True)

    steps = [
        ("📷", "#dbeafe", "Face Detection",      "Locating facial landmarks"),
        ("🧠", "#fce7f3", "Feature Extraction",   "Extracting deep features"),
        ("📊", "#ede9fe", "Pattern Analysis",     "Analyzing morphing patterns"),
        ("✅", "#dcfce7", "Morph Classification", "Final prediction processing"),
    ]
    for icon, bg, name, desc in steps:
        st.markdown(f"""
        <div class="step-item">
          <div class="step-icon" style="background:{bg}">{icon}</div>
          <div>
            <div class="step-name">{name}</div>
            <div class="step-desc">{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  BOTTOM ROW
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
b1, b2 = st.columns([3, 2], gap="medium")


# ══════════════════════════════════════════════════════════════════════════════
#  BOTTOM LEFT – Accuracy Graph
# ══════════════════════════════════════════════════════════════════════════════
with b1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    epochs    = [1, 2, 3, 4, 5, 6]
    train_acc = [0.43, 0.91, 0.94, 0.95, 0.96, 0.97]
    val_acc   = [0.90, 0.90, 0.93, 0.94, 0.95, 0.96]

    fig_acc = go.Figure()
    fig_acc.add_trace(go.Scatter(
        x=epochs, y=train_acc, mode="lines+markers", name="Train Accuracy",
        line=dict(color="#5865f2", width=2.5),
        marker=dict(size=7, color="#5865f2", line=dict(color="#fff", width=1.5)),
        fill="tozeroy", fillcolor="rgba(88,101,242,0.06)",
    ))
    fig_acc.add_trace(go.Scatter(
        x=epochs, y=val_acc, mode="lines+markers", name="Validation Accuracy",
        line=dict(color="#f97316", width=2.5),
        marker=dict(size=7, color="#f97316", line=dict(color="#fff", width=1.5)),
        fill="tozeroy", fillcolor="rgba(249,115,22,0.05)",
    ))
    fig_acc.update_layout(
        title=dict(
            text="<b>MODEL ACCURACY OVER EPOCHS</b>",
            font=dict(size=12, family="Inter", color="#374151"), x=0,
        ),
        height=320,
        margin=dict(l=4, r=4, t=40, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Epoch", tickvals=epochs,
            gridcolor="#f1f5f9", linecolor="#e5e7eb",
            tickfont=dict(size=11, family="Inter"),
        ),
        yaxis=dict(
            title="Accuracy", range=[0.3, 1.02],
            gridcolor="#f1f5f9", linecolor="#e5e7eb",
            tickfont=dict(size=11, family="Inter"),
            tickformat=".0%",
        ),
        legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.08,
        font=dict(
            size=11,
            family="Inter"
        ),
        tracegroupgap=10
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig_acc, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  BOTTOM RIGHT – Model Details
# ══════════════════════════════════════════════════════════════════════════════
with b2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🤖 Model Details &amp; Information</div>', unsafe_allow_html=True)

    details = [
        ("Model Architecture", "InceptionV3"),
        ("Accuracy",           "97.44%"),
        ("Total Images",       "2,348"),
        ("Dataset",            "Real vs Morph"),
        ("Training Epochs",    "6"),
        ("AUC Score",          "0.974"),
        ("Input Size",         "224 × 224"),
        ("Optimizer",          "Adam"),
    ]
    st.markdown('<div class="detail-grid">', unsafe_allow_html=True)
    for key, val in details:
        st.markdown(f"""
        <div class="detail-cell">
          <div class="detail-key">{key}</div>
          <div class="detail-val">{val}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-strip">
      ⚠️ Model is well-trained with high precision and strong generalization.
    </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)