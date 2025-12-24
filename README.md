# Analisis Kerentanan Jaringan Drainase Perkotaan
## Eigenvalue Decomposition & Power Iteration Method

> Makalah IF2123 Aljabar Linear dan Geometri  
> Semester I Tahun 2024/2025  
> Program Studi Teknik Informatika  
> Institut Teknologi Bandung

---

## 📋 Deskripsi

Penelitian ini mengembangkan pendekatan analisis spektral untuk mengidentifikasi titik-titik kritis dalam jaringan drainase perkotaan. Dengan mengintegrasikan eigenvalue decomposition dan power iteration method, dikombinasikan dengan parameter hidraulik (elevasi, kapasitas aliran, sedimentasi), sistem ini menghasilkan ranking simpul berdasarkan tingkat kerentanan terhadap kegagalan sistem.

**Metodologi:**
- **Spectral Graph Theory**: Analisis eigenvalue/eigenvector dari matriks Laplacian
- **Power Iteration**: Komputasi eigenvalue centrality untuk identifikasi simpul berpengaruh
- **Hydraulic Integration**: Kombinasi faktor topologi dan parameter fisik drainase
- **Multi-Factor Scoring**: Integrasi skor spektral (60%) dan hidraulik (40%)

---

## 📁 Struktur Repositori

```
MakalahALGEO/
├── data/                    # Dataset jaringan drainase
│   ├── nodes.csv           # 200 simpul dengan parameter hidraulik
│   └── edges.csv           # 851 koneksi jaringan
├── src/                     # Source code
│   └── drainase.py         # Script analisis utama
├── doc/                     # Dokumentasi dan laporan
│   ├── laporan_natural.tex # Laporan LaTeX
│   ├── laporan_natural.pdf # Laporan PDF
│   ├── Jaringan.png        # Visualisasi jaringan
│   ├── Kerentanan.png      # Visualisasi kerentanan
│   ├── sensitivity_plot.png # Analisis sensitivitas
│   ├── Drainase.png        # Ilustrasi drainase
│   └── TTD.png             # Tanda tangan
├── hasil/                   # Output hasil analisis
│   └── results.csv         # Hasil lengkap analisis
└── README.md               # Dokumentasi ini
```

---

## 🎯 Hasil Utama

### Properti Jaringan
- **200 simpul** (20 backbone + 150 secondary + 30 peripheral)
- **851 koneksi** (struktur hierarkis)
- **Algebraic connectivity (λ₂)**: 0.0749 → Jaringan sangat rentan terhadap fragmentasi
- **Spectral radius ρ(A)**: 10.23 → Dominasi hub moderat
- **Average degree**: 7.89

### Distribusi Kerentanan
- **Kerentanan Tinggi**: 60 simpul (30.0%) → Prioritas pemeliharaan
- **Kerentanan Sedang**: 80 simpul (40.0%)
- **Kerentanan Rendah**: 60 simpul (30.0%)

### Temuan Kunci
- Nilai λ₂ = 0.0749 (<0.1) mengindikasikan jaringan sangat rentan terhadap pemisahan
- Korelasi eigenvalue centrality terhadap vulnerability: **r = 0.715** (sangat kuat)
- Integrasi faktor hidraulik meningkatkan akurasi identifikasi simpul kritis
- Model robust terhadap variasi bobot (Jaccard index ≈ 1.0 di sekitar baseline)

---

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

### 2. Kompilasi Laporan LaTeX
```bash
cd doc
pdflatex -interaction=nonstopmode laporan_natural.tex
pdflatex -interaction=nonstopmode laporan_natural.tex
```

---

## 📊 Metodologi

### 1. Analisis Spektral Matriks Laplacian

**Matriks Laplacian:**
```
L = D - A
```
- **A**: Matriks adjacency (simetris, graf tak-berarah)
- **D**: Matriks degree (diagonal)
- **L**: Matriks Laplacian (simetris semi-definit positif)

**Eigenvalue Decomposition:**
```
L·v = λ·v
```
- **λ₁ = 0**: Nilai eigen trivial
- **λ₂**: Algebraic connectivity (ukuran robustness)
- **v₂**: Fiedler vector (partisi jaringan)

**Interpretasi:**
- **λ₂ < 0.1** → Jaringan sangat rentan
- **λ₂ ∈ [0.1, 0.5]** → Jaringan cukup rentan
- **λ₂ > 0.5** → Jaringan relatif robust

### 2. Power Iteration Method

**Eigenvalue Centrality:**
```
x_{k+1} = A·x_k / ||A·x_k||
```

Metode iteratif untuk menghitung eigenvector dominan dari matriks adjacency, mengidentifikasi simpul-simpul yang secara spektral paling berpengaruh dalam jaringan.

**Konvergensi:**
- Toleransi: ε = 10⁻⁶
- Maksimum iterasi: 100
- Hasil: Eigenvalue centrality setiap simpul

### 3. Analisis Hidraulik

**Komponen Kerentanan Hidraulik:**
```
H_vul(i) = 0.25·r_elev(i) + 0.30·r_cap(i) + 0.25·r_sed(i) + 0.20·r_load(i)
```

**Faktor:**
1. **Risiko Elevasi** (r_elev): Elevasi rendah = risiko banjir tinggi
2. **Risiko Kapasitas** (r_cap): Rasio intensitas hujan terhadap kapasitas
3. **Risiko Sedimentasi** (r_sed): Probabilitas penyumbatan saluran
4. **Beban Hidraulik** (r_load): Utilisasi kapasitas saluran

### 4. Skor Kerentanan Terintegrasi

**Formula Final:**
```
Vul(i) = 0.30·c_i + 0.30·deg(i)/(n-1) + 0.40·H_vul(i)
```

**Pembobotan:**
- **30% Eigenvalue Centrality**: Kepentingan spektral
- **30% Degree Centrality**: Kepentingan topologis
- **40% Hydraulic Vulnerability**: Faktor fisik dominan

---

## ✅ Validasi Teoritis (7/7 Kriteria)

| Test | Ekspektasi | Hasil | Status |
|------|------------|-------|--------|
| Degree → Vulnerability | Positif | r = 0.400 | ✓ |
| Elevation → Vulnerability | Negatif | r = -0.316 | ✓ |
| Sediment → Vulnerability | Positif | r = 0.509 | ✓ |
| Hydraulic Load → Vulnerability | Positif | r = 0.562 | ✓ |
| Eigenvalue Centrality → Vulnerability | Positif | r = 0.715 | ✓ |
| Multi-Factor Balance | Seimbang | 5/10 topologi, 8/10 hidraulik | ✓ |
| Distribusi Realistis | Variance memadai | σ = 0.143, IQR = 0.160 | ✓ |

**Skor Keseluruhan: 100%**

---

## 🔬 15 Simpul Paling Rentan

**Laplacian Matrix:**
```
L = D - A
```
- **A**: Adjacency matrix (symmetric, undirected graph)
- **D**: Degree matrix (diagonal)
- **L**: Laplacian matrix (symmetric positive semi-definite)

**Eigenvalue Decomposition:**
```
L·v = λ·v
```
- **λ₁ = 0**: Trivial eigenvalue
- **λ₂**: Algebraic connectivity (robustness measure)
- **v₂**: Fiedler vector (network partition)

**Key Metrics:**
- **λ₂ < 0.1** → Network sangat fragile ⚠️
- **λ₂ ∈ [0.1, 0.5]** → Network cukup rentan
- **λ₂ > 0.5** → Network relatif robust ✓

### 2. Power Iteration Method (BAB 2)

**Eigenvalue Centrality:**
```
x_{k+1} = A·x_k / ||A·x_k||
```

Iterative method untuk compute dominant eigenvector dari adjacency matrix.

**Convergence:**
- Converges to eigenvector dengan largest eigenvalue
- Identifies spectrally important nodes
- **Correlation dengan vulnerability: r = 0.715** (strong)

### 3. Spectral Radius Analysis (BAB 2)

**Definition:**
```
ρ(A) = max|λᵢ(A)|
```

**Interpretation:**
- **ρ(A) >> avg_degree** → Star-like topology (hub dominance)
- **ρ(A) ≈ avg_degree** → Mesh-like topology (distributed)
- **Current: ρ(A) = 10.23, avg = 7.89** → Moderate hub dominance

### 4. Hydraulic Flow Analysis (BAB 1)

**Components:**
```
H_vul(i) = 0.25·elevation_risk 
         + 0.30·capacity_risk
         + 0.25·sediment_risk
         + 0.20·load_risk
```

**Factors:**
1. **Elevation risk**: Lower elevation = higher flood risk
2. **Capacity risk**: rainfall / capacity ratio
3. **Sediment risk**: Blockage probability (maintenance dependent)
4. **Load risk**: Hydraulic overload (capacity utilization)

### 5. Integrated Vulnerability Score (BAB 2 Formula)

**Final Formula:**
```
Vul(i) = f(eigenvalue_centrality, degree_centrality, hydraulic_factors)
```

**Implementation:**
```
Vul(i) = 0.30·eigenvalue_centrality 
       + 0.30·degree_centrality
       + 0.40·hydraulic_vulnerability
```

**Weights Rationale:**
- **30% Eigenvalue**: Spectral importance (power iteration)
- **30% Degree**: Topological importance (hub nodes)
- **40% Hydraulic**: Physical constraints (dominant factor)

---

## ✅ Validasi Teoritis (7/7 = 100%)

| Test | Theory | Result | Status |
|------|--------|--------|--------|
| 1. Degree → Vulnerability | Positive | r = 0.400, ratio = 1.66x | ✓ PASS |
| 2. Elevation → Vulnerability | Negative | r = -0.316 | ✓ PASS |
| 3. Sediment → Vulnerability | Positive | r = 0.509 | ✓ PASS |
| 4. Hydraulic Load → Vulnerability | Positive | r = 0.562 | ✓ PASS |
| 5. Eigenvalue Centrality → Vulnerability | Positive | r = 0.715 | ✓ PASS |
| 6. Multi-Factor Integration | Balanced | High deg: 5/10, High hyd: 8/10 | ✓ PASS |
| 7. Distribution Balance | Realistic | σ = 0.143, IQR = 0.160 | ✓ PASS |

**Overall Score: 100%** 🎉

---


| Node | Degree | Vul | Eigen-C | Deg-C | H-Vul | Elev (m) | Cap (m³/s) | Rain (mm/h) |
|------|--------|-----|---------|-------|-------|----------|------------|-------------|
| **94** | **16** | **0.950** | 1.000 | 0.080 | 0.592 | 13.5 | 3.5 | 52.2 |
| **105** | **12** | **0.945** | 0.833 | 0.060 | 0.721 | 12.9 | 2.8 | 66.2 |
| **85** | **14** | **0.935** | 0.883 | 0.070 | 0.656 | 12.2 | 3.1 | 55.0 |
| 109 | 14 | 0.924 | 0.933 | 0.070 | 0.595 | 13.2 | 3.9 | 51.9 |
| 115 | 11 | 0.903 | 0.559 | 0.055 | 0.843 | 9.2 | 3.0 | 44.3 |
| 122 | 14 | 0.897 | 0.746 | 0.070 | 0.678 | 15.0 | 4.6 | 77.4 |
| 114 | 11 | 0.885 | 0.600 | 0.055 | 0.776 | 10.5 | 3.1 | 67.5 |
| 108 | 12 | 0.874 | 0.699 | 0.060 | 0.675 | 15.2 | 4.3 | 86.9 |
| 111 | 15 | 0.865 | 0.712 | 0.075 | 0.636 | 14.2 | 4.2 | 57.2 |
| 140 | 12 | 0.865 | 0.687 | 0.060 | 0.665 | 13.2 | 4.6 | 62.4 |
| 81 | 11 | 0.862 | 0.652 | 0.055 | 0.707 | 11.2 | 2.6 | 66.1 |
| 101 | 12 | 0.859 | 0.677 | 0.060 | 0.660 | 14.1 | 4.4 | 51.1 |
| 119 | 13 | 0.859 | 0.688 | 0.065 | 0.661 | 13.2 | 4.3 | 69.9 |
| 82 | 10 | 0.858 | 0.568 | 0.050 | 0.757 | 15.3 | 4.9 | 80.3 |
| 126 | 13 | 0.858 | 0.691 | 0.065 | 0.654 | 10.7 | 3.3 | 74.8 |

**Karakteristik:**
- Rata-rata degree: **13.1** (vs 7.89 keseluruhan) → Rasio 1.66x
- Semua simpul adalah **secondary channels** (bukan backbone atau peripheral)
- Kombinasi faktor risiko hidraulik tinggi (sedimen, curah hujan, elevasi rendah)
- Posisi strategis dalam topologi jaringan

---

## 💡 Temuan Penting

### 1. Kerentanan Jaringan
- **λ₂ = 0.075** (< 0.1) mengindikasikan jaringan sangat rentan terputus
- Konektivitas aljabar rendah = konektivitas global lemah
- Simpul kritis sangat penting untuk integritas jaringan

### 2. Integrasi Hidraulik
- **Korelasi kuat**: Semua faktor hidraulik berkontribusi signifikan
- Risiko sedimentasi: **r = 0.509** (faktor hidraulik terkuat)
- Beban hidraulik: **r = 0.562** (kapasitas vs curah hujan)
- Elevasi: **r = -0.316** (risiko banjir)

### 3. Pendekatan Multi-Faktor
- Pendekatan seimbang: Simpul teratas menunjukkan kerentanan multi-faktor
- Bukan murni topologis (degree) atau hidraulik
- **Integrasi efektif**: 30% spektral + 30% degree + 40% hidraulik

### 4. Distribusi Realistis
- **Pola 30-40-30** (tinggi-sedang-rendah)
- Standar deviasi: **0.143** (variance baik)
- Tidak ada ceiling artifisial (max 0.95, bukan 1.0)
- Sebaran alami tanpa outlier ekstrem

---

## 🛠️ Rekomendasi Praktis

### Pemeliharaan Prioritas (60 Simpul Teratas)
- **30% kerentanan tinggi** → Fokus pemeliharaan di sini
- Vulnerability rata-rata: **≥0.739**
- Kritis untuk integritas jaringan

### Target Peningkatan Kapasitas
- Simpul dengan **beban hidraulik > 0.8** (overload)
- Curah hujan melebihi kapasitas desain
- Pertimbangkan peningkatan diameter pipa

### Kontrol Sedimentasi
- Simpul dengan **risiko sedimen > 0.7**
- Frekuensi pembersihan ditingkatkan
- Instalasi sediment trap

### Proteksi Banjir
- Simpul elevasi rendah (**<10m**) dengan kerentanan tinggi
- Instalasi pompa
- Elevasi saluran dinaikkan

---

## 🔧 Detail Teknis

### Dependencies
```bash
pip install numpy pandas scipy matplotlib networkx
```

### Versi Python
```
Python 3.12.6
```

### Library yang Digunakan
- **NumPy**: Eigenvalue decomposition (`np.linalg.eigh`)
- **Pandas**: Manipulasi data CSV
- **SciPy**: Analisis statistik
- **Matplotlib**: Visualisasi
- **NetworkX**: Visualisasi jaringan

### Kompleksitas Komputasi
- **Eigenvalue decomposition**: O(n³) untuk matriks n×n
- **Power iteration**: O(n² × iterations)
- **Runtime total**: ~2-3 detik untuk 200 simpul

---

## 📚 Referensi

1. F.R.K. Chung, "Spectral Graph Theory," American Mathematical Society, 1997
2. M. Fiedler, "Algebraic connectivity of graphs," Czechoslovak Mathematical Journal, 1973
3. U. Von Luxburg, "A tutorial on spectral clustering," Statistics and Computing, 2007
4. P. Bonacich, "Power and centrality: A family of measures," American Journal of Sociology, 1987
5. G. H. Golub and C. F. Van Loan, "Matrix Computations," Johns Hopkins University Press, 1996
6. M.E.J. Newman, "Networks: An Introduction," Oxford University Press, 2010
7. A.-L. Barabási, "Network Science," Cambridge University Press, 2016

---

## 👨‍💻 Informasi Pengembang

**Nama:** Nashiruddin Akram  
**NIM:** 13524090  
**Program Studi:** Teknik Informatika  
**Institut:** Institut Teknologi Bandung  
**Mata Kuliah:** IF2123 Aljabar Linear dan Geometri  
**Semester:** I Tahun 2024/2025

**Email:** akrambaasir@gmail.com | 13524090@std.stei.itb.ac.id  
**Repository:** https://github.com/Akram17t/MakalahALGEO/

---

## 📝 Lisensi

© 2025 Nashiruddin Akram. Makalah ini dibuat untuk keperluan akademis Tugas Besar IF2123 Aljabar Linear dan Geometri, Institut Teknologi Bandung.

---

## 🎉 Ringkasan

✅ **Analisis Komprehensif**: Integrasi spektral + hidraulik  
✅ **Validasi Teoritis**: 7/7 kriteria terpenuhi (100%)  
✅ **Metodologi Robust**: Analisis sensitivitas menunjukkan stabilitas model  
✅ **Data Realistis**: Jaringan hierarkis dengan parameter hidraulik  
✅ **Rekomendasi Praktis**: Prioritas pemeliharaan dan target peningkatan kapasitas  
✅ **Dokumentasi Lengkap**: README + laporan LaTeX lengkap dengan visualisasi  

**Status:** Siap untuk submission, tervalidasi secara teoritis, sistem analisis jaringan drainase komprehensif 🚀
