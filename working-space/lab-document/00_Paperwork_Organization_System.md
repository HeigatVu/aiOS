# Paperwork Organization & Naming Convention System

## 1. Directory Structure (Hybrid + Reference Model)
*Sắp xếp theo mô hình 4 tầng: Biểu mẫu, Thư viện tái sử dụng, Kho dự án, và Tài liệu tham khảo.*

- **01_Templates/**: Chứa các biểu mẫu trắng hoặc file chuẩn chưa điền thông tin. Dùng để bắt đầu một hồ sơ mới.
- **02_Library_Assets/**: Tài liệu có thể tái sử dụng ngay cho nhiều dự án (CV của team, LoS, hồ sơ đối tác).
- **03_Projects_Archive/**: Kho lưu trữ các dự án, gom nhóm theo `Năm_Quỹ_TênDựÁn`.
- **04_References/**: Tài liệu tham khảo từ dự án khác, ví dụ mẫu, hướng dẫn, quy cách. Không phải sản phẩm chính thức.

## 2. Document Type Codes (Mã loại giấy tờ)
*Sử dụng các mã này trong tên file để tìm kiếm nhanh.*

| Mã (Code) | Loại (Category) | Tiếng Việt tương đương |
| :--- | :--- | :--- |
| **CV** | Curriculum Vitae | Lý lịch khoa học / Bio / Resume |
| **PRO** | Proposal / Protocol | Thuyết minh đề tài / Đề cương / Đăng ký |
| **CON** | Contract / Agreement | Hợp đồng / Thỏa thuận / Cam kết |
| **ETH** | Ethics / IRB | Hồ sơ đạo đức / Y đức / ICF |
| **BUD** | Budget / Finance | Dự toán / Chi phí / Tài chính / Quyết toán |
| **REQ** | Request / Official Letter | Giấy đề nghị / Công văn / Đơn xin |
| **ADM** | Admin / Support | Thư ủng hộ (LoS) / Xác nhận phối hợp / Giấy giới thiệu |
| **REP** | Report | Báo cáo (Tiến độ / Kết quả / Self-evaluation) |
| **SCH** | Schedule | Kế hoạch / Gantt chart |
| **PRE** | Presentation | Slide thuyết trình |
| **CRF** | Case Report Form | Phiếu thu thập dữ liệu / Phiếu phân tích |
| **FIG** | Figure / Image | Hình ảnh / Sơ đồ / Diagram |
| **GDL** | Guideline / Regulation | Hướng dẫn / Quy cách / Quy định |
| **COR** | Correspondence | Email / Thư trao đổi / Confirmation Letter |

## 3. Naming Convention (Quy tắc đặt tên)
**Công thức:** `YYYYMMDD_[Scope]_[Type]_[Subject]_[Status]_[vX].[ext]`

| Trường | Bắt buộc | Mô tả |
| :--- | :--- | :--- |
| `YYYYMMDD` | Có | Ngày chỉnh sửa cuối cùng của file |
| `[Scope]` | Có | Tên quỹ/dự án hoặc tổ chức (xem Mục 4) |
| `[Type]` | Có | Mã loại giấy tờ từ bảng trên |
| `[Subject]` | Có | Nội dung hoặc người liên quan |
| `[Status]` | Không | Trạng thái: `Draft`, `Final`, `Signed` (chỉ dùng khi cần phân biệt) |
| `[vX]` | Có | Số phiên bản: v1, v2... |

*Ví dụ:*
- `20250620_BV175_CON_ThueKhoan_MinhDuc_Signed_v1.docx`
- `20260426_VinIF_BUD_DuToan_v2.xlsx`
- `20260101_SVI_PRO_Proposal_Final_v3.docx`
- `20250315_Terumo_COR_ConfirmationLetter_Signed_v1.pdf`

## 4. Quy tắc chọn [Scope]

| Ngữ cảnh | [Scope] là gì | Ví dụ |
| :--- | :--- | :--- |
| File trong `03_Projects_Archive/` | **Tên quỹ tài trợ / đối tác dự án** | `VinIF`, `Terumo`, `SVI`, `BV175` |
| File trong `02_Library_Assets/` | **Tên trường / tổ chức** của người sở hữu | `BK`, `IU`, `ND2` |
| File dùng chung, không gắn tổ chức nào | `Common` | `Common` |
| File trong `04_References/` | **Nguồn gốc** của tài liệu tham khảo | `BV175`, `ND2`, `IBRO`, `KC` |

**Bảng viết tắt tổ chức:**

| Viết tắt | Tên đầy đủ |
| :--- | :--- |
| `BK` | Đại học Bách Khoa (HCMUT) |
| `IU` | International University (HCMIU) |
| `ND2` | Bệnh viện Nhi Đồng 2 |
| `BV175` | Bệnh viện Quân y 175 |
| `VinIF` | Vingroup Innovation Foundation |
| `Terumo` | Terumo Life Science Foundation |
| `SVI` | SVI Seed Grant |
| `VIBE` | VIBE Voice AI |
| `IBRO` | IBRO (International Brain Research Organization) |
| `KC` | State Budget / Ngân sách Nhà nước (Vietnamese government funding) |
| `Common` | Dùng chung / Không gắn tổ chức |

## 5. Bảng đối chiếu chuyển đổi (Ví dụ)

| Tên file cũ | Tên file đề xuất mới |
| :--- | :--- |
| `hợp đồng thuê khoán chuyên môn_...Đức_Mẫu.docx` | `YYYYMMDD_BV175_CON_ThueKhoan_Template.docx` |
| `5. Lý lịch khoa học- Thầy Hoàng Anh.docx` | `YYYYMMDD_BK_CV_HoangAnh_v1.docx` |
| `3 Bản thông tin và phiếu chấp thuận...ICF.docx` | `YYYYMMDD_VinIF_ETH_ICF_v1.docx` |
| `Nội dung đăng ký VinIF.docx` | `YYYYMMDD_VinIF_PRO_Registration_v1.docx` |
| `4.1 phiếu phân tích phát âm - crf.pdf` | `YYYYMMDD_VinIF_CRF_Pronunciation_v1.pdf` |
| `Confirmation Letter_for PI_signed.pdf` | `YYYYMMDD_Terumo_COR_ConfirmLetter_Signed_v1.pdf` |
| `Hợp-đồng-giao-nhiệm-vụ_Final File.docx` | `YYYYMMDD_BV175_CON_GiaoNhiemVu_Final_v1.docx` |
| `LoS_Cô-Hiệp - Signed.pdf` | `YYYYMMDD_Common_ADM_LoS_CoHiep_Signed_v1.pdf` |
| `phase2.png` | `YYYYMMDD_SVI_FIG_Phase2_v1.png` |

---
**Ghi chú:**
- `YYYYMMDD` lấy theo ngày chỉnh sửa cuối cùng (Last Modified Date) của file gốc.
- `[Status]` chỉ thêm khi file có nhiều trạng thái (Draft → Final → Signed). Nếu chỉ có 1 bản duy nhất, bỏ qua.
- Khi cùng một file tồn tại nhiều format (.docx và .pdf), dùng cùng tên chỉ khác extension.
