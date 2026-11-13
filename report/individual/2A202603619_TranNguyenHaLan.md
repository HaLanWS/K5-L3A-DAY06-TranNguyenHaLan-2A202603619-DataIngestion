# Báo cáo cá nhân — Day 6: Data Ingestion Engineering

**Học viên:** Trần Nguyễn Hà Lan  
**MSSV:** 2A202603619  
**Lớp:** L3A  

---

## Dữ liệu và pipeline
- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:**
  - *Chủ đề:* Quy chế Đào tạo trình độ đại học của Đại học Bách khoa Hà Nội qua hai giai đoạn văn bản (2023 và 2025).
  - *Nguồn và quyền sử dụng:* Văn bản quy chế đào tạo công khai ban hành kèm theo Quyết định số 4600/QĐ-ĐHBK (ngày 09/06/2023) và Quyết định số 5445/QĐ-ĐHBK (năm 2025) của Giám đốc Đại học Bách khoa Hà Nội, phục vụ công tác tra cứu học tập của sinh viên.
  - *Số trang và quy tắc tính:*
    - File 1 (`QCDT-2023-upload.pdf`): Tổng 32 trang vật lý; loại trừ trang bìa (trang 1) và mục lục (trang 2–3) $\rightarrow$ **29 trang nội dung thực tế** (từ trang 4 đến 32), đạt 70.522 ký tự.
    - File 2 (`QCDT_2025_5445_QD-DHBK.pdf`): Tổng 34 trang vật lý; loại trừ quyết định ban hành, bìa và mục lục (trang 1–4) $\rightarrow$ **30 trang nội dung thực tế** (từ trang 5 đến 34), đạt 70.267 ký tự.
    - **Tổng số trang nội dung hợp lệ:** $29 + 30 = \mathbf{59\text{ trang}}$ (vượt xa yêu cầu tối thiểu $\ge 30$ trang), tổng cộng 140.789 ký tự chuẩn hóa. Chi tiết lưu tại [data/manifest.json](file:///c:/Users/Admin/Downloads/K5-L3A-DAY06-TranNguyenHaLan-2A202603619-DataIngestion/data/manifest.json).
- **Chuẩn hóa, lỗi và giới hạn:**
  - Toàn bộ văn bản PDF được trích xuất qua `pypdf`, chuẩn hóa khoảng trắng thừa Unicode, loại bỏ ngắt dòng bất thường giữa từ ngữ tiếng Việt.
  - *Giới hạn:* Một số bảng biểu có định dạng cột phức tạp (như bảng quy đổi thang điểm chữ ở Điều 5) khi trích xuất text thuần có thể mất viền bảng; giải pháp là giữ nguyên chuỗi liên tục để bảo tồn ngữ nghĩa.
- **Embedding model/provider/version/số chiều, vector store/version, metric, lệnh chạy và chi phí:**
  - *Embedding model:* `sentence-transformers/all-MiniLM-L6-v2` (chạy local offline, 384 chiều, chuẩn hóa vector L2).
  - *Vector store:* `ChromaDB v1.5.9` (Persistent Client lưu tại `./starter/chroma_db`), độ đo tương đồng `Cosine Distance`.
  - *Lệnh chạy pipeline:* `python starter/src/pipeline.py`
  - *Chi phí:* **$0.00** (Chạy offline 100% trên GPU/CPU nội bộ, không tốn phí API).
- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:**
  - *Metadata bắt buộc:* `document_id` (`QCDT_2023`, `QCDT_2025`), `source` (tên văn bản), `page` (số trang vật lý để truy vết bằng chứng).
  - *Trường lọc bổ sung:*
    - `year` (kiểu số nguyên: `2023`, `2025`): Trích xuất trực tiếp từ năm ban hành văn bản. Đây là trường lọc cực kỳ quan trọng giúp phân biệt giữa các quy chế qua từng năm, giải quyết triệt để lỗi người dùng hỏi quy chế năm này nhưng kết quả trả về của năm kia.
    - `section`: Tên chương/điều khoản (ví dụ: `Điều 19. Cảnh báo học tập`) phục vụ định vị phân đoạn logic.

---

## Cấu hình và benchmark
- **A / B / C (tham số cụ thể, khác biệt duy nhất B–C):**
  - **Cấu hình A (Baseline Fixed-size):** Chunking kích thước cố định `chunk_size=500` ký tự, `overlap=50` ký tự. Metadata gồm `document_id`, `source`, `page`, `year`, `section=General`. Không lọc (`filter=None`).
  - **Cấu hình B (Structure/Article-based):** Chunking theo cấu trúc Điều khoản (`Điều x`), giới hạn tối đa 1.000 ký tự một chunk để tránh tràn ngữ cảnh. Giữ nguyên cấu trúc logic của điều luật. Không lọc (`filter=None`).
  - **Cấu hình C (Metadata Filtered):** Chiến lược chunking giống hệt B. Điểm khác biệt duy nhất giữa B và C: Khi câu hỏi có ràng buộc năm văn bản (được giả định cung cấp trước qua query context), áp dụng filter metadata `where={'year': year}`.
- **≥20 câu: phân chia ≥15 dev / ≥5 test, câu metadata filter và cách kiểm chứng evidence:**
  - Tổng số câu hỏi: **20 câu** (15 câu Dev, 5 câu Test). Phân chia cố định trước khi chạy pipeline.
  - Có 4 câu kiểm tra metadata filter (3 câu ở Dev: `DEV_13`, `DEV_14`, `DEV_15`; 1 câu ở Test: `TEST_05`).
  - Toàn bộ bằng chứng (`evidence_quote`) được kiểm chứng tự động qua script [starter/scripts/verify_evidence.py](file:///c:/Users/Admin/Downloads/K5-L3A-DAY06-TranNguyenHaLan-2A202603619-DataIngestion/starter/scripts/verify_evidence.py), bảo đảm 100% (20/20 câu) trích dẫn tồn tại chính xác tại trang nguồn tương ứng.
- **Tiêu chí chọn chiến lược đã chốt trước khi xem test:**
  - Ưu tiên 1: Evidence Hit@3 cao nhất trên tập Dev.
  - Ưu tiên 2: Tính mạch lạc (Coherence) của chunk $\ge 1.5/2.0$.
  - Ưu tiên 3: Tối ưu số lượng chunk và thời gian tạo vector.

---

## Kết quả

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---|---|---|---|---|
| **Strategy A** (Fixed 500/50) | Dev | 1/15 (6.7%) | 1/15 (6.7%) | 331 | 28.39s | $0.00 |
| **Strategy A** (Fixed 500/50) | Test | 0/5 (0.0%) | 0/5 (0.0%) | 331 | 28.39s | $0.00 |
| **Strategy B** (Structure/Article) | Dev | 3/15 (20.0%) | 5/15 (33.3%) | 178 | 3.66s | $0.00 |
| **Strategy B** (Structure/Article) | Test | 1/5 (20.0%) | 2/5 (40.0%) | 178 | 3.66s | $0.00 |
| **Strategy C** (Filtered) | Dev | 3/15 (20.0%) | 5/15 (33.3%) | 178 | 3.66s | $0.00 |
| **Strategy C** (Filtered) | Test | 1/5 (20.0%) | 3/5 (60.0%) | 178 | 3.66s | $0.00 |

| Strategy | Coherence trung bình /2 (n=10) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N) | Grounding 0/1/2 (số câu) và TB /2 |
|---|---|---|---|---|
| **Strategy A** | 0.70 / 2.0 (n=10) | 15/15 (100%) | N/A (không áp dụng lọc) | 0: 3 câu, 1: 2 câu, 2: 0 câu (TB: 0.40/2) |
| **Strategy B** | 2.00 / 2.0 (n=10) | 15/15 (100%) | N/A (không áp dụng lọc) | 0: 0 câu, 1: 3 câu, 2: 2 câu (TB: 1.40/2) |
| **Strategy C** | 2.00 / 2.0 (n=10) | 15/15 (100%) | 1/1 (100% trên Test) | 0: 0 câu, 1: 1 câu, 2: 4 câu (TB: 1.80/2) |

- **Đường dẫn trace, nhãn thủ công và cách chọn mẫu:**
  - File kết quả trace chi tiết: [starter/results/benchmark_trace.json](file:///c:/Users/Admin/Downloads/K5-L3A-DAY06-TranNguyenHaLan-2A202603619-DataIngestion/starter/results/benchmark_trace.json).
  - File đánh giá thủ công Coherence & Grounding: [starter/results/manual_evaluation.json](file:///c:/Users/Admin/Downloads/K5-L3A-DAY06-TranNguyenHaLan-2A202603619-DataIngestion/starter/results/manual_evaluation.json).
  - Cách chọn mẫu Coherence: Chọn 10 vị trí điều khoản trọng tâm trải đều từ trang 6 đến trang 19 của cả hai tài liệu (Điều 3, 4, 5, 10, 13, 18, 19, 20) trước khi quan sát điểm số.

---

## Phân tích và kết luận
- **So sánh A–B và B–C; 2 ví dụ sai có ID câu và nguồn:**
  - *So sánh A–B (Tác động của Chunking):*
    - Chiến lược A (Fixed 500 ký tự) tạo ra tới 331 chunks, mất 28.39s ingest. Do cắt cứng 500 ký tự, nhiều mệnh đề pháp lý bị xé đôi giữa chừng. Ví dụ ở `DEV_05` và `TEST_01`, điều kiện nâng/hạ mức cảnh báo học tập bị đứt lìa khỏi tiêu đề Điều 19, dẫn tới Coherence chỉ đạt 0.70/2.0 và Hit@3 trên Test tụt về 0%.
    - Chiến lược B (Structure/Article) gom trọn vẹn theo từng Điều/Khoản, chỉ còn 178 chunks (giảm 46% số chunk), thời gian ingest chỉ còn 3.66s. Coherence đạt điểm tuyệt đối 2.00/2.0. Hit@3 trên Test tăng vọt lên 40.0%.
  - *So sánh B–C (Tác động của Metadata Filter):*
    - Vì corpus gồm 2 phiên bản văn bản (2023 và 2025) có kết cấu điều khoản tương tự nhau (đều có Điều 20 về Xử lý vi phạm), chiến lược B không có bộ lọc nên bị nhầm lẫn giữa hai văn bản.
    - Cấu hình C áp dụng `where={'year': 2025}` giúp câu `TEST_05` chuyển từ **Miss** (bị xếp hạng sai do nhầm sang năm 2023) thành **Hit** ở ngay rank đầu tiên, nâng Hit@3 tập Test từ 40% lên **60%**, và điểm Grounding trung bình tăng từ 1.40 lên **1.80/2.0**.
  - *2 ví dụ truy xuất sai thực tế:*
    1. **Câu `DEV_08` trên Cấu hình A:** Hỏi về thời điểm sớm nhất đăng ký song bằng. Nguồn chuẩn là Điều 18 (Trang 16). Trong cấu hình A, chunk chứa câu *"Sinh viên được đăng ký học chương trình thứ hai sớm nhất khi đã được xếp trình độ năm thứ hai..."* bị cắt cụt ở chữ *"xếp"* (khoảng ký tự thứ 500), làm mất vế sau *"trình độ năm thứ hai của chương trình thứ nhất"*, khiến câu không đạt Hit do thiếu bằng chứng.
    2. **Câu `TEST_05` trên Cấu hình B:** Hỏi quy định xử lý vi phạm trong văn bản 2025. Vì không có metadata filter, cấu hình B trả về Điều 20 của văn bản năm 2023 (`QCDT_2023`, trang 17) do từ khóa tương đồng ngữ nghĩa cao hơn, dẫn tới trích dẫn sai phiên bản văn bản.
- **Chiến lược chọn, đánh đổi, điều kiện áp dụng:**
  - **Chiến lược chọn:** Cấu hình **C (Structure Chunking + Metadata Filtering)** là tối ưu nhất trên mọi tiêu chí: Hit@3 cao nhất (60% trên Test), Coherence tuyệt đối (2.0/2.0), Grounding cao nhất (1.80/2.0) và tiết kiệm tài nguyên bộ nhớ lưu trữ (178 chunks).
  - *Đánh đổi:* Để áp dụng Cấu hình C, hệ thống phải trích xuất chính xác metadata ngữ cảnh (như năm áp dụng, chủ đề) từ câu hỏi của người dùng trước khi truy vấn vector store.
- **Hạn chế của dữ liệu, nhãn, test nhỏ, đo thời gian/chi phí:**
  - Tập Test gồm 5 câu là mẫu tương đối nhỏ, có thể mang sai số thống kê nhất định và không nên suy rộng tuyệt đối ngoài bộ quy chế đại học này.
  - Model embedding `all-MiniLM-L6-v2` là mô hình đa ngữ nhẹ (384 dims), tối ưu tốt cho câu ngắn nhưng khi gặp văn phong pháp lý tiếng Việt phức tạp đôi khi độ tương đồng cosine giữa các điều khoản tương tự chưa thực sự cách biệt lớn.
- **Nếu làm lại hoặc mở rộng, cải tiến gì?**
  - Mở rộng sang **Hybrid Search**: Kết hợp Dense Vector Retrieval với Từ khóa Sparse BM25 (dành riêng cho việc tra cứu chính xác số hiệu Điều/Khoản và số tín chỉ).
  - Bổ sung trường metadata `level` (`dai_hoc`, `thac_si`, `tien_si`) để sinh viên thuộc bậc học nào chỉ cần truy vấn trong phạm vi bậc học đó.
