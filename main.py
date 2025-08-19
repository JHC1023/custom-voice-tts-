"""
메인 번역기 모듈
"""
import os
import time
from googletrans import Translator

# 모듈 임포트
from pronunciation_converter import EnglishToKoreanPronunciation
from tts_model_loader import TTSModelLoader
from audio_handler import AudioHandler


class KoreanVoiceTTSTranslator:
    """한국어 TTS 번역기 메인 클래스"""

    def __init__(self, data_path=None):
        """한국어 TTS 모델을 사용한 번역기 초기화"""
        print("🚀 한국어 TTS 음성 번역기 시작...")

        # 번역기 초기화
        self.translator = Translator()

        # 영어->한글 발음 변환기 초기화
        self.pronunciation_converter = EnglishToKoreanPronunciation()

        # TTS 모델 로더 초기화
        self.tts_loader = TTSModelLoader(data_path)
        self.models_loaded = self.tts_loader.load_models()

        # 오디오 핸들러 초기화
        self.audio_handler = AudioHandler()

        print("✅ 초기화 완료!")

    def translate_to_english(self, korean_text):
        """한국어를 영어로 번역"""
        try:
            print("🌍 영어로 번역 중...")
            result = self.translator.translate(korean_text, src='ko', dest='en')
            english_text = result.text
            print(f"🔤 번역 결과: {english_text}")
            return english_text
        except Exception as e:
            print(f"❌ 번역 오류: {e}")
            return None

    def convert_english_to_hangul_pronunciation(self, english_text):
        """영어를 한글 발음으로 변환"""
        print("🔄 영어를 한글 발음으로 변환 중...")
        hangul_pronunciation = self.pronunciation_converter.convert_text(english_text)
        print(f"🎵 한글 발음: {hangul_pronunciation}")
        return hangul_pronunciation

    def synthesize_speech(self, hangul_text):
        """한글 텍스트를 음성 합성"""
        try:
            print("🎤 음성 합성 중...")
            print(f"📝 입력 텍스트: {hangul_text}")

            if not self.models_loaded:
                print("🎵 TTS 시뮬레이션 모드")
                print(f"🔊 텍스트 출력: {hangul_text}")
                return

            # TTS 모델로 음성 합성
            wav = self.tts_loader.synthesize(hangul_text)

            if wav is not None:
                print(f"✅ 음성 합성 완료 (길이: {len(wav)} samples)")
                print("🎵 오디오 출력 중...")
                self.audio_handler.play_audio(wav, 22050)
                print(f"🔊 음성 합성 완료: {hangul_text}")
            else:
                print("🎵 TTS 시뮬레이션 모드")
                print(f"🔊 텍스트 출력: {hangul_text}")

        except Exception as e:
            print(f"❌ 음성 합성 오류: {e}")
            print(f"🔊 텍스트 출력: {hangul_text}")

    def run_translation_loop(self):
        """번역 반복 실행"""
        print("\n" + "=" * 60)
        print("🎯 한국어 TTS 번역기")
        print("1️⃣ 한국어 → 영어 번역 → 한글 발음 → TTS")
        print("2️⃣ 한국어 직접 → TTS (번역 없이)")
        print("종료하려면 'quit', 'exit', '종료'라고 말하세요")
        print("=" * 60)

        while True:
            try:
                # 모드 선택
                print("\n🔤 모드를 선택하세요:")
                print("   [Enter] - 번역 모드 (한국어 → 영어 번역 → TTS)")
                print("   'k' + [Enter] - 한국어 모드 (한국어 → 직접 TTS)")

                mode_input = input("   모드 선택: ").strip().lower()

                if mode_input == 'k':
                    # 한국어 직접 모드
                    print("\n🇰🇷 한국어 직접 TTS 모드")
                    result = self.korean_direct_mode()
                    if result == 'exit':
                        break
                else:
                    # 번역 모드 (기본)
                    print("\n🌍 번역 모드")
                    result = self.translation_mode()
                    if result == 'exit':
                        break

            except KeyboardInterrupt:
                print("\n👋 번역기를 종료합니다.")
                break
            except Exception as e:
                print(f"❌ 예상치 못한 오류: {e}")
                print("💡 계속 진행합니다...")

    def korean_direct_mode(self):
        """한국어 직접 TTS 모드"""
        print("🗣️  한국어로 말해주세요 (직접 TTS)...")

        korean_text = self.audio_handler.listen_korean()

        if korean_text is None:
            print("💡 다시 시도해주세요...")
            return

        # 종료 명령 확인
        if korean_text.lower() in ['quit', 'exit', '종료', '끝', '그만']:
            print("👋 번역기를 종료합니다.")
            return 'exit'

        print(f"📝 한국어 원문: {korean_text}")

        # 한국어 직접 TTS
        self.synthesize_speech(korean_text)

        print("\n" + "-" * 40)
        time.sleep(1)

    def translation_mode(self):
        """번역 모드"""
        print("🗣️  한국어로 말해주세요 (번역 후 TTS)...")

        korean_text = self.audio_handler.listen_korean()

        if korean_text is None:
            print("💡 다시 시도해주세요...")
            return

        # 종료 명령 확인
        if korean_text.lower() in ['quit', 'exit', '종료', '끝', '그만']:
            print("👋 번역기를 종료합니다.")
            return 'exit'

        # 영어로 번역
        english_text = self.translate_to_english(korean_text)

        if english_text:
            # 영어를 한글 발음으로 변환
            hangul_pronunciation = self.convert_english_to_hangul_pronunciation(english_text)

            # 한글 발음을 TTS
            self.synthesize_speech(hangul_pronunciation)
        else:
            print("❌ 번역에 실패했습니다.")

        print("\n" + "-" * 40)
        time.sleep(1)


def main():
    """메인 실행 함수"""
    try:
        # 데이터 경로 설정
        data_path = r"C:\Users\KimJoungMin\PycharmProjects\fianl_tts\data"

        print(f"📁 TTS 모델 데이터 경로: {data_path}")

        if not os.path.exists(data_path):
            print(f"❌ 경로가 존재하지 않습니다: {data_path}")
            return

        # 번역기 생성 및 실행
        translator = KoreanVoiceTTSTranslator(data_path)
        translator.run_translation_loop()

    except Exception as e:
        print(f"❌ 초기화 실패: {e}")


if __name__ == "__main__":
    main()
