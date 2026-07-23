import numpy as np
import pandas as pd
import plotly.express as px

# Imports for Stats & AI
from scipy import stats
import streamlit as st

# Optional OpenAI import
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Set page config
st.set_page_config(
    page_title="A/B Test Decision Engine", page_icon="📊", layout="wide"
)

st.title("📊 A/B Test Analyzer & AI Decision Copilot")
st.markdown(
    "Translate raw experimental metrics into actionable product deployment decisions & AI-driven next steps."
)

# Sidebar Options
st.sidebar.header("1. Data Source Setup")
data_source = st.sidebar.radio(
    "Choose Data Input", ["Simulate Sample Data", "Upload CSV File"]
)

alpha = st.sidebar.slider(
    "Significance Level (α)",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01,
)
min_sample_size = st.sidebar.number_input(
    "Minimum Required Sample Size per Variant", value=1000, step=100
)

# AI Sidebar Config
st.sidebar.header("2. AI Copilot Setup")
openai_api_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password")

# Data Prep
df = None

if data_source == "Simulate Sample Data":
    st.sidebar.subheader("Simulation Settings")
    n_control = st.sidebar.number_input("Control Sample Size", value=1200)
    cr_control = st.sidebar.slider("Control Conversion Rate", 0.01, 0.50, 0.10)

    n_variant = st.sidebar.number_input("Variant Sample Size", value=1250)
    cr_variant = st.sidebar.slider("Variant Conversion Rate", 0.01, 0.50, 0.13)

    control_conv = np.random.binomial(1, cr_control, n_control)
    variant_conv = np.random.binomial(1, cr_variant, n_variant)

    df_control = pd.DataFrame({"group": "Control", "converted": control_conv})
    df_variant = pd.DataFrame({"group": "Variant", "converted": variant_conv})
    df = pd.concat([df_control, df_variant], ignore_index=True)

else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "group" not in df.columns or "converted" not in df.columns:
            st.error("CSV must contain 'group' and 'converted' columns.")
            df = None

if df is not None:
    summary = (
        df.groupby("group")["converted"]
        .agg(sample_size="count", conversions="sum", conversion_rate="mean")
        .reset_index()
    )

    control_data = summary[summary["group"] == "Control"].iloc[0]
    variant_data = summary[summary["group"] == "Variant"].iloc[0]

    # Metrics Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Control Rate", f"{control_data['conversion_rate']:.2%}")
    col2.metric("Variant Rate", f"{variant_data['conversion_rate']:.2%}")

    lift = (
        variant_data["conversion_rate"] - control_data["conversion_rate"]
    ) / control_data["conversion_rate"]
    col3.metric("Relative Lift", f"{lift:+.2%}")

    st.markdown("---")

    # Statistical Test
    contingency_table = [
        [
            control_data["conversions"],
            control_data["sample_size"] - control_data["conversions"],
        ],
        [
            variant_data["conversions"],
            variant_data["sample_size"] - variant_data["conversions"],
        ],
    ]
    chi2, p_value, dof, _ = stats.chi2_contingency(contingency_table)

    underpowered = (
        control_data["sample_size"] < min_sample_size
        or variant_data["sample_size"] < min_sample_size
    )

    # Decision Engine
    if underpowered:
        decision = "INCONCLUSIVE: Low Sample Size"
        decision_color = "orange"
        recommendation = "Do not ship yet. The sample size is below the required statistical threshold."
    elif p_value < alpha and lift > 0:
        decision = "SHIP IT: Statistically Significant Positive Lift"
        decision_color = "green"
        recommendation = f"The variant outperformed control with a relative lift of {lift:.2%} (p-value: {p_value:.4f} < α: {alpha})."
    elif p_value < alpha and lift < 0:
        decision = "KILL IT: Statistically Significant Negative Impact"
        decision_color = "red"
        recommendation = f"The variant degraded the key metric by {lift:.2%} (p-value: {p_value:.4f} < α: {alpha}). Roll back changes."
    else:
        decision = "DO NOT SHIP: No Significant Difference"
        decision_color = "gray"
        recommendation = f"The observed difference is not statistically significant (p-value: {p_value:.4f} ≥ α: {alpha})."

    # Render Memo
    st.subheader("📝 Product Decision Memo")
    st.markdown(
        f"""
    <div style="padding: 15px; border-radius: 8px; border: 2px solid {decision_color}; margin-bottom: 20px;">
        <h3 style="color: {decision_color}; margin: 0;">Recommendation: {decision}</h3>
        <p style="margin-top: 10px; font-size: 16px;">{recommendation}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Visualization & Diagnostic
    col_left, col_right = st.columns(2)
    with col_left:
        fig = px.bar(
            summary,
            x="group",
            y="conversion_rate",
            color="group",
            text_auto=".2%",
            title="Conversion Rate Comparison",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        diag_df = pd.DataFrame(
            {
                "Metric": [
                    "Control Sample Size",
                    "Variant Sample Size",
                    "p-value",
                    "Significance Threshold (α)",
                    "Statistically Significant?",
                ],
                "Value": [
                    f"{control_data['sample_size']:,}",
                    f"{variant_data['sample_size']:,}",
                    f"{p_value:.4f}",
                    f"{alpha}",
                    "Yes" if p_value < alpha else "No",
                ],
            }
        )
        st.dataframe(diag_df, hide_index=True, use_container_width=True)

    st.markdown("---")

    # AI PM Copilot Section
    st.subheader("🤖 AI Product Manager Copilot")

    if st.button("Generate Strategic Next Steps"):
        if openai_api_key and HAS_OPENAI:
            client = OpenAI(api_key=openai_api_key)
            prompt = f"""
            You are a Senior Product Manager at a tech company evaluating an A/B test result.
            
            Experiment Summary:
            - Control Conversion Rate: {control_data['conversion_rate']:.2%} (N={control_data['sample_size']})
            - Variant Conversion Rate: {variant_data['conversion_rate']:.2%} (N={variant_data['sample_size']})
            - Relative Lift: {lift:+.2%}
            - p-value: {p_value:.4f} (Alpha: {alpha})
            - Primary Decision: {decision}
            
            Provide 3 actionable, strategic next steps for the Product Team. 
            Format as bullet points with bold headings. Focus on post-experiment actions (e.g., user research, segmentation, follow-up tests, rollout strategies).
            """
            with st.spinner("Analyzing experiment results with AI..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error calling OpenAI API: {e}")
        else:
            # Fallback mock AI output if no API key is entered
            st.info("💡 **Demo AI Output** (Enter an OpenAI API Key in the sidebar for live AI insights):")
            if "SHIP IT" in decision:
                st.markdown(
                    """
                * **1. Phased 100% Rollout:** Begin a staged rollout to 100% of users over 3 days while monitoring guardrail metrics (e.g., latency, error rates, churn).
                * **2. Segmented Deep-Dive:** Slice conversion data by user demographic or device type to identify where the variant yielded the strongest impact.
                * **3. Formulate Iterative Follow-Up:** Hypothesis-test why the change succeeded to design the next optimization sprint.
                """
                )
            else:
                st.markdown(
                    """
                * **1. Qualitative User Research:** Conduct user session replays or interviews to understand why users did not convert on the variant.
                * **2. Behavioral Segmentation:** Analyze whether specific high-intent cohorts responded positively even if the overall test was neutral/negative.
                * **3. Formulate Alternative Hypothesis:** Re-evaluate the core user pain point and iterate on a second variant test rather than deploying to production.
                """
                )