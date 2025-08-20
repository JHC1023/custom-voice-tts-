# custom-voice-tts 🎙️

실시간 음성 입력 및 번역 기능을 갖춘 다목적 한국어 음성 합성(TTS) 프로젝트입니다. 이 프로젝트는 커스텀으로 학습된 Glow-TTS와 HiFi-GAN 모델을 사용하여 자연스러운 한국어 음성을 생성합니다.

## ✨ 주요 기능

- **고품질 한국어 TTS**: Glow-TTS와 HiFi-GAN을 사용하여 음성을 생성합니다.
- **실시간 음성 입력**: 마이크를 통해 한국어 음성을 입력받습니다.
- **두 가지 작동 모드**:
    1.  **직접 모드**: 입력된 한국어 텍스트를 바로 음성으로 합성합니다.
    2.  **번역 모드**: 한국어 음성을 영어로 번역하고, 번역된 영어를 다시 한글 발음으로 변환한 뒤 음성으로 합성합니다.
- **모듈화된 코드**: 오디오 처리, 모델 로딩, 텍스트 변환 등 기능별로 체계적으로 코드가 분리되어 이해하기 쉽습니다.

---

## 🛠️ 설치 및 설정 방법

### 1. 준비물

- Python 3.8 이상
- Git

### 2. 이 저장소 복제(Clone)하기

```bash
git clone https://github.com/[your-username]/custom-voice-tts.git
cd custom-voice-tts
```
*(참고: `[your-username]` 부분은 실제 GitHub 사용자 이름으로 변경해주세요.)*

### 3. 의존성 라이브러리 설치

이 프로젝트는 두 개의 외부 라이브러리를 필요로 합니다. 프로젝트 폴더 내에 직접 클론해주세요.

- **Coqui TTS (SCE-TTS Fork)**:
  ```bash
  git clone https://github.com/sce-tts/TTS.git
  ```
- **English-Korean Transliteration**:
  ```bash
  git clone https://github.com/muik/transliteration.git
  ```

위 라이브러리들을 클론한 후, 필요한 파이썬 패키지들을 설치합니다.

```bash
pip install -r requirements.txt
```

### 4. 데이터 및 모델 준비

#### 모델
애플리케이션을 실행하려면 미리 학습된 모델이 필요합니다. `data/` 디렉토리 안에 아래와 같은 구조로 Glow-TTS와 HiFi-GAN 모델을 위치시켜 주세요.

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

#### 학습 데이터 (모델 학습 시)
만약 제공된 스크립트로 직접 모델을 학습시키려면, LJSpeech 형식의 데이터셋이 필요합니다. `data/` 디렉토리 안에 아래와 같은 구조로 학습 데이터 파일리스트를 준비해주세요.

```
data/
└── filelists/
    ├── ljs_audio_text_train_filelist.txt
    ├── ljs_audio_text_val_filelist.txt
    ├── metadata.csv
    └── wavs/
        ├── audio1.wav
        └── ...
```
- `.txt` 파일들은 각 오디오 파일 경로와 그에 해당하는 텍스트를 연결하는 목록입니다.
- `wavs` 폴더는 모든 `.wav` 오디오 파일을 포함합니다.

---

## 🚀 사용 방법

터미널에서 메인 애플리케이션을 실행합니다.

```bash
python main.py
```

프로그램이 시작되면 두 가지 모드를 선택할 수 있습니다.

- **번역 모드 (기본)**: `Enter` 키를 눌러 시작합니다. 한국어로 말하면, 프로그램이 영어로 번역 후 다시 한글 발음으로 변환하여 음성으로 출력합니다.
- **직접 한국어 모드**: `k`를 입력하고 `Enter` 키를 눌러 시작합니다. 한국어로 말하면, 프로그램이 해당 내용을 바로 음성으로 합성합니다.

프로그램을 종료하려면 "종료"라고 말하거나 터미널에서 `Ctrl+C`를 누르세요.

---

## 🗣️ 나만의 목소리로 TTS 모델 학습 및 사용하기

이 프로젝트는 `voice_recorder` 디렉토리에 포함된 스크립트를 통해 자신만의 목소리를 녹음하고, 그 데이터로 새로운 TTS 모델을 학습시키는 전체 과정을 지원합니다.

### 1단계: 목소리 데이터셋 생성

1.  **필요 라이브러리 설치:**
    먼저, 목소리 녹음에 필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r voice_recorder/requirements.txt
    ```

2.  **녹음용 문장 준비:**
    `voice_recorder` 폴더에 있는 `prompts.example.csv` 파일을 `recording_prompts.csv` 라는 이름으로 복사합니다. 그 후, `recording_prompts.csv` 파일을 열어 직접 녹음하고 싶은 자신만의 문장으로 수정하거나 추가합니다.

3.  **녹음 스크립트 실행:**
    다음 명령어로 녹음 스크립트를 실행합니다.
    ```bash
    python voice_recorder/create_dataset.py
    ```
    - 스크립트가 실행되면 `recording_prompts.csv`에 있는 문장들이 순서대로 화면에 나타납니다.
    - 안내에 따라 문장을 읽고 녹음을 진행하세요.
    - 녹음이 완료되면, 모델 학습에 필요한 `metadata.csv`와 `ljs_audio_text_val_filelist.txt` 파일이 `voice_recorder` 폴더 내에 자동으로 생성되고, 음성 파일은 `voice_recorder/recordings` 폴더에 저장됩니다.

### 2단계: 커스텀 모델 학습

- 1단계에서 생성된 데이터셋(`metadata.csv` 등)을 사용하여 `train_glowtts.py`와 `train_hifigan.py` 스크립트로 자신만의 TTS 모델을 학습시킵니다.
- `data/filelists/` 경로 아래에 1단계에서 생성된 파일들을 올바르게 배치하거나, 훈련 스크립트 내의 파일 경로를 수정해야 할 수 있습니다.


---

## 🧠 모델 학습

`train_glowtts.py`와 `train_hifigan.py` 스크립트를 사용하여 자신만의 커스텀 모델을 학습할 수 있습니다. 이 스크립트들은 본래 Google Colab 환경에 맞게 설계되었으며, 학습 환경 설정 및 과정에 필요한 명령어들을 포함하고 있습니다.

---

## 📄 라이선스

이 프로젝트는 현재 라이선스가 지정되어 있지 않습니다. 필요에 따라 MIT, Apache 2.0 등 적절한 라이선스를 추가하는 것을 고려해볼 수 있습니다.