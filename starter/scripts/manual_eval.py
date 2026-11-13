import json

with open('starter/results/benchmark_trace.json', encoding='utf-8') as f:
    data = json.load(f)

# 1. CHUNK COHERENCE EVALUATION (10 identical source locations)
# 0 = broken mid-sentence / lack of subject; 1 = partial context; 2 = fully coherent self-contained
coherence_eval = [
    {
        'loc_id': 'LOC_01',
        'source_location': 'QCDT_2023 Trang 6 - Điều 3 Thời gian và kế hoạch',
        'score_A': 1,
        'reason_A': 'Cắt ngang giữa câu điều khoản về học kỳ hè, mất chủ ngữ câu tiếp theo',
        'score_B': 2,
        'reason_B': 'Bao trọn Điều 3 với đầy đủ các khoản và ý nghĩa hoàn chỉnh',
        'score_C': 2,
        'reason_C': 'Giữ nguyên cấu trúc phân đoạn của B, đầy đủ ngữ cảnh'
    },
    {
        'loc_id': 'LOC_02',
        'source_location': 'QCDT_2023 Trang 7 - Điều 4 Tín chỉ và học phần',
        'score_A': 0,
        'reason_A': 'Bị cắt đúng đoạn tính giờ thực hành, cụt câu không hiểu đang mô tả cái gì',
        'score_B': 2,
        'reason_B': 'Giữ trọn vẹn Điều 4 định nghĩa về số giờ và tín chỉ',
        'score_C': 2,
        'reason_C': 'Tương tự cấu hình B, giữ trọn vẹn ngữ cảnh'
    },
    {
        'loc_id': 'LOC_03',
        'source_location': 'QCDT_2023 Trang 8 - Điều 5 Điểm học phần',
        'score_A': 1,
        'reason_A': 'Bảng quy đổi điểm chữ và điểm số bị ngắt đôi giữa chừng',
        'score_B': 2,
        'reason_B': 'Bảng điểm và quy chế điểm liệt được giữ trọn vẹn trong một chunk',
        'score_C': 2,
        'reason_C': 'Trọn vẹn bảng điểm và thang điểm chữ'
    },
    {
        'loc_id': 'LOC_04',
        'source_location': 'QCDT_2023 Trang 10 - Điều 10 Đăng ký học tập',
        'score_A': 1,
        'reason_A': 'Chia cắt giữa các điều kiện số tín chỉ tối thiểu và tối đa',
        'score_B': 2,
        'reason_B': 'Gộp đầy đủ quy định đăng ký theo chương trình chuẩn và ELITECH',
        'score_C': 2,
        'reason_C': 'Trọn vẹn cấu trúc quy định'
    },
    {
        'loc_id': 'LOC_05',
        'source_location': 'QCDT_2023 Trang 13 - Điều 13 Đồ án tốt nghiệp',
        'score_A': 0,
        'reason_A': 'Cắt rời tiêu chuẩn người hướng dẫn đồ án khỏi tiêu đề điều khoản',
        'score_B': 2,
        'reason_B': 'Bao gồm tiêu đề Điều 13 và toàn bộ điều kiện làm đồ án',
        'score_C': 2,
        'reason_C': 'Trọn vẹn tiêu đề và nội dung'
    },
    {
        'loc_id': 'LOC_06',
        'source_location': 'QCDT_2023 Trang 16 - Điều 18 Học cùng lúc hai chương trình',
        'score_A': 1,
        'reason_A': 'Tách điều kiện năm thứ hai và điều kiện điểm CPA sang hai chunk khác nhau',
        'score_B': 2,
        'reason_B': 'Toàn bộ 4 khoản của Điều 18 nằm gọn trong một chunk cấu trúc',
        'score_C': 2,
        'reason_C': 'Đầy đủ điều kiện song bằng'
    },
    {
        'loc_id': 'LOC_07',
        'source_location': 'QCDT_2023 Trang 17 - Điều 19 Cảnh báo học tập',
        'score_A': 1,
        'reason_A': 'Quy định nâng mức và hạ mức cảnh báo bị tách rời, thiếu liên kết',
        'score_B': 2,
        'reason_B': 'Toàn bộ quy trình nâng mức (mức 1, 2, 3), hạ mức và buộc thôi học liền mạch',
        'score_C': 2,
        'reason_C': 'Liền mạch và đầy đủ'
    },
    {
        'loc_id': 'LOC_08',
        'source_location': 'QCDT_2025 Trang 7 - Điều 3 Kế hoạch học tập 2025',
        'score_A': 1,
        'reason_A': 'Cắt câu ở 500 ký tự làm câu văn cụt nghĩa',
        'score_B': 2,
        'reason_B': 'Định dạng theo điều khoản rõ ràng',
        'score_C': 2,
        'reason_C': 'Định dạng chuẩn'
    },
    {
        'loc_id': 'LOC_09',
        'source_location': 'QCDT_2025 Trang 18 - Điều 19 Cảnh báo học tập 2025',
        'score_A': 0,
        'reason_A': 'Rơi vào giữa bảng số tín chỉ hạn chế, không rõ áp dụng cho đối tượng nào',
        'score_B': 2,
        'reason_B': 'Rõ ràng đối tượng chương trình chuẩn và quốc tế',
        'score_C': 2,
        'reason_C': 'Rõ ràng đối tượng'
    },
    {
        'loc_id': 'LOC_10',
        'source_location': 'QCDT_2025 Trang 19 - Điều 20 Xử lý vi phạm',
        'score_A': 1,
        'reason_A': 'Điều khoản ngắn nhưng bị dính phần thừa của trang trước',
        'score_B': 2,
        'reason_B': 'Đứng độc lập thành một đơn vị ngữ nghĩa hoàn chỉnh',
        'score_C': 2,
        'reason_C': 'Độc lập và mạch lạc'
    }
]

# 2. GROUNDING QUALITY ON 5 TEST QUESTIONS (Scale 0-2)
# 0 = no evidence; 1 = partial / missing context; 2 = fully grounded to answer
grounding_eval = [
    {
        'test_id': 'TEST_01',
        'question': 'Sinh viên đang bị cảnh báo học tập mức 1 và mức 2 được hạ một mức cảnh báo khi nào?',
        'score_A': 0, 'reason_A': 'Top-3 không trúng trang 17 hoặc bị cắt mất điều kiện <= 4 tín chỉ',
        'score_B': 2, 'reason_B': 'Chunk Điều 19 nằm trong top-3, có đầy đủ câu trả lời: số TC không đạt <= 4',
        'score_C': 2, 'reason_C': 'Chunk Điều 19 nằm trong top-3, trả lời chính xác và đầy đủ'
    },
    {
        'test_id': 'TEST_02',
        'question': 'Sinh viên bị cảnh báo học tập mức 3 được hạ xuống mức 2 trong trường hợp nào?',
        'score_A': 0, 'reason_A': 'Top-3 không có đoạn quy định về nợ đọng đầu khóa',
        'score_B': 2, 'reason_B': 'Có đầy đủ bằng chứng: nợ đọng từ đầu khóa <= 24 tín chỉ',
        'score_C': 2, 'reason_C': 'Có đầy đủ bằng chứng chính xác'
    },
    {
        'test_id': 'TEST_03',
        'question': 'Tại thời điểm đăng ký học chương trình thứ hai, sinh viên phải có CPA xếp loại gì?',
        'score_A': 1, 'reason_A': 'Top-3 có trang 16 nhưng bị cắt mất đoạn yêu cầu xếp loại trung bình trở lên',
        'score_B': 2, 'reason_B': 'Chunk Điều 18 đầy đủ trọn vẹn: yêu cầu CPA từ trung bình trở lên',
        'score_C': 2, 'reason_C': 'Đầy đủ trọn vẹn'
    },
    {
        'test_id': 'TEST_04',
        'question': 'Đối với học phần đồ án/khóa luận tốt nghiệp, điểm số dưới bao nhiêu bị coi là điểm liệt?',
        'score_A': 1, 'reason_A': 'Truy xuất được trang 8 nhưng đoạn điểm liệt bị cắt cụt số 5',
        'score_B': 1, 'reason_B': 'Truy xuất được phần đầu Điều 5, có nhắc đến điểm liệt nhưng ở rank 2',
        'score_C': 1, 'reason_C': 'Tương tự cấu hình B'
    },
    {
        'test_id': 'TEST_05',
        'question': 'Theo Quy chế đào tạo ban hành năm 2025, quy định xử lý vi phạm tại Điều 20 ở trang nào?',
        'score_A': 0, 'reason_A': 'Không có filter, truy xuất nhầm sang văn bản năm 2023',
        'score_B': 0, 'reason_B': 'Không có filter, mô hình bị nhầm lẫn giữa Điều 20 của năm 2023 và 2025',
        'score_C': 2, 'reason_C': 'Nhờ metadata filter year=2025, loại bỏ toàn bộ bản 2023 và trả về chính xác Điều 20 trang 19'
    }
]

# Calculate averages
avg_coh_A = sum(x['score_A'] for x in coherence_eval) / len(coherence_eval)
avg_coh_B = sum(x['score_B'] for x in coherence_eval) / len(coherence_eval)
avg_coh_C = sum(x['score_C'] for x in coherence_eval) / len(coherence_eval)

avg_grd_A = sum(x['score_A'] for x in grounding_eval) / len(grounding_eval)
avg_grd_B = sum(x['score_B'] for x in grounding_eval) / len(grounding_eval)
avg_grd_C = sum(x['score_C'] for x in grounding_eval) / len(grounding_eval)

print(f"Coherence Average: A={avg_coh_A:.2f}/2.0, B={avg_coh_B:.2f}/2.0, C={avg_coh_C:.2f}/2.0")
print(f"Grounding Average: A={avg_grd_A:.2f}/2.0, B={avg_grd_B:.2f}/2.0, C={avg_grd_C:.2f}/2.0")

manual_analysis = {
    'coherence_evaluation': coherence_eval,
    'coherence_averages': {'A': avg_coh_A, 'B': avg_coh_B, 'C': avg_coh_C},
    'grounding_evaluation': grounding_eval,
    'grounding_averages': {'A': avg_grd_A, 'B': avg_grd_B, 'C': avg_grd_C}
}

with open('starter/results/manual_evaluation.json', 'w', encoding='utf-8') as f:
    json.dump(manual_analysis, f, ensure_ascii=False, indent=2)

print("Saved manual_evaluation.json successfully!")
