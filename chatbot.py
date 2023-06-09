import pandas as pd
import numpy as np

# 챗봇 클래스를 정의
class Levenshtein_ChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # CSV 파일로부터 질문과 답변 데이터를 불러와 리스트에 담는 메소드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    # 사용자 입력내용과 기존 질문 간의 레벤슈타인 거리 계산
    # 계산 후 레벤슈타인 거리를 이용하여 계산한 유사도 중 가장 낮은 숫자의 대답을 반환
    def levenshtein_distance(self, input_sentence):
        similarities  = []
        for temp in self.questions:
            if temp == input_sentence:
                similarities.append(0) # 같으면 0을 유사도에 추가
                break
            questions_len = len(temp) 
            input_sentence_len = len(input_sentence) 
            if temp == "": 
                similarities.append(input_sentence_len)  # 기존 질문이 공백이면 사용자 입력 내용 길이를 유사도에 추가
                break
            if input_sentence == "": 
                similarities.append(questions_len) # 사용자 입력 내용이 공백이면 기존 질문 길이를 유사도에 추가
                break
            matrix = [[] for i in range(questions_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
            for i in range(questions_len+1): # 0으로 초기화
                matrix[i] = [0 for j in range(input_sentence_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
            # 0일 때 표에 들어갈 초깃값 설정
            for i in range(questions_len+1):
                matrix[i][0] = i
            for j in range(input_sentence_len+1):
                matrix[0][j] = j
            for i in range(1, questions_len+1):
                ac = temp[i-1]
                for j in range(1, input_sentence_len+1):
                    bc = input_sentence[j-1] 
                    cost = 0 if (ac == bc) else 1 
                    matrix[i][j] = min([
                        matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                        matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                        matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                    ])
            similarities.append(matrix[questions_len][input_sentence_len])       
        best_match_index = np.argmin(similarities)
        return self.answers[best_match_index]
    
# 데이터 파일의 경로를 지정합니다.
filepath = 'ChatbotData.csv'

# 챗봇 객체를 생성합니다.
chatbot = Levenshtein_ChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    print(chatbot.levenshtein_distance(input_sentence))