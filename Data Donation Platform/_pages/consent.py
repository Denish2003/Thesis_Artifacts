import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from components.go_to_page import go_to_page
from components.ui import inline_notice, page_header

def consent_page(isModal=False):
    """Render the study consent page."""
    if isModal:
        scroll_to_here(0, key="top")

    if not st.session_state.consent:
        if st.button("⬅ Back to Home"):
            go_to_page("home")

    page_header(
        "Adult Consent Form",
        "Please read this form carefully before participating in the Princeton University research study.",
        eyebrow="Princeton University",
    )

    st.markdown("""
                **TITLE OF RESEARCH:** Emotional Risks and Ethical Challenges in AI Companionship: A Case Study of ChatGPT

                **PRINCIPAL INVESTIGATOR:** Manoel Horta Ribeiro  
                **DEPARTMENT:** Department of Computer Science  

                **Purpose of the research:**  
                The purpose of this study is to understand how people use ChatGPT in emotionally meaningful or sensitive conversations. We aim to identify patterns in these interactions that may relate to emotional support, dependence, or risks, so that future AI systems can be designed more safely and ethically.

                **Expected duration:**  
                Your participation will take approximately **10–20 minutes**, depending on the amount of conversation data you choose to review and donate.

                **Procedures:**  
                - Read this consent form and indicate your agreement  
                - Upload your ChatGPT conversation history to our secure platform  
                - Review, edit, delete, or redact any parts you do not wish to share  
                - All data is anonymized **on your device** before being submitted  
                - Submit the anonymized data and complete a brief survey

                **Withdrawing:**  
                You may decline to participate or stop at any time **before submitting** your final anonymized data.  
                Once submitted, your data **cannot be withdrawn**, because no identifiable information is collected.
                """)

    st.markdown("""
                **Risks:**  
                This study involves minimal risk; however, potential risks include:
                -   Emotional discomfort: Reviewing past conversations, especially those involving sensitive or emotional topics, may cause mild distress, embarrassment, or discomfort. You may skip any content you do not wish to review or share.
                -   Privacy risk: The main potential risk is accidental disclosure of personal or sensitive information through your conversation text. To reduce this risk, you will review your data before sharing it, and our system automatically flags many types of personal information, which will then go through manual review and will be removed.
                -   Data security risk: Although we use secure, password-protected servers and follow standard data protection practices, there is a small risk of loss of confidentiality due to unforeseen data breaches.

                **Benefits:**  
                - Insights about your ChatGPT data  
                - **$20 USD compensation** upon donating your data  
                - Contribution to safer and more ethical AI system design
                """)

    st.markdown("""
                **Confidentiality:**  
                All records from this study will be kept confidential.  
                Your responses will remain anonymous, and **no personally identifiable information is collected**.  
                Research records will be stored securely on password-protected servers.  
                Anonymized data may be used in academic publications, presented at conferences, and shared in public scientific data repositories.

                **Compensation:**  
                You will receive **$20 USD** upon submission of your anonymized ChatGPT conversation logs.
                """)

    st.markdown("""
                **Principal Investigator:** manoel@cs.princeton.edu  

                **Institutional Review Board:**  
                - Phone: (609) 258-8543  
                - Email: irb@princeton.edu
                """)

    st.markdown("""
                I understand that:

                - My participation is voluntary  
                - Refusal to participate involves no penalty or loss of benefits  
                - I may discontinue participation at any time without penalty  
                - I do not waive any legal rights or release Princeton University or its agents from liability for negligence
                """)

    st.markdown("---")
    st.markdown("**By clicking “I Consent,” I give my consent to participate in this research.**")
    
    if not st.session_state.consent:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("I Consent", width="stretch"):
                st.session_state.consent = True
                go_to_page("instructions")
        with col2:
            if st.button("I Do Not Consent", width="stretch"):
                st.session_state.consent = False
                go_to_page("home")

    inline_notice(
        "Your data stays on your device until you explicitly choose to donate the cleaned result.",
        tone="info",
    )

