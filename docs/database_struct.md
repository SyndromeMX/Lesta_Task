# Структура базы данных проекта Term Frequency

Проект использует две основные сущности в базе данных:

---

## 📁 Document

Хранит загружаемые `.txt` файлы.

| Поле        | Тип               | Описание                       |
|-------------|------------------|--------------------------------|
| id          | AutoField (PK)   | Уникальный идентификатор       |
| file        | FileField        | Файл, загруженный пользователем |
| uploaded_at | DateTimeField    | Дата и время загрузки файла    |

---

## 📊 FileMetric

Сохраняет метрики, связанные с обработкой файла.

| Поле             | Тип            | Описание                                        |
|------------------|----------------|-------------------------------------------------|
| id               | AutoField (PK) | Уникальный идентификатор                        |
| filename         | CharField      | Имя загруженного файла                          |
| uploaded_at      | DateTimeField  | Дата загрузки файла                             |
| file_size        | IntegerField   | Размер файла в байтах                           |
| processed        | BooleanField   | Был ли файл успешно обработан                   |
| error_count      | IntegerField   | Количество ошибок при обработке                 |
| processing_time  | FloatField     | Время обработки (в секундах, до 3 знаков)       |

---

## 💡 Диаграмма (ERD)

```mermaid
erDiagram
    Document ||--o{ FileMetric : "связанное с"
    Document {
        int id PK
        file file
        datetime uploaded_at
    }
    FileMetric {
        int id PK
        string filename
        datetime uploaded_at
        int file_size
        boolean processed
        int error_count
        float processing_time
    }
