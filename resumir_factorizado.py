import re
import nltk
import heapq  
from pdfminer.high_level import extract_text
nltk.download('punkt')
nltk.download('stopwords')


def normalizer(pdf):
    pdf_text = extract_text(pdf)
    normalized_text = pdf_text.replace("[ edit ]", "")
    normalized_text = re.sub(r'\[[0-9]*\]', ' ', normalized_text)  
    normalized_text = re.sub(r'\s+', ' ', normalized_text)
    return normalized_text

def formatter_text(text):
    formatted_text = re.sub('[^a-zA-Z]', ' ', text)  
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    return formatted_text

def word_frequency(text):
    word_frequency = {}
    stopwords = nltk.corpus.stopwords.words('spanish')
        
    for word in nltk.word_tokenize(text):  
        if word not in stopwords:
            if word not in word_frequency.keys():
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1
                
    return word_frequency

def repeated_sentences(word_frequency, words_list):
    max_sentence = {}
    max_sentence_length = 70
    for sent in words_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequency.keys():
                if len(sent.split(' ')) < max_sentence_length:
                    if sent not in max_sentence.keys():
                        max_sentence[sent] = word_frequency[word]
                    else:
                        max_sentence[sent] += word_frequency[word]
                        
    return max_sentence
    
def text_summarizer(pdf):
    normalized_text = normalizer(pdf)    
    formatted_text = formatter_text(normalized_text)
        
    word_frequency_variable = word_frequency(formatted_text)
    max_frequency = max(word_frequency_variable.values())

    for word in word_frequency_variable.keys():  
        word_frequency_variable[word] /= max_frequency

    words_list = nltk.sent_tokenize(normalized_text)
    max_repeated_sentences = repeated_sentences(word_frequency_variable, words_list)

    resumed_text = heapq.nlargest(7, max_repeated_sentences, key=max_repeated_sentences.get)
    resumen = ' '.join(resumed_text)  
    print(resumen)
    return resumen

def save_resume_in_file(resume):
    with open("resume.txt", "w") as resume_file:
        resume_file.write("##############\tRESUMEN\t#############\n")
        resume_file.write(resume)
    
def main():
    # pdf_name = input("Ingrese el nombre del archivo pdf (recuerda que debe de estar en el mismo directorio): ")
    pdf_name = "Dialnet-ElDominioDeLosHemisferiosCerebrales-5210276.pdf"
    
    resume = text_summarizer(pdf_name)
    
    save_resume_in_file(resume)
    
    print("Completado")

if __name__ == "__main__":
    main()