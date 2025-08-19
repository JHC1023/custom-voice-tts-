"""
영어를 한글 발음으로 변환하는 개선된 모듈
"""
import re


class EnglishToKoreanPronunciation:
    """영어를 한글 발음으로 변환하는 클래스 (개선된 버전)"""

    def __init__(self):
        # 확장된 영어 단어 -> 한글 발음 사전
        self.word_dict = {
            # 기본 인사말
            'hello': '헬로', 'hi': '하이', 'hey': '헤이', 'bye': '바이', 'goodbye': '굿바이',
            'yes': '예스', 'no': '노', 'okay': '오케이', 'ok': '오케이',

            # 감사/사과 표현
            'thank': '땡크', 'thanks': '땡크스', 'you': '유', 'welcome': '웰컴',
            'please': '플리즈', 'sorry': '쏘리', 'excuse': '익스큐즈', 'me': '미',

            # 시간 관련
            'good': '굿', 'morning': '모닝', 'afternoon': '애프터눈', 'evening': '이브닝',
            'night': '나이트', 'day': '데이', 'time': '타임', 'today': '투데이',
            'tomorrow': '투모로', 'yesterday': '예스터데이', 'now': '나우', 'later': '레이터',
            'early': '얼리', 'late': '레이트', 'soon': '순',

            # 인사 관련
            'nice': '나이스', 'meet': '미트', 'to': '투', 'great': '그레이트',
            'wonderful': '원더풀', 'amazing': '어메이징', 'awesome': '어썸',

            # 숫자 (확장)
            'zero': '지로', 'one': '원', 'two': '투', 'three': '쓰리', 'four': '포', 'five': '파이브',
            'six': '식스', 'seven': '세븐', 'eight': '에이트', 'nine': '나인', 'ten': '텐',
            'eleven': '일레븐', 'twelve': '트웰브', 'thirteen': '써틴', 'fourteen': '포틴',
            'fifteen': '피프틴', 'sixteen': '식스틴', 'seventeen': '세븐틴', 'eighteen': '에이틴',
            'nineteen': '나인틴', 'twenty': '트웬티', 'thirty': '써티', 'forty': '포티',
            'fifty': '피프티', 'sixty': '식스티', 'seventy': '세븐티', 'eighty': '에이티',
            'ninety': '나인티', 'hundred': '헌드레드', 'thousand': '사우전드', 'million': '밀리언',

            # 자주 사용되는 동사 (확장)
            'go': '고', 'come': '컴', 'see': '시', 'look': '룩', 'watch': '와치',
            'want': '원트', 'need': '니드', 'have': '해브', 'get': '겟', 'give': '기브',
            'take': '테이크', 'make': '메이크', 'do': '두', 'did': '디드', 'done': '던',
            'put': '풋', 'bring': '브링', 'think': '띵크', 'know': '노', 'understand': '언더스탠드',
            'say': '세이', 'tell': '텔', 'speak': '스피크', 'talk': '토크', 'listen': '리슨',
            'hear': '히어', 'eat': '이트', 'drink': '드링크', 'sleep': '슬립', 'work': '워크',
            'play': '플레이', 'read': '리드', 'write': '라이트', 'learn': '런', 'teach': '티치',
            'help': '헬프', 'try': '트라이', 'use': '유즈', 'buy': '바이', 'sell': '셀',
            'pay': '페이', 'cost': '코스트', 'find': '파인드', 'lose': '루즈', 'win': '윈',
            'stop': '스탑', 'start': '스타트', 'begin': '비긴', 'end': '엔드', 'finish': '피니시',
            'open': '오픈', 'close': '클로즈', 'turn': '턴', 'move': '무브', 'walk': '워크',
            'run': '런', 'drive': '드라이브', 'fly': '플라이', 'travel': '트래블',

            # 대명사 및 소유격
            'i': '아이', 'me': '미', 'my': '마이', 'mine': '마인', 'myself': '마이셀프',
            'you': '유', 'your': '유어', 'yours': '유어스', 'yourself': '유어셀프',
            'he': '히', 'him': '힘', 'his': '히즈', 'himself': '힘셀프',
            'she': '쉬', 'her': '허', 'hers': '허즈', 'herself': '허셀프',
            'it': '잇', 'its': '잇츠', 'itself': '잇셀프',
            'we': '위', 'us': '어스', 'our': '아워', 'ours': '아워즈', 'ourselves': '아워셀브즈',
            'they': '데이', 'them': '뎀', 'their': '데어', 'theirs': '데어즈', 'themselves': '뎀셀브즈',
            'this': '디스', 'that': '댓', 'these': '디즈', 'those': '도즈',
            'who': '후', 'what': '왓', 'where': '웨어', 'when': '웬', 'why': '와이', 'how': '하우',

            # 접속사/전치사 (확장)
            'and': '앤드', 'or': '오어', 'but': '벗', 'so': '소', 'because': '비코즈',
            'if': '이프', 'when': '웬', 'while': '와일', 'until': '언틸', 'since': '신스',
            'before': '비포어', 'after': '애프터', 'during': '듀링',
            'in': '인', 'on': '온', 'at': '앳', 'to': '투', 'for': '포', 'with': '위드',
            'without': '위다웃', 'by': '바이', 'from': '프롬', 'about': '어바웃',
            'under': '언더', 'over': '오버', 'above': '어보브', 'below': '빌로',
            'between': '비트윈', 'among': '어몽', 'through': '쓰루', 'across': '어크로스',
            'into': '인투', 'onto': '온투', 'off': '오프', 'out': '아웃', 'up': '업', 'down': '다운',

            # 형용사 (확장)
            'big': '빅', 'small': '스몰', 'large': '라지', 'little': '리틀', 'tiny': '타이니',
            'long': '롱', 'short': '쇼트', 'tall': '톨', 'high': '하이', 'low': '로',
            'wide': '와이드', 'narrow': '내로', 'thick': '씩', 'thin': '씬',
            'hot': '핫', 'cold': '콜드', 'warm': '웜', 'cool': '쿨', 'dry': '드라이', 'wet': '웻',
            'clean': '클린', 'dirty': '더티', 'new': '뉴', 'old': '올드', 'young': '영',
            'fast': '패스트', 'slow': '슬로', 'quick': '퀵', 'easy': '이지', 'difficult': '디피컬트',
            'hard': '하드', 'soft': '소프트', 'light': '라이트', 'heavy': '헤비',
            'strong': '스트롱', 'weak': '위크', 'safe': '세이프', 'dangerous': '데인저러스',
            'beautiful': '뷰티풀', 'ugly': '어글리', 'pretty': '프리티', 'handsome': '핸섬',
            'smart': '스마트', 'stupid': '스투피드', 'clever': '클레버', 'funny': '퍼니',
            'serious': '시리어스', 'happy': '해피', 'sad': '새드', 'angry': '앵그리',
            'excited': '익사이티드', 'tired': '타이어드', 'hungry': '헝그리', 'thirsty': '써스티',

            # 부사
            'very': '베리', 'really': '리얼리', 'quite': '콰이트', 'too': '투', 'enough': '이너프',
            'much': '머치', 'many': '메니', 'more': '모어', 'most': '모스트',
            'less': '레스', 'least': '리스트', 'few': '퓨', 'little': '리틀',
            'some': '썸', 'any': '애니', 'all': '올', 'every': '에브리', 'each': '이치',
            'both': '보스', 'either': '아이더', 'neither': '나이더',
            'here': '히어', 'there': '데어', 'everywhere': '에브리웨어', 'somewhere': '썸웨어',
            'nowhere': '노웨어', 'anywhere': '애니웨어',
            'always': '올웨이즈', 'never': '네버', 'sometimes': '썸타임즈', 'often': '오픈',
            'usually': '유주얼리', 'seldom': '셀덤', 'rarely': '레얼리',
            'already': '올레디', 'yet': '옛', 'still': '스틸', 'just': '저스트',
            'only': '온리', 'also': '올소', 'too': '투', 'either': '아이더',

            # 음식 및 음료
            'food': '푸드', 'water': '워터', 'coffee': '커피', 'tea': '티', 'milk': '밀크',
            'juice': '주스', 'beer': '비어', 'wine': '와인', 'bread': '브레드', 'rice': '라이스',
            'meat': '미트', 'fish': '피시', 'chicken': '치킨', 'beef': '비프', 'pork': '포크',
            'vegetable': '베지터블', 'fruit': '프루트', 'apple': '애플', 'banana': '바나나',
            'orange': '오렌지', 'grape': '그레이프', 'strawberry': '스트로베리',
            'pizza': '피자', 'hamburger': '햄버거', 'sandwich': '샌드위치', 'salad': '샐러드',
            'soup': '수프', 'cake': '케이크', 'cookie': '쿠키', 'ice': '아이스', 'cream': '크림',

            # 색깔
            'red': '레드', 'blue': '블루', 'green': '그린', 'yellow': '옐로', 'purple': '퍼플',
            'orange': '오렌지', 'pink': '핑크', 'brown': '브라운', 'gray': '그레이', 'grey': '그레이',
            'black': '블랙', 'white': '화이트', 'silver': '실버', 'gold': '골드',

            # 가족 관계
            'family': '패밀리', 'father': '파더', 'mother': '마더', 'dad': '대드', 'mom': '맘',
            'parent': '패런트', 'child': '차일드', 'son': '선', 'daughter': '도터',
            'brother': '브라더', 'sister': '시스터', 'husband': '허즈번드', 'wife': '와이프',
            'grandfather': '그랜드파더', 'grandmother': '그랜드마더', 'uncle': '엉클', 'aunt': '앤트',
            'cousin': '커즌', 'nephew': '네퓨', 'niece': '니스',

            # 직업
            'job': '잡', 'work': '워크', 'teacher': '티처', 'student': '스튜던트', 'doctor': '닥터',
            'nurse': '너스', 'lawyer': '로이어', 'engineer': '엔지니어', 'manager': '매니저',
            'worker': '워커', 'driver': '드라이버', 'cook': '쿡', 'waiter': '웨이터',
            'police': '폴리스', 'fire': '파이어', 'fighter': '파이터',

            # 장소
            'home': '홈', 'house': '하우스', 'school': '스쿨', 'office': '오피스', 'hospital': '하스피탈',
            'store': '스토어', 'shop': '샵', 'market': '마켓', 'bank': '뱅크', 'post': '포스트',
            'restaurant': '레스토랑', 'hotel': '호텔', 'airport': '에어포트', 'station': '스테이션',
            'park': '파크', 'beach': '비치', 'mountain': '마운틴', 'river': '리버', 'lake': '레이크',
            'city': '시티', 'town': '타운', 'country': '컨트리', 'street': '스트리트', 'road': '로드',

            # 교통수단
            'car': '카', 'bus': '버스', 'train': '트레인', 'plane': '플레인', 'ship': '쉽',
            'boat': '보트', 'bicycle': '바이시클', 'bike': '바이크', 'taxi': '택시', 'subway': '서브웨이',

            # 동물
            'animal': '애니멀', 'dog': '도그', 'cat': '캣', 'bird': '버드', 'fish': '피시',
            'horse': '호스', 'cow': '카우', 'pig': '피그', 'sheep': '쉽', 'chicken': '치킨',
            'tiger': '타이거', 'lion': '라이언', 'elephant': '엘리펀트', 'monkey': '몽키',

            # 날씨
            'weather': '웨더', 'sunny': '써니', 'cloudy': '클라우디', 'rainy': '레이니',
            'snowy': '스노위', 'windy': '윈디', 'storm': '스톰', 'thunder': '선더',
            'rain': '레인', 'snow': '스노', 'wind': '윈드', 'sun': '선', 'cloud': '클라우드',

            # 계절과 달
            'spring': '스프링', 'summer': '서머', 'fall': '폴', 'autumn': '오텀', 'winter': '윈터',
            'january': '잰유어리', 'february': '페브루어리', 'march': '마치', 'april': '에이프릴',
            'may': '메이', 'june': '준', 'july': '줄라이', 'august': '오거스트',
            'september': '셉템버', 'october': '옥토버', 'november': '노벰버', 'december': '디셈버',

            # 요일
            'monday': '먼데이', 'tuesday': '튜즈데이', 'wednesday': '웬즈데이', 'thursday': '써즈데이',
            'friday': '프라이데이', 'saturday': '새터데이', 'sunday': '선데이',

            # 신체 부위
            'body': '바디', 'head': '헤드', 'face': '페이스', 'eye': '아이', 'nose': '노즈',
            'mouth': '마우스', 'ear': '이어', 'hair': '헤어', 'neck': '넥', 'shoulder': '숄더',
            'arm': '암', 'hand': '핸드', 'finger': '핑거', 'leg': '레그', 'foot': '풋',
            'back': '백', 'stomach': '스터막', 'heart': '하트',

            # 의류
            'clothes': '클로즈', 'shirt': '셔트', 'pants': '팬츠', 'dress': '드레스', 'skirt': '스커트',
            'jacket': '재킷', 'coat': '코트', 'shoes': '슈즈', 'hat': '햇', 'cap': '캡',
            'socks': '삭스', 'gloves': '글러브즈', 'belt': '벨트', 'tie': '타이',

            # 감정 표현
            'love': '러브', 'like': '라이크', 'hate': '헤이트', 'enjoy': '인조이', 'prefer': '프리퍼',
            'feel': '필', 'emotion': '이모션', 'smile': '스마일', 'laugh': '래프', 'cry': '크라이',
            'worry': '워리', 'fear': '피어', 'hope': '호프', 'dream': '드림',
        }

        # 고급 음성학적 규칙들
        self.phonetic_rules = [
            # 복합 자음 조합들
            ('tion', '션'), ('sion', '션'), ('cial', '셜'), ('tial', '셜'),
            ('ough', '어프'), ('augh', '오프'), ('eigh', '에이'),
            ('ght', 'ㅌ'), ('ck', 'ㅋ'), ('ng', 'ㅇ'),
            ('th', 'ㅅ'), ('sh', '쉬'), ('ch', '치'), ('ph', 'ㅍ'),
            ('wh', '우'), ('qu', '큐'), ('kn', 'ㄴ'), ('wr', 'ㄹ'),
            ('mb', 'ㅁ'), ('bt', 'ㅌ'), ('mn', 'ㅁ'),

            # 모음 조합들
            ('ai', '에이'), ('ay', '에이'), ('ee', '이'), ('ea', '이'),
            ('ie', '아이'), ('oe', '오'), ('ue', '유'), ('ui', '유이'),
            ('oo', '우'), ('ou', '아우'), ('ow', '아우'), ('au', '오'),
            ('aw', '오'), ('ew', '유'), ('ey', '에이'), ('oy', '오이'),

            # 자음 + 모음 조합
            ('ce', '스'), ('ci', '시'), ('cy', '시'),
            ('ge', '지'), ('gi', '지'), ('gy', '지'),
            ('dge', '지'), ('tch', '치'),

            # 어미 변화
            ('ed', '드'), ('ing', '잉'), ('er', '어'), ('est', '에스트'),
            ('ly', '리'), ('ty', '티'), ('ry', '리'), ('ny', '니'),
            ('ful', '풀'), ('less', '레스'), ('ness', '네스'),
        ]

        # 단일 문자 매핑 (개선됨)
        self.single_char_map = {
            # 모음들
            'a': '아', 'e': '에', 'i': '이', 'o': '오', 'u': '우', 'y': '이',

            # 자음들 (상황별 다른 발음)
            'b': 'ㅂ', 'c': 'ㅋ', 'd': 'ㄷ', 'f': 'ㅍ', 'g': 'ㄱ',
            'h': 'ㅎ', 'j': 'ㅈ', 'k': 'ㅋ', 'l': 'ㄹ', 'm': 'ㅁ',
            'n': 'ㄴ', 'p': 'ㅍ', 'q': 'ㅋ', 'r': 'ㄹ', 's': 'ㅅ',
            't': 'ㅌ', 'v': 'ㅂ', 'w': 'ㅇ', 'x': 'ㅋㅅ', 'z': 'ㅈ'
        }

    def advanced_phonetic_conversion(self, word):
        """고급 음성학적 변환"""
        word = word.lower().strip()

        # 사전에 있는 단어는 바로 반환
        if word in self.word_dict:
            return self.word_dict[word]

        result = word

        # 1단계: 복합 패턴 적용
        for pattern, replacement in self.phonetic_rules:
            result = result.replace(pattern, replacement)

        # 2단계: 남은 문자들을 개별 변환
        final_result = ""
        i = 0
        while i < len(result):
            char = result[i]

            # 한글이 이미 있으면 그대로 유지
            if ord(char) >= 0xAC00 and ord(char) <= 0xD7A3:  # 한글 완성형 범위
                final_result += char
            elif char in 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ':  # 한글 자모
                final_result += char
            elif char in self.single_char_map:
                final_result += self.single_char_map[char]
            elif char in ' .,!?;:-_()[]{}"\'/\\':
                final_result += char
            else:
                # 알 수 없는 문자는 음성학적으로 추정
                final_result += self.guess_pronunciation(char)

            i += 1

        return final_result

    def guess_pronunciation(self, char):
        """알 수 없는 문자의 발음 추정"""
        # 숫자 처리
        number_map = {
            '0': '제로', '1': '원', '2': '투', '3': '쓰리', '4': '포',
            '5': '파이브', '6': '식스', '7': '세븐', '8': '에이트', '9': '나인'
        }

        if char in number_map:
            return number_map[char]

        # 특수 문자는 그대로 유지
        if not char.isalpha():
            return char

        # 기본 자음/모음 매핑 사용
        return self.single_char_map.get(char, char)

    def handle_contractions(self, text):
        """축약형 처리"""
        contractions = {
            "i'm": "아이 앰", "you're": "유 아", "he's": "히 이즈", "she's": "쉬 이즈",
            "it's": "잇 이즈", "we're": "위 아", "they're": "데이 아",
            "isn't": "이즌트", "aren't": "아런트", "wasn't": "와즌트", "weren't": "워런트",
            "don't": "돈트", "doesn't": "더즌트", "didn't": "디든트",
            "won't": "원트", "wouldn't": "우든트", "can't": "캔트", "couldn't": "쿠든트",
            "shouldn't": "슈든트", "mustn't": "머슨트",
            "i'll": "아일", "you'll": "율", "he'll": "힐", "she'll": "쉴",
            "we'll": "윌", "they'll": "데일",
            "i've": "아이브", "you've": "유브", "we've": "위브", "they've": "데이브",
            "i'd": "아이드", "you'd": "유드", "he'd": "히드", "she'd": "쉬드",
            "we'd": "위드", "they'd": "데이드",
        }

        # 축약형을 공백으로 분리해서 처리
        for contraction, expanded in contractions.items():
            text = re.sub(r'\b' + contraction + r'\b', expanded, text, flags=re.IGNORECASE)

        return text

    def handle_special_endings(self, word):
        """특수 어미 처리"""
        # -s 복수형 처리
        if word.endswith('s') and len(word) > 1:
            base_word = word[:-1]
            if base_word in self.word_dict:
                return self.word_dict[base_word] + '스'

        # -ed 과거형 처리
        if word.endswith('ed') and len(word) > 2:
            base_word = word[:-2]
            if base_word in self.word_dict:
                return self.word_dict[base_word] + '드'

        # -ing 진행형 처리
        if word.endswith('ing') and len(word) > 3:
            base_word = word[:-3]
            if base_word in self.word_dict:
                return self.word_dict[base_word] + '잉'

        # -ly 부사 처리
        if word.endswith('ly') and len(word) > 2:
            base_word = word[:-2]
            if base_word in self.word_dict:
                return self.word_dict[base_word] + '리'

        return None

    def convert_text(self, english_text):
        """영어 텍스트를 한글 발음으로 변환 (개선된 버전)"""
        if not english_text:
            return ""

        # 1단계: 축약형 처리
        text = self.handle_contractions(english_text)

        # 2단계: 문장부호 보존을 위한 처리
        sentences = re.split(r'([.!?]+)', text)
        converted_sentences = []

        for sentence in sentences:
            if re.match(r'^[.!?]+$', sentence):
                converted_sentences.append(sentence)
                continue

            # 3단계: 단어 단위로 분리 (구두점 보존)
            words = re.findall(r'\b\w+\b|[^\w\s]', sentence.lower())
            converted_words = []

            for word in words:
                if not word.isalpha():
                    # 구두점이나 숫자는 그대로 유지
                    converted_words.append(word)
                    continue

                # 4단계: 특수 어미 처리 시도
                special_result = self.handle_special_endings(word)
                if special_result:
                    converted_words.append(special_result)
                    continue

                # 5단계: 일반 변환 처리
                converted_word = self.advanced_phonetic_conversion(word)
                converted_words.append(converted_word)

            if converted_words:
                converted_sentences.append(' '.join(converted_words))

        # 최종 결과 조합
        result = ''.join(converted_sentences)

        # 후처리: 불필요한 공백 정리
        result = re.sub(r'\s+', ' ', result).strip()

        return result

    def convert_with_context(self, english_text, context_type="general"):
        """문맥을 고려한 변환"""
        # 문맥별 특수 처리
        if context_type == "formal":
            # 격식체 변환
            english_text = english_text.replace("hi", "hello")
            english_text = english_text.replace("yeah", "yes")

        elif context_type == "casual":
            # 구어체 변환
            english_text = english_text.replace("going to", "gonna")
            english_text = english_text.replace("want to", "wanna")

        return self.convert_text(english_text)

    def get_pronunciation_confidence(self, word):
        """발음 변환 신뢰도 반환"""
        word = word.lower().strip()

        if word in self.word_dict:
            return 0.95  # 사전에 있는 단어는 높은 신뢰도

        # 규칙 기반 패턴이 적용되는지 확인
        rule_matches = sum(1 for pattern, _ in self.phonetic_rules if pattern in word)

        if rule_matches >= 2:
            return 0.8  # 여러 규칙이 적용되면 높은 신뢰도
        elif rule_matches == 1:
            return 0.6  # 하나의 규칙이 적용되면 중간 신뢰도
        else:
            return 0.3  # 추측 기반 변환은 낮은 신뢰도

    def batch_convert(self, word_list):
        """단어 목록 일괄 변환"""
        results = []
        for word in word_list:
            converted = self.convert_text(word)
            confidence = self.get_pronunciation_confidence(word)
            results.append({
                'original': word,
                'converted': converted,
                'confidence': confidence
            })
        return results

    def add_custom_word(self, english_word, korean_pronunciation):
        """사용자 정의 단어 추가"""
        self.word_dict[english_word.lower()] = korean_pronunciation
        print(f"✅ 사용자 단어 추가: {english_word} -> {korean_pronunciation}")

    def get_word_variants(self, base_word):
        """단어의 변형들 생성"""
        variants = {}
        base_pronunciation = self.word_dict.get(base_word.lower(),
                                               self.advanced_phonetic_conversion(base_word))

        # 복수형
        variants[f"{base_word}s"] = f"{base_pronunciation}스"

        # 과거형 (-ed)
        if not base_word.endswith('e'):
            variants[f"{base_word}ed"] = f"{base_pronunciation}드"
        else:
            variants[f"{base_word}d"] = f"{base_pronunciation}드"

        # 진행형 (-ing)
        if base_word.endswith('e'):
            variants[f"{base_word[:-1]}ing"] = f"{base_pronunciation[:-1]}잉"
        else:
            variants[f"{base_word}ing"] = f"{base_pronunciation}잉"

        # 부사형 (-ly)
        if base_word.endswith('y'):
            variants[f"{base_word[:-1]}ily"] = f"{base_pronunciation[:-1]}일리"
        else:
            variants[f"{base_word}ly"] = f"{base_pronunciation}리"

        return variants

    def analyze_pronunciation_patterns(self, text):
        """발음 패턴 분석"""
        words = re.findall(r'\b\w+\b', text.lower())
        analysis = {
            'total_words': len(words),
            'dictionary_matches': 0,
            'rule_based_conversions': 0,
            'guessed_conversions': 0,
            'confidence_distribution': {'high': 0, 'medium': 0, 'low': 0}
        }

        for word in words:
            confidence = self.get_pronunciation_confidence(word)

            if word in self.word_dict:
                analysis['dictionary_matches'] += 1
            elif any(pattern in word for pattern, _ in self.phonetic_rules):
                analysis['rule_based_conversions'] += 1
            else:
                analysis['guessed_conversions'] += 1

            if confidence >= 0.8:
                analysis['confidence_distribution']['high'] += 1
            elif confidence >= 0.5:
                analysis['confidence_distribution']['medium'] += 1
            else:
                analysis['confidence_distribution']['low'] += 1

        return analysis

    def suggest_improvements(self, word):
        """발음 개선 제안"""
        word = word.lower().strip()
        suggestions = []

        if word not in self.word_dict:
            # 유사한 단어 찾기
            similar_words = []
            for dict_word in self.word_dict.keys():
                if len(word) == len(dict_word):
                    differences = sum(1 for a, b in zip(word, dict_word) if a != b)
                    if differences <= 2:  # 2글자 이하 차이
                        similar_words.append(dict_word)

            if similar_words:
                suggestions.append(f"유사한 단어들: {', '.join(similar_words[:3])}")

            # 발음 규칙 제안
            applicable_rules = [pattern for pattern, _ in self.phonetic_rules if pattern in word]
            if applicable_rules:
                suggestions.append(f"적용된 규칙들: {', '.join(applicable_rules)}")

            confidence = self.get_pronunciation_confidence(word)
            suggestions.append(f"변환 신뢰도: {confidence:.2f}")

        return suggestions

    def export_dictionary(self, filename="custom_pronunciation_dict.json"):
        """사용자 사전 내보내기"""
        try:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.word_dict, f, ensure_ascii=False, indent=2)
            print(f"✅ 사전 내보내기 완료: {filename}")
        except Exception as e:
            print(f"❌ 사전 내보내기 실패: {e}")

    def import_dictionary(self, filename="custom_pronunciation_dict.json"):
        """사용자 사전 가져오기"""
        try:
            import json
            with open(filename, 'r', encoding='utf-8') as f:
                imported_dict = json.load(f)

            # 기존 사전과 병합
            original_size = len(self.word_dict)
            self.word_dict.update(imported_dict)
            new_size = len(self.word_dict)

            print(f"✅ 사전 가져오기 완료: {new_size - original_size}개 단어 추가")
        except Exception as e:
            print(f"❌ 사전 가져오기 실패: {e}")

    def create_pronunciation_report(self, text):
        """발음 변환 보고서 생성"""
        converted = self.convert_text(text)
        analysis = self.analyze_pronunciation_patterns(text)

        report = f"""
📊 발음 변환 보고서
================

📝 원문: {text}
🔊 변환: {converted}

📈 통계:
- 총 단어 수: {analysis['total_words']}
- 사전 매칭: {analysis['dictionary_matches']}개
- 규칙 기반: {analysis['rule_based_conversions']}개  
- 추측 변환: {analysis['guessed_conversions']}개

🎯 신뢰도 분포:
- 높음 (80%+): {analysis['confidence_distribution']['high']}개
- 중간 (50-80%): {analysis['confidence_distribution']['medium']}개
- 낮음 (50% 미만): {analysis['confidence_distribution']['low']}개

💡 전체 신뢰도: {(analysis['dictionary_matches'] + analysis['rule_based_conversions'] * 0.7) / analysis['total_words'] * 100:.1f}%
"""
        return report


# 사용 예시 및 테스트 함수들
def test_pronunciation_converter():
    """발음 변환기 테스트"""
    converter = EnglishToKoreanPronunciation()

    test_sentences = [
        "Hello, how are you today?",
        "I'm going to the store to buy some food.",
        "The weather is really nice and sunny.",
        "She's working on her computer right now.",
        "We'll meet at the restaurant at seven o'clock.",
        "Can you help me with this difficult problem?",
        "The children are playing in the beautiful garden.",
        "I'd like to order a hamburger and french fries, please.",
        "Technology is changing our lives very quickly.",
        "Happy birthday! I hope you have a wonderful day!"
    ]

    print("🧪 발음 변환기 테스트")
    print("=" * 60)

    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{i}. 원문: {sentence}")
        converted = converter.convert_text(sentence)
        print(f"   변환: {converted}")

        # 분석 정보
        analysis = converter.analyze_pronunciation_patterns(sentence)
        confidence = (analysis['dictionary_matches'] + analysis['rule_based_conversions'] * 0.7) / analysis['total_words'] * 100
        print(f"   신뢰도: {confidence:.1f}%")

def demo_advanced_features():
    """고급 기능 데모"""
    converter = EnglishToKoreanPronunciation()

    print("\n🚀 고급 기능 데모")
    print("=" * 40)

    # 사용자 단어 추가
    print("\n1. 사용자 단어 추가:")
    converter.add_custom_word("smartphone", "스마트폰")
    converter.add_custom_word("blockchain", "블록체인")

    # 단어 변형 생성
    print("\n2. 단어 변형 생성:")
    variants = converter.get_word_variants("play")
    for variant, pronunciation in variants.items():
        print(f"   {variant} -> {pronunciation}")

    # 발음 보고서
    print("\n3. 발음 변환 보고서:")
    sample_text = "I love technology and smartphones!"
    report = converter.create_pronunciation_report(sample_text)
    print(report)


if __name__ == "__main__":
    # 메인 테스트 실행
    test_pronunciation_converter()
    demo_advanced_features()