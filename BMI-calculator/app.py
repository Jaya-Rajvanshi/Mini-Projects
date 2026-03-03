import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="BMI Calculator", page_icon="⚕️", layout="wide")

st.markdown(
    """
    <style>
    .bmi-app-wrapper {
        max-width: 1100px;
        margin: 0 auto;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }

    .bmi-header {
        background: rgba(20, 20, 20, 0.95);
        border-radius: 0.9rem;
        padding: 1.1rem 1.5rem 1.25rem 1.5rem;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .bmi-header-main {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .bmi-header-icon {
        font-size: 1.8rem;
        line-height: 1;
    }

    .bmi-header-text h1 {
        margin: 0;
        font-size: 1.7rem;
    }

    .bmi-header-text p {
        margin: 0.15rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.85;
    }

    .bmi-header-divider {
        margin-top: 0.9rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .bmi-content {
        margin-top: 1.6rem;
    }

    .bmi-card {
        background: rgba(20, 20, 20, 0.95);
        border-radius: 0.9rem;
        padding: 1.15rem 1.3rem 1.25rem 1.3rem;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .bmi-card + .bmi-card {
        margin-top: 1rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 0.6rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        padding-top: 0.6rem;
        padding-bottom: 0.6rem;
    }

    div[data-testid="stTable"] table {
        font-size: 0.9rem;
    }

    div[data-testid="stTable"] th,
    div[data-testid="stTable"] td {
        padding: 0.4rem 0.75rem !important;
    }

    @media (max-width: 900px) {
        .bmi-app-wrapper {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate BMI using the formula:
    BMI = weight_kg / (height_meters^2)
    """
    height_m = height_cm / 100  # convert centimeters to meters
    return weight_kg / (height_m**2)


def get_bmi_category(bmi: float) -> str:
    """
    Map a numeric BMI value to a human‑readable category.
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"


def show_bmi_category_table() -> None:
    """
    Display a simple BMI category table using st.table.
    """
    data = {
        "Category": ["Underweight", "Normal weight", "Overweight", "Obese"],
        "BMI Range": ["< 18.5", "18.5 – 24.9", "25 – 29.9", "30 and above"],
    }
    df = pd.DataFrame(data)
    st.subheader("BMI Categories")
    st.table(df)


def plot_bmi_ranges_with_user_value(bmi: float | None) -> None:
    """
    Show a small bar chart of BMI ranges and optionally mark the user's BMI.
    """
    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    # Representative values for the height of each bar (mid‑points of the ranges)
    representative_bmis = [17, 22, 27, 32]

    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(categories, representative_bmis, color=["#5DADE2", "#58D68D", "#F5B041", "#EC7063"])

    ax.set_ylabel("BMI")
    ax.set_title("BMI Ranges")

    # Optionally overlay the user's BMI as a horizontal line
    if bmi is not None:
        ax.axhline(bmi, color="black", linestyle="--", linewidth=2, label=f"Your BMI: {bmi:.2f}")
        ax.legend()

    # Show the numerical values on top of each bar for clarity
    for bar, value in zip(bars, representative_bmis):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.2, f"{value}", ha="center", va="bottom", fontsize=8)

    st.pyplot(fig)


def main() -> None:
    """
    Main entry point for the Streamlit app.
    """
    st.markdown('<div class="bmi-app-wrapper">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="bmi-header">
            <div class="bmi-header-main">
                <div class="bmi-header-icon">⚕️</div>
                <div class="bmi-header-text">
                    <h1>BMI Calculator</h1>
                    <p>Calculate your Body Mass Index</p>
                </div>
            </div>
            <div class="bmi-header-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="bmi-content">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.15, 1])

    bmi_result: float | None = None

    with left_col:
        st.markdown('<div class="bmi-card">', unsafe_allow_html=True)

        st.markdown(
            "Enter your height and weight below to calculate your BMI and see which category you fall into."
        )

        # User inputs
        height_cm = st.number_input("Height (in centimeters)", min_value=0.0, step=0.1, format="%.1f")
        weight_kg = st.number_input("Weight (in kilograms)", min_value=0.0, step=0.1, format="%.1f")

        if st.button("Calculate BMI"):
            # Basic input validation
            if height_cm <= 0 or weight_kg <= 0:
                st.error("Please enter valid positive numbers for both height and weight.")
            else:
                bmi_result = calculate_bmi(weight_kg, height_cm)
                category = get_bmi_category(bmi_result)

                # Display the result inside a styled box
                st.success(
                    f"Your BMI is **{bmi_result:.2f}**.\n\n"
                    f"This falls in the **{category}** category."
                )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="bmi-card">', unsafe_allow_html=True)
        # Show BMI category table
        show_bmi_category_table()
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="bmi-card">', unsafe_allow_html=True)
        # Show bar chart for BMI ranges, optionally overlaying the user's BMI if available
        st.subheader("BMI Range Chart")
        plot_bmi_ranges_with_user_value(bmi_result)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("Created by **Jaya Rajvanshi**")
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

