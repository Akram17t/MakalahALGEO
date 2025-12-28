# Analisis Kerentanan Jaringan Drainase Perkotaan
## Eigenvalue Decomposition & Power Iteration Method

> Makalah IF2123 Aljabar Linear dan Geometri  
> Semester I Tahun 2024/2025  
> Program Studi Teknik Informatika  
> Institut Teknologi Bandung

## 🚀 Cara Penggunaan

### 1. Menjalankan Analisis
```bash
cd src
python drainase.py
```

**Input:**
- `data/nodes.csv` - Data simpul dengan koordinat dan parameter hidraulik
- `data/edges.csv` - Data koneksi dengan flow rate

**Output:**
- `hasil/results.csv` - Hasil analisis lengkap dengan semua metrik
- Console: Statistik jaringan dan 15 simpul paling rentan




## 🔧 Detail Teknis

### Dependencies
```bash
pip install numpy pandas scipy matplotlib networkx
```

### Versi Python
```
Python 3.12.6
```

