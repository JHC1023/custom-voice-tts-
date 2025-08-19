"""
TTS 모델 로더 모듈 (개선된 버전)
"""
import os
import json
import torch


class TTSModelLoader:
    """TTS 모델 로딩 및 초기화를 담당하는 클래스"""

    def __init__(self, data_path):
        self.data_path = data_path
        self.glowtts_path = None
        self.hifigan_path = None
        self.glowtts_config = None
        self.hifigan_config = None
        self.glowtts_checkpoint = None
        self.hifigan_checkpoint = None
        self.models_loaded = False
        self.use_synthesizer = False
        self.synthesizer = None

    def find_model_paths(self):
        """모델 경로 자동 탐지"""
        if not self.data_path or not os.path.exists(self.data_path):
            return False

        try:
            # Glow-TTS 모델 경로 찾기
            glowtts_base = os.path.join(self.data_path, "glowtts-v2")
            if os.path.exists(glowtts_base):
                for folder in os.listdir(glowtts_base):
                    if folder.startswith("glowtts-v2-"):
                        self.glowtts_path = os.path.join(glowtts_base, folder)
                        break

            # HiFi-GAN 모델 경로 찾기
            hifigan_base = os.path.join(self.data_path, "hifigan-v2")
            if os.path.exists(hifigan_base):
                for folder in os.listdir(hifigan_base):
                    if folder.startswith("hifigan-v2-"):
                        self.hifigan_path = os.path.join(hifigan_base, folder)
                        break

            print(f"📁 Glow-TTS 경로: {self.glowtts_path}")
            print(f"📁 HiFi-GAN 경로: {self.hifigan_path}")

            return self.glowtts_path is not None and self.hifigan_path is not None

        except Exception as e:
            print(f"❌ 경로 탐지 실패: {e}")
            return False

    def find_checkpoint_files(self, model_path):
        """체크포인트 파일들 찾기 (중복 config 파일 제외)"""
        files = {'checkpoint': None, 'config': None}

        try:
            if not os.path.exists(model_path):
                return files

            print(f"   📁 스캔 중: {model_path}")

            for root, dirs, filenames in os.walk(model_path):
                for filename in filenames:
                    filepath = os.path.join(root, filename)

                    # 체크포인트 파일들 찾기
                    if filename.endswith(('.pth', '.pt', '.ckpt', '.pth.tar')):
                        if 'best_model' in filename.lower() or not files['checkpoint']:
                            files['checkpoint'] = filepath
                            print(f"      ✅ 체크포인트: {filename}")

                    # 원본 설정 파일만 찾기 (fixed 파일들 제외)
                    elif filename == 'config.json':  # 정확히 config.json만
                        files['config'] = filepath
                        print(f"      ✅ 설정 파일: {filename}")

        except Exception as e:
            print(f"⚠️ 파일 스캔 실패: {e}")

        return files

    def cleanup_old_config_files(self, model_path):
        """기존의 fixed config 파일들 정리"""
        try:
            if not os.path.exists(model_path):
                return

            cleaned_count = 0
            for root, dirs, filenames in os.walk(model_path):
                for filename in filenames:
                    # config_fixed로 시작하는 파일들 삭제
                    if filename.startswith('config_fixed') and filename.endswith('.json'):
                        filepath = os.path.join(root, filename)
                        try:
                            os.remove(filepath)
                            cleaned_count += 1
                        except:
                            pass  # 삭제 실패해도 계속 진행

            if cleaned_count > 0:
                print(f"      🧹 기존 config 파일 {cleaned_count}개 정리 완료")

        except Exception as e:
            print(f"⚠️ config 파일 정리 실패: {e}")

    def fix_config_paths(self, config, model_path):
        """설정 파일의 Colab 경로들을 로컬 경로로 수정"""
        try:
            print(f"      🔧 경로 수정 중...")

            colab_indicators = ['/content/drive/My Drive', '/content/', 'Colab Notebooks']

            def fix_paths_recursive(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, str):
                            if any(indicator in value for indicator in colab_indicators):
                                filename = os.path.basename(value)
                                new_path = self.find_file_in_model_path(model_path, filename)
                                if new_path and os.path.exists(new_path):
                                    obj[key] = new_path
                                    print(f"      ✅ 경로 수정: {key}")
                                else:
                                    obj[key] = None
                                    print(f"      ⚠️ 파일 없음: {key}")
                        elif isinstance(value, (dict, list)):
                            fix_paths_recursive(value)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        if isinstance(item, str):
                            if any(indicator in item for indicator in colab_indicators):
                                filename = os.path.basename(item)
                                new_path = self.find_file_in_model_path(model_path, filename)
                                if new_path and os.path.exists(new_path):
                                    obj[i] = new_path
                                else:
                                    obj[i] = None
                        elif isinstance(item, (dict, list)):
                            fix_paths_recursive(item)

            fix_paths_recursive(config)
            return config

        except Exception as e:
            print(f"      ❌ 경로 수정 실패: {e}")
            return config

    def find_file_in_model_path(self, model_path, filename):
        """모델 경로에서 파일 찾기"""
        try:
            search_paths = [model_path, os.path.dirname(model_path), self.data_path]

            for search_path in search_paths:
                if not search_path or not os.path.exists(search_path):
                    continue

                for root, dirs, files in os.walk(search_path):
                    if filename in files:
                        return os.path.join(root, filename)
            return None

        except Exception as e:
            print(f"         ❌ 파일 검색 실패: {e}")
            return None

    def load_config_file(self, config_path, model_type="glowtts"):
        """설정 파일 로드 및 경로 수정 (고정된 파일명 사용)"""
        try:
            print(f"      📂 {model_type} 설정 로딩 중: {os.path.basename(config_path)}")

            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 경로 수정
            if model_type == "glowtts":
                config = self.fix_config_paths(config, self.glowtts_path)
            else:
                config = self.fix_config_paths(config, self.hifigan_path)

            # 수정된 config를 고정된 이름으로 저장
            self.save_fixed_config(config, config_path, model_type)

            print(f"      ⚙️ {model_type} 설정 로드 완료!")
            return config

        except Exception as e:
            print(f"      ❌ {model_type} 설정 로드 실패: {e}")
            return None

    def save_fixed_config(self, config, original_path, model_type):
        """수정된 설정을 고정된 파일명으로 저장"""
        try:
            dir_name = os.path.dirname(original_path)
            # 고정된 파일명 사용 (더 이상 중복 생성 안됨)
            temp_config_path = os.path.join(dir_name, f"config_{model_type}_runtime.json")

            with open(temp_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"      💾 런타임 설정 파일 저장: {os.path.basename(temp_config_path)}")

            # 경로 업데이트
            if model_type == "glowtts":
                self.glowtts_config_path = temp_config_path
            else:
                self.hifigan_config_path = temp_config_path

        except Exception as e:
            print(f"      ⚠️ 런타임 설정 파일 저장 실패: {e}")
            if model_type == "glowtts":
                self.glowtts_config_path = original_path
            else:
                self.hifigan_config_path = original_path

    def load_models(self):
        """TTS 모델들 로드"""
        try:
            if not self.find_model_paths():
                print("⚠️ TTS 모델 경로를 찾을 수 없습니다.")
                return False

            print("🤖 TTS 모델들 로드 중...")

            # 기존 fixed config 파일들 정리
            self.cleanup_old_config_files(self.glowtts_path)
            self.cleanup_old_config_files(self.hifigan_path)

            # 파일들 찾기
            glowtts_files = self.find_checkpoint_files(self.glowtts_path)
            hifigan_files = self.find_checkpoint_files(self.hifigan_path)

            # 체크포인트 로드
            if glowtts_files['checkpoint']:
                print(f"   📦 Glow-TTS 체크포인트: {os.path.basename(glowtts_files['checkpoint'])}")
                self.glowtts_checkpoint = torch.load(glowtts_files['checkpoint'], map_location='cpu')

            if glowtts_files['config']:
                print(f"   ⚙️ Glow-TTS 설정: {os.path.basename(glowtts_files['config'])}")
                self.glowtts_config = self.load_config_file(glowtts_files['config'], "glowtts")

            if hifigan_files['checkpoint']:
                print(f"   📦 HiFi-GAN 체크포인트: {os.path.basename(hifigan_files['checkpoint'])}")
                self.hifigan_checkpoint = torch.load(hifigan_files['checkpoint'], map_location='cpu')

            if hifigan_files['config']:
                print(f"   ⚙️ HiFi-GAN 설정: {os.path.basename(hifigan_files['config'])}")
                self.hifigan_config = self.load_config_file(hifigan_files['config'], "hifigan")

            # 모델 초기화
            if (self.glowtts_checkpoint and self.hifigan_checkpoint and
                    self.glowtts_config and self.hifigan_config):
                print("🚀 TTS 모델 초기화 중...")
                return self.initialize_synthesizer()
            else:
                print("⚠️ 일부 모델 파일을 찾을 수 없습니다.")
                return False

        except Exception as e:
            print(f"❌ TTS 모델 로드 실패: {e}")
            return False

    def initialize_synthesizer(self):
        """TTS Synthesizer 초기화"""
        try:
            from TTS.utils.synthesizer import Synthesizer
            print("   ✅ TTS Synthesizer import 성공")

            # 체크포인트 파일 경로들
            glowtts_files = self.find_checkpoint_files(self.glowtts_path)
            hifigan_files = self.find_checkpoint_files(self.hifigan_path)

            # 런타임 config 파일 경로 사용
            glowtts_config_path = getattr(self, 'glowtts_config_path', glowtts_files['config'])
            hifigan_config_path = getattr(self, 'hifigan_config_path', hifigan_files['config'])

            self.synthesizer = Synthesizer(
                glowtts_files['checkpoint'],
                glowtts_config_path,
                None,
                hifigan_files['checkpoint'],
                hifigan_config_path,
                None,
                None,
                False,
            )

            print(f"   ✅ Synthesizer 초기화 완료!")
            self.models_loaded = True
            self.use_synthesizer = True
            return True

        except Exception as e:
            print(f"   ❌ Synthesizer 초기화 실패: {e}")
            self.models_loaded = False
            self.use_synthesizer = False
            return False

    def normalize_text(self, text):
        """텍스트 정규화"""
        try:
            import re

            # 기본 정리
            text = text.strip()

            # 문장부호 정리
            for c in ",;:":
                text = text.replace(c, ".")

            # 영어 알파벳을 한글로 변환
            alphabet_map = {
                'a': '에이', 'b': '비', 'c': '씨', 'd': '디', 'e': '이', 'f': '에프',
                'g': '쥐', 'h': '에이치', 'i': '아이', 'j': '제이', 'k': '케이', 'l': '엘',
                'm': '엠', 'n': '엔', 'o': '오', 'p': '피', 'q': '큐', 'r': '알',
                's': '에스', 't': '티', 'u': '유', 'v': '브이', 'w': '더블유', 'x': '엑스',
                'y': '와이', 'z': '지'
            }

            for eng, kor in alphabet_map.items():
                text = re.sub(f'({eng}|{eng.upper()})', kor, text)

            # 마침표 추가
            if text and text[-1] not in '.!?':
                text += '.'

            return text

        except Exception as e:
            print(f"   ⚠️ 정규화 실패: {e}")
            return text

    def synthesize(self, text):
        """텍스트를 음성으로 합성"""
        if not self.models_loaded or not self.use_synthesizer:
            return None

        try:
            normalized_text = self.normalize_text(text)
            wav = self.synthesizer.tts(normalized_text, None, None)
            return wav
        except Exception as e:
            print(f"❌ 음성 합성 실패: {e}")
            return None

    def cleanup_runtime_files(self):
        """프로그램 종료 시 런타임 파일들 정리 (선택사항)"""
        try:
            paths_to_clean = [
                getattr(self, 'glowtts_config_path', None),
                getattr(self, 'hifigan_config_path', None)
            ]

            cleaned_count = 0
            for path in paths_to_clean:
                if path and os.path.exists(path) and 'runtime' in path:
                    try:
                        os.remove(path)
                        cleaned_count += 1
                    except:
                        pass

            if cleaned_count > 0:
                print(f"🧹 런타임 파일 {cleaned_count}개 정리 완료")

        except Exception as e:
            print(f"⚠️ 런타임 파일 정리 실패: {e}")

    def __del__(self):
        """소멸자 - 런타임 파일 자동 정리"""
        try:
            self.cleanup_runtime_files()
        except:
            pass  # 소멸자에서는 예외 무시