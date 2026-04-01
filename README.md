# Vocabulary App

Ung dung hoc tu vung tieng Anh theo chu de, duoc xay dung de demo cach ap dung mot so design pattern trong backend voi FastAPI.

Project hien co 2 phan:
- `back-end`: FastAPI + PostgreSQL
- `front-end`: React + Vite

## Muc tieu

Backend tap trung vao 3 bai toan chinh:
- Lay danh sach tu vung theo chu de
- Danh dau tu da hoc theo `session_id`
- Sinh du lieu bai hoc theo tung che do hoc nhu `flashcard`, `multiple choice`, va danh sach on tap

## Design Patterns Dang Dung

### 1. Strategy Pattern

Duoc dung de quan ly cac `study mode`.

Hien tai co cac strategy:
- `FlashcardStudyModeStrategy`
- `MultipleChoiceStudyModeStrategy`

Interface chung:
- [study_mode_strategy.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/strategy/study_mode_strategy.py)

Context:
- [study_mode_context.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/strategy/study_mode_context.py)

Vai tro sau khi refactor:
- `service` lay du lieu tu vung
- `context` giu strategy hien tai
- `strategy` chi build payload tra ve cho frontend

Vi du:
- `FlashcardStudyModeStrategy` tra ve thong tin day du cua 1 tu
- `MultipleChoiceStudyModeStrategy` build payload gom `word`, `correct_answer`, `answers`

### 2. Factory Pattern

Duoc dung de quan ly bo tu vung theo chu de.

Hien tai co cac factory:
- `AnimalFactory`
- `FamilyFactory`
- `SchoolFactory`
- `TravelFactory`
- `WorkFactory`

Provider:
- [factory_provider.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/factory/factory_provider.py)

Vai tro:
- Chon factory theo `Topic`
- Lay du lieu tu vung tu database

### 3. Singleton Pattern

Duoc dung de luu tien trinh hoc theo `session_id`.

Class:
- [LearningProgressManager.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/singleton/LearningProgressManager.py)

Vai tro:
- Moi session co 1 danh sach tu da hoc rieng
- Dung cho demo khi chua co login/user_id
- Lam nguon du lieu cho review list / SR mode trong bo nho

### 4. Observer Pattern

Duoc dung de day du lieu realtime qua websocket khi danh sach tu da hoc thay doi.

Files:
- [IObserver.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/observer/IObserver.py)
- [ObserverLearnedProcess.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/observer/ObserverLearnedProcess.py)
- [websocket.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/core/websocket.py)

Flow:
- User hoc xong 1 tu
- `LearningProgressManager` cap nhat session
- Observer duoc notify
- WebSocket push list da hoc moi nhat ve frontend

## Cau truc chinh

```text
vocabulary_app/
|-- back-end/
|   |-- app/
|   |   |-- core/
|   |   |-- models/
|   |   |-- patterns/
|   |   |-- routes/
|   |   |-- services/
|   |   `-- main.py
|-- front-end/
|-- docker-compose.yml
`-- README.md
```

## Backend Flow

### 1. Hoc tu vung theo chu de

- Frontend goi API lay danh sach tu theo `topic`
- User hoc tung tu
- Khi hoc xong, frontend goi API `learned/add` de danh dau tu da hoc

### 2. Luu tien trinh hoc

- Backend dung `session_id` de phan biet nguoi hoc
- Moi tu da hoc duoc luu vao `LearningProgressManager`

### 3. Sinh exam object

Khi frontend can hien thi bai hoc:
- `service` lay `Vocabulary`
- chon `StudyModeStrategy`
- strategy build payload phu hop voi mode hoc

### 4. On tap

Hien tai API SR dang tra ve danh sach `word_id` da hoc theo `session_id`.

File:
- [SR_mode_strategy.py](/d:/Extend/DP/FINAL/vocabulary_app/back-end/app/patterns/strategy/SR_mode_strategy.py)

Luu y:
- Phan nay hien tai moi la review list dua tren tu da hoc
- Chua phai spaced repetition day du vi chua co `interval`, `next_review_at`, `ease factor`

## API Chinh

### Vocabulary

- `GET /vocabulary?topic=animal`

Lay danh sach tu vung theo chu de.

### Learned Progress

- `POST /learned/add?session_id=abc&word_id=1`
- `GET /learned/words?session_id=abc`
- `GET /learned/reset?session_id=abc`
- `GET /learned/all`

### Exam

- `GET /exam/exam-object-flashcard?word_id=1`
- `GET /exam/exam-object-multiple-choices?word_id=1`
- `GET /exam/exam-object-sr?session_id=abc`

### WebSocket

- `ws://localhost:8000/ws?session_id=abc`

Khi connect:
- backend gui ngay list tu da hoc hien tai cua session

Khi co thay doi:
- backend push list moi nhat qua websocket

## Cach chay nhanh

### Cach 1: chay bang Docker

```bash
docker-compose up --build
```

### Cach 2: chay backend thu cong

Di chuyen vao thu muc backend:

```bash
cd back-end
```

Cai dependencies:

```bash
pip install -r requirements.txt
```

Chay server:

```bash
uvicorn app.main:app --reload
```

## Diem can mo rong trong tuong lai

- Tach rieng `ReviewStrategy` khoi `StudyModeStrategy`
- Nang cap `SR_mode_strategy` thanh spaced repetition that su
- Luu progress xuong database thay vi singleton memory
- Chuan hoa response schema bang Pydantic
- Them README rieng cho frontend va backend neu can trinh bay chi tiet hon

## Tom tat kien truc hien tai

Kien truc sau khi chinh lai strategy:
- `Factory/Service` lay du lieu
- `StudyModeContext` chon che do hoc
- `StudyModeStrategy` build payload
- `Singleton` luu progress theo session
- `Observer + WebSocket` push realtime cho frontend

Day la mot phien ban phu hop de demo y tuong design pattern trong ung dung hoc tu vung, dong thoi van de mo rong them `review strategy` va `spaced repetition` o cac buoc sau.
