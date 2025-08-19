"""
오디오 입출력 처리 모듈
"""
import speech_recognition as sr
import time
import numpy as np


class AudioHandler:
    """오디오 입출력을 담당하는 클래스"""

    def __init__(self):
        # 음성 인식기 초기화
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # 마이크 보정
        self.calibrate_microphone()

    def calibrate_microphone(self):
        """마이크 보정"""
        print("🎤 마이크 환경소음 보정 중...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=3)
                self.recognizer.dynamic_energy_threshold = True
            print("✅ 마이크 보정 완료!")
        except Exception as e:
            print(f"❌ 마이크 보정 실패: {e}")

    def listen_korean(self):
        """한국어 음성 인식"""
        print("\n🗣️  한국어로 말해주세요...")

        try:
            with self.microphone as source:
                print("   🔴 듣고 있습니다...")
                audio = self.recognizer.listen(source, timeout=20, phrase_time_limit=15)
                print("   ⚫ 녹음 완료! 인식 중...")

            result = self.recognizer.recognize_google(audio, language='ko-KR')
            print(f"📝 인식된 한국어: {result}")
            return result

        except sr.WaitTimeoutError:
            print("   ⏰ 시간 초과")
            return None
        except Exception as e:
            print(f"   ❌ 음성 인식 실패: {e}")
            return None

    def play_audio(self, audio_array, sample_rate=22050):
        """생성된 오디오 재생"""
        try:
            try:
                import sounddevice as sd
                print(f"      🔊 오디오 재생 중... (샘플레이트: {sample_rate}Hz)")
                sd.play(audio_array, sample_rate)
                sd.wait()
                print("      ✅ 오디오 재생 완료")
            except ImportError:
                print("      ⚠️ sounddevice 없음. 파일로 저장합니다.")
                self.save_audio(audio_array, sample_rate)
        except Exception as e:
            print(f"      ❌ 오디오 재생 실패: {e}")
            try:
                self.save_audio(audio_array, sample_rate)
            except:
                print("      ❌ 오디오 저장도 실패")

    def save_audio(self, audio_array, sample_rate=22050):
        """생성된 오디오를 파일로 저장"""
        try:
            import scipy.io.wavfile as wavfile

            timestamp = int(time.time())
            filename = f"tts_output_{timestamp}.wav"

            # 오디오 정규화
            if np.max(np.abs(audio_array)) > 1.0:
                audio_array = audio_array / np.max(np.abs(audio_array))

            audio_16bit = (audio_array * 32767).astype(np.int16)
            wavfile.write(filename, sample_rate, audio_16bit)
            print(f"      💾 오디오 저장 완료: {filename}")
        except Exception as e:
            print(f"      ❌ 오디오 저장 실패: {e}")