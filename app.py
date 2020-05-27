import cv2
import streamlit as st
import mahotas
import io
import numpy as np


def main():
 options = st.sidebar.selectbox("Menu",['Inicio','Suavização','Binarização','Segmentação'])


 if options == "Inicio":
    st.title("Introdução a OpenCV com python")
    st.subheader("Uma abordagem usando python e streamlit ")
    st.markdown("""

        Aqui vamos aprender sobre os principais filtros existentes, tipos de suavização e Segmentação de imagens.

        ---
        ## Bons estudos !
        ![](https://i.pinimg.com/originals/77/e1/26/77e12645ebd3cca00798fbeaae56e6ed.gif)



        ### Referencial Teorico !
        link - http://professor.luzerna.ifc.edu.br/ricardo-antonello/wp-content/uploads/sites/8/2017/02/Livro-Introdu%C3%A7%C3%A3o-a-Vis%C3%A3o-Computacional-com-Python-e-OpenCV-3.pdf
        """)

 if options=="Suavização":
    st.title(options)
    st.markdown("""
            ## O que é Suavização de imagem ?
            A  suavisação  da  imagem(do  inglês Smoothing),  também  chamada  de  ‘blur’  ou ‘blurring’ que podemos traduzir para “borrão”, é um efeito que podemos notar nas fotografias fora de foco ou desfocadas onde tudo fica embasado.
            Esse  efeito  é  muito  útil  quando  utilizamos algoritmos  de  identificação de  objetos  em  imagens  pois  os  processos  de  detecção  de  bordas por exemplo, funcionam melhor depois de aplicar uma suavização na imagem

                """)
    file_bytes = st.file_uploader("Upload a file", type=("png", "jpg"))
    menu = st.sidebar.selectbox("Tipos de suavização",['Sem Suavização','cálculo da média','Gaussiana','mediana','filtro bilateral'])
    st.subheader(menu)

    if file_bytes is not None and menu == 'Sem Suavização':
      #print(file_bytes)
      decode_img = cv2.imdecode(np.frombuffer(file_bytes.getbuffer(), np.uint8), -1)
      cv2.imwrite("image.jpg",decode_img)
      st.image(file_bytes)

    if file_bytes is not None and menu == 'cálculo da média':
      blur_1 = st.sidebar.slider("Tupla para - blurring kernel size X.",1,255,1)
      blur_2 = st.sidebar.slider("Tupla para - blurring kernel size Y.",1,255,1)
      img = cv2.imread('image.jpg')
      img_blur = cv2.blur(img,(blur_1,blur_2))
      resultado = np.vstack([np.hstack([img, img_blur])])
      st.image(resultado)

    if file_bytes is not None and menu == 'Gaussiana':
      blur_2 = st.sidebar.slider("blurring kernel size (img,blurring).",3,9,3)
      img = cv2.imread('image.jpg')
      img_blur = cv2.GaussianBlur(img,(blur_2,blur_2),0)
      resultado = np.vstack([np.hstack([img, img_blur])])
      st.image(resultado)

    if file_bytes is not None and menu == 'mediana':
      img = cv2.imread('image.jpg')
      img_blur = cv2.medianBlur(img,5)
      resultado = np.vstack([np.hstack([img, img_blur])])
      st.image(resultado)


    if file_bytes is not None and menu == 'filtro bilateral':
      img = cv2.imread('image.jpg')
      img_blur = cv2.bilateralFilter(img,9,75,75)
      resultado = np.vstack([np.hstack([img, img_blur])])
      st.image(resultado)


 if options=="Binarização":
    menu = st.sidebar.selectbox("Binarização",["Threshold adaptativo","Threshold com Otsu e Riddler-Calvard"])
    st.subheader(menu)
    st.subheader("O que é Binarização de imagem ?")
    st.write("consiste em separar uma imagem, em regiões de interesse e não interesse através da escolha de um ponto de corte, Essas  regiões  podem  ser  representadas  por pixel  pretos  e  brancos.")


    file_bytes = st.file_uploader("Upload a file", type=("png", "jpg"))
    if file_bytes is not None and menu == 'Threshold adaptativo':
        img = cv2.imread('image.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converte
        suave = cv2.GaussianBlur(img, (5, 5), 0) # aplica blur
        bin1 = cv2.adaptiveThreshold(suave, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        resultado = np.vstack([np.hstack([img, bin1])])
        st.image(resultado)

    if file_bytes is not None and menu == 'Threshold com Otsu e Riddler-Calvard':
        img = cv2.imread('image.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converte
        suave = cv2.GaussianBlur(img, (7, 7), 0) # aplica blur
        T = mahotas.thresholding.otsu(suave)
        temp = img.copy()
        temp[temp > T] = 255
        temp[temp < 255] = 0
        temp = cv2.bitwise_not(temp)
        T = mahotas.thresholding.rc(suave)
        temp2 = img.copy()
        temp2[temp2 > T] = 255
        temp2[temp2 < 255] = 0
        temp2 = cv2.bitwise_not(temp2)
        resultado = np.vstack([np.hstack([img, suave]),np.hstack([temp, temp2])])
        st.image(resultado)



 if options=="Segmentação":
    menu = st.sidebar.selectbox("Segmentação e métodos de detecção de bordas",["Sobel","Filtro Laplaciano","Detector de bordas Canny"])
    st.subheader(menu)
    st.subheader("O que é Segmentação de imagem ?")
    st.write("")

    file_bytes = st.file_uploader("Upload a file", type=("png", "jpg"))
    if file_bytes is not None and menu == 'Sobel':
        img = cv2.imread('image.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sobelX = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        sobelY = cv2.Sobel(img, cv2.CV_64F, 0, 1)
        sobelX = np.uint8(np.absolute(sobelX))
        sobelY = np.uint8(np.absolute(sobelY))
        sobel = cv2.bitwise_or(sobelX, sobelY)
        resultado = np.vstack(
                 [np.hstack([img,    sobelX]),
                  np.hstack([sobelY, sobel])]
                  )
        st.image(resultado)

    if file_bytes is not None and menu == 'Filtro Laplaciano':
        img = cv2.imread('image.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(img, cv2.CV_64F)
        lap = np.uint8(np.absolute(lap))
        resultado = np.vstack([img, lap])
        st.image(resultado)

    if file_bytes is not None and menu == 'Detector de bordas Canny':
        img = cv2.imread('image.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        suave = cv2.GaussianBlur(img, (7, 7), 0)
        canny1 = cv2.Canny(suave, 20, 120)
        canny2 = cv2.Canny(suave, 70, 200)
        resultado = np.vstack([
              np.hstack([img,    suave ]),
              np.hstack([canny1, canny2])])
        st.image(resultado)





if __name__ == "__main__":
    main()
