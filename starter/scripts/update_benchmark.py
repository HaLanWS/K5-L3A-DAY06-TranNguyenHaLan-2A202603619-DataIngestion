import json

questions = [
  # --- DEV SET (15 questions: 12 no filter, 3 with filter) ---
  {
    'id': 'DEV_01',
    'split': 'dev',
    'question': 'Theo quy định, một năm học tại ĐHBK Hà Nội bao gồm những học kỳ nào?',
    'expected_answer': 'Một năm học bao gồm hai học kỳ chính và một học kỳ hè.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 6,
    'evidence_quote': 'Một năm học bao gồm hai học kỳ chính và một học kỳ hè',
    'filter': None,
    'type': 'direct'
  },
  {
    'id': 'DEV_02',
    'split': 'dev',
    'question': 'Sinh viên bị nâng một mức cảnh báo học tập khi có số tín chỉ không đạt trong học kỳ là bao nhiêu?',
    'expected_answer': 'Khi có số tín chỉ không đạt trong học kỳ lớn hơn 8.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Nâng một mức cảnh báo học tập đối với sinh vi ên có số TC không đạt trong học kỳ lớn hơn 8',
    'filter': None,
    'type': 'direct'
  },
  {
    'id': 'DEV_03',
    'split': 'dev',
    'question': 'Sinh viên bị áp dụng cảnh báo học tập mức 3 khi nào?',
    'expected_answer': 'Khi có số tín chỉ nợ đọng từ đầu khóa lớn hơn 24.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Áp dụng cản h báo học tập  mức 3 đối với sinh viên có số TC nợ đọng từ đầu khóa lớn hơn 24',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'DEV_04',
    'split': 'dev',
    'question': 'Học kỳ hè có xem xét cảnh báo học tập đối với sinh viên không?',
    'expected_answer': 'Không xem xét cảnh báo học tập với học kỳ hè.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Không xem xét cảnh báo học tập với học kỳ hè',
    'filter': None,
    'type': 'exception'
  },
  {
    'id': 'DEV_05',
    'split': 'dev',
    'question': 'Sinh viên thuộc CTĐT chuẩn bị hạn chế khối lượng học tập được đăng ký tối đa bao nhiêu tín chỉ trong một học kỳ chính?',
    'expected_answer': 'Được đăng ký tối đa 14 tín chỉ và tối thiểu 8 tín chỉ cho một học kỳ chính.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Sinh viên thuộc các CTĐT chuẩn được đăng ký tối đa 14 T C và tối thiểu 8 TC cho một học kỳ chính',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'DEV_06',
    'split': 'dev',
    'question': 'Sinh viên chương trình ELITECH bị hạn chế khối lượng học tập được đăng ký tối đa bao nhiêu tín chỉ?',
    'expected_answer': 'Được đăng ký tối đa 18 tín chỉ và tối thiểu 8 tín chỉ cho một học kỳ chính.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Sinh viên thuộc các chương trình ELITECH và cá c CTĐT hợp tác q uốc tế được đăng ký tối đa 18 TC và tối thiểu 8 TC',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'DEV_07',
    'split': 'dev',
    'question': 'Trường hợp nào sinh viên bị buộc thôi học do cảnh báo học tập?',
    'expected_answer': 'Sinh viên bị cảnh báo học tập mức 3 lần thứ hai liên tiếp.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Sinh viên bị cảnh báo học tập mức 3 lần thứ hai liên tiếp',
    'filter': None,
    'type': 'direct'
  },
  {
    'id': 'DEV_08',
    'split': 'dev',
    'question': 'Sinh viên được phép đăng ký học chương trình thứ hai sớm nhất khi nào?',
    'expected_answer': 'Sớm nhất khi đã được xếp trình độ năm thứ hai của chương trình thứ nhất.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 16,
    'evidence_quote': 'Sinh viên được đăng ký học c hương trình thứ hai sớm nhất khi đã được xếp trình độ năm thứ hai của chương trình thứ nhất',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'DEV_09',
    'split': 'dev',
    'question': 'Điểm đạt của học phần là từ điểm chữ nào trở lên?',
    'expected_answer': 'Điểm đạt là điểm học phần từ D trở lên, riêng các học phần tốt nghiệp phải từ C trở lên.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 8,
    'evidence_quote': 'Điểm đạt là điểm học phần từ D trở lên, riêng đối với các học phần tốt nghiệp phải từ C trở lên',
    'filter': None,
    'type': 'direct'
  },
  {
    'id': 'DEV_10',
    'split': 'dev',
    'question': 'Luận văn thạc sĩ đạt yêu cầu khi điểm bảo vệ đạt từ mức nào theo thang điểm?',
    'expected_answer': 'Khi điểm bảo vệ luận văn đạt từ điểm C trở lên và không có điểm thành viên nào dưới 5 theo thang 10.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 23,
    'evidence_quote': 'Luận văn đạt yêu cầu khi điểm bảo vệ luận văn đạt từ điểm C trở lên và không có điểm của thành viên Hội đồng nào dưới 5 theo thang điểm 10',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'DEV_11',
    'split': 'dev',
    'question': 'Khung kế hoạch thời gian năm học của ĐHBK Hà Nội áp dụng cho đối tượng nào, ngoại trừ trường hợp nào?',
    'expected_answer': 'Tuân theo Khung kế hoạch của ĐHBK Hà Nội, ngoại trừ các học phần tiến sĩ được bố trí riêng.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 6,
    'evidence_quote': 'ngoại trừ các học phần tiến sĩ được bố trí l ịch giảng dạy và lịch thi riêng theo tiến độ học tập của nghiên cứu sinh',
    'filter': None,
    'type': 'exception'
  },
  {
    'id': 'DEV_12',
    'split': 'dev',
    'question': 'Chương trình tích hợp cử nhân - kỹ sư có thời gian thiết kế là bao nhiêu năm?',
    'expected_answer': 'Chương trình tích hợp cử nhân - kỹ sư có thời gian thiết kế là 5,5 năm.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 5,
    'evidence_quote': 'Chương trình tích hợp cử nhân -kỹ sư có thời gian thiết kế là 5,5 năm',
    'filter': None,
    'type': 'direct'
  },
  {
    'id': 'DEV_13',
    'split': 'dev',
    'question': 'Theo Quy chế đào tạo ban hành năm 2025, quy định tại Điều 3 về thời gian và kế hoạch học tập nằm ở trang nào?',
    'expected_answer': 'Thời gian và kế hoạch học tập được quy định tại Điều 3.',
    'gold_source_id': 'QCDT_2025',
    'gold_page': 7,
    'evidence_quote': 'Điều 3. Thời gian và kế hoạch học tập',
    'filter': {'year': 2025},
    'type': 'metadata_filter'
  },
  {
    'id': 'DEV_14',
    'split': 'dev',
    'question': 'Trong văn bản năm 2023, quy định về học cùng lúc hai chương trình tại Điều 18 nằm ở trang nào?',
    'expected_answer': 'Điều 18. Học cùng lúc hai chương trình.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 16,
    'evidence_quote': 'Điều 18. Học cùng lúc hai chương trình',
    'filter': {'year': 2023},
    'type': 'metadata_filter'
  },
  {
    'id': 'DEV_15',
    'split': 'dev',
    'question': 'Theo văn bản Quy chế năm 2025, quy định tại Điều 23 về đăng ký tốt nghiệp kỹ sư nằm ở trang nào?',
    'expected_answer': 'Điều 23. Đăng ký tốt nghiệp kỹ sư nằm ở trang 20.',
    'gold_source_id': 'QCDT_2025',
    'gold_page': 20,
    'evidence_quote': 'Điều 23. Đăng ký tốt nghiệp kỹ sư',
    'filter': {'year': 2025},
    'type': 'metadata_filter'
  },

  # --- TEST SET (5 questions: 4 no filter, 1 with filter) ---
  {
    'id': 'TEST_01',
    'split': 'test',
    'question': 'Sinh viên đang bị cảnh báo học tập mức 1 và mức 2 được hạ một mức cảnh báo khi nào?',
    'expected_answer': 'Nếu số tín chỉ không đạt trong học kỳ nhỏ hơn hoặc bằng 4.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Sinh viên đang bị cảnh báo học tập mức 1 và mức 2, nế u số TC không đạt trong học kỳ nhỏ hơn hoặc bằng 4 thì được hạ một mức cảnh báo học tập',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'TEST_02',
    'split': 'test',
    'question': 'Sinh viên bị cảnh báo học tập mức 3 được hạ xuống mức 2 trong trường hợp nào?',
    'expected_answer': 'Nếu số tín chỉ nợ đọng từ đầu khóa nhỏ hơn hoặc bằng 24.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 17,
    'evidence_quote': 'Sinh viên đang bị cảnh báo họ c tập mức 3, nếu số TC nợ đọng từ đầu khóa nhỏ hơn hoặc bằng 24 thì được hạ cảnh báo học tập xuống mức 2',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'TEST_03',
    'split': 'test',
    'question': 'Tại thời điểm đăng ký học chương trình thứ hai, sinh viên phải có điểm trung bình tích lũy CPA xếp loại gì?',
    'expected_answer': 'Phải có học lực tính theo điểm trung bình tích lũy (CPA) xếp loại từ trung bình trở lên.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 16,
    'evidence_quote': 'sinh viên phải có học lực tính theo điểm t rung bình tích lũy (CPA) xếp',
    'filter': None,
    'type': 'condition'
  },
  {
    'id': 'TEST_04',
    'split': 'test',
    'question': 'Đối với học phần đồ án hoặc khóa luận tốt nghiệp, điểm số dưới bao nhiêu thì bị coi là điểm liệt?',
    'expected_answer': 'Điểm số dưới 5 đối với học phần đồ án/khóa luận tốt nghiệp được coi là điểm liệt.',
    'gold_source_id': 'QCDT_2023',
    'gold_page': 8,
    'evidence_quote': 'điểm số dưới 5 đối với học phần đồ án/khóa luận tốt nghiệp và điểm số dưới 3 đối với các học phần khác được coi là điểm liệt',
    'filter': None,
    'type': 'direct'
  },
  {
    'id': 'TEST_05',
    'split': 'test',
    'question': 'Theo Quy chế đào tạo ban hành năm 2025, quy định xử lý vi phạm đối với sinh viên được ghi nhận tại Điều 20 ở trang nào?',
    'expected_answer': 'Điều 20. Xử lý vi phạm đối với sinh viên nằm ở trang 19.',
    'gold_source_id': 'QCDT_2025',
    'gold_page': 19,
    'evidence_quote': 'Điều 20. Xử lý vi phạm đối với sinh viên',
    'filter': {'year': 2025},
    'type': 'metadata_filter'
  }
]

with open('data/benchmark_questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print('Updated benchmark_questions.json with 20 questions!')
