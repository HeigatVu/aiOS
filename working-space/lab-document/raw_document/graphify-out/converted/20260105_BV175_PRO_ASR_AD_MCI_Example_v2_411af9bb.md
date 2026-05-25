<!-- converted from 20260105_BV175_PRO_ASR_AD_MCI_Example_v2.docx -->

THUYẾT MINH
ĐỀ TÀI KHOA HỌC VÀ CÔNG NGHỆ1
# I. THÔNG TIN CHUNG VỀ ĐỀ TÀI


_____________________
2 Một (01) tháng quy đổi là tháng làm việc gồm 22 ngày, mỗi ngày làm việc gồm 8 tiếng.

# II. MỤC TIÊU, NỘI DUNG KH&CN VÀ PHƯƠNG ÁN TỔ CHỨC THỰC HIỆN ĐỀ TÀI
12
Mục tiêu của đề tài (Bám sát và cụ thể hoá định hướng mục tiêu theo đặt hàng- nếu có)

Nhận thấy được phát triển đáng kể của trí tuệ nhân tạo trong lĩnh vực khoa học sức khỏe và tiềm năng việc sử dụng giọng nói dùng để chẩn đoán các bệnh liên quan đến thoái hóa ngôn ngữ ở Việt Nam, nhóm nghiên cứu quyết định sẽ xây dựng dự án theo hai hướng như sau: (1) tập trung vào việc dùng các đặc điểm của giọng nói trong lĩnh vực ngôn ngữ học và âm thanh học để xác định những dấu hiệu của bệnh Alzheimer. Bên cạnh việc tập trung vào nghiên cứu sự khác biệt trong giọng nói, chúng tôi sẽ xây dựng các mô hình trí tuệ nhân tạo đa phương thức và phát triển các mô hình trí tuệ nhân tạo trong việc nhận diện giọng nói dùng để nâng cao chất lượng mô hình phân loại; (2) tập trung xây dựng ứng dụng chẩn đoán từ xa thông qua giọng nói dành cho bệnh nhận ở Việt Nam bao gồm thông tin nhân khẩu học, giọng nói thông qua các bài can thiệp nhận thức và điểm số nhận thức.
Ứng dụng rèn luyện nhận thức và mô hình dự đoán hiệu quả can thiệp này hướng đến việc chuyển giao công nghệ cho các bệnh viện, sở y tế để giúp các bác sĩ tiết kiệm thời gian và có thêm nhiều lựa chọn can thiệp cho bệnh nhân.

Đề tài nghiên cứu nhắm đến ba mục tiêu chính sau:
Phát triển bộ công cụ thu thập và đánh giá lĩnh vực ngôn ngữ (bao gồm giọng nói và tốc độ)
Đánh giá suy giảm ngôn ngữ ở người lớn tuổi  Suy giảm nhận thức nhẹ và bệnh Alzheimer
Xây dựng ứng dụng Voice AI dùng để chẩn đoán sớm và từ xa giành cho người lớn tuổi có suy giảm nhận thức

13
Tình trạng đề tài
☒ Mới	☐ Kế tiếp hướng nghiên cứu của chính nhóm tác giả
☐ Kế tiếp nghiên cứu của người khác


14
Tổng quan tình hình nghiên cứu, luận giải về mục tiêu và những nội dung nghiên cứu của đề tài
14.1.  Đánh giá tổng quan tình hình nghiên cứu thuộc lĩnh vực của đề tài

Ngoài nước (Phân tích đánh giá được những công trình nghiên cứu có liên quan và những kết quả nghiên cứu mới nhất trong lĩnh vực nghiên cứu của đề tài; nêu được những bước tiến về trình độ KH&CN của những kết quả nghiên cứu đó)

Sa sút trí tuệ là một hội chứng đặc trưng bởi sự suy giảm nhận thức quá mức do hậu quả lão hoá sinh học. Bệnh biểu hiện như là một sự xáo trộn của đa dạng chức năng nhận thức vỏ não cao hơn như học tập, ghi nhớ, sự chú ý phức tạp, chức năng điều hành, ngôn ngữ, nhận thức vận động và nhận thức xã hội. Điều này ảnh hưởng đến khả năng thực hiện thực hiện các hoạt động độc lập hằng ngày. Theo Tổ chức Y tế Thế giới (WHO) ước tính số người mắc sa sút trí tuệ trên thế giới xấp xỉ 55 triệu, có khả năng đạt đến xấp xỉ 78 triệu trong năm 2030 và 139 triệu vào năm 2050. Bệnh tạo ra gánh nặng tài chính toàn thế giới ước tính 1.3 nghìn tỉ vào năm 2019 và có thể lên đến 2.8 nghìn tỉ trong năm 2030 (Shin, 2022). Như là một nước với thu nhập thấp và vừa, Việt Nam đang trải qua một xu hướng tương tự với số người mắc sa sút trí tuệ gấp đôi mỗi 20 năm (Vu, et al., 2024). Bệnh Alzheimer (AD) là một rối loạn thoái hoá thần kinh tiến triển và cũng là một dạng của sa sút trí tuệ phổ biến nhất chiếm ít nhất hai phần ba trường hợp sa sút trí tuệ ở những người từ 65 tuổi trở lên (Safiri, et al., 2024). Trước khi một người chuyển sang sa sút trí tuệ, người bệnh sẽ trải qua giai đoạn tiền sa sút trí tuệ, còn được biết đến như “suy giảm nhận thức nhẹ” (MCI). Đây là giai đoạn chuyển tiếp giữa quá trình lão hóa bình thường và chứng sa sút trí tuệ, ảnh hưởng xấu đến một hoặc nhiều lĩnh vực nhận thức như Trí nhớ, Tập trung, Ngôn ngữ và Toán học (Farias, et al., 2006; Liss, et al., 2021).

























Hình 1. Các giai đoạn của bệnh Alzheimer (Alcheimer's Association, 2024)

Nguyên nhân và cơ chế gây bệnh của AD rất phức tạp và hiện chưa có phương pháp điều trị hiệu quả. Bên cạnh đó hầu hết bệnh nhân nhận được chẩn đoán AD khi họ đã đến giai đoạn vừa và nặng của bệnh, giai đoạn mà những hoạt động hằng ngày cơ bản thì mất đi. Nhầm lẫn và chậm trễ trong chẩn đoán phản ánh các khoảng trống trong kiến thức về bệnh cùng với các yếu tố khác như nhầm lẫn trong niềm tin là mất trí nhớ và các vấn đề nhận thức là do tuổi già,; thiếu công nhận giữa bệnh nhân và người chăm sóc; và không có có dấu hiệu sinh học AD đáng tin cậy, chính xác và đơn giản (Liss, et al., 2021). Không những thế một điều quang trọng ở giai đoạn MCI là “thời kỳ cửa sổ” (critical window) kéo dài khoảng hai đến ba năm kể từ khi bệnh khởi phát, đại diện cho một cơ hội để can thiệp và thay đổi chiều hướng tiến triển của sự suy giảm nhận thức. Ở giai đoạn này, số lượng tế bào thần kinh chưa bị tổn thương đáng kể, các kết nối tế bào thần kinh vẫn được bảo toàn, nhiều vùng não vẫn chưa bị teo lại. Do đó, việc phát hiện dẫn đến các can thiệp sớm có thể phục hồi hoặc củng cố kết nối tế bào thần kinh để cải thiện nhận thức của bệnh nhân và giảm thiểu xác suất chuyển đổi từ MCI thành sa sút trí tuệ (Haroutunian, Hoffman, & Been, 2009; Wang, et al., 2020). Vì thế, sàng lọc, chẩn đoán và can thiệp AD sớm rất quan trọng, nhưng gần đây chẩn đoán AD với độ chính xác cao liên quan phân tích cấu trúc não dùng chụp cộng hưởng từ (MRI) và chụp ghi hình cắt lớp positron (PET). Tuy nhiên, những phương pháp này không phù hợp cho việc sàng lọc và chẩn doán sớm vì cần các chuyên viên y tế và tốn kém chi phí (Fu, Xu, Zhang, Zhang, & Cao, 2024). Việc phát triển một mô hình hỗ trợ trong việc sàng lọc cho AD tận dụng trí tuệ nhân tạo (AI) có thể cung cấp một ý nghĩa về kinh tế và tiện lợi trong việc phát hiện sớm bệnh AD là một điều cần thiết. Có những nghiên cứu  nhận thấy các suy giảm khả năng ngôn ngữ ở bệnh nhân AD trong giai đoạn sớm cũng là một lý do nền tảng cho việc tận dụng phân tích giọng nói để tạo một ứng dụng tiện lợi trong hỗ trợ sàng lọc giúp cho người bệnh có thể biết tình trạng sức khoẻ não bộ của bản thân để có thể tới bệnh viện nhận các hỗ trợ sớm từ y bác sĩ và các chuyên viên y tế giúp giảm quá trình phát triển của bệnh. (Fu, Xu, Zhang, Zhang, & Cao, 2024; Ivanova, Martínez-Nicolás, & Meilán, 2024; Pulido, et al., 2020).

Tín hiệu âm thanh gồm 2 dạng thông tin:
Các đặc trưng âm học (acoustic features) dựa trên các đặc tính vật lý của âm thanh như âm sắc, tần số cơ bản, cấu trúc hài hoà và phân bố năng lượng trong các miền thời gian và tần số,… Những đặc trưng này phản ánh sự khác biệt giữa các cá thể và những thay đổi trong việc truyền tải những thay đổi cảm xúc và ngữ điệu trong lời nói (Fu, Xu, Zhang, Zhang, & Cao, 2024). Việc dựa trên các đặc trưng âm học có thể biểu thị sự khác nhau giữa các bệnh nhân MCI, AD và người khỏe mạnh được phản ánh trong những thay đổi về tốc độ nói, ngắt nghỉ và độ trôi chạy, vì sự thay đổi trong đặc điểm âm học này là kết quả của những khó khăn trong việc tìm lại từ, xây dựng câu và duy trì tính mạch lạc (Haider, De La Fuente, & Luz, 2020).
Các đặc trưng âm học có thể lấy trước tiếp từ file âm thanh bằng các công cụ mã nguồn mở: ComParE (Bae, et al., 2023), eGeMAPS (Bae, et al., 2023), Bag-of-Audio-Words (BoAW) (Maximilian, Fabien, & Schuller, 2016), and Multi-resolution Cochleagram features (MRCGs) (Chen, Wang, & Wang, 2014).
Đối với máy học, feature embedding là một kỹ thuật trong học máy bằng cách chuyển dự liệu nhiều chiều (high-dimension data) thành các vec-tơ đặc trưng với ít chiều hơn (lower-dimensional vector). Điều này giúp bảo toàn các thông tin cần thiết khi đưa vào các thuật toán máy học để dự đoán hay phân loại. Một số mô hình giúp tạo các feature embedding giúp tạo ra các đặc trưng âm học: VGGish (Koo, Lee, Pyo, Jo, & Lee, 2020), Log-Mel spectrograms (Nicholas, et al., 2020), wav2vec2 (Baevski, Zhou, Mohamed, & Auli, 2020).
Các đặc trưng ngữ nghĩa (semantic features) dựa trên nội dung được truyền tải trong lời nói. Trong các nghiên cứu về phân tích giọng nói ở các bệnh nhân AD nhận thấy các vấn đề thường tập trung ở các thông tin ngôn ngữ ở cấp độ từ vựng, cú pháp và logic ý nghĩa trong câu nói (Fu, Xu, Zhang, Zhang, & Cao, 2024).
Part-of-speech (POS): giúp phát hiện những thay đổi nào ở bệnh nhân AD/MCI (ví dụ: giảm sử dụng tính từ, trạng từ; tăng tỷ lệ danh từ hoặc từ đệm; cấu trúc câu đơn giản hơn) (Shakeri & Farmanbar, 2025).
TF-IDF: phản ánh sự nghèo nàn về từ vựng hoặc lặp lại từ ngữ ở bệnh nhân (Shakeri & Farmanbar, 2025).
Word embedding (Word2Vec, BERT, GPT,…): nắm bắt ngữ nghĩa sâu sắc hơn, phát hiện sự mơ hồ, khó khăn trong việc tìm từ (word-finding difficulties), hoặc sự thiếu mạch lạc trong diễn đạt mà các phương pháp đơn giản hơn có thể bỏ lỡ (Shakeri & Farmanbar, 2025).

Dựa trên 2 dạng thông tin trên chúng ta có thể chia thành 3 loại phương pháp chẩn đoán AD dựa trên máy học:
Phương pháp sử dụng các đặc trưng âm học (method using acoustic features) tận dụng các đặc trưng âm học để đưa ra dự đoán.
Phương pháp sử dụng các đặc trưng ngữ nghĩa (method using semantic features) tận dụng các đặc trưng ngữ nghĩa để đưa ra các dự đoán.
Phương pháp dung hợp đa phương thức (multimodal fusion method) để kết hợp 2 loại đặc trưng lại để đưa ra dự đoán.

Trong nước (Phân tích, đánh giá tình hình nghiên cứu trong nước thuộc lĩnh vực nghiên cứu của đề tài, đặc biệt phải nêu cụ thể được những kết quả KH&CN liên quan đến đề tài mà các cán bộ tham gia đề tài đã thực hiện. Nếu có các đề tài cùng bản chất đã và đang được thực hiện ở cấp khác, nơi khác thì phải giải trình rõ các nội dung kỹ thuật liên quan đến đề tài này; Nếu phát hiện có đề tài đang tiến hành mà đề tài này có thể phối hợp nghiên cứu được thì cần ghi rõ Tên đề tài, Tên Chủ nhiệm đề tài và đơn vị chủ trì thực hiện đề tài đó)

Hiện tại trong nước để kiểm tra các vấn đề để phát hiện sớm bệnh AD hay MCI bằng các bài kiểm tra tuyền thống tại bệnh viện:
Kiểm tra trạng thái tâm thần tối thiểu (Mini-Mental State Examination - MMSE): bài kiểm tra có 20 câu hỏi chia làm 5 phần (định hướng, ghi nhớ, chú ý, tính toán, nhớ lại và ngôn ngữ) với tổng điểm 30 với trung bình 7 phút thực hiện. Nếu dưới 24 là ngưỡng MCI với độ nhạy 88% và độ đặc hiệu 72%, dưới 19 là ngưỡng sa sút trí tuệ với độ nhạy 75% và độ đặc hiệu 93%. Tuy nhiên, bài kiểm tra này cũng có thể bị ảnh hưởng bởi học vấn, ngôn ngữ, vận động và thị lực của người làm bài kiểm tra (Nhi, et al., 2018; Quoc & Nhi, 2006; Long, Thanh, & Toan, 2022).
Đánh giá nhận thức Montreal (Montreal Cognitive Assessment – MoCA): cũng tương tự MMSE là một bài kiểm tra thân thiện và dễ dùng cho sàng lọc MCI với việc đánh giá các chức năng nhận thức (chú ý, tập trung, chức năng điều hành, ghi nhớ, ngôn ngữ, kỹ năng thị giác không gian, trừu tượng, tính toán và định hướng), tổng điểm là 30 điểm với trung bình 10 phút để thực hiện. So với MMSE thì MoCA có độ nhạy cao hơn trong việc phát hiện MCI, với ngưỡng bằng hoặc dưới 26 điểm có độ nhạy 90% (Julayanont, 2017; Do, et al., 2022; Nhi, et al., 2018), ngưỡng dưới 22 điểm có độ nhạy 76.3% và độ đặc hiệu 71.3% (Quang, et al., 2023)
Với 2 bài kiểm tra trên các bác sĩ sẽ đánh giá thông qua lời nói, hành động và câu viết của người được kiểm tr để xem các vấn đề như mức độ lưu loát, lặp câu, thông hiểu và định danh đồ vật nhằm đánh giá các khía cạnh của nhận thức (Julayanont, 2017). Vì các bài kiểm tra thường được làm tại viện nên việc sàng lọc cộng đồng còn khó khăn và nhiều thách thức.

Bên cạnh đó, như đã nói ở phần “nước ngoài” hiện tại chẩn đoán AD với độ chính xác cao liên quan phân tích cấu trúc não bằng cách dùng MRI và PET (Fu, Xu, Zhang, Zhang, & Cao, 2024). Mặc dù trong những năm qua Việt Nam đã cải thiện nhiều với việc tăng cường cung cấp các máy CT, MRI và PET cho các bệnh viện tuyến tỉnh và các bệnh viện tuyến đầu. Nhưng vẫn có các khó khăn cần khắc phục trong tương lai:
Tính khả dụng của các thiết bị CT, MRI, PET trên khắp Việt Nam còn hạn chế dẫn đến nguồn lực làm việc hiệu quả với các thiết bị này còn thiếu (Duc, Huy, & Thong, 2019).
Các bác sĩ chẩn đoán hình ảnh giỏi chủ yếu tập trung ở các thành phố lớn như Hà Nội, Hồ Chí Minh và Đà Nẵng. Từ đó có sự khác biệt đáng kể về trình độ nguồn lực ở các tỉnh thành (Duc, Huy, & Thong, 2019).

Khi đến với khía cạnh máy học, trong vài thập kỉ qua, AI nhận được nhiều sự chú ý và cũng được xem như là con đường để tới cuộc cách mạng công nghiệp lần thứ 4 (Truong, Vo, Tran, Nguyen, & Pham, 2023). Vì thế, Bộ Y tế Việt Nam đã đưa ra quyết định số 4888/QD-BYT về các ứng dụng và phát triển chăm sóc sức khỏe thông minh trong năm 2019-2025. Trong đó nhấn mạnh tầm quan trọng công nghệ kỹ thuật số bao gồm AI trong lĩnh vực chăm sóc sức khỏe (Bộ y tế, 2019).

Bảng 2: Một số nghiên cứu ứng dụng AI vào y tế ở Việt Nam

Từ bảng 2, chúng tôi nhận thấy tiềm năng ứng dụng AI trong y tế tại Việt Nam rất lớn, tuy nhiên, chúng chủ yếu tập trung vào xử lý hình ảnh, dữ liệu dạng bảng hoặc xử lý ngôn ngữ tự nhiên, chưa đi sâu vào phân tích tín hiệu giọng nói phức tạp cho chẩn đoán bệnh lý thần kinh như AD hay MCI. Bên cạnh đó, việc tìm kiếm các công trình công bố trong nước về ứng dụng AI phân tích đặc điểm giọng nói để sàng lọc hay hỗ trợ chẩn đoán AD và MCI cho người Việt hiện chưa có. Từ đó cho thấy lĩnh vực này vẫn còn là một khoảng trống lớn chưa được khai phá nhiều. Mặt khác, Việc đánh giá các đặc điểm lời nói như độ lưu loát, lặp từ trong các bài test truyền thống hiện nay phụ thuộc nhiều vào kinh nghiệm và đánh giá chủ quan của người khám. Điều này mở ra tiềm năng cho việc ứng dụng AI để phân tích các đặc trưng giọng nói một cách khách quan, định lượng và tự động hóa, hỗ trợ sàng lọc trên quy mô rộng hơn.

Để giải quyết khoảng trống này, nhóm nghiên cứu chúng tôi đã tích lũy được kinh nghiệm đáng kể trong các lĩnh vực liên quan, tạo nền tảng vững chắc cho đề tài này:
Kinh nghiệm về AI và chẩn đoán Alzheimer: Nhóm đã thực hiện đề tài "Xây dựng cơ sở dữ liệu hình ảnh cộng hưởng từ não (MRI) của bệnh nhân Alzheimer Việt Nam và ứng dụng trí tuệ nhân tạo (AI) trong chẩn đoán bệnh Alzheimer". Phần mềm phát triển có khả năng tính toán các thông số đặc trưng của não và phân biệt bất thường cấu trúc não dựa trên ảnh MRI, đạt độ chính xác ~96% khi thử nghiệm trên cơ sở dữ liệu ADNI (Mỹ). Điều này chứng tỏ năng lực trong phát triển ứng dụng, xây dựng cơ sở dữ liệu và mô hình học máy cho bệnh Alzheimer.
Kinh nghiệm xây dựng cơ sở dữ liệu quy mô lớn: Từ năm 2020, nhóm là thành viên chủ chốt trong đề tài cấp quốc gia (K.C) "Nghiên cứu xây dựng cơ sở dữ liệu lớn video sóng não của người Việt Nam phục vụ ứng dụng điều khiển thông minh và bước đầu ứng dụng hỗ trợ phục hồi chức năng vận động trên bệnh nhân đột quỵ" (mã số: KC-4.0 -07/19-25). Kinh nghiệm này rất quan trọng cho việc thu thập và quản lý dữ liệu giọng nói trong đề tài này.
Kinh nghiệm phát triển ứng dụng cho người cao tuổi và game rèn luyện nhận thức: Nhóm đã thực hiện dự án "Phát triển và thương mại hóa ứng dụng BrainTrain (phiên bản beta) nhắm vào người cao tuổi Việt Nam". Ứng dụng này bao gồm các trò chơi nghiêm túc (serious games) trên điện thoại thông minh giúp phòng ngừa sa sút trí tuệ và suy giảm trí nhớ ở người già. Và phiên bản BrainTrain phiên bản chính thức đã được chạy tại bệnh viện quân y 175 cũng như đạt giải trong “Thành tựu Y khoa Việt Nam” năm 2024. Kinh nghiệm này rất hữu ích cho việc phát triển giao diện thu thập dữ liệu giọng nói thân thiện với người dùng và tiềm năng tích hợp các bài kiểm tra/game vào ứng dụng trong tương lai.


14.2.  Luận giải về việc đặt ra mục tiêu và những nội dung cần nghiên cứu của đề tài
(Trên cơ sở đánh giá tình hình nghiên cứu trong và ngoài nước, phân tích những công trình nghiên cứu có liên quan, những kết quả mới nhất trong lĩnh vực nghiên cứu đề tài, đánh giá những khác biệt về trình độ KH&CN trong nước và thế giới, những vấn đề đã được giải quyết, cần nêu rõ những vấn đề còn tồn tại, chỉ ra những hạn chế cụ thể, từ đó nêu được hướng giải quyết mới - luận giải  và cụ thể hoá mục tiêu đặt ra của đề tài và những nội dung cần thực hiện trong đề tài để đạt được mục tiêu)

Tính mới của đề tài nghiên cứu thể hiện ở các mặt như sau:

Với những phân tích ở mục 14.1, việc nghiên cứu phát triển một hệ thống AI ứng dụng phân tích giọng nói để hỗ trợ sàng lọc sớm sa sút trí tuệ và MCI cho người Việt là hoàn toàn cần thiết và có cơ sở vững chắc. Đề tài này không chỉ bắt kịp xu hướng công nghệ y tế tiên tiến trên thế giới mà còn giải quyết trực tiếp những hạn chế và khoảng trống trong thực tiễn sàng lọc, chẩn đoán tại Việt Nam. Việc ứng dụng AI để phân tích giọng nói một cách khách quan giúp khắc phục được tính chủ quan trong đánh giá lời nói của các bài kiểm tra truyền thống hiện tại, đồng thời mở ra khả năng sàng lọc sớm trong cộng đồng một cách tiện lợi và tiết kiệm chi phí.

Do đó đề tài đặt ra mục tiêu chính:
Xây dựng và đánh giá hiệu quả của mô hình Trí tuệ nhân tạo sử dụng các đặc trưng từ giọng nói tiếng Việt để hỗ trợ sàng lọc sớm Alzheimer và MCI.
Để đạt được mục tiêu trên, đề tài cần thực hiện nội dung nghiên cứu cốt lõi sau:
Thu thập và xây dựng bộ dữ liệu giọng nói tiếng việt: Thiết kế quy trình thu thập giọng nói chuẩn hóa dựa trên bài kiểm tra SAGE từ các nhóm đối tượng: người khỏe mạnh, người được chẩn đoán MCI, và người được chẩn đoán AD tại Việt Nam. Tiến hành tiền xử lý và gán nhãn dữ liệu.
Xây dựng và huấn luyện mô hình AI: Thử nghiệm và lựa chọn các kiến trúc mô hình máy học/học sâu (ví dụ: SVM, Random Forest, CNN, RNN/LSTM, Transformer) phù hợp để phân loại các nhóm đối tượng trên.
Đánh giá và kiểm định mô hình: Đánh giá hiệu năng của mô hình đã xây dựng trên tập dữ liệu kiểm tra độc lập bằng các chỉ số như độ chính xác (Accuracy), độ nhạy (Sensitivity), độ đặc hiệu (Specificity), AUC-ROC. So sánh kết quả với các phương pháp sàng lọc truyền thống (MMSE và MoCA).
Phân tích kết quả và đề xuất: Phân tích các đặc trưng giọng nói có giá trị nhất trong việc phân biệt các nhóm bệnh. Đề xuất hướng phát triển ứng dụng thực tế (ví dụ: ứng dụng di động, công cụ hỗ trợ bác sĩ) dựa trên mô hình đã xây dựng.

15
Liệt kê danh mục các công trình nghiên cứu, tài liệu có liên quan đến đề tài đã trích dẫn khi đánh giá tổng quan
(Tên công trình, tác giả, nơi và năm công bố, chỉ nêu những danh mục đã được trích dẫn để luận giải cho sự cần thiết nghiên cứu đề tài).

# Tài liệu tham khảo
Alcheimer's Association. (2024). 2024 Alzheimer's disease facts and figures. Alzheimer's & dementia : the journal of the Alzheimer's Association, 20(5), 3708–3821.
Bae, M., Seo, M.-G., Ko, H., Ham, H., Kim, K. Y., & Lee, J.-Y. (2023). The efficacy of memory load on speech-based detection of Alzheimer’s disease. Frontiers in Aging Neuroscience, 1186786.
Baevski, A., Zhou, H., Mohamed, A., & Auli, M. (2020). wav2vec 2.0: a framework for self-supervised learning of speech representations. NIPS'20: Proceedings of the 34th International Conference on Neural Information Processing Systems, (pp. 12449-12460).
Bộ y tế. (2019, 10 18). Thư Viện Pháp Luật. Retrieved from thuvienphapluat: https://thuvienphapluat.vn/van-ban/EN/Cong-nghe-thong-tin/Decision-4888-QD-BYT-2019-the-scheme-for-application-of-smart-healthcare-information-technology/428330/tieng-anh.aspx
Chen, J., Wang, Y., & Wang, D. (2014). A Feature Study for Classification-Based Speech Separation at Low Signal-to-Noise Ratios. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 1993-2002.
Do, M., Bui, B. K., Pham, N. K., Anglewicz, P., Nguyen, L., Nguyen, T., . . . van Landingham, M. (2022). Validation of MoCA test in Vietnamese language for cognitive impairment screening. Journal of Global Health Neurology and Psychiatry, e2022008.
Duc, N. M., Huy, H. Q., & Thong, P. M. (2019). Vietnamese Society of Radiology and Nuclear Medicine: past, current and future. Acta Informatica Medica, 374.
Er, M. B. (2020). A novel approach for classification of speech emotions based on deep and acoustic features. Ieee Access, 221640-221653.
Farias, S., Mungas, D., Reed, B., Harvey, D., Cahn-Weiner, D., & Decarli, C. (2006). MCI is associated with deficits in everyday functioning. Alzheimer Dis Assoc Disord. Alzheimer disease and associated disorders, 217-223.
Fu, Y., Xu, L. a., Zhang, L., Zhang, P., & Cao, L. a. (2024). Classification and diagnosis model for Alzheimer’s disease based on multimodal data fusion. Medicine, e41016.
Haider, F., De La Fuente, S., & Luz, S. (2020). An assessment of paralinguistic acoustic features for detection of Alzheimer's dementia in spontaneous speech. IEEE Journal of Selected Topics in Signal Processing, 272-281.
Han, T. T., Nguyen Duy, T., Nguyen Dang Son, L., Nguyen Van, H., Trong, T. D., Nguyen Viet, D., & … Vu Dang, L. (2022). Features extraction of MRI image using complex network with low computational complexity to distinguish inflammatory lesions from tumors in the human brain. Computer Methods in Biomechanics and Biomedical Engineering: Imaging & Visualization, 94-102.
Haroutunian, V., Hoffman, L. B., & Been, M. S. (2009). Is there a neuropathology difference between mild cognitive impairment and dementia? Dialogues in clinical neuroscience, 171-179.
Ivanova, O., Martínez-Nicolás, I., & Meilán, J. (2024). Speech changes in old age: methodological considerations for speech-based discrimination of healthy ageing and Alzheimer's disease. International Journal of Language and Communication Disorders, 13-37.
Julayanont, P. N. (2017). Montreal Cognitive Assessment (MoCA): Concept and Clinical Review. Cognitive screening instruments: A practical approach, 139-195.
Koo, J., Lee, J. H., Pyo, J., Jo, Y., & Lee, K. (2020). Exploiting Multi-Modal Features from Pre-Trained Networks for Alzheimer’s Dementia Recognition. Interspeech 2020, (pp. 2217-2221).
Liss, J., Seleri Assuno, S., Cummings, J., Atri, A., Geldmacher, D., Candela, S., . . . Mintzer, J. (2021). Practical recommendations for timely, accurate diagnosis of symptomatic Alzheimer’s disease (MCI and dementia) in primary care: a review and synthesis. Journal of internal medicine, 310-334.
Long, c. M., Thanh, H. T., & Toan, T. K. (2022). Giá trị của trắc nghiệm đánh giá trạng thái tâm thần tối thiểu (MMSE) trong sàng lọc sa sút trí tuệ ở người cao tuổi tại cộng đồng. Tạp chí nghiên cứu y học, 149 (1).
Maximilian, S., Fabien, R., & Schuller, B. (2016). At the Border of Acoustics and Linguistics: Bag-of-Audio-Words for the Recognition of Emotions in Speech. Interspeech 2016, (pp. 495--499).
Nhat, P. T., Van Hao, N., Tho, P. V., Kerdegari, H., Pisani, L., Thu, L. N., . . . others. (2023). Clinical benefit of AI-assisted lung ultrasound in a resource-limited intensive care unit. Critical Care, 257.
Nhat, P. T., Van Hao, N., Yen, L. M., Anh, N. H., Khiem, D. P., Kerdegari, H., . . . others. (2024). Clinical evaluation of AI-assisted muscle ultrasound for monitoring muscle wasting in ICU patients. Scientific reports, 14798.
Nhi, V. A., Thang, P., Thang, T. C., Hung, N. T., Lieu, N. V., Chinh, N. D., . . . Thanh, N. V. (2018, 04 03). Hội Alzheimer và rối loạn thần kinh nhận thức Việt Nam. Retrieved from Alzvietnam: http://alzvietnam.org/tai-lieu/huong-dan-chan-doan-va-dieu-tri-sa-sut-tri-tue-2018-85.html
Nicholas, C., Yilin, P., Zhao, R., Julian, F., Venkata, S. N., Heidi, C., . . . Aki, H. (2020). A Comparison of Acoustic and Linguistics Methodologies for Alzheimer’s Dementia Recognition. Interspeech 2020, (pp. 2182-2186).
Pulido, M. L., Hernández, J. B., MBallester, i. Á., Gonzalez, C. M., Mekyska, J., & Smékal, Z. (2020). Alzheimer's disease and automatic speech analysis: a review. Expert Systems with Applications, 113213.
Quoc, N. K., & Nhi, V. A. (2006). KHẢO SÁT THANG ĐIỂM MINI-MENTAL STATE EXAMINATION (MMSE) TRÊN NGƯỜI VIỆT NAM BÌNH THƯỜNG. Tạp chí Y học Thành phố Hồ Chí Minh, 237.
Safiri, S., Ghaffari Jolfayi, A., Fazlollahi, A., Morsali, S., Sarkesh, A., Daei Sorkhabi, A., . . . Hamidi, S. (2024). Alzheimer's disease: a comprehensive review of epidemiology, risk factors, symptoms diagnosis, management, caregiving, advanced treatments and associated challenges. Frontiers in Medicine, 1474043.
Shakeri, A., & Farmanbar, M. (2025). Natural language processing in Alzheimer's disease research: Systematic review of methods, data, and efficacy. Alzheimer's & dementia (Amsterdam, Netherlands), e70082.
Shin, J.-H. (2022). Dementia epidemiology fact sheet 2022. Annals of Rehabilitation Medicine, 53-59.
Tran Quoc, V., Nguyen Thi Ngoc, D., Nguyen Hoang, T., Vu Thi, H., Tong Duc, M., Do Pham Nguyet, T., . . . Bui Duc, T. (2023). Predicting antibiotic resistance in ICUs patients by applying machine learning in Vietnam. Infection and Drug Resistance, 5535-5546.
Tran, K., Nguyen, A., Vo, C., & Nguyen, P. (2022). Vietnamese Electronic Medical Record Management with Text Preprocessing for Spelling Errors. 2022 9th NAFOSTED Conference on Information and Computer Science (NICS), 223-229.
Truong, N. M., Vo, T. Q., Tran, H. T., Nguyen, H. T., & Pham, V. N. (2023). Healthcare students’ knowledge, attitudes, and perspectives toward artificial intelligence in the southern Vietnam. Heliyon, 12 (9).
Vu, H. T., Nguyen, T. A., Nguyen, T. T., Nguyen, A. T., Tran, D., Nguyen, H., . . . Pham, T. (2024). A national program to advance dementia research in Vietnam. BMC Health Services Research, 156.
Wang, Y.-q., Jia, R.-x., Liang, J.-h., Li, J., Qian, S., Li, J.-y., & Xu, Y. (2020). Effects of non-pharmacological therapies for people with mild cognitive impairment. A Bayesian network meta-analysis. International journal of geriatric psychiatry, 591-600.

16
Nội dung nghiên cứu khoa học, triển khai thực nghiệm của đề tài và phương án thực hiện


Triển khai các nội dung nghiên cứu của đề tài:

https://docs.google.com/spreadsheets/d/1LjSpN0cWYI9VbeEzOK4JRf0MTKTV7BWvrHkcIqqIeYs/edit?gid=0#gid=0

Khó khăn và giải pháp khắc phục:
Là nền tảng cho các nghiên cứu tiếp theo, việc chuẩn hóa các bài can thiệp nhận thức thông qua thu giọng nói là một bước quan trọng. Trong nghiên cứu này, chúng tôi sẽ khảo sát mức độ khó của các bài can thiệp nhằm đảm bảo rằng chúng phù hợp với bệnh nhân từ ba nhóm: bệnh nhân Alzheimer (AD), suy giảm nhận thức nhẹ (MCI) và nhóm đối chứng khỏe mạnh (HC), đồng thời duy trì tính thách thức đủ để thu được bộ cơ sở dữ liệu chất lượng.

Ứng dụng VoiceAI được xây dựng dựa trên một protocol kết hợp giữa SAGE , một công cụ đã được sử dụng rộng rãi để đánh giá suy giảm nhận thức, protocol DementiaBank ở năm 2023 và protocol của Talker và cộng sự 2024. Tuy nhiên, để khẳng định tính hiệu quả của phương pháp này, chúng tôi sẽ so sánh kết quả với các thang đo tiêu chuẩn như MMSE và MoCA.

Ngoài ra, một thách thức quan trọng là đảm bảo dữ liệu thu giọng nói có tính đồng nhất và đại diện tốt. Chúng tôi chỉ thu giọng nói của người miền Nam và hạn chế sự ảnh hưởng của phương ngữ nhằm đảm bảo chất lượng dữ liệu đầu vào. Đồng thời, việc thu thập dữ liệu sẽ được thực hiện sao cho đảm bảo sự phân bố đều về mặt nhân khẩu học giữa ba nhóm, giúp mô hình trí tuệ nhân tạo có thể học một cách tổng quát hơn.

Khi xây dựng mô hình trí tuệ nhân tạo để dự đoán hiệu quả can thiệp, chúng tôi kỳ vọng mô hình sẽ đạt độ chính xác trên 80%. Nếu mô hình không đạt được mức chính xác mong muốn, chúng tôi sẽ áp dụng các thuật toán tối ưu hóa mới để cải thiện hiệu suất, đồng thời xem xét các đặc trưng giọng nói quan trọng hơn nhằm tăng cường khả năng phân biệt giữa ba nhóm đối tượng nghiên cứu.

18
Cách tiếp cận, phương pháp nghiên cứu, kỹ thuật sử dụng

* Chỉ ghi những cá nhân có tên tại Mục 12


III. SẢN PHẨM KH&CN CỦA ĐỀ TÀI



V. NHU CẦU KINH PHÍ THỰC HIỆN ĐỀ TÀI VÀ NGUỒN KINH PHÍ 
(Giải trình chi tiết trong phụ lục kèm theo)

Đơn vị tính: Triệu đồng

(*): chỉ dự toán khi đề tài đã được phê duyệt




| 1 | Tên đề tài: VoiceAI: phát hiện sớm Alzheimer và suy giảm nhận thức nhẹ thông qua phân tích lời nói. | Tên đề tài: VoiceAI: phát hiện sớm Alzheimer và suy giảm nhận thức nhẹ thông qua phân tích lời nói. | Tên đề tài: VoiceAI: phát hiện sớm Alzheimer và suy giảm nhận thức nhẹ thông qua phân tích lời nói. | Tên đề tài: VoiceAI: phát hiện sớm Alzheimer và suy giảm nhận thức nhẹ thông qua phân tích lời nói. | 1a | Mã số (được cấp khi Hồ sơ trúng tuyển) | Mã số (được cấp khi Hồ sơ trúng tuyển) | Mã số (được cấp khi Hồ sơ trúng tuyển) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |
| 2 | Thời gian thực hiện: 12 tháng | Thời gian thực hiện: 12 tháng | Thời gian thực hiện: 12 tháng | Thời gian thực hiện: 12 tháng | 3 | Cấp quản lý | Cấp quản lý | Cấp quản lý |
| (Từ tháng 12/2025 đến tháng 12/2026) | (Từ tháng 12/2025 đến tháng 12/2026) | (Từ tháng 12/2025 đến tháng 12/2026) | (Từ tháng 12/2025 đến tháng 12/2026) | (Từ tháng 12/2025 đến tháng 12/2026) | Bộ	                               ☐
Ngành                 	         ☐   
Cơ sở 	                               ☒ | Bộ	                               ☐
Ngành                 	         ☐   
Cơ sở 	                               ☒ | Bộ	                               ☐
Ngành                 	         ☐   
Cơ sở 	                               ☒ |  |
| 4 | Tổng kinh phí thực hiện: | Tổng kinh phí thực hiện: | Tổng kinh phí thực hiện: | Tổng kinh phí thực hiện: | Tổng kinh phí thực hiện: | Tổng kinh phí thực hiện: | Tổng kinh phí thực hiện: |  |
| Nguồn | Nguồn | Nguồn | Nguồn | Kinh phí (triệu đồng) | Kinh phí (triệu đồng) | Kinh phí (triệu đồng) | Kinh phí (triệu đồng) |  |
| - Tự túc | - Tự túc | - Tự túc | - Tự túc |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| 5 | Phương thức khoán chi: | Phương thức khoán chi: | Phương thức khoán chi: |  |  |  |  |  |
| Khoán đến sản phẩm cuối cùng | Khoán đến sản phẩm cuối cùng | Khoán đến sản phẩm cuối cùng | Khoán đến sản phẩm cuối cùng | Khoán từng phần, trong đó: | Khoán từng phần, trong đó: | Khoán từng phần, trong đó: | Khoán từng phần, trong đó: |  |
|  |  |  |  | - Kinh phí khoán: 
- Kinh phí không khoán: | - Kinh phí khoán: 
- Kinh phí không khoán: | - Kinh phí khoán: 
- Kinh phí không khoán: | - Kinh phí khoán: 
- Kinh phí không khoán: |  |
| 6 | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác |  |
|  | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác | Hình thức: Đề tài          Nhiệm vụ                              
Thuộc:
☐   Chương trình, Đề án KH&CN (Ghi rõ tên chương trình, nếu có), Mã số:
☐   Dự án KH&CN (Ghi rõ tên dự án, nếu có), Mã số:
☒   Độc lập, Mã số:
☐   Khác |  |
| 7 | Lĩnh vực khoa học | Lĩnh vực khoa học | Lĩnh vực khoa học | Lĩnh vực khoa học | Lĩnh vực khoa học | Lĩnh vực khoa học | Lĩnh vực khoa học |  |
|  | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. | ☐   Tự nhiên;                             	☐   Nông, lâm, ngư nghiệp;
 	☒   Kỹ thuật và công nghệ;    	☒  Y dược. |  |
| 8 | Chủ nhiệm đề tài | Chủ nhiệm đề tài | Chủ nhiệm đề tài | Chủ nhiệm đề tài | Chủ nhiệm đề tài | Chủ nhiệm đề tài | Chủ nhiệm đề tài |  |
| Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: | Họ và tên: Ths. Hoàng Tiến Trọng Nghĩa
Ngày, tháng, năm sinh:  11/10/ 1986       Giới tính:  Nam          / Nữ:
Chức danh chuyên môn - kỹ thuật - nghiệp vụ:  Bác sĩ
Học hàm, học vị: Thạc sĩ                          Chức vụ: Chủ nghiệm khoa Nội Thần kinh
Điện thoại: 0976035999
       Đơn vị:  
Nhà riêng:                                                 Mobile: 
Fax:                                                           E-mail: dr.hnghia@gmail.com
Tên đơn vị đang công tác: Khoa Nội Thần kinh, Bệnh viện Quân y 175
       Địa chỉ đơn vị: 786 Nguyễn Kiệm, phường 3, quận Gò Vấp, TPHCM
Địa chỉ nhà riêng: |  |
| 9 | Đơn vị chủ trì thực hiện đề tài | Đơn vị chủ trì thực hiện đề tài | Đơn vị chủ trì thực hiện đề tài | Đơn vị chủ trì thực hiện đề tài | Đơn vị chủ trì thực hiện đề tài | Đơn vị chủ trì thực hiện đề tài | Đơn vị chủ trì thực hiện đề tài |  |
| Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 | Tên đơn vị chủ trì thực hiện đề tài: Khoa Nội Thần kinh, Bệnh viện Quân y 175
Họ và tên thủ trưởng đơn vị: 
Tên đơn vị chủ quản đề tài: Bệnh viện Quân y 175 |  |
| 10 | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) | Các đơn vị phối hợp chính thực hiện đề tài (nếu có) |  |
|  |  |  |  |  |  |  |  |  |
| 11 | Các cán bộ thực hiện đề tài | Các cán bộ thực hiện đề tài | Các cán bộ thực hiện đề tài | Các cán bộ thực hiện đề tài | Các cán bộ thực hiện đề tài | Các cán bộ thực hiện đề tài | Các cán bộ thực hiện đề tài |  |
| (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) | (Ghi những người có đóng góp khoa học và chủ trì thực hiện những nội dung chính thuộc đơn vị chủ trì và đơn vị phối hợp tham gia thực hiện đề tài, không quá 10 người kể cả chủ nhiệm đề tài) |  |
| TT | TT | Họ và tên, cấp bậc,
học hàm, học vị | Tổ chức
công tác | Tổ chức
công tác | Nội dung, 
công việc chính tham gia | Nội dung, 
công việc chính tham gia | Thời gian làm việc cho đề tài  
(Số tháng
 quy đổi2) |  |
| 1 | 1 | TS. Hà Thị Thanh Hương | Trường Đại học Quốc tế
ĐHQG TPHCM | Trường Đại học Quốc tế
ĐHQG TPHCM | Chủ nhiệm
đề tài | Chủ nhiệm
đề tài | 12 tháng |  |
| 2 | 2 | TS. Ngô Thanh Hoàn | Florida Southern College | Florida Southern College | Đồng Chủ nhiệm đề tài | Đồng Chủ nhiệm đề tài | 12 tháng |  |
| 3 | 3 | ThS. BS. Hoàng Tiến Trọng Nghĩa | Bệnh viện Quân Y 175 | Bệnh viện Quân Y 175 | Đồng 
chủ nhiệm 
đề tài | Đồng 
chủ nhiệm 
đề tài | 12 tháng |  |
| 4 | 4 | ThS.BS. Huỳnh Đăng Lộc | Bệnh viện Quân Y 175 | Bệnh viện Quân Y 175 | Thành viên | Thành viên | 12 tháng |  |
| 5 | 5 | BS. Lý Minh Đăng | Bệnh viện Quân Y 175 | Bệnh viện Quân Y 175 | Thành viên | Thành viên | 12 tháng |  |
| 6 | 6 | BS. Nguyễn Xuân Diệu | Bệnh viện Quân Y 175 | Bệnh viện Quân Y 175 | Thành viên | Thành viên | 12 tháng |  |
| 7 | 7 | BS. Trần Thị Hoài Thu | Bệnh viện Quân Y 175 | Bệnh viện Quân Y 175 | Thành viên | Thành viên | 12 tháng |  |
| 8 | 8 | Nguyễn Trương Thanh Nhật | Trường Đại học Quốc tế
ĐHQG TPHCM | Trường Đại học Quốc tế
ĐHQG TPHCM | Thành viên | Thành viên | 12 tháng |  |
| 9 | 9 | Vũ Nguyễn Minh Đức | Trường Đại học Quốc tế
ĐHQG TPHCM | Trường Đại học Quốc tế
ĐHQG TPHCM | Thành viên | Thành viên | 12 tháng |  |
| 10 | 10 | Phan Ngọc Minh Thư | Trường Đại học Quốc tế
ĐHQG TPHCM | Trường Đại học Quốc tế
ĐHQG TPHCM | Thành viên | Thành viên | 12 tháng |  |
| 11 | 11 | Đỗ Nguyễn Ánh Nhân | Trường Đại học Quốc tế
ĐHQG TPHCM | Trường Đại học Quốc tế
ĐHQG TPHCM | Thành viên | Thành viên | 12 tháng | 12 tháng |
| Lĩnh vực ứng dụng | Mô tả nghiên cứu | Nơi lấy dữ liệu |
| --- | --- | --- |
| Chẩn đoán hình ảnh (CT, MRI, X-Quang) | Sử dụng AI để hỗ trợ trong siêu âm cơ và phổi ở đơn vị hồi sức tích cực (ICU) (Nhat, et al., 2023; Nhat, et al., 2024).
Dùng AI để phân biệt tổn thương viêm từ khối u trong não bằng ảnh MRI (Han, et al., 2022). | Bệnh viện Bạch Mai |
| Dự đoán nguy cơ trong y tế | Dự đoán kháng thuốc ở bệnh nhân ICU bằng áp dụng học máy ở Việt Nam (Tran Quoc, et al., 2023). | Bệnh viện Phú Thọ và bệnh viện quân y 175 |
| Xử lý ngôn ngữ y khoa | Ứng dụng công nghệ vào việc sửa lỗi chính tả ở các hồ sơ điện tử (Tran, Nguyen, Vo, & Nguyen, 2022). |  |
| (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. | (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. | (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. | (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. | (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. | (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. | (Luận cứ rõ cách tiếp cận vấn đề nghiên cứu, thiết kế nghiên cứu, phương pháp nghiên cứu, kỹ thuật sẽ sử dụng gắn với từng nội dung chính của đề tài; so sánh với các phương pháp giải quyết tương tự khác và phân tích để làm rõ được tính mới, tính độc đáo, tính sáng tạo của đề tài)


PHƯƠNG PHÁP TIẾP CẬN
Tuyển chọn mẫu:
Tổng cộng n = 180 với phân phối cụ thể: 60 người khoẻ mạnh (nhóm chứng), 60 người bệnh được chẩn đoán MCI, 60 người bệnh được chẩn đoán AD.
Tiêu chuẩn lựa chọn: 
+ Người bệnh MCI và AD được chẩn đoán (1) thỏa tiêu chuẩn của National Institute on Aging and the Alzheimer’s Association (NIA-AA 2011) bao gồm sử dụng các bài kiểm tra chức năng nhận thức phổ biến hiện nay, ví dụ: Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ, (2) trình độ học vấn 9/12, (3) đồng ý tham gia nghiên cứu.
+ Người khoẻ mạnh: không thoả tiêu chuẩn MCI hoặc AD theo NIA-AA 2011
Tiêu chuẩn loại trừ: (1) điều trị bằng thuốc ức chế cholinesterase hoặc các loại thuốc khác có thể ảnh hưởng đến hoạt động nhận thức, (2) mắc bất kỳ bệnh nào ảnh hưởng đến hệ thần kinh trung ương (đa xơ cứng - Multiple Sclerosis, Parkinson, đột quỵ, …), (3) nghiện rượu, (4) mất hoặc giảm thính lực, (5) có vấn đề về thị lực cản trở việc sử dụng ứng dụng, (6) không đồng ý tham gia nghiên cứu.
Về nguồn để tuyển đối tượng tham gia nghiên cứu: nhóm nghiên cứu dựa trên lưu lượng bệnh nhân đến khám bệnh tại bệnh viện Quân Y 175. Bên cạnh lưu lượng bệnh nhân chủ động đến khám bệnh, nhóm nghiên cứu còn tận dụng nguồn bệnh nhân là đoàn thăm khám sức khoẻ đến từ các công ty và tổ chức đăng ký dịch vụ khám tại bệnh viện 175. Hồ sơ y đức sẽ phải được thông qua trước khi nghiên cứu bắt đầu. Tất cả các tình nguyện viên đủ điều kiện sẽ được yêu cầu ký vào biên bản đồng ý tham gia nghiên cứu.
Dự liệu thu từ bệnh nhân:
Nhân khẩu học:

Tiền sử bệnh: ghi nhận các thông tin chi tiết về những vấn đề sức khỏe có liên quan đến suy giảm nhận thức mà người bệnh đang trải qua trong cuộc sống (ví dụ: bệnh tiểu đường, cao huyết áp, mỡ trong máu cao, tim mạch, đột quỵ, béo phì, trầm cảm, bệnh lý liên quan đến giấc ngủ. 
Kết quả bài đánh giá nhận thức: MMSE, MoCA, Test nhớ từ CERAD, Trail Making Test, Digit Span, Lưu loát từ, Vẽ đồng hồ
Kết quả đánh giá rối loạn hành vi tâm lý: NPI-Q
Dữ liệu âm thanh (chi tiết ở phần dưới)

Thiết kế phòng thu dữ liệu:
Phòng cách âm.
Một bàn ở giữa.
Hai ghế tựa lưng có tay vịn ở 2 bên bàn.
Một laptop chạy ứng dụng thu âm.
Một micro thu dữ liệu âm thanh từ người tham gia.
Một bản photo những câu hỏi để khai thác thông tin lời nói từ người tham gia.
5 bức ảnh đồ vật thông thường.
2 bức ảnh để người tham gia mô tả.
Một giấy chứa bộ câu 2 câu hỏi để người tham gia đọc theo
Quá trình thu nhận dữ liệu âm thanh:
Nhiệm vụ lời nói (speech tasks) (dự kiến 20 phút):
Kéo dài âm “a” (1 phút):
Hướng dẫn: “Cô/ chú hãy hít một hơi thật sâu và nói `aaa` kéo dài hết mức có thể.”
Đọc câu (2 – 3 phút):
Hướng dẫn: “Cô/ chú hãy đọc to và rõ ràng các câu sau đây:”
		“Tôi chỉ biết rằng Nam là người cần được giúp đỡ hôm nay”
		“Con mèo hay trốn dưới đi vắng khi con chó ở trong phòng”
Chỉ vào từng câu cho người tham gia đọc.
Lặp lại cụm từ (1 phút):
Hướng dẫn: “Cô/ chú hãy lặp lại từ ‘lấp lánh’ nhanh và rõ ràng nhất có thể trong 10 giây.” 
Bấm 10 giây khi người tham gia bắt đầu.
Nhiệm vụ nhận thức – ngôn ngữ (cognitive – linguistic tasks):
Mô tả tranh (3 phút): hiển thị 2 bức tranh phức tạp 

Hướng dẫn: “Giờ cô/ chú hãy mô tả tất cả những gì cô/ chú thấy trong bức tranh này càng chi tiết càng tốt. Cô/ Chú có 60 giây cho mỗi bức tranh.”
Truy hồi câu chuyện (tức thì và trì hoãn) (2 – 3 phút):
Hướng dẫn: “Bây giờ con sẽ đọc cho bạn nghe một câu chuyện ngắn. Cô/ Chú hãy lắng nghe cẩn thận vì sau đó con sẽ nhờ cô/ chú kể lại.”
Câu chuyện: “Cửa hàng bách hóa của ông Bình tổ chức đợt khuyến mãi lớn hàng năm, từ thứ Ba đến hết tuần. Các mặt hàng thể thao được giảm giá 75%, còn áo khoác thì giảm 30%. Khách mua hàng rất đông, chen lấn nhau để giành lấy những món đồ tốt nhất. Sau giờ đóng cửa, khi đợt khuyến mãi kết thúc, ông chủ đã tặng mỗi nhân viên một phần quà cảm ơn họ đã làm việc vất vả.”

Hướng dẫn với `tức thì`: “Bây giờ, cô/ chú hãy kể lại tất cả những gì cô/ chú nhớ về câu chuyện con vừa kể.”
Kể truyện theo tranh (3 – 4 phút):
“Dự chuyện tấm cám”

Hướng dẫn: “Giờ cô/ chú hãy nhìn các bức tranh này theo thứ tự. Sau đó kể lại một câu chuyện về những gì cô/ chú thấy. Cô/ chú nhớ kể câu chuyện có phần mở đầu, diễn biến và kết thúc.”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc thứ 2:
“Cô/ chú nhòn xem (chỉ vào tranh) và kể cho con bất kì phần nào của câu chuyện cũng được ạ.”
Nếu phản hồi ít hơn 2 – 3 câu hoặc dừng quá sớm, đưa ra lời nhắc thức 3:
“Cô/ chú có thể cho con biết thêm điều già khác về câu chuyện được không?” hay “chuyện gì xảy ra tiếp theo ạ.” 
Liệt kê từ theo chủ đề (3 phút):
Chủ đề ngữ nghĩa: “Trong 60 giây, cô/ chú kể tên càng nhiều loại động vật càng tốt cho con nghe được không?”
Chủ đề âm vị: “Trong 60 giây, cô/ chú hãy kể tên càng nhiều từ bắt đầu bằng chữ `L` càng tốt, không kể tên riêng hay địa danh nha cô. chú.”
Gọi tên đồ vật (2 phút): hiển thị hình ảnh 5 đồ vật thông thường:

Câu hỏi: “Đây là cái gì?”
Tìm điểm tương đồng (1 phút):
Hướng dẫn: “Giờ cô/ chú nghĩ một cái đồng hồ và một cái thước kẻ giống nhau ở điểm nào?”
Nếu không có phản hồi trong 10 giây, có thể nhắc: “Bạn nghĩ xem chúng có điểm gì chung.”
Giải thích quy trình (2 phút):
Hướng dẫn: “Cô/ chú có thể giải thích các bước để pha một tách trà được không?”
Nếu không có phản hồi trong 10 giây, đưa ra lời nhắc: “Nếu muốn pha một tách trà, cô/ chú sẽ làm các bước thể nào ạ?”
Tính toán đơn giản: (xem xét cần không?)
Hướng dẫn: “Nếu bạn mua một món đồ giá 35 ngàn và đưa 100 ngàn, bạn được trả lại bao nhiêu tiền?”
Câu hướng dẫn với `trì hoãn` (1 – 2 phút):
Hướng dẫn: “Lúc trước, con có kể cho cô/ chú nghe một câu chuyện. Bây giờ cô/ chú có thể kể lại tất cả những gì cô/ chú nhớ về câu chuyện đó không?”
Nếu trong 10 giây người tham gia không nhớ, gợi ý chung: “Cô/ chú có nhớ con đã kể một câu chuyện không?”
Kết thúc:
Câu nói: “Chúng ta đã hoàn thành bài kiểm tra ngày hôm nay. Con cảm ơn cô/ chú rất nhiều vì đã giành thời gian tham gia nghiên cứu của con ạ.”

Đánh giá hiệu quả ứng dụng:
Đánh giá độ khó bài can thiệp: Phân tích tỷ lệ hoàn thành, thời gian thực hiện và lỗi sai của từng nhóm (AD, MCI, HC) để xem các bài tập có phù hợp và đủ thách thức không. 
Xác thực tương quan (Concurrent Validity): So sánh kết quả (điểm số hoặc chỉ số) từ VoiceAI với điểm số từ các thang đo chuẩn như MMSE và MoCA trên cùng một nhóm người tham gia. Tính toán hệ số tương quan để xem VoiceAI đo lường có giống các công cụ đã được kiểm chứng hay không.
Đánh giá hiệu suất Mô hình AI: 
Độ chính xác (Accuracy): Tính tỷ lệ phần trăm dự đoán đúng nhóm (AD, MCI, HC) hoặc hiệu quả can thiệp. Mục tiêu là trên 80%.
Precision, Recall, F1-Score: Đánh giá hiệu suất cho từng nhóm riêng biệt.
Ma trận nhầm lẫn (Confusion Matrix): Xem xét cụ thể các loại lỗi mà mô hình mắc phải.
Kiểm tra chất lượng dữ liệu: Đảm bảo sự cân bằng về nhân khẩu học giữa ba nhóm và tính đồng nhất về phương ngữ (giọng miền Nam) trong dữ liệu giọng nói thu thập được. 
So sánh với nghiên cứu trước: Đối chiếu kết quả tương quan giữa VoiceAI và MMSE/MoCA của bạn với các kết quả đã được công bố trong các nghiên cứu trước đây về SAGE. |
| --- | --- | --- | --- | --- | --- | --- |
| 19 | Phương án phối hợp với các tổ chức, đơn vị nghiên cứu và cơ sở sản xuất trong nước | Phương án phối hợp với các tổ chức, đơn vị nghiên cứu và cơ sở sản xuất trong nước | Phương án phối hợp với các tổ chức, đơn vị nghiên cứu và cơ sở sản xuất trong nước | Phương án phối hợp với các tổ chức, đơn vị nghiên cứu và cơ sở sản xuất trong nước | Phương án phối hợp với các tổ chức, đơn vị nghiên cứu và cơ sở sản xuất trong nước | Phương án phối hợp với các tổ chức, đơn vị nghiên cứu và cơ sở sản xuất trong nước |
| (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 | (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 | (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 | (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 | (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 | (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 | (Trình bày rõ phương án phối hợp: tên các tổ chức, đơn vị phối hợp chính tham gia thực hiện đề tài và nội dung công việc tham gia trong đề tài, kể cả các cơ sở sản xuất hoặc những người sử dụng kết quả nghiên cứu; khả năng đóng góp về nhân lực, tài chính, cơ sở hạ tầng-nếu có). 

Đối với đề tài VoiceAI này, chúng tôi nhận được sự hợp tác rất lớn từ Khoa Nội thần Kinh của bệnh viện Quân Y 175, mà cụ thể đó chính là sự hợp tác của nhóm nghiên cứu của Bác sĩ Hoàng Tiến Trọng Nghĩa.
Trong nghiên cứu lần này, nhóm tôi đã nhận được sự hỗ trợ rất lớn từ phía bệnh viện Quân Y 175 ở những mục sau: 
Đề xuất, góp ý và hỗ trợ chỉnh sửa đề cương khoa học trước khi tiến hành thực hiện nghiên cứu 
Hỗ trợ xin Y Đức ở Hội đồng Y Đức tại bệnh viện Quân Y 175
Hỗ trợ nghiên cứu và đề xuất bộ tiêu chuẩn tuyển chọn đối tượng bệnh nhân MCI tham gia nghiên cứu
Hỗ trợ tuyển đối tượng tham gia nghiên cứu từ nguồn bệnh nhân đến và thăm khám tại bệnh viện Quân Y 175 |
| 20 | Phương án hợp tác quốc tế (nếu có)
(Trình bày rõ phương án phối hợp: tên đối tác nước ngoài; nội dung đã hợp tác- đối với đối tác đã có hợp tác từ trước; nội dung cần hợp tác trong khuôn khổ đề tài; hình thức thực hiện. Phân tích rõ lý do cần hợp tác và dự kiến kết quả hợp tác, tác động của hợp tác đối với kết quả của đề tài) | Phương án hợp tác quốc tế (nếu có)
(Trình bày rõ phương án phối hợp: tên đối tác nước ngoài; nội dung đã hợp tác- đối với đối tác đã có hợp tác từ trước; nội dung cần hợp tác trong khuôn khổ đề tài; hình thức thực hiện. Phân tích rõ lý do cần hợp tác và dự kiến kết quả hợp tác, tác động của hợp tác đối với kết quả của đề tài) | Phương án hợp tác quốc tế (nếu có)
(Trình bày rõ phương án phối hợp: tên đối tác nước ngoài; nội dung đã hợp tác- đối với đối tác đã có hợp tác từ trước; nội dung cần hợp tác trong khuôn khổ đề tài; hình thức thực hiện. Phân tích rõ lý do cần hợp tác và dự kiến kết quả hợp tác, tác động của hợp tác đối với kết quả của đề tài) | Phương án hợp tác quốc tế (nếu có)
(Trình bày rõ phương án phối hợp: tên đối tác nước ngoài; nội dung đã hợp tác- đối với đối tác đã có hợp tác từ trước; nội dung cần hợp tác trong khuôn khổ đề tài; hình thức thực hiện. Phân tích rõ lý do cần hợp tác và dự kiến kết quả hợp tác, tác động của hợp tác đối với kết quả của đề tài) | Phương án hợp tác quốc tế (nếu có)
(Trình bày rõ phương án phối hợp: tên đối tác nước ngoài; nội dung đã hợp tác- đối với đối tác đã có hợp tác từ trước; nội dung cần hợp tác trong khuôn khổ đề tài; hình thức thực hiện. Phân tích rõ lý do cần hợp tác và dự kiến kết quả hợp tác, tác động của hợp tác đối với kết quả của đề tài) | Phương án hợp tác quốc tế (nếu có)
(Trình bày rõ phương án phối hợp: tên đối tác nước ngoài; nội dung đã hợp tác- đối với đối tác đã có hợp tác từ trước; nội dung cần hợp tác trong khuôn khổ đề tài; hình thức thực hiện. Phân tích rõ lý do cần hợp tác và dự kiến kết quả hợp tác, tác động của hợp tác đối với kết quả của đề tài) |
|  |  |  |  |  |  |  |
| 21 | 21 | Tiến độ thực hiện | Tiến độ thực hiện | Tiến độ thực hiện | Tiến độ thực hiện | Tiến độ thực hiện |
|  |  | Các nội dung, công việc
 chủ yếu cần được thực hiện; các mốc đánh giá chủ yếu | Kết quả phải đạt | Thời gian (bắt đầu,
 kết thúc) | Cá nhân, 
tổ chức 
thực hiện* | Dự kiến 
kinh phí |
| (1) | (1) | (2) | (3) | (4) | (5) | (6) |
| 1 | 1 | Nghiên cứu và đề xuất đề cương khoa học | Bộ đề cương nghiên cứu khoa học về dự án VoiceAI | 02 – 06/2025 | Chủ nhiệm đề tài và nhóm nghiên cứu |  |
| 2 | 2 | Chuẩn bị Hồ sơ cho Nghiên cứu | Bộ hồ sơ cho đề tài bao gồm: (1) Thuyết minh đề tài (bản tiếng Việt), (2) Thuyết minh đề tài (bản tiếng Anh), (3) Hồ sơ Y Đức, (4) Lý lịch Khoa học của các thành viên nhóm nghiên cứu | 02 – 06/2025 | Chủ nhiệm đề tài và nhóm nghiên cứu |  |
| 3 | 3 | Nộp hồ sơ Y Đức | Sự cho phép nghiên cứu từ hội đồng Y Đức tại bệnh viện Quân Y 175 | 04/2025 | Chủ nhiệm đề tài, nhóm nghiên cứu và nhóm đồng nghiên cứu đến từ bệnh viện Quân Y 175 |  |
| 4 | 4 | Trình bày đề cương, đề xuất hợp tác | Trình bày đề cương nghiên cứu đến nhóm nghiên cứu hợp tác | 06/2025 | Chủ nhiệm đề tài và nhóm nghiên cứu |  |
| 5 | 5 | Xác định nội dung và tính năng ứng dụng VoiceAI | VoiceAI
(bản thử nghiệm) | 06/2025 – 07/2025 | Chủ nhiệm đề tài và nhóm nghiên cứu |  |
| 6 | 6 | Tuyển chọn đối tượng tham gia nghiên cứu | Danh sách 180 (nhóm AD: 60, nhóm MCI: 60, nhóm đối chứng: 60) đối tượng đồng ý tham gia nghiên cứu | 07/2025 | Chủ nhiệm đề tài, nhóm nghiên cứu, nhóm đồng nghiên cứu đến từ bệnh viện Quân Y 175 |  |
| 7 | 7 | Nghiên cứu thị trường và tối ưu hoá VoiceAI | VoiceAI
(bản chính thức sử dụng cho nghiên cứu) | 10/2025 – 11/2025 | Chủ nhiệm đề tài và nhóm nghiên cứu |  |
| 8 | 8 | Tiến hành thu thập dữ liệu từ nhóm đối tượng nghiên cứu | Dữ liệu âm thanh lời nói và điểm số nhận thức thu từ nhóm cỡ mẫu | 09/2025 – 01/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu, nhóm đồng nghiên cứu đến từ bệnh viện Quân Y 175 |  |
| 9 | 9 | Đánh giá sự hiệu quả ứng dụng | Xác định mức độ chính xác của ứng dụng so với các thang đo MMSE và MoCA | 02/2026 – 03/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu |  |
| 10 | 10 | Tiền xử lý dữ liệu thu thập | Bộ dữ liệu sau khi lọc nhiễu và loại bỏ những đoạn dữ liệu không cần thiết | 01/2026 – 02/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu |  |
| 11 | 11 | Trích xuất đặc trưng dữ liệu | Bộ dữ liệu với các trích xuất đặc trưng được nghiên cứu về âm học và ngôn ngữ học. | 02/2026 – 03/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu |  |
| 12 | 12 | Xây dựng mô hình và đánh giá hiệu suất | Mô hình được viết và đánh giá dựa trên ngôn ngữ lập trinh Python | 01/2026 – 03/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu |  |
| 13 | 13 | Tối ưu hoá mô hình | Báo cáo sau mỗi lần điều chỉnh mô hình và mô hình phân loại mới | 04/2026 – 06/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu |  |
| 14 | 14 | Thu thập kết quả nghiên cứu và viết báo cáo | Bản báo cáo về kết quả nghiên cứu, bàn luận cũng như hướng phát triển tiếp theo cho nghiên cứu | 06/2026 | Chủ nhiệm đề tài, nhóm nghiên cứu |  |
| 22 | 22 | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) | Sản phẩm KH&CN chính của đề tài và yêu cầu chất lượng cần đạt (Liệt kê theo dạng sản phẩm) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) | Dạng I: Mẫu (model, maket); sản phẩm (Vũ khí, trang bị kỹ thuật; vật liệu; thiết bị, máy móc, dây chuyền công nghệ...) |
| Số TT | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Đơn vị đo | Đơn vị đo | Mức chất lượng | Mức chất lượng | Mức chất lượng | Mức chất lượng | Dự kiến số lượng/quy mô sản phẩm tạo ra | Dự kiến số lượng/quy mô sản phẩm tạo ra |
| Số TT | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Đơn vị đo | Đơn vị đo | Cần đạt | Mẫu tương tự 
(theo các tiêu chuẩn mới nhất) | Mẫu tương tự 
(theo các tiêu chuẩn mới nhất) | Mẫu tương tự 
(theo các tiêu chuẩn mới nhất) | Dự kiến số lượng/quy mô sản phẩm tạo ra | Dự kiến số lượng/quy mô sản phẩm tạo ra |
| Số TT | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu của sản phẩm | Đơn vị đo | Đơn vị đo | Cần đạt | Trong nước | Trong nước | Thế giới | Dự kiến số lượng/quy mô sản phẩm tạo ra | Dự kiến số lượng/quy mô sản phẩm tạo ra |
| (1) | (2) | (2) | (2) | (3) | (3) | (4) | (5) | (5) | (6) | (7) | (7) |
| 1 | Ứng dụng hỗ trợ sàng lọc MCI và AD (VoiceAI). | Ứng dụng hỗ trợ sàng lọc MCI và AD (VoiceAI). | Ứng dụng hỗ trợ sàng lọc MCI và AD (VoiceAI). | Ứng dụng | Ứng dụng |  |  |  |  |  |  |
| 2 | Bộ dữ liệu âm thanh của 60 bệnh nhân MCI, 60 bệnh nhân AD và 60 người khoẻ mạnh. | Bộ dữ liệu âm thanh của 60 bệnh nhân MCI, 60 bệnh nhân AD và 60 người khoẻ mạnh. | Bộ dữ liệu âm thanh của 60 bệnh nhân MCI, 60 bệnh nhân AD và 60 người khoẻ mạnh. | Bộ | Bộ |  |  |  |  |  |  |
| 3 | Mô hình dự đoán bệnh AD, MCI bằng lời nói. | Mô hình dự đoán bệnh AD, MCI bằng lời nói. | Mô hình dự đoán bệnh AD, MCI bằng lời nói. | Mô hình | Mô hình |  |  |  |  |  |  |
| 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) | 22.1. Mức chất lượng các sản phẩm (Dạng I) so với các sản phẩm tương tự trong nước và nước ngoài (Làm rõ cơ sở khoa học và thực tiễn để xác định các chỉ tiêu về chất lượng cần đạt của các sản phẩm của đề tài) |
| Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác | Dạng II: Báo cáo tổng hợp kết quả đề tài; tài liệu thiết kế, tài liệu công nghệ, tính năng chiến - kỹ thuật sản phẩm; nguyên lý ứng dụng; phương pháp; tiêu chuẩn; quy phạm; phần mềm máy tính; sơ đồ, bản đồ; số liệu, cơ sở dữ liệu; Báo cáo phân tích; Tài liệu dự báo (phương pháp, quy trình, mô hình,...); đề án, quy hoạch; luận chứng kinh tế - kỹ thuật, báo cáo nghiên cứu khả thi và các sản phẩm khác |
| TT | TT | Tên sản phẩm | Tên sản phẩm | Tên sản phẩm | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Ghi chú |
| 2 | 2 | Ứng dụng hỗ trợ sàng lọc MCI và AD (VoiceAI). | Ứng dụng hỗ trợ sàng lọc MCI và AD (VoiceAI). | Ứng dụng hỗ trợ sàng lọc MCI và AD (VoiceAI). | Đảm bảo tính Y Đức trong phát triển và tối ưu hóa mô hình khi thu thập phản hồi từ bệnh nhân | Đảm bảo tính Y Đức trong phát triển và tối ưu hóa mô hình khi thu thập phản hồi từ bệnh nhân | Đảm bảo tính Y Đức trong phát triển và tối ưu hóa mô hình khi thu thập phản hồi từ bệnh nhân | Đảm bảo tính Y Đức trong phát triển và tối ưu hóa mô hình khi thu thập phản hồi từ bệnh nhân | Đảm bảo tính Y Đức trong phát triển và tối ưu hóa mô hình khi thu thập phản hồi từ bệnh nhân | Đảm bảo tính Y Đức trong phát triển và tối ưu hóa mô hình khi thu thập phản hồi từ bệnh nhân |  |
| 3 | 3 | Bộ dữ liệu của nhóm đối tượng tham gia nghiên cứu | Bộ dữ liệu của nhóm đối tượng tham gia nghiên cứu | Bộ dữ liệu của nhóm đối tượng tham gia nghiên cứu | Bộ dữ liệu phải được thu thập từ nhóm đối tượng tham gia nghiên cứu phù hợp với bộ tiêu chí tuyển đối tượng tham gia nghiên cứu | Bộ dữ liệu phải được thu thập từ nhóm đối tượng tham gia nghiên cứu phù hợp với bộ tiêu chí tuyển đối tượng tham gia nghiên cứu | Bộ dữ liệu phải được thu thập từ nhóm đối tượng tham gia nghiên cứu phù hợp với bộ tiêu chí tuyển đối tượng tham gia nghiên cứu | Bộ dữ liệu phải được thu thập từ nhóm đối tượng tham gia nghiên cứu phù hợp với bộ tiêu chí tuyển đối tượng tham gia nghiên cứu | Bộ dữ liệu phải được thu thập từ nhóm đối tượng tham gia nghiên cứu phù hợp với bộ tiêu chí tuyển đối tượng tham gia nghiên cứu | Bộ dữ liệu phải được thu thập từ nhóm đối tượng tham gia nghiên cứu phù hợp với bộ tiêu chí tuyển đối tượng tham gia nghiên cứu |  |
| 4 | 4 | Mô hình dự đoán AD, MCI bằng lời nói. | Mô hình dự đoán AD, MCI bằng lời nói. | Mô hình dự đoán AD, MCI bằng lời nói. | Đảm bảo tính Y Đức trong mô hình | Đảm bảo tính Y Đức trong mô hình | Đảm bảo tính Y Đức trong mô hình | Đảm bảo tính Y Đức trong mô hình | Đảm bảo tính Y Đức trong mô hình | Đảm bảo tính Y Đức trong mô hình |  |
| 5 | 5 | Báo cáo nghiệm thu về kết quả thí nghiệm | Báo cáo nghiệm thu về kết quả thí nghiệm | Báo cáo nghiệm thu về kết quả thí nghiệm | Đảm bảo theo quy định | Đảm bảo theo quy định | Đảm bảo theo quy định | Đảm bảo theo quy định | Đảm bảo theo quy định | Đảm bảo theo quy định |  |
| Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác | Dạng III: Bài báo, sách, giáo trình và các ấn phẩm khác |
| Số TT | Số TT | Tên sản phẩm | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Yêu cầu khoa học cần đạt | Dự kiến nơi công bố (Tạp chí, Nhà xuất bản) | Dự kiến nơi công bố (Tạp chí, Nhà xuất bản) | Dự kiến nơi công bố (Tạp chí, Nhà xuất bản) | Ghi chú |
| (1) | (1) | (2) | (3) | (3) | (3) | (3) | (3) | (4) | (4) | (4) | (5) |
| 1 | 1 | 01 Bài báo khoa học | Tạp chí chuyên ngành | Tạp chí chuyên ngành | Tạp chí chuyên ngành | Tạp chí chuyên ngành | Tạp chí chuyên ngành |  |  |  |  |
| 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: | 22.2. Sản phẩm dự kiến đăng ký bảo hộ quyền sở hữu công nghiệp, sở hữu trí tuệ, giải pháp hữu ích, sáng kiến cải tiến kỹ thuật: |
| 23 | 23 | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu | Khả năng ứng dụng và phương thức chuyển giao kết quả nghiên cứu |
| 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) | 23.1. Khả năng về thị trường (Nhu cầu quân sự, quốc phòng, kinh tế - xã hội, nêu tên và nhu cầu đơn vị sử dụng cụ thể; điều kiện cần thiết để có thể đưa sản phẩm ra thị trường?)
	23.2. Khả năng về ứng dụng các kết quả nghiên cứu vào sản xuất kinh doanh (Khả năng cạnh tranh về giá thành và chất lượng sản phẩm)
	23.3.  Khả năng liên doanh liên kết với các doanh nghiệp trong quá trình nghiên cứu
        23.4 Mô tả phương thức chuyển giao
(Chuyển giao công nghệ trọn gói, chuyển giao công nghệ có đào tạo, chuyển giao theo hình thức trả dần theo tỷ lệ % của doanh thu; liên kết với doanh nghiệp để sản xuất hoặc góp vốn với đơn vị phối hợp nghiên cứu hoặc với cơ sở sẽ áp dụng kết quả nghiên cứu theo tỷ lệ đã thỏa thuận để cùng triển khai sản xuất; tự thành lập doanh nghiệp trên cơ sở kết quả nghiên cứu tạo ra…) |
| 24 | 24 | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài | Phạm vi và địa chỉ (dự kiến) ứng dụng các kết quả của đề tài |
| Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 | Phạm vi ứng dụng: Các bệnh viện, sở y tế, trung tâm sa sút trí tuệ ở miền nam Việt Nam
Địa chỉ dự kiến ứng dụng: Khoa Nội thần kinh Bệnh viện Quân y 175 |
| 25 | 25 | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu | Tác động và lợi ích mang lại của kết quả nghiên cứu |
| 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. | 25.1 Đối với quân sự, quốc phòng, kinh tế - xã hội và môi trường
Kết quả nghiên cứu của đề tài sẽ góp phần hỗ trợ sàng lọc bệnh MCI, AD từ giai đoạn sớm, từ đó đi khám tại các cơ sở y tế để nhận được các can thiệp kịp thời để ngăn tiến triển bệnh đến giai đoạn nặng hơn. Từ đó nghiên cứu định hướng thêm về việc tang cường chất lượng tầm soát ở tuyến xã, huyện.
 Đối với lĩnh vực KH&CN có liên quan
 Ở trong nước: Hiện nay, ở Việt Nam các lĩnh vực liên quan đến sức khỏe não bộ vẫn chưa được người dân chú trọng và quan tâm nhiều, thiếu các kiến thức liên quan đến bệnh lý về não “Năm 2020, Việt Nam có 500.000 bị Alzheimer nhưng chỉ có 5.000 người được chẩn đoán và điều trị (tương đương 1%).”(Thu, 2024)  và  không có kiến thức về bệnh lý MCI “Hơn 80% người tham gia ban đầu ít hoặc không biết về MCI’’ (Quỳnh, 2022). Do đó, chẩn đoán tại các cơ sở y tế thường không phải là giai đoạn sớm của bệnh và vấn đề điều trị và chăm sóc bệnh gặp rất nhiều khó khăn, đa số bệnh nhân được chăm sóc và theo dõi tại nhà. Tuy trên thế giới đã có dự án CognoSpeak tại trường đại học Sheffield ở Anh đã thực hiện nhưng chưa thực sự phù hợp với người Việt vì bị khác ngôn ngữ. Dự án VoiceAI for AD với mục đích tạo một hệ dữ liệu dành riêng cho người Việt. VoiceAI for AD với giá thành thấp, dễ tiếp cận (từ nông thôn đến thành thị) sẽ giúp người bệnh điều trị ngoại trú cũng như người nhà bệnh nhân có thể can thiệp kịp thời. Cũng như giúp bác sĩ xác định biện pháp can thiệp phù hợp nhất trong giai đoạn tiến triển quan trọng của bệnh. 
Ở quốc tế: Ở Anh, trường Sheffield đã có dự án CognoSpeak – là dự án sử dụng trí tuệ nhân tạo và công nghệ giọng nói để tự động phân tích ngôn ngữ và các mẫu giọng nói có thể đảm bảo sự điều tra chuyên môn sâu hơn và là dấu hiệu ban đầu của chứng mất trí hoặc bệnh Alzheimer với bộ dữ liệu bằng tiếng Anh nhưng còn hạn chế do chỉ có bộ ngôn ngữ tiếng Anh. Dự án trên được phát triển bởi Tiến sĩ Dan Blackburn từ Khoa Thần kinh học và Giáo sư Heidi Christensen từ Khoa Khoa học Máy tính tại Đại học Sheffield với mục đích giúp bệnh nhân bắt đầu hỗ trợ chẩn đoán, điều trị sớm hơn và giảm gánh nặng cho ngành y tế đồng thời bệnh nhân có thể được điều trị ngoại trú dưới sự theo dõi của các bác sỹ. Theo một cuộc khảo sát của Hiệp hội Alzheimer cho thấy “85% số người muốn ở nhà nếu được chẩn đoán mắc chứng mất trí” (Huxtable, 2025).
        25.3 Đối với đơn vị chủ trì và các cơ sở ứng dụng kết quả nghiên cứu
Đối với tổ chức chủ trì:
Dự án Voice AI làm tăng tính ứng dụng thực tiễn của các nghiên cứu về sức khỏe não bộ đến gần hơn với người dân và cộng đồng. Từ đó, sẽ thu hút các tổ chức y tế và doanh nghiệp.
Đối với các cơ sở ứng dụng kết quả nghiên cứu: 
Voice AI ra đời với kỳ vọng giúp giảm tải cho các bệnh viện và cơ sở y tế khi bệnh nhân có thể thực hiện kiểm tra nhận thức, có thể theo dõi tiến trình điều trị của bệnh nhân từ xa.
Hỗ trợ bác sĩ trong việc đánh giá bệnh nhân thông qua phân tích giọng nói, cách sử dụng ngôn từ, truyền đạt ý nghĩa lời nói và các bài kiểm tra nhận thức, giúp giảm thiểu sai sót chủ quan. |
| Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home | Danh sách tham khảo:
Thu, H. (2024, September 16). Chỉ 1% người mắc Alzheimer ở Việt Nam được thăm khám và điều trị. Retrieved April 10, 2025, from https://yte.nghean.gov.vn/tin-chuyen-nganh/chi-1-nguoi-mac-alzheimer-o-viet-nam-duoc-tham-kham-va-dieu-tri-691699?pageindex=0#:~:text=N%C4%83m%202020%2C%20Vi%E1%BB%87t%20Nam%20c%C3%B3,khai%20%C4%91i%E1%BB%81u%20tr%E1%BB%8B%20b%E1%BB%87nh%20Alzheimer
Quỳnh, C. (2022, March 21). Những dấu hiệu sớm của bệnh Alzheimer ít người biết đến. Retrieved April 10, 2025, from https://dienbientv.vn/tin-tuc-su-kien/y-te-suc-khoe/202203/nhung-dau-hieu-som-cua-benh-alzheimer-it-nguoi-biet-den-5770418/
Huxtable, A. (2025, March 25). Harnessing technology to help people with dementia remain at home. Retrieved April 10, 2025, from https://www.sheffield.ac.uk/news/harnessing-technology-help-people-dementia-remain-home |
| 27 | Kinh phí thực hiện đề tài phân theo các khoản chi | Kinh phí thực hiện đề tài phân theo các khoản chi | Kinh phí thực hiện đề tài phân theo các khoản chi | Kinh phí thực hiện đề tài phân theo các khoản chi | Kinh phí thực hiện đề tài phân theo các khoản chi | Kinh phí thực hiện đề tài phân theo các khoản chi | Kinh phí thực hiện đề tài phân theo các khoản chi |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | Nguồn kinh phí | Tổng số | Trong đó | Trong đó | Trong đó | Trong đó | Trong đó |
|  | Nguồn kinh phí | Tổng số | Trả công lao động (khoa học, phổ thông) | Nguyên, vật liệu, năng lượng | Thiết bị, máy móc | Xây dựng, sửa chữa nhỏ | Chi khác
(Thuế) |
| 1 | Tự túc |  |  |  |  |  |  |
|  | Tổng kinh phí |  |  |  |  | 5 |  |
|  |
| --- |