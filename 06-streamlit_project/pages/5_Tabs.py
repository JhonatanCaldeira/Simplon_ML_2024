import streamlit as st

st.title('Tableau de Bord avec Onglets Streamlit')
st.sidebar.markdown('# Tableau de Bord avec Onglets Streamlit')

tab1, tab2, tab3 = st.tabs(['Français','Anglais','Portuguais'])

with tab1:
    st.header('L\'origine de la langue française', divider='rainbow')
    st.write('La langue française est née vers le 9e siècle d\'un mélange de latin, \
             de langue germanique et de francique. Elle se nommait alors le « françois » \
             (prononcé « franswè »). À l\'époque, la langue française n\'était parlée que dans \
             les régions d\'Orléans, de Paris et de Senlis, et ce, par les classes sociales les plus aisées.')

with tab2:
    st.header('The origins of english language', divider='rainbow')
    st.write('The history of the English language really started with the \
             arrival of three Germanic tribes who invaded Britain during the \
             5th century AD. These tribes, the Angles, the Saxons and the Jutes, \
             crossed the North Sea from what today is Denmark and northern Germany.')
    
with tab3:
    st.header('A origem da lingua portuguesa', divider='rainbow')
    st.write('Sua origem está altamente conectada a outra língua (o galego), \
             mas, o português é uma língua própria e independente. Apesar da \
             influência dos tempos tê-la alterado, adicionando vocábulos franceses, \
             ingleses, espanhóis, ela ainda tem sua identidade única, \
             sem a força que tinha no seu ápice, quando era quase tão difundida como agora é o inglês.')