flowchart TD
  A[Halaman Login] --> B{Authentication Success}
  B -- No --> A
  B -- Yes --> C{User Role}
  C -- Pegawai --> D[Dashboard Pegawai]
  C -- Owner --> E[Dashboard Owner]
  D --> F[Halaman Input Pesanan]
  D --> G[Data Pelanggan]
  D --> H[Halaman Cek Status Laundry]
  D --> I[Daftar Transaksi]
  E --> G
  E --> J[Data Pegawai]
  E --> H
  E --> I
  F --> K[Submit Pesanan]
  K --> I
  H --> L[Masukkan Nomor Order]
  L --> M{Order Found}
  M -- No --> H
  M -- Yes --> N[Tampilkan Status]