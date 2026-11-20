import streamlit as st
import streamlit.components.v1 as components
import time


def show_splash():

    if st.session_state.get("splash_completed", False):
        return

    # Hide Streamlit chrome only while the splash screen is displayed.
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"],
        header[data-testid="stHeader"],
        footer,
        [data-testid="stToolbar"] {
            display: none !important;
        }

        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMain"] > div,
        .stApp {
            background: #030611 !important;
            padding: 0 !important;
            margin: 0 !important;
            min-height: 100vh !important;
        }

        [data-testid="stMain"] {
            padding-top: 0 !important;
        }

        [data-testid="stVerticalBlock"],
        [data-testid="stElementContainer"] {
            gap: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        iframe {
            display: block !important;
            width: 100% !important;
            max-width: 100% !important;
            height: 100vh !important;
            min-height: 100vh !important;
            border: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    html = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #030611;
            font-family: Arial, Helvetica, sans-serif;
        }

        .nd-galaxy {
            position: relative;
            width: 100%;
            height: 100vh;
            min-height: 100vh;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            isolation: isolate;
            background:
                radial-gradient(ellipse at 50% 48%,
                    rgba(45, 48, 115, .55) 0%,
                    rgba(14, 20, 54, .78) 36%,
                    #030611 78%);
        }

        #nd-galaxy-canvas {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        .nd-nebula {
            position: absolute;
            z-index: 0;
            width: min(75vw, 760px);
            aspect-ratio: 1;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                rgba(124, 58, 237, .25) 0%,
                rgba(79, 70, 229, .13) 38%,
                rgba(34, 211, 238, .06) 58%,
                transparent 72%
            );
            filter: blur(38px);
            animation: nd-nebula-pulse 4s ease-in-out infinite alternate;
        }

        .nd-content {
            position: relative;
            z-index: 3;
            width: min(92%, 760px);
            text-align: center;
            padding: 24px 12px;
            animation: nd-reveal 1.25s ease both;
        }

        .nd-core {
            width: 104px;
            height: 104px;
            margin: 0 auto 27px;
            border: 1px solid rgba(255, 255, 255, .22);
            border-radius: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 61px;
            line-height: 1;
            background: linear-gradient(135deg, #7048ed 0%, #a34df2 52%, #12b9dc 100%);
            box-shadow:
                0 0 28px rgba(139, 92, 246, .58),
                0 0 85px rgba(34, 211, 238, .19),
                inset 0 1px 16px rgba(255, 255, 255, .22);
            animation: nd-core-float 3s ease-in-out infinite;
        }

        .nd-title {
            color: #fff;
            font-size: clamp(36px, 6vw, 64px);
            line-height: 1.08;
            font-weight: 850;
            letter-spacing: -2.4px;
            background: linear-gradient(
                90deg, #fff 0%, #b7c5ff 32%, #c084fc 67%, #67e8f9 100%
            );
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 20px rgba(139, 92, 246, .2));
        }

        .nd-subtitle {
            margin-top: 16px;
            color: #a3aecb;
            font-size: 12px;
            letter-spacing: 3.6px;
        }

        .nd-loader {
            width: min(250px, 72vw);
            height: 4px;
            margin: 39px auto 15px;
            overflow: hidden;
            border-radius: 20px;
            background: rgba(148, 163, 184, .19);
        }

        .nd-progress {
            width: 0;
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #6366f1, #a855f7, #22d3ee);
            box-shadow: 0 0 16px rgba(129, 140, 248, .9);
            animation: nd-loading 4s linear forwards;
        }

        .nd-loading {
            color: #9aa7c5;
            font-size: 10px;
            letter-spacing: 2.8px;
        }

        .nd-footer {
            position: absolute;
            z-index: 3;
            bottom: 20px;
            left: 0;
            width: 100%;
            text-align: center;
            color: rgba(148, 163, 184, .48);
            font-size: 9px;
            letter-spacing: 2.4px;
        }

        @keyframes nd-reveal {
            from { opacity: 0; transform: translateY(24px) scale(.98); }
            to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes nd-core-float {
            0%, 100% { transform: translateY(0) rotate(-2deg); }
            50%      { transform: translateY(-10px) rotate(2deg); }
        }

        @keyframes nd-nebula-pulse {
            from { transform: scale(.88); opacity: .65; }
            to   { transform: scale(1.08); opacity: 1; }
        }

        @keyframes nd-loading {
            from { width: 0; }
            to   { width: 100%; }
        }

        @media (max-width: 600px) {
            .nd-galaxy { min-height: 560px; }
            .nd-core {
                width: 82px;
                height: 82px;
                border-radius: 26px;
                font-size: 49px;
                margin-bottom: 23px;
            }
            .nd-title { letter-spacing: -1.5px; }
            .nd-subtitle { font-size: 9px; letter-spacing: 2px; }
            .nd-loading { font-size: 8px; letter-spacing: 1.7px; }
        }

        @media (prefers-reduced-motion: reduce) {
            .nd-content, .nd-core, .nd-nebula, .nd-progress {
                animation-duration: .01ms !important;
            }
        }
        /* FUTURISTIC TOP HEADER */

.nd-topbar {
    position: absolute;
    top: 25px;
    left: 35px;
    right: 35px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}

.nd-topbrand {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #ffffff;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.nd-topbrand-mark {
    width: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: linear-gradient(135deg,#6366f1,#a855f7);
    font-size: 22px;
}

.nd-topnote {
    padding: 10px 17px;
    background: rgba(99,102,241,.10);
    border: 1px solid rgba(129,140,248,.3);
    border-radius: 30px;
    color: #a5b4fc;
    font-size: 10px;
    letter-spacing: 1.5px;
}

.nd-topline {
    position: absolute;
    top: 78px;
    left: 35px;
    right: 35px;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(129,140,248,.5),
        transparent
    );
}

@media(max-width:600px) {
    .nd-topbar {
        left: 15px;
        right: 15px;
    }

    .nd-topnote {
        font-size: 8px;
        padding: 8px;
    }
}
    </style>
    </head>
    <body>
        <main class="nd-galaxy">
            <div class="nd-nebula"></div>
            <canvas id="nd-galaxy-canvas" aria-hidden="true"></canvas>

            <section class="nd-content">
                <div class="nd-core">✦</div>
                <div class="nd-title">NeuralDocs AI</div>
                <div class="nd-subtitle">INTELLIGENT RESEARCH ASSISTANT</div>
                <div class="nd-loader"><div class="nd-progress"></div></div>
                <div class="nd-loading">EXPLORING THE UNIVERSE OF KNOWLEDGE...</div>
            </section>

            <div class="nd-footer">POWERED BY INTELLIGENCE</div>
        </main>

        <script>
        (() => {
            const canvas = document.getElementById("nd-galaxy-canvas");
            const ctx = canvas.getContext("2d");
            if (!ctx) return;

            let width = 0;
            let height = 0;
            let dpr = 1;
            let particles = [];
            let rotation = 0;
            let animationFrame = null;

            const palette = [
                "167,139,250",
                "192,132,252",
                "103,232,249",
                "129,140,248",
                "226,232,255"
            ];

            function resize() {
                dpr = Math.min(window.devicePixelRatio || 1, 2);
                width = window.innerWidth;
                height = window.innerHeight;
                canvas.width = Math.round(width * dpr);
                canvas.height = Math.round(height * dpr);
                ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            }

            function makeParticles() {
                particles = [];
                const count = Math.min(1100, Math.max(550, Math.floor(width * height / 1050)));

                for (let i = 0; i < count; i++) {
                    const arm = Math.floor(Math.random() * 5);
                    const distance = Math.pow(Math.random(), .78);
                    const angle = arm * (Math.PI * 2 / 5)
                        + distance * 5.2
                        + (Math.random() - .5) * .85;

                    particles.push({
                        angle,
                        distance,
                        size: .45 + Math.random() * 1.65,
                        speed: .00035 + Math.random() * .0009,
                        alpha: .32 + Math.random() * .66,
                        color: palette[Math.floor(Math.random() * palette.length)]
                    });
                }
            }

            function draw() {
                ctx.clearRect(0, 0, width, height);

                const cx = width / 2;
                const cy = height / 2;
                const scale = Math.min(width, height) * .47;

                rotation += .0017;

                const glow = ctx.createRadialGradient(cx, cy, 2, cx, cy, scale);
                glow.addColorStop(0, "rgba(139,92,246,.13)");
                glow.addColorStop(.42, "rgba(79,70,229,.07)");
                glow.addColorStop(1, "rgba(3,6,17,0)");
                ctx.fillStyle = glow;
                ctx.fillRect(0, 0, width, height);

                particles.forEach(p => {
                    const angle = p.angle + rotation;
                    const radius = p.distance * scale;
                    const x = cx + Math.cos(angle) * radius;
                    const y = cy + Math.sin(angle) * radius * .52;
                    const twinkle = .72 + Math.sin(rotation * 35 + p.angle * 3) * .28;

                    ctx.beginPath();
                    ctx.arc(x, y, p.size, 0, Math.PI * 2);
                    ctx.fillStyle = `rgba(${p.color},${p.alpha * twinkle})`;
                    ctx.shadowBlur = p.size * 5;
                    ctx.shadowColor = `rgb(${p.color})`;
                    ctx.fill();
                });

                ctx.shadowBlur = 0;

                // Soft orbital energy rings around the galaxy centre.
                for (let i = 0; i < 3; i++) {
                    ctx.beginPath();
                    ctx.ellipse(
                        cx, cy,
                        scale * (.17 + i * .075),
                        scale * (.055 + i * .026),
                        rotation * (i % 2 === 0 ? 1 : -1),
                        0, Math.PI * 2
                    );
                    ctx.strokeStyle = `rgba(167,139,250,${.12 - i * .025})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }

                animationFrame = requestAnimationFrame(draw);
            }

            resize();
            makeParticles();
            draw();

            window.addEventListener("resize", () => {
                resize();
                makeParticles();
            });

            // Stop drawing when the iframe is no longer visible.
            document.addEventListener("visibilitychange", () => {
                if (document.hidden && animationFrame) {
                    cancelAnimationFrame(animationFrame);
                    animationFrame = null;
                } else if (!document.hidden && !animationFrame) {
                    draw();
                }
            });
        })();
        </script>
        <div class="nd-topbar">

    <div class="nd-topbrand">
        <span class="nd-topbrand-mark">✦</span>
        NEURALDOCS AI
    </div>

    <div class="nd-topnote">
        ✦ AI POWERED RESEARCH PLATFORM
    </div>

</div>

<div class="nd-topline"></div>
    </body>
    </html>
    """

    # Keep the splash inside the available Streamlit page area.
    components.html(
        html,
        height=1000,
        scrolling=False,
    )

    time.sleep(4)

    st.session_state["splash_completed"] = True
    st.rerun()
