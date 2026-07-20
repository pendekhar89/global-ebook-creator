import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

st.title("Automated Ebook Generator")
st.write("Generate a simple ebook (at least 3 short chapters) using Google Gemini AI.")

api_key = st.text_input("Google Gemini API Key", type="password")
book_title = st.text_input("Book Title")
book_topic = st.text_input("Book Topic")

def generate_content(key, title, topic):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        f"Write an ebook titled '{title}' about the topic '{topic}'. "
        "The ebook must contain at least 3 short chapters. "
        "Please provide plain text with clear chapter headings, and do not use complex markdown formatting or special characters, so it is easy to read."
    )
    response = model.generate_content(prompt)
    return response.text

def create_pdf(title, text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("helvetica", "B", 16)
    safe_title = title.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 10, safe_title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    # Body
    pdf.set_font("helvetica", "", 12)
    safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, safe_text)

    return bytes(pdf.output())

if st.button("Generate Ebook"):
    if not api_key:
        st.error("Please enter your Gemini API Key.")
    elif not book_title or not book_topic:
        st.error("Please enter both a Book Title and a Book Topic.")
    else:
        with st.spinner("Generating ebook content..."):
            try:
                ebook_content = generate_content(api_key, book_title, book_topic)
                st.session_state["ebook_content"] = ebook_content
                st.session_state["pdf_bytes"] = create_pdf(book_title, ebook_content)
                st.session_state["generated"] = True
                st.success("Ebook generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state.get("generated", False):
    # Show preview
    st.subheader("Preview")
    st.text_area("Content", st.session_state["ebook_content"], height=300)

    st.download_button(
        label="Download Ebook as PDF",
        data=st.session_state["pdf_bytes"],
        file_name=f"{book_title.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
