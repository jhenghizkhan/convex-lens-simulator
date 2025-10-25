import streamlit as st
import matplotlib.pyplot as plt

# --- 1. Lens Parameters ---
LENS_X = 0
LENS_HEIGHT = 15
PRINCIPAL_AXIS_Y = 0

def draw_lens_and_axis(f):
    """Draws the principal axis and the convex lens symbol."""
    
    plt.axhline(PRINCIPAL_AXIS_Y, color='black', linestyle='-', linewidth=0.5)

    # Lens Line
    plt.plot([LENS_X, LENS_X], [-LENS_HEIGHT/2, LENS_HEIGHT/2], 'b-', linewidth=2)
    plt.plot([LENS_X], [LENS_HEIGHT/2], marker='^', color='blue', markersize=8)
    plt.plot([LENS_X], [-LENS_HEIGHT/2], marker='v', color='blue', markersize=8)
    
    # Mark Focal Points (F1, 2F1, F2, 2F2)
    plt.plot(-f, PRINCIPAL_AXIS_Y, 'ro', markersize=4)
    plt.text(-f, -1.5, r'$F_1$', fontsize=10, color='red')
    plt.plot(-2*f, PRINCIPAL_AXIS_Y, 'go', markersize=4)
    plt.text(-2*f, -1.5, r'$2F_1$', fontsize=10, color='green')
    
    plt.plot(f, PRINCIPAL_AXIS_Y, 'ro', markersize=4)
    plt.text(f, -1.5, r'$F_2$', fontsize=10, color='red')
    plt.plot(2*f, PRINCIPAL_AXIS_Y, 'go', markersize=4)
    plt.text(2*f, -1.5, r'$2F_2$', fontsize=10, color='green')
    
    plt.text(0.5, 0.5, '$C$', fontsize=12)


def draw_ray_diagram(u, h_o, f):
    """Draws the complete ray diagram."""

    try:
        # Physics Calculation
        v = 1 / (1/f + 1/u)
        h_i = -v * h_o / u
    except ZeroDivisionError:
        v = float('inf')
        h_i = float('inf')

    # --- 2. Setup Plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Convex Lens Ray Tracing Simulation (محاكاة العدسة المحدبة)")
    ax.set_xlabel("Distance (cm)")
    ax.set_ylabel("Height (cm)")
    ax.grid(True, linestyle=':', alpha=0.5)

    draw_lens_and_axis(f)

    # --- 3. Draw Object ---
    plt.plot([u, u], [PRINCIPAL_AXIS_Y, h_o], 'm-', linewidth=3)
    plt.plot([u], [h_o], marker='^', color='purple', markersize=8)
    plt.text(u-1.5, h_o+0.5, 'Object (جسم)', color='purple', fontsize=10)

    # --- 4. Draw Image ---
    image_color = 'c'
    if abs(v) < 100:
        if v > 0:
            line_style = '-'
            image_type = "REAL, INVERTED (حقيقي، مقلوب)"
        else:
            line_style = '--'
            image_type = "VIRTUAL, ERECT (وهمي، معتدل)"
            
        plt.plot([v, v], [PRINCIPAL_AXIS_Y, h_i], image_color + line_style, linewidth=3)
        plt.plot([v], [h_i], marker='^', color=image_color, markersize=8)
        plt.text(v+0.5, h_i+0.5, 'Image (صورة)', color='c', fontsize=10)

    else:
        image_type = "Image at INFINITY (صورة عند اللانهاية)"
        
    # --- 5. Draw Ray Tracing Lines (Simplified for display) ---
    plt.plot([u, LENS_X], [h_o, h_o], 'b-', linewidth=1.5, alpha=0.7) # Parallel Ray
    if abs(v) < 100:
        plt.plot([LENS_X, v], [h_o, h_i], 'b-', linewidth=1.5, alpha=0.7)
    
    plt.plot([u, v], [h_o, h_i], 'g-', linewidth=1.5, alpha=0.7) # Central Ray
    
    if u < -f:
        y_hit = h_o - (h_o/u) * (-u + f)
        plt.plot([u, LENS_X], [h_o, y_hit], 'r-', linewidth=1.5, alpha=0.7) # Focal Ray Incoming
        if abs(v) < 100:
            plt.plot([LENS_X, v], [y_hit, h_i], 'r-', linewidth=1.5, alpha=0.7) # Focal Ray Outgoing

    # --- 6. Final Plot Adjustments ---
    max_dist = max(abs(u), abs(v), 2*f) * 1.5
    plt.xlim(-max_dist, max_dist)
    max_height = max(abs(h_o), abs(h_i), LENS_HEIGHT/2) * 1.5
    plt.ylim(-max_height, max_height)
    
    # --- 7. Display Results in Streamlit ---
    st.pyplot(fig)
    
    if abs(v) < 100:
        st.subheader("Image Properties (خصائص الصورة):")
        st.markdown(f"""
        - **Image Location ($v$):** **{v:.2f} cm** - **Image Height ($h_i$):** **{h_i:.2f} cm**
        - **Image Type (نوع الصورة):** **{image_type}**
        - **Magnification (التكبير):** **{-v/u:.2f}**
        """)
    else:
        st.warning(f"Image is formed at infinity. (تتشكل الصورة عند اللانهاية.)")


# --- 8. Streamlit App Interface ---

st.title("Convex Lens Ray Diagram Simulator 🔬")
st.markdown("Use the sliders to adjust the **Focal Length** and **Object Position** to see how the image changes. (استخدم أشرطة التمرير لضبط البعد البؤري وموقع الجسم لمعرفة كيف تتغير الصورة.)")

st.sidebar.header("Controls (أدوات التحكم)")

# Focal Length control
f_input = st.sidebar.slider("1. Focal Length (f) [البعد البؤري]:", min_value=5, max_value=20, value=10, step=1)

# Object Height control
h_o_input = st.sidebar.slider("2. Object Height ($h_o$) [ارتفاع الجسم]:", min_value=1.0, max_value=10.0, value=5.0,