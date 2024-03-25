import streamlit as st
import spacy
import PyPDF2
from streamlit_lottie import st_lottie
import requests
# st.set_page_config(layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

def lemmatize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text

def match_cvs(cv1, cv2):
    lemmatized_cv1 = lemmatize_text(cv1)
    lemmatized_cv2 = lemmatize_text(cv2)


    ratio = similarity_ratio(lemmatized_cv1, lemmatized_cv2)
    return ratio

def similarity_ratio(text1, text2):

    common_words = set(text1.split()) & set(text2.split())
    total_words = set(text1.split()) | set(text2.split())
    ratio = len(common_words) / len(total_words)
    return ratio


st.image("IOH.jpg", width=200)
st.title("CV Matcher IOH")
st.text("Powered by Lemmatizing Method to Improve the Parameters")

col1, col2, col3 = st.columns([1,2,1])
with col2:
     lotieurl="https://lottie.host/c92a4ead-e27f-4e32-86fd-a05d6952ad26/fF9qQlcivd.json"
     lottie_json = load_lottieurl(lotieurl)
     st_lottie(lottie_json, height=300, width=300)

st.warning("What's new on this update? We use Improvement using Lemmatization!",icon="💡")

st.markdown("Lemmatization adalah proses dalam pemrosesan bahasa alami (Natural Language Processing atau NLP) di mana kata-kata infleksional atau turunan diubah menjadi bentuk dasarnya atau kata dasar.Tujuannya adalah untuk mengurangi kata-kata ke bentuk akar mereka sehingga mereka dapat diidentifikasi sebagai bentuk dasar yang sama.Dalam bahasa Inggris, misalnya, lemmatization akan mengubah kata-kata ke bentuk dasarnya. Contohnya: ")
st.markdown('"running" menjadi "run"')
st.markdown('"better" menjadi "good"')
st.markdown('"happiest" menjadi "happy"')
st.markdown("Penggunaan lemmatization dapat membantu dalam analisis teks dan pemrosesan bahasa alami karena memastikan bahwa kata-kata dengan makna yang sama, namun dalam bentuk yang berbeda,dianggap sebagai entitas yang sama. Hal ini dapat meningkatkan akurasi dan keseragaman analisis teks.")


def main():
    st.title("")


    input_option = st.radio("Select input type:", ["Text", "PDF"])
    cv1 = ""
    cv2 = ""

    if input_option == "Text":
        cv1 = st.text_area("Enter CV:", "")
        cv2 = st.text_area("Enter Requirements:", "")
    elif input_option == "PDF":
        pdf_file1 = st.file_uploader("Upload CV 1 (PDF)", type=["pdf"])
        pdf_file2 = st.file_uploader("Upload CV 2 (PDF)", type=["pdf"])

        if pdf_file1 and pdf_file2:
            cv1 = extract_text_from_pdf(pdf_file1)
            cv2 = extract_text_from_pdf(pdf_file2)

    if st.button("Calculate The Similarity"):
        if cv1 and cv2:
            similarity = match_cvs(cv1, cv2)
            similarity_percentage = similarity * 100
            st.write(f"Similarity Ratio: {similarity_percentage:.2f}%")

if __name__ == "__main__":
    main()
