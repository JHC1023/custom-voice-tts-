# custom-voice-tts 🎙️

실시간 음성 입력 및 번역 기능을 갖춘 다목적 한국어 음성 합성(TTS) 프로젝트입니다. 이 프로젝트는 `voice_recorder`를 통해 나만의 목소리를 녹음하고, Glow-TTS와 HiFi-GAN 모델을 직접 훈련하여 자연스러운 커스텀 음성을 생성하는 전체 과정을 지원합니다.

## ✨ 주요 기능

- **커스텀 목소리 훈련**: 자신만의 목소리를 녹음하여 TTS 모델을 처음부터 훈련할 수 있습니다.
- **고품질 한국어 TTS**: 훈련된 Glow-TTS와 HiFi-GAN을 사용하여 자연스러운 음성을 생성합니다.
- **실시간 음성 입력**: 마이크를 통해 한국어 음성을 입력받습니다.
- **두 가지 작동 모드**:
    1.  **직접 모드**: 입력된 한국어 텍스트를 바로 음성으로 합성합니다.
    2.  **번역 모드**: 한국어 음성을 영어로 번역하고, 번역된 영어를 다시 한글 발음으로 변환한 뒤 음성으로 합성합니다.

---

## 🚀 나만의 목소리 모델 만들기 및 사용법

이 가이드는 프로젝트를 처음 설정하는 것부터 자신만의 목소리로 음성을 생성하기까지의 전체 과정을 안내합니다.

### 1단계: 설치 및 초기 설정

1.  **이 저장소 복제(Clone)하기:**
    ```bash
    git clone https://github.com/JHC1023/custom-voice-tts-.git
    cd custom-voice-tts
    ```

2.  **의존성 라이브러리 복제:**
    이 프로젝트는 두 개의 외부 라이브러리를 필요로 합니다. 프로젝트 폴더 내에 직접 클론해주세요.
    - **Coqui TTS (SCE-TTS Fork)**:
      ```bash
      git clone https://github.com/sce-tts/TTS.git
      ```
    - **English-Korean Transliteration**:
      ```bash
      git clone https://github.com/muik/transliteration.git
      ```

3.  **필요 파이썬 패키지 설치:**
    메인 애플리케이션에 필요한 패키지를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

### 2단계: 목소리 데이터셋 생성

`voice_recorder` 디렉토리의 스크립트를 사용하여 모델 훈련에 필요한 음성 데이터셋을 만듭니다.

1.  **녹음용 패키지 설치:**
    ```bash
    pip install -r voice_recorder/requirements.txt
    ```

2.  **녹음용 문장 준비:**
    `voice_recorder` 폴더의 `prompts.example.csv` 파일을 `recording_prompts.csv` 라는 이름으로 복사합니다. 그 후, `recording_prompts.csv` 파일을 열어 직접 녹음하고 싶은 자신만의 문장으로 수정하거나 추가합니다.

3.  **녹음 스크립트 실행:**
    ```bash
    python voice_recorder/create_dataset.py
    ```
    - 스크립트의 안내에 따라 `recording_prompts.csv`에 있는 문장을 읽고 녹음합니다.
    - 녹음이 완료되면 `voice_recorder` 폴더 안에 음성 파일(`recordings/`), 학습용 목록 파일(`metadata.csv`, `ljs_audio_text_val_filelist.txt`)이 생성됩니다.

### 3단계: 모델 훈련

이제 생성된 데이터셋으로 Glow-TTS와 HiFi-GAN 모델을 훈련시킵니다.

1.  **훈련 데이터 배치:**
    2단계에서 생성된 결과물들을 학습 스크립트가 인식할 수 있도록 `data/filelists/` 폴더로 이동시킵니다.
    - `voice_recorder/recordings` 폴더의 모든 `.wav` 파일을 `data/filelists/wavs/` 폴더로 복사합니다.
    - `voice_recorder`에서 생성된 `metadata.csv`와 `ljs_audio_text_val_filelist.txt` 파일을 `data/filelists/` 폴더로 복사합니다.

2.  **훈련 스크립트 실행:**
    `train_glowtts.py`와 `train_hifigan.py` 스크립트를 사용하여 모델을 학습시킵니다.
    *(참고: 모델 훈련은 고사양 GPU가 필요하며, 상당한 시간이 소요될 수 있습니다. Google Colab과 같은 클라우드 환경에서 실행하는 것을 권장합니다.)*

### 4단계: 최종 애플리케이션 실행

모델 훈련이 완료되면, 최종 결과물을 사용하여 메인 프로그램을 실행할 수 있습니다.

1.  **훈련된 모델 배치:**
    3단계의 훈련 과정에서 생성된 최종 모델 폴더(날짜와 해시값 포함)를 `data/` 디렉토리 안으로 복사합니다. 최종적으로 아래와 같은 구조가 되어야 합니다.
    ```
    data/
    ├── glowtts-v2/
    │   └── glowtts-v2-[DATE]_[HASH]/
    │       ├── best_model.pth.tar
    │       └── config.json
    └── hifigan-v2/
        └── hifigan-v2-[DATE]_[HASH]/
            ├── best_model.pth.tar
            └── config.json
    ```

2.  **메인 프로그램 실행:**
    ```bash
    python main.py
    ```
    - 프로그램이 시작되면 안내에 따라 '직접 한국어 모드' 또는 '번역 모드'를 선택하여 자신의 목소리로 생성된 음성을 확인할 수 있습니다.

---

## 💬 참고 및 감사의 글 (References & Acknowledgements)

이 프로젝트는 [SCE-TTS 프로젝트](https://sce-tts.github.io/)를 깊이 참고하여 제작되었습니다. 복잡한 라이선스 환경 속에서도 훌륭한 결과물을 오픈소스로 공개해주신 원작자 및 기여자들께 감사드립니다.

---

## 📄 라이선스 (License)

이 프로젝트에서 직접 작성된 코드(`main.py`, `audio_handler.py` 등)는 **MIT 라이선스**에 따라 배포됩니다.

단, 이 프로젝트는 여러 오픈소스 구성요소에 의존하고 있으며, 각 구성요소는 자체 라이선스를 따릅니다. 이 프로젝트를 사용하시는 분은 아래의 라이선스들을 모두 준수해야 합니다.

- **Coqui TTS:** `Mozilla Public License 2.0`
- **g2pK:** `Apache License 2.0`
- **mimic-recording-studio:** `Apache License 2.0`
- **한국어 데이터 원본 (AI Hub):** `CC-BY 2.0`

전체적인 라이선스에 대한 자세한 정보는 SCE-TTS 프로젝트의 원본 정보를 참고해 주시기 바랍니다.

2.  **의존성 라이브러리 복제:**
    이 프로젝트는 두 개의 외부 라이브러리를 필요로 합니다. 프로젝트 폴더 내에 직접 클론해주세요.
    - **Coqui TTS (SCE-TTS Fork)**:
      ```bash
      git clone https://github.com/sce-tts/TTS.git
      ```
    - **English-Korean Transliteration**:
      ```bash
      git clone https://github.com/muik/transliteration.git
      ```

3.  **필요 파이썬 패키지 설치:**
    메인 애플리케이션에 필요한 패키지를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

### 2단계: 목소리 데이터셋 생성

`voice_recorder` 디렉토리의 스크립트를 사용하여 모델 훈련에 필요한 음성 데이터셋을 만듭니다.

1.  **녹음용 패키지 설치:**
    ```bash
    pip install -r voice_recorder/requirements.txt
    ```

2.  **녹음용 문장 준비:**
    `voice_recorder` 폴더의 `prompts.example.csv` 파일을 `recording_prompts.csv` 라는 이름으로 복사합니다. 그 후, `recording_prompts.csv` 파일을 열어 직접 녹음하고 싶은 자신만의 문장으로 수정하거나 추가합니다.

3.  **녹음 스크립트 실행:**
    ```bash
    python voice_recorder/create_dataset.py
    ```
    - 스크립트의 안내에 따라 `recording_prompts.csv`에 있는 문장을 읽고 녹음합니다.
    - 녹음이 완료되면 `voice_recorder` 폴더 안에 음성 파일(`recordings/`), 학습용 목록 파일(`metadata.csv`, `ljs_audio_text_val_filelist.txt`)이 생성됩니다.

### 3단계: 모델 훈련

이제 생성된 데이터셋으로 Glow-TTS와 HiFi-GAN 모델을 훈련시킵니다.

1.  **훈련 데이터 배치:**
    2단계에서 생성된 결과물들을 학습 스크립트가 인식할 수 있도록 `data/filelists/` 폴더로 이동시킵니다.
    - `voice_recorder/recordings` 폴더의 모든 `.wav` 파일을 `data/filelists/wavs/` 폴더로 복사합니다.
    - `voice_recorder`에서 생성된 `metadata.csv`와 `ljs_audio_text_val_filelist.txt` 파일을 `data/filelists/` 폴더로 복사합니다.

2.  **훈련 스크립트 실행:**
    `train_glowtts.py`와 `train_hifigan.py` 스크립트를 사용하여 모델을 학습시킵니다.
    *(참고: 모델 훈련은 고사양 GPU가 필요하며, 상당한 시간이 소요될 수 있습니다. Google Colab과 같은 클라우드 환경에서 실행하는 것을 권장합니다.)*

### 4단계: 최종 애플리케이션 실행

모델 훈련이 완료되면, 최종 결과물을 사용하여 메인 프로그램을 실행할 수 있습니다.

1.  **훈련된 모델 배치:**
    3단계의 훈련 과정에서 생성된 최종 모델 폴더(날짜와 해시값 포함)를 `data/` 디렉토리 안으로 복사합니다. 최종적으로 아래와 같은 구조가 되어야 합니다.
    ```
    data/
    ├── glowtts-v2/
    │   └── glowtts-v2-[DATE]_[HASH]/
    │       ├── best_model.pth.tar
    │       └── config.json
    └── hifigan-v2/
        └── hifigan-v2-[DATE]_[HASH]/
            ├── best_model.pth.tar
            └── config.json
    ```

2.  **메인 프로그램 실행:**
    ```bash
    python main.py
    ```
    - 프로그램이 시작되면 안내에 따라 '직접 한국어 모드' 또는 '번역 모드'를 선택하여 자신의 목소리로 생성된 음성을 확인할 수 있습니다.

---

---

## 💬 참고 및 감사의 글 (References & Acknowledgements)

이 프로젝트는 [SCE-TTS 프로젝트](https://sce-tts.github.io/)의 연구와 코드를 깊이 참고하여 제작되었습니다. 훌륭한 오픈소스 프로젝트에 감사드립니다.

---

## 📄 라이선스

이 프로젝트는 현재 라이선스가 지정되어 있지 않습니다. 필요에 따라 MIT, Apache 2.0 등 적절한 라이선스를 추가하는 것을 고려해볼 수 있습니다.
