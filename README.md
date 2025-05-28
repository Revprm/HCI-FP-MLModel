# NutriGrow ML Model API

## Overview

Proyek ini bertujuan untuk memprediksi status gizi balita dan mendeteksi risiko stunting berdasarkan indikator pertumbuhan seperti umur, jenis kelamin, dan tinggi badan. Model ini menggunakan algoritma machine learning dan dikemas dalam bentuk REST API dengan FastAPI.

## API Documentation

* 🔗 [Postman Documentation](https://documenter.getpostman.com/view/39901805/2sB2qUnPvX)

## Cara Menjalankan Aplikasi

### 1. Clone Repository

```bash
git clone https://github.com/revprm/HCI-FP-MLModel.git
cd NutriGrow-MLModel
```

### 2. (Opsional) Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
# Atau
.\venv\Scripts\activate   # Untuk Windows
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan API

```bash
python main.py
```

## Endpoint

### `POST /predict`

Melakukan prediksi status gizi dan memberikan tingkat kepercayaan berdasarkan input data anak.

#### Contoh Request

```json
{
  "Umur (bulan)": 21,
  "Jenis Kelamin": 1,
  "Tinggi Badan (cm)": 77
}
```

#### Field Keterangan

| Field             | Tipe | Deskripsi                            | Contoh |
| ----------------- | ---- | ------------------------------------ | ------ |
| Umur (bulan)      | int  | Umur balita dalam bulan              | 21     |
| Jenis Kelamin     | int  | 0 = Laki-laki, 1 = Perempuan         | 1      |
| Tinggi Badan (cm) | int  | Tinggi badan balita dalam sentimeter | 77     |

#### Contoh Response

```json
{
  "Status_Gizi": 2,
  "confidence": 0.864
}
```

#### Penjelasan `Status_Gizi`

| Kode | Keterangan        |
| ---- | ----------------- |
| 0    | normal            |
| 1    | severely stunted  |
| 2    | stunted           |
| 3    | tinggi            |
