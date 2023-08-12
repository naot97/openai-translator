import streamlit as st
from model.translator import get_translation_from_text
def main():
    st.image(["ThinkPrompt.png"], width=120)
    st.title("Think Prompt Translator")
    
    # st.subheader("Your text")
    question = st.text_input(label="Type your text and click :red[Submit] to see the translation")

    dest = st.selectbox(
        "Destination language",
        ("VietNamese", "English", "French")
    )
    is_click = st.button(label=":red[Submit]")
    # Display the answer and additional context
    st.subheader('Translation')
    answer = ""
    if is_click and question != "":
        with st.spinner('Translating...'):
            answer, _ =  get_translation_from_text(dest, question)
        
    st.text_area(label="", value=answer, height=100)
    st.write("Powered by https://github.com/naot97")
    
if __name__ == "__main__":
    main()