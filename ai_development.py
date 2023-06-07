import pandas as pd
from Levenshtein_Distance import calc_distance 
import unicodedata

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers, self.data  = self.load_data(filepath)

    def load_data(self, filepath): #챗봇데이터를 읽고, 질문, 답, 데이터프레임을 리턴해주는 함수
        data = pd.read_csv(filepath) 
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        for i in range(len(questions)):
            questions[i] = unicodedata.normalize('NFC',questions[i]) #애플 한글자모 분리문제 해결
        for i in range(len(answers)):
            answers[i] = unicodedata.normalize('NFC',answers[i])#애플 한글자모 분리문제 해결
        return questions, answers, data
    
    def find_best_answer_byLVD(self,input_sentence): #입력된 문장에 대한 레벤슈타인 거리 계산 및 최소거리인 답 문장 리턴 함수
        self.LVD_list = [] # 레벤슈타인거리 리스트
        for i in range(len(self.questions)):
            self.LVD_list.append(calc_distance(unicodedata.normalize('NFC',input_sentence),self.questions[i])) #입력된 질문과 챗봇데이터의 질문을 각각 비교하여 레벤슈타인 거리를 구한 뒤, 리스트에 입력
        self.data['레벤슈타인 거리'] = self.LVD_list # 데이터 프레임의 '레벤슈타인 거리'컬럼에 리스트 대입
        self.data.sort_values(by=['레벤슈타인 거리'],ascending=True,inplace=True)  #레벤슈타인 거리 컬럼을 기준하여 오름차순으로 정렬
        return self.data.iat[0,1]   #레벤슈타인 거리가 최소인 행의 답 문장 리턴
        
# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer_byLVD(input_sentence)
    chatbot.__init__(filepath) # 변수 초기화 목적
    print('질문: ',input_sentence)
    print('Chatbot:', response)
    
