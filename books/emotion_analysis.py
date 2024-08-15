from transformers import pipeline, BertForSequenceClassification, BertTokenizer
import os

def emotion_analysis(input_post):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(BASE_DIR, 'books/kobert_fine_tuning_weight')

    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # model = BertForSequenceClassification.from_pretrained('./kobert_fine_tuning_weight')
    # tokenizer = BertTokenizer.from_pretrained('./kobert_fine_tuning_weight')
    
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    text = [input_post]
    
    result = nlp(text)[0]
    
    label = result['label']
    score = result['score']
    
    if label == 'LABEL_0':
        score = 0 - score
    
    return score

# data = "《아기돼지 삼형제》는 오랜 시간 동안 사랑받아온 고전 동화이지만, 현대적인 관점에서 보면 몇 가지 아쉬운 점들이 눈에 띕니다. 이 독서록에서는 이 이야기가 가진 한계와 비판적인 시각에서 본 문제점들을 다루어보겠습니다.우선, 이야기의 전개가 다소 단순하고 이분법적이라는 점이 아쉽습니다. 첫째와 둘째 돼지가 집을 짓는 과정을 너무 쉽게 처리하고, 셋째 돼지가 벽돌집을 짓는 과정을 강조하는 방식은 '성실함이 항상 성공을 보장한다'는 메시지를 전달하려는 의도가 강합니다. 그러나 현실에서는 노력과 결과가 항상 일치하지 않는 경우도 많고, 다양한 접근 방식이 존재할 수 있음에도 이 이야기는 지나치게 단순화된 교훈을 제시합니다.또한, 셋째 돼지의 성공만을 강조하다 보니, 첫째와 둘째 돼지가 실패한 이유를 너무 간단히 취급하는 경향이 있습니다. 이들은 단지 '게으르고 성급해서' 실패한 것으로 그려지며, 결과적으로 '노력하지 않은 자는 당연히 실패한다'는 메시지를 강화합니다. 하지만 이 접근은 개개인의 상황이나 배경을 무시하고, 모든 문제를 개인의 노력 부족으로 돌리는 것처럼 보일 수 있습니다. 이러한 메시지는 현대 사회에서 지나치게 성과 중심적인 사고를 강화할 위험이 있습니다.더 나아가, 늑대라는 캐릭터가 일방적인 악역으로 그려지는 것도 다소 아쉽습니다. 늑대는 그저 삼형제의 집을 부수고자 하는 악당으로 등장하며, 그 이유나 배경에 대한 설명이 전혀 없습니다. 이러한 단순한 악역 설정은 어린이들이 세계를 이분법적으로 바라보게 할 위험이 있으며, '악'에 대한 이해를 방해할 수 있습니다.마지막으로, 이 이야기가 전하는 메시지가 시대에 뒤떨어진 측면도 있습니다. 셋째 돼지의 성실함을 칭찬하는 것은 중요하지만, 오늘날의 사회는 협력, 창의성, 융통성 등 다양한 가치들을 필요로 합니다. 그러나 이 이야기는 지나치게 '벽돌집을 짓는 것'만을 강조함으로써, 다른 형태의 지혜나 가치들을 간과하고 있다는 느낌을 줍니다.결론적으로, 《아기돼지 삼형제》는 분명 고전으로서의 가치가 있지만, 그 이분법적이고 단순화된 메시지는 현대적 관점에서 재고할 필요가 있습니다. 이 동화를 읽으면서 단순히 성실함만이 성공을 보장한다는 생각보다는, 다양한 관점에서 상황을 이해하고, 다양한 가치들을 인정하는 자세가 필요하다고 느꼈습니다."
# a = emotion_analysis(data)
# print(a)