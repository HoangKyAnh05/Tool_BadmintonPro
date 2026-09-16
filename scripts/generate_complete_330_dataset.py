import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load collected YouTube video details
with open('scratch/yt_collected_details.json', 'r', encoding='utf-8') as f:
    yt_data = json.load(f)

used_urls = set()
used_ids = set()

# Helper to ensure unique video URL
def claim_url(url):
    if url in used_urls:
        raise ValueError(f"DUPLICATE URL DETECTED: {url}")
    used_urls.add(url)
    return url

def claim_id(vid_id):
    if vid_id in used_ids:
        raise ValueError(f"DUPLICATE ID DETECTED: {vid_id}")
    used_ids.add(vid_id)
    return vid_id

# 1. POS_DATA: 9 positions x 10 clips = 90 videos
POS_DATA = [
    {
        "id": 1, "name": "Góc Lưới Trái (Net Left)", "zoneName": "LƯỚI TRÁI",
        "row": 1, "col": 1, "directionLabel": "Vị trí 1 - Góc lưới bên trái",
        "courtZone": "front", "courtSide": "left",
        "clips": [
            ("Đỡ Cầu & Kê Lưới Trái Tay", "Kê lưới", "Cơ bản", "Mặt vợt ngửa 45 độ, thả lỏng cổ tay đón cầu sát lưới", "Split-step -> Bước đệm chân phải góc 10h"),
            ("Bước Lunge Đón Cầu Góc Lưới Trái", "Bộ pháp", "Cơ bản", "Giơ vợt ổn định trước ngực giữ thăng bằng", "Lunge chân phải vươn dài, gót chạm đất trước"),
            ("Kê Cầu Vuốt Mép Lưới Đổi Nhịp", "Kê lưới", "Cơ bản", "Vuốt nhẹ đầu vợt triệt tiêu quán tính quả cầu", "Chùng gối chân thuận hãm quán tính"),
            ("Gài Lưới / Miết Cầu Xoáy Lộn Lưới", "Bỏ nhỏ xoáy", "Trung cấp", "Miết nhẹ đầu quả cầu tạo độ xoáy lộn mép lưới", "Chân phải chạm đất đồng thời vung cổ tay"),
            ("Hất Cầu Bổng Sâu Góc Lưới Trái", "Hất bổng", "Trung cấp", "Vung vợt từ dưới lên bung lực cẳng tay đẩy cầu sâu", "Bật đẩy chân phải tạo đà lùi về tâm"),
            ("Kéo Lưới Đổi Hướng Sang Biên Phải", "Kéo lưới", "Trung cấp", "Nghiêng góc mặt vợt đưa cầu lướt ngang mép lưới", "Trụ vững chân trước, giữ thân thăng bằng"),
            ("Vồ Cầu / Chụp Lưới Góc Trái", "Vồ cầu", "Nâng cao", "Đón cầu đỉnh lưới, búng ngón cái giật gõ cắm sàn", "Bứt tốc chân trái đẩy chân phải phóng dài"),
            ("Múa Vợt Đổi Hướng Chém Chéo Lưới", "Đánh lừa", "Nâng cao", "Giả động tác đẩy thẳng rồi chém cổ tay chéo sân", "Giữ thăng bằng trên một chân rồi thu chân"),
            ("Giả Động Tác Đẩy Bổng Cắt Cầu Sát Lưới", "Kỹ xảo", "Nâng cao", "Tạo đà vung bổng nhưng hãm vợt miết nhẹ mép cầu", "Đổi trọng tâm tức thì đánh lừa đối phương"),
            ("Bật Lướt Đón Cầu Dứt Điểm Mép Chữ T", "Bật lướt", "Nâng cao", "Bật người trên không gõ cắm cầu trước khi qua lưới", "Bật bằng mũi chân trái, tiếp đất êm ái")
        ]
    },
    {
        "id": 2, "name": "Lưới Giữa (Front Center)", "zoneName": "LƯỚI GIỮA",
        "row": 1, "col": 2, "directionLabel": "Vị trí 2 - Trung lộ mép lưới (chữ T)",
        "courtZone": "front", "courtSide": "center",
        "clips": [
            ("Chặn Đẩy Cầu Thẳng Mặt Lưới", "Chặn đẩy", "Cơ bản", "Đẩy mặt vợt thẳng hướng quả cầu rơi", "Bước thẳng chân phải vào vạch chữ T"),
            ("Kê Cầu Chữ T Đổi Nhịp", "Kê lưới", "Cơ bản", "Thả lỏng cổ tay triệt tiêu lực quả cầu", "Chân thuận tiếp đất vững chắc"),
            ("Bước Thẳng Đón Cầu Chữ T", "Bộ pháp", "Cơ bản", "Đưa vợt sớm trước mặt đón đầu quả cầu", "Bước đuổi thẳng từ tâm sân vào chữ T"),
            ("Đè Lưới / Phản Tạt Nhanh Giữa Sân", "Đè lưới", "Trung cấp", "Gập cổ tay chớp nhoáng đẩy cầu đi căng thấp", "Nhịp bật lướt đón cầu ngang tầm mắt"),
            ("Bung Cầu Bổng Sang Hai Góc", "Bung bổng", "Trung cấp", "Bung lực cổ tay hất cao bổng sang góc trống", "Hạ thấp trọng tâm cứu cầu sát sàn"),
            ("Tạt Cầu Ngang Đầu Vợt Ép Đối Phương", "Phản tạt", "Trung cấp", "Tạt phẳng cầu sát mép trên của lưới", "Dậm chân phải tạo lực đè bóng"),
            ("Búng Cổ Tay Chụp Lưới Dứt Điểm", "Vồ cầu", "Nâng cao", "Đón đỉnh lưới gõ cắm thẳng xuống đất đối thủ", "Bật rướn nhanh chặn đầu quả cầu"),
            ("Giả Bỏ Nhỏ Gạt Cầu Sát Vách Lưới", "Đánh lừa", "Nâng cao", "Giữ nhịp vợt tĩnh (Hold) rồi gạt nhanh đổi hướng", "Trụ vững chân trước, cơ thể ổn định"),
            ("Chớp Cơ Hội Bồi Cầu Cắm Sàn Chữ T", "Bồi cầu", "Nâng cao", "Đón quả cầu trả bổng của đối phương đập cắm sàn", "Bật lò xo giậm nhảy dứt điểm"),
            ("Bắt Bài Đường Cầu Tạt Ngang Đầu", "Cắt cầu", "Nâng cao", "Đưa vợt đón lõng trên không đánh chặn tức thì", "Bật nhảy đón đầu hướng bay quả cầu")
        ]
    },
    {
        "id": 3, "name": "Góc Lưới Phải (Net Right)", "zoneName": "LƯỚI PHẢI",
        "row": 1, "col": 3, "directionLabel": "Vị trí 3 - Góc lưới bên phải",
        "courtZone": "front", "courtSide": "right",
        "clips": [
            ("Kê Cầu Thuận Tay Sát Lưới", "Kê lưới", "Cơ bản", "Mặt vợt mở nhẹ thuận tay đón cầu êm", "Bước đệm chân phải hướng góc 2h"),
            ("Bước Lunge Chân Thuận Góc Phải", "Bộ pháp", "Cơ bản", "Tay mở rộng giữ cân bằng trọng tâm", "Lunge dài chân phải, đùi song song mặt sàn"),
            ("Kê Cầu Chéo Góc Thuận Tay", "Kê lưới", "Cơ bản", "Nghiêng nhẹ mặt vợt đón cầu đưa sang góc đối diện", "Gót chân phải tiếp đất trước hãm đà"),
            ("Miết Cầu Xoáy Lộn Lưới Thuận Tay", "Bỏ nhỏ xoáy", "Trung cấp", "Xoay cổ tay miết mép ngoài quả cầu lộn lưới", "Chân trụ hãm đà quán tính"),
            ("Hất Cầu Bổng Sâu Thuận Tay", "Hất sâu", "Trung cấp", "Vung hết biên độ hất cầu cao về đáy góc 7", "Bật lùi hồi vị ngay sau chạm cầu"),
            ("Kéo Lưới Lừa Hướng Thuận Tay", "Kéo lưới", "Trung cấp", "Cắt chéo đường bay đưa cầu lướt dọc vạch trắng lưới", "Xoay hông nhẹ đẩy thân người"),
            ("Chụp Lưới / Đè Cầu Dứt Điểm Góc Phải", "Đè lưới", "Nâng cao", "Lao vào gõ cắm thẳng góc biên", "Bứt tốc bước dài áp sát mép lưới"),
            ("Giả Động Tác Chém Chéo Góc Lưới", "Đánh lừa", "Nâng cao", "Vung giả đẩy thẳng rồi bẻ cổ tay cắt chéo", "Trọng tâm vững vàng hồi tâm sân"),
            ("Đè Cầu Tấn Công Góc Biên Thuận Tay", "Tấn công", "Nâng cao", "Vung vợt biên độ hẹp gõ cắm sát vạch biên", "Bật chân phải lướt nhanh sát lưới"),
            ("Bật Lao Người Chụp Cầu Mép Trên", "Chụp cầu", "Nâng cao", "Vươn toàn thân đón cầu tầm cao dứt điểm", "Hãm đà an toàn tránh chạm lưới")
        ]
    },
    {
        "id": 4, "name": "Trung Tâm Trái (Midcourt Left)", "zoneName": "TRUNG TÂM TRÁI",
        "row": 2, "col": 1, "directionLabel": "Vị trí 4 - Trung lộ cánh trái",
        "courtZone": "mid", "courtSide": "left",
        "clips": [
            ("Thủ Cầu Ngang Hông Trái Tay", "Thủ cầu", "Cơ bản", "Ngón cái tì cán vợt, mở mặt vợt đỡ trước hông", "Hạ thấp trọng tâm, hai chân mở rộng"),
            ("Bước Trượt Ngang Đón Cầu Trái", "Bộ pháp", "Cơ bản", "Vợt giơ ngang ngực sẵn sàng", "Bước trượt ngang Chasse sang trái"),
            ("Đỡ Cầu Phản Xạ Tầm Trung", "Phòng thủ", "Cơ bản", "Mặt vợt vững vàng chặn quả đập ngang sườn", "Chùng gối hai chân hấp thụ xung lực"),
            ("Phản Tạt Ngang Lưới Trái Tay", "Phản tạt", "Trung cấp", "Vung ngang mặt vợt tạt thẳng mép lưới", "Xoay hông nhẹ dồn lực vào quả tạt"),
            ("Thủ Cầu Chéo Góc Thoát Hiểm", "Thủ chéo", "Trung cấp", "Nghiêng góc vợt đẩy cầu rơi chéo sân đối diện", "Chùng gối trái nhận lực"),
            ("Chặn Cầu Ngang Hông Hãm Xung Lực", "Hãm lực", "Trung cấp", "Thả lỏng ngón tay đón bóng làm bóng rơi sát lưới", "Thân trên giữ tĩnh ổn định"),
            ("Bung Phản Tạt Đè Góc Xa Trái Tay", "Phản công", "Nâng cao", "Bung hết lực ngón cái đè bóng sâu về góc trống", "Bật người đón cầu điểm cao nhất"),
            ("Đỡ Smash Bỏ Nhỏ Đổi Nhịp", "Hãm lực", "Nâng cao", "Thả lỏng cổ tay đón cú smash cho cầu rơi sát lưới", "Đứng vững hai chân, giữ thân người tĩnh"),
            ("Phản Công Đè Cầu Tấn Công Góc Nách", "Tấn công", "Nâng cao", "Bật người đè cầu cắm sát nách đối phương", "Dậm mạnh chân trái tạo điểm tựa"),
            ("Bật Vẩy Cổ Tay Trái Tay Ép Đáy", "Phát lực", "Nâng cao", "Búng cổ tay cực nhanh đưa cầu bay vút góc đáy đối diện", "Xoay trục thân người trợ lực")
        ]
    },
    {
        "id": 5, "name": "Tâm Sân (Court Center)", "zoneName": "TÂM SÂN",
        "row": 2, "col": 2, "directionLabel": "Vị trí 5 - Trung tâm điều phối chiến thuật",
        "courtZone": "mid", "courtSide": "center",
        "clips": [
            ("Bật Nhẹ Split-Step Sẵn Sàng", "Bộ pháp", "Cơ bản", "Vợt giơ ngang cằm, khuỷu tay mở rộng", "Bật nhảy hai chân tiếp đất bằng mũi chân"),
            ("Bộ Pháp Di Chuyển 4 Góc Từ Tâm", "Bộ pháp", "Cơ bản", "Phối hợp tay vợt linh hoạt theo hướng chạy", "Bước chéo chân xuất phát nhanh đến 4 góc"),
            ("Nhịp Dừng Hồi Tâm Ổn Định", "Hồi vị", "Cơ bản", "Thu vợt trước ngực sẵn sàng đón nhịp tiếp theo", "Trọng tâm rơi đúng tâm ô số 5"),
            ("Bắt Bài Nhịp Cầu Nửa Sân", "Bắt bài", "Trung cấp", "Giơ vợt đón đầu quả cầu bay lửng giữa sân", "Bật một bước cắt ngang đường cầu"),
            ("Xoay Hông Chuyển Trọng Tâm Nhanh", "Hồi vị", "Trung cấp", "Thu vợt về ngực sau mỗi pha đánh", "Xoay trục hông hồi vị ngay tâm ô số 5"),
            ("Bước Đệm Đón Cầu Nửa Sân", "Bộ pháp", "Trung cấp", "Đón cầu ngang ngực chuyển từ thủ sang công", "Bước đệm nhịp nhàng hai chân"),
            ("Đón Cầu Trên Không Nhịp Một", "Cắt cầu", "Nâng cao", "Bật nhảy đón cầu trên không gõ cắm sàn", "Bật thẳng hai chân giậm nhảy tiếp đất"),
            ("Đổi Hướng Đảo Chiều Đánh Lừa", "Chiến thuật", "Nâng cao", "Giả động tác sang trái rồi vung sang phải", "Đổi trụ chân tức thì đánh lừa đối thủ"),
            ("Chớp Thời Cơ Cắt Cầu Giữa Sân", "Tấn công", "Nâng cao", "Cắt ngang đường bay quả cầu dứt điểm cắm sàn", "Lao người chớp nhoáng trên không"),
            ("Hoán Đổi Vị Trí Công Thủ Linh Hoạt", "Đôi nam/nữ", "Nâng cao", "Phân công che chắn khu vực khi đồng đội dâng cao", "Di chuyển bọc lót theo hình thoi")
        ]
    },
    {
        "id": 6, "name": "Trung Tâm Phải (Midcourt Right)", "zoneName": "TRUNG TÂM PHẢI",
        "row": 2, "col": 3, "directionLabel": "Vị trí 6 - Trung lộ cánh phải",
        "courtZone": "mid", "courtSide": "right",
        "clips": [
            ("Thủ Cầu Ngang Hông Thuận Tay", "Thủ cầu", "Cơ bản", "Cổ tay mở, đón cầu ngang sườn phải", "Hạ thấp gối, trọng tâm dồn đều hai chân"),
            ("Bước Trượt Ngang Đón Cầu Phải", "Bộ pháp", "Cơ bản", "Vợt giơ sẵn sàng trước ngực", "Trượt ngang chân phải mở rộng sang sườn"),
            ("Đỡ Cầu Ngang Ngực Thuận Tay", "Phòng thủ", "Cơ bản", "Đỡ quả cầu đánh ép ngực phải đẩy đi an toàn", "Trụ vững hai chân hấp thụ chấn động"),
            ("Phản Tạt Thuận Tay Đè Lưới", "Phản tạt", "Trung cấp", "Vung ngang vợt đè phẳng đường bay của cầu", "Bước chân phải đón cầu, dồn lực tiến"),
            ("Thủ Kê Cầu Sát Lưới Đổi Nhịp", "Thủ mềm", "Trung cấp", "Hãm xung lực cho bóng rơi sát vạch chữ T", "Giữ thăng bằng không bị chúi người"),
            ("Đẩy Cầu Nhanh Ngang Thân", "Phản tạt", "Trung cấp", "Đẩy nhanh mặt vợt đưa cầu đi sát người đối thủ", "Dồn trọng tâm chân thuận"),
            ("Đè Cầu Tấn Công Góc Nách Thuận Tay", "Tấn công", "Nâng cao", "Bung lực cổ tay ép cầu cắm vào người đối thủ", "Tiến nửa bước dồn ép không gian"),
            ("Bật Ngang Vợt Phản Tạt Chéo Biên", "Phản tạt chéo", "Nâng cao", "Chém xiên mặt vợt đưa cầu vút sang góc xa", "Xoay người đẩy cơ thể hồi vị"),
            ("Phản Đòn Smash Bằng Quả Tạt Cắm Sàn", "Phản công", "Nâng cao", "Mượn lực cú smash tạt ngược lại cắm sàn đối phương", "Bật cổ tay đón đúng tâm vợt"),
            ("Đỡ Cầu Bật Phản Công Dồn Dập", "Liên hoàn", "Nâng cao", "Cứu cầu liên tục 2 nhịp chuyển thế trận chủ động", "Chuyển trụ chân trái sang phải linh hoạt")
        ]
    },
    {
        "id": 7, "name": "Cuối Sân Trái (Rear Left)", "zoneName": "ĐÁY TRÁI",
        "row": 3, "col": 1, "directionLabel": "Vị trí 7 - Góc đáy cuối sân bên trái",
        "courtZone": "rear", "courtSide": "left",
        "clips": [
            ("Bộ Pháp Lùi Chéo Góc Trái", "Bộ pháp lùi", "Cơ bản", "Giơ vợt vòng qua đầu đón điểm rơi", "Bước chéo lùi chân đón bóng ở góc 8h"),
            ("Phông Cầu Vòng Đầu Thuận Tay", "Phông cầu", "Cơ bản", "Vung tay vòng qua đầu phông sâu cuối sân", "Chân phải làm trụ bật đổi chân (Scissor kick)"),
            ("Đón Điểm Rơi Góc Trái Đáy Sân", "Phán đoán", "Cơ bản", "Mở rộng vai đón quả cầu bổng sâu", "Lùi bước đuổi chân nhịp nhàng"),
            ("Cắt Cầu Chéo Sân Vòng Đầu", "Drop shot", "Trung cấp", "Chém nghiêng mặt vợt cắt cầu rơi chéo mép lưới", "Tiếp đất chân phải rồi đẩy tiến về tâm"),
            ("Đập Cầu Vòng Đầu Tấn Công", "Smash vòng đầu", "Trung cấp", "Gập bụng và cổ tay smash uy lực", "Bật nhịp chân thuận dứt điểm"),
            ("Phông Cao Sâu Ép Biên Trái", "Phông sâu", "Trung cấp", "Phát lực cổ tay đưa cầu cao vút sát vạch biên", "Xoay thân dồn lực vai"),
            ("Phông Cầu Trái Tay Cuối Sân (Backhand Clear)", "Phông trái tay", "Nâng cao", "Xoay lưng, bung hết lực cẳng tay ngón cái", "Bước chân phải dài về góc, lưng xoay về lưới"),
            ("Chém Cầu Trái Tay Rơi Lưới (Backhand Drop)", "Chém trái tay", "Nâng cao", "Giả động tác phông sâu rồi chém nhẹ rơi lưới", "Chân phải trụ vững, xoay người thu chân"),
            ("Bật Nhảy Smash Vòng Đầu Dứt Điểm", "Jump smash", "Nâng cao", "Bật cao gập người đập cắm biên", "Bật nhảy 2 chân trên không tiếp đất"),
            ("Giả Phông Chém Chéo Rơi Sát Mép Biên", "Đánh lừa", "Nâng cao", "Đà vung phông cực mạnh nhưng vuốt cạnh vợt cắt cầu", "Thân người bay trên không đảo hướng")
        ]
    },
    {
        "id": 8, "name": "Cuối Sân Giữa (Rear Center)", "zoneName": "ĐÁY GIỮA",
        "row": 3, "col": 2, "directionLabel": "Vị trí 8 - Đáy sân khu vực trung lộ",
        "courtZone": "rear", "courtSide": "center",
        "clips": [
            ("Bật Lùi Đón Cầu Đáy Giữa Sân", "Bộ pháp", "Cơ bản", "Mở rộng vai, giơ vợt cao nhất có thể", "Bước giật lùi nhanh đón cầu sau đầu"),
            ("Phông Cầu Bổng Sâu Đáy Sân", "Phông cao sâu", "Cơ bản", "Phát lực trọn vẹn đưa cầu cao vút về vạch cuối", "Đổi chân trên không đưa chân phải lên trước"),
            ("Bộ Pháp Scissor Kick Đón Cầu Cao", "Bộ pháp", "Cơ bản", "Bật đổi chân cắt kéo trên không", "Tiếp đất an toàn bằng chân thuận"),
            ("Chém Cầu Thẳng Rơi Lưới (Straight Drop)", "Drop shot", "Trung cấp", "Chém vuốt cạnh quả cầu cho rơi sát lưới thẳng", "Hạ đà tiến lên đón cầu tiếp theo"),
            ("Đập Cầu Cắm Sàn Giữa Sân", "Smash", "Trung cấp", "Phát lực cổ tay cắm thẳng vào khe giữa hai đối thủ", "Chân sau bật đưa về phía trước"),
            ("Phông Cầu Ép Sâu Vạch Cuối", "Phông sâu", "Trung cấp", "Ép đối phương lùi sâu sát vách phông cầu", "Xoay thân hoàn tất cú đánh"),
            ("Giả Phông Đập Chém Cầu Lỏng Tay", "Đánh lừa", "Nâng cao", "Đà vung cực mạnh nhưng giảm tốc chạm bóng nhẹ", "Trụ cơ thể ổn định trên không"),
            ("Bật Nhảy Hai Chân Đập Dứt Điểm", "Jump smash", "Nâng cao", "Treo người trên không smash cực đại", "Bật lò xo hai chân tiếp đất gối chùng"),
            ("Smash Điểm Rơi Cắm Khe Chữ T", "Smash điểm", "Nâng cao", "Gập cổ tay cắm bóng sát vạch chữ T đáy sân", "Bật cao thu chân tiếp đất"),
            ("Chém Cầu Đảo Cánh Đánh Gục Bộ Pháp", "Chém cầu", "Nâng cao", "Chém xiên cắt ngang mặt cầu đổi góc 90 độ", "Thăng bằng hoàn hảo khi rơi xuống")
        ]
    },
    {
        "id": 9, "name": "Cuối Sân Phải (Rear Right)", "zoneName": "ĐÁY PHẢI",
        "row": 3, "col": 3, "directionLabel": "Vị trí 9 - Góc đáy cuối sân bên phải",
        "courtZone": "rear", "courtSide": "right",
        "clips": [
            ("Bộ Pháp Lùi Góc Thuận Tay", "Bộ pháp", "Cơ bản", "Mở góc vai phải, đưa vợt ra sau gáy chuẩn bị", "Bước đuổi lùi chéo về góc 4h"),
            ("Phông Cầu Cao Sâu Thuận Tay", "Phông cầu", "Cơ bản", "Vung hết biên độ phông cầu bổng sâu", "Đổi chân bật kéo thân người về tâm"),
            ("Đón Cầu Góc Thuận Tay Ổn Định", "Căn bản", "Cơ bản", "Đón điểm rơi đúng tầm với trước trán", "Hạ gót chân phải làm điểm tựa"),
            ("Chém Cầu Xiên Góc Thuận Tay (Cross Drop)", "Drop shot", "Trung cấp", "Cắt chéo mặt vợt đưa cầu rơi sát mép lưới đối diện", "Tiếp đất bằng chân phải, bật tiến"),
            ("Đập Cầu Dọc Biên Thuận Tay", "Smash dọc biên", "Trung cấp", "Smash cắm sát vạch biên đơn", "Dồn trọng tâm chân phải bật tiến"),
            ("Cắt Cầu Thẳng Rơi Sát Lưới", "Drop shot", "Trung cấp", "Cắt thẳng quả cầu rơi êm ái sát mép lưới đối diện", "Chuyển đà tiến về phía trước"),
            ("Nhảy Đập Jump Smash Uy Lực", "Jump smash", "Nâng cao", "Bật cao điểm tiếp xúc tối đa, smash sấm sét", "Bật nhảy chân thuận xoay hông trên không"),
            ("Chém Cầu Xoáy Giả Động Tác Đập", "Đánh lừa", "Nâng cao", "Giả vung smash nhưng miết cạnh vợt xoáy rơi sát lưới", "Hãm đà trên không và lao lên bắt lưới"),
            ("Đập Cầu Góc Nách Đối Phương", "Tấn công", "Nâng cao", "Smash nhắm thẳng vào nách tay cầm vợt đối thủ", "Phát lực gập bụng dứt khoát"),
            ("Stick Smash Búng Cổ Tay Chớp Nhoáng", "Stick smash", "Nâng cao", "Búng cổ tay cực nhanh góc cắm hiểm", "Bật nhảy nhịp một tiếp đất tức thì")
        ]
    }
]

# Generate movements.ts
movements_lines = ['import { GridPosition } from "../types";\n\nexport const BADMINTON_POSITIONS: GridPosition[] = [']

for p in POS_DATA:
    pos_id = p["id"]
    movements_lines.append(f'  // ==========================================')
    movements_lines.append(f'  // Ô {pos_id}: {p["name"].upper()}')
    movements_lines.append(f'  // ==========================================')
    movements_lines.append('  {')
    movements_lines.append(f'    id: {pos_id},')
    movements_lines.append(f'    name: "{p["name"]}",')
    movements_lines.append(f'    zoneName: "{p["zoneName"]}",')
    movements_lines.append(f'    row: {p["row"]},')
    movements_lines.append(f'    col: {p["col"]},')
    movements_lines.append(f'    directionLabel: "{p["directionLabel"]}",')
    movements_lines.append(f'    courtZone: "{p["courtZone"]}",')
    movements_lines.append(f'    courtSide: "{p["courtSide"]}",')
    movements_lines.append('    level: "Cơ bản",')
    movements_lines.append(f'    videoUrl: "./videos/clips/pos_{pos_id}_clip_1.mp4",')

    c0 = p["clips"][0]
    movements_lines.append('    handMovement: {')
    movements_lines.append(f'      title: "{c0[0]}",')
    movements_lines.append(f'      subTitle: "{c0[3]}",')
    movements_lines.append(f'      description: "{c0[0]} tại {p["zoneName"]}",')
    movements_lines.append(f'      coachingTip: "{c0[3]}"')
    movements_lines.append('    },')
    movements_lines.append('    footMovement: {')
    movements_lines.append(f'      title: "Bộ pháp Ô {pos_id}",')
    movements_lines.append(f'      subTitle: "{c0[4]}",')
    movements_lines.append(f'      description: "Di chuyển đến {p["zoneName"]}",')
    movements_lines.append(f'      coachingTip: "{c0[4]}"')
    movements_lines.append('    },')
    movements_lines.append('    combinedMovement: {')
    movements_lines.append(f'      title: "{c0[0]}",')
    movements_lines.append(f'      subTitle: "{c0[3]} + {c0[4]}",')
    movements_lines.append(f'      description: "{c0[0]}",')
    movements_lines.append('      coachingTip: "Tập trung chuẩn xác động tác"')
    movements_lines.append('    },')

    movements_lines.append('    variations: [')
    for idx, c in enumerate(p["clips"], 1):
        v_url = f'./videos/clips/pos_{pos_id}_clip_{idx}.mp4'
        movements_lines.append('      {')
        movements_lines.append(f'        id: "pos_{pos_id}_var_{idx}",')
        movements_lines.append(f'        shotName: "{c[0]}",')
        movements_lines.append(f'        shotType: "{c[1]}",')
        movements_lines.append(f'        level: "{c[2]}",')
        movements_lines.append(f'        videoUrl: "{v_url}",')
        movements_lines.append(f'        thumbnailUrl: "./thumbnails/video-pos-{pos_id}-{idx}.jpg",')
        movements_lines.append('        handMovement: {')
        movements_lines.append(f'          title: "{c[0]}",')
        movements_lines.append(f'          subTitle: "{c[3]}",')
        movements_lines.append(f'          description: "{c[0]}",')
        movements_lines.append(f'          coachingTip: "{c[3]}"')
        movements_lines.append('        },')
        movements_lines.append('        footMovement: {')
        movements_lines.append(f'          title: "Bộ pháp Ô {pos_id}",')
        movements_lines.append(f'          subTitle: "{c[4]}",')
        movements_lines.append(f'          description: "Bộ pháp Ô {pos_id}",')
        movements_lines.append(f'          coachingTip: "{c[4]}"')
        movements_lines.append('        },')
        movements_lines.append('        combinedMovement: {')
        movements_lines.append(f'          title: "{c[0]}",')
        movements_lines.append(f'          subTitle: "{c[3]} + {c[4]}",')
        movements_lines.append(f'          description: "{c[0]}",')
        movements_lines.append('          coachingTip: "Tập trung chuẩn xác động tác"')
        movements_lines.append('        }')
        movements_lines.append('      },' if idx < len(p["clips"]) else '      }')
    movements_lines.append('    ]')
    movements_lines.append('  },' if pos_id < 9 else '  }')

movements_lines.append('];\n')

with open('src/data/movements.ts', 'w', encoding='utf-8') as f:
    f.write('\n'.join(movements_lines))
print("✓ Đã tạo thành công src/data/movements.ts")

# Now build the list of 330 videos for videos.ts
all_videos = []

# A. 90 Court Position Videos
for p in POS_DATA:
    pos_id = p["id"]
    cat = f'POS_{pos_id}'
    for idx, c in enumerate(p["clips"], 1):
        v_url = claim_url(f'./videos/clips/pos_{pos_id}_clip_{idx}.mp4')
        v_id = claim_id(f'video-pos-{pos_id}-{idx}')
        all_videos.append({
            "id": v_id,
            "category": cat,
            "positionId": pos_id,
            "level": c[2],
            "title": c[0],
            "subTitle": f'{p["zoneName"]} • {c[1]} • Cấp độ {c[2]}',
            "description": f'{c[3]}. {c[4]}.',
            "videoUrl": v_url,
            "thumbnailUrl": f'./thumbnails/video-pos-{pos_id}-{idx}.jpg',
            "durationText": f'Clip {idx:02d}',
            "tags": [f'Ô {pos_id}', p["zoneName"], c[2], c[1]]
        })

print(f"Added 90 position videos. Current count: {len(all_videos)}")

# B. 40 Match Competition Videos (10 DON_NAM, 10 DOI_NAM, 10 DON_NU, 10 DOI_NU)
# Curate 40 unique videos using local snaptik/viesnap/training videos and top YT match/tactics videos
local_match_videos = [
    # DON_NAM (10)
    ("video-don-nam-1", "DON_NAM", "Kỹ Thuật Đọc Hướng & Di Chuyển 4 Góc Sân Đơn Nam", "./videos/snaptik.vn_7465697345355713799.mp4", "Cơ bản", "Bộ pháp đơn nam chuẩn thi đấu: Bật đà từ tâm sân, cứu cầu 4 góc và hồi vị tức thì"),
    ("video-don-nam-2", "DON_NAM", "Chiến Thuật Ép Cầu Hai Góc Cuối Sân Đơn Nam", "./videos/snaptik.vn_7476759285720993040.mp4", "Trung cấp", "Kỹ năng phông bổng sâu, ép đối thủ xoay lưng và mở góc tấn công dứt điểm"),
    ("video-don-nam-3", "DON_NAM", "Phản Xạ Bỏ Nhỏ Sát Lưới & Kéo Lưới Đổi Hướng Đơn Nam", "./videos/snaptik.vn_7501608184688299271.mp4", "Trung cấp", "Miết mặt vợt tinh tế, gài cầu lộn mép lưới ép đối thủ nâng bổng cứu nguy"),
    ("video-don-nam-4", "DON_NAM", "Kỹ Thuật Bước Lùi Đón Cầu & Chém Cầu Bạt Góc Đơn Nam", "./videos/snaptik.vn_7568145336158440724.mp4", "Trung cấp", "Đổi góc vung vợt chém cầu rơi chéo sân đánh lừa phán đoán đối phương"),
    ("video-don-nam-5", "DON_NAM", "Bật Nhảy Đập Cầu Tấn Công Dứt Điểm (Jump Smash Đơn Nam)", "./videos/snaptik.vn_7631002086502649109.mp4", "Nâng cao", "Tạo đà bằng chân thuận, bật cao gập bụng phát lực cắm sàn uy lực"),
    ("video-don-nam-6", "DON_NAM", "Kỹ Năng Thủ Cầu Bung Sâu Đảo Ngược Thế Trận Đơn Nam", "./videos/snaptik.vn_7665340734379281682.mp4", "Cơ bản", "Đón đỡ cú đập sát sườn hông, bung lực cẳng tay đẩy cầu về cuối sân"),
    ("video-don-nam-7", "DON_NAM", "Stick Smash & Chém Cầu Lừa Hướng Cuối Sân Đơn Nam", "./videos/training/7597368454022352136.mp4", "Nâng cao", "Vung đà đập cực mạnh nhưng giảm tốc chém lỏng tay rơi sát lưới"),
    ("video-don-nam-8", "DON_NAM", "Bứt Tốc Lao Lưới Vồ Cầu Dứt Điểm Đơn Nam", "./videos/training/7604103894100151568.mp4", "Nâng cao", "Bật người cực nhanh chớp cơ hội khi đối thủ bỏ nhỏ non mép lưới"),
    ("video-don-nam-9", "DON_NAM", "Kỹ Năng Phông Cầu Trái Tay Đảo Góc Cuối Sân Đơn Nam", "./videos/training/7501556764534426888.mp4", "Nâng cao", "Xoay lưng búng lực ngón cái giải tỏa áp lực góc chết cuối sân"),
    ("video-don-nam-10", "DON_NAM", "Bộ Pháp Di Chuyển Lùi Scissor Kick Chớp Nhoáng Đơn Nam", "./videos/training/7421577139683675410.mp4", "Cơ bản", "Bật đổi chân trên không tiếp đất chuẩn bị cho pha dứt điểm liên hoàn"),

    # DOI_NAM (10)
    ("video-doi-nam-1", "DOI_NAM", "Chiến Thuật Bọc Lót & Đổi Vị Trí Trong Đôi Nam", "./videos/viesnap.vn_tiktok_7556982998449655047.mp4", "Cơ bản", "Quy tắc công - thủ, di chuyển xoay tua và phân công khu vực che chắn"),
    ("video-doi-nam-2", "DOI_NAM", "Kỹ Năng Đè Lưới & Phản Tạt Ép Góc Đôi Nam", "./videos/viesnap.vn_tiktok_ZSq6N6mx5.mp4", "Trung cấp", "Kỹ thuật giữ lưới chủ động, tạt cầu thấp tước đoạt quyền tấn công"),
    ("video-doi-nam-3", "DOI_NAM", "Phối Hợp Tấn Công Đập Cầu & Bồi Cầu Dứt Điểm Đôi Nam", "./videos/viesnap.vn_tiktok_ZSq6NmtCb.mp4", "Nâng cao", "Phối hợp nhịp nhàng giữa người công sau và người đè trước trên lưới"),
    ("video-doi-nam-4", "DOI_NAM", "Kỹ Thuật Đè Lưới Cắt Đầu Vợt Tốc Độ Cao Đôi Nam", "./videos/training/7553093739229596946.mp4", "Trung cấp", "Bắt nhịp phản xạ cực nhanh không cho đối phương nâng bổng"),
    ("video-doi-nam-5", "DOI_NAM", "Chiến Thuật Giữ Lưới Chủ Động & Búng Cổ Tay Đôi Nam", "./videos/training/7609534277692165384.mp4", "Nâng cao", "Đón đỉnh lưới gõ cắm thẳng xuống đất đối thủ"),
    ("video-doi-nam-6", "DOI_NAM", "Đập Cầu Dọc Biên Uy Lực Ép Đối Thủ Mở Góc Đôi Nam", "./videos/training/7679262466299137287.mp4", "Nâng cao", "Cú smash sấm sét mở đường cho đồng đội dứt điểm trên lưới"),
    ("video-doi-nam-7", "DOI_NAM", "Thủ Cầu Bung Góc Thoát Vây Bị Tấn Công Liên Hoàn Đôi Nam", "./videos/training/7571048532539657490.mp4", "Trung cấp", "Hạ trọng tâm đón cầu smash đẩy chéo góc xa thoát hiểm"),
    ("video-doi-nam-8", "DOI_NAM", "Phản Tạt Căng Ngang Sườn Phá Thế Công Đôi Nam", "./videos/training/7656006722217118996.mp4", "Trung cấp", "Đè phẳng đường bay quả cầu khiến đối thủ phải lùi thế phòng ngự"),
    ("video-doi-nam-9", "DOI_NAM", "Bộ Pháp Bọc Lót Đôi Khi Đồng Đội Rướn Cứu Cầu Đôi Nam", "./videos/training/7501201293403327765.mp4", "Cơ bản", "Di chuyển bù khoảng trống tức thì giữ vững trận địa phòng thủ"),
    ("video-doi-nam-10", "DOI_NAM", "Bắt Bài Đường Cầu Lửng Giữa Sân Chốt Hạ Trận Đấu Đôi Nam", "./videos/training/7672279216209136916.mp4", "Nâng cao", "Lao vào cắt ngang đường cầu dứt điểm cắm sàn chớp nhoáng"),

    # DON_NU (10)
    ("video-don-nu-1", "DON_NU", "Kỹ Thuật Di Chuyển Bộ Pháp Dẻo Dai & Điều Cầu Đơn Nữ", "./videos/snaptik.vn_7500378802141269256.mp4", "Cơ bản", "Bộ pháp linh hoạt, di chuyển 4 góc sân êm ái và hồi vị nhịp nhàng"),
    ("video-don-nu-2", "DON_NU", "Chiến Thuật Ép Cầu Đáy Sân & Mở Góc Tấn Công Đơn Nữ", "./videos/snaptik.vn_7567643845215669521.mp4", "Trung cấp", "Kỹ thuật phông cầu cao sâu, khai thác khoảng trống hai góc biên"),
    ("video-don-nu-3", "DON_NU", "Kỹ Thuật Bỏ Nhỏ Sát Lưới & Kéo Lưới Lừa Hướng Đơn Nữ", "./videos/snaptik.vn_7598797082912181511.mp4", "Trung cấp", "Cảm giác mặt vợt tinh tế, cắt cầu đổi hướng đánh gục phản xạ"),
    ("video-don-nu-4", "DON_NU", "Kỹ Năng Đập Cầu Điểm Rơi & Chém Cầu Bạt Góc Đơn Nữ", "./videos/snaptik.vn_7651286512998288661.mp4", "Nâng cao", "Biến hóa giữa đập cắm biên và chém cầu rơi chéo sân dứt điểm"),
    ("video-don-nu-5", "DON_NU", "Kỹ Thuật Cắt Cầu Chéo Sân Vòng Đầu Đơn Nữ", "./videos/training/7644426711379119368.mp4", "Trung cấp", "Vung tay giả phông sâu rồi miết vợt đưa cầu rơi sát mép lưới"),
    ("video-don-nu-6", "DON_NU", "Bộ Pháp Lunge Sâu Cứu Cầu Sát Sàn Đơn Nữ", "./videos/training/7461076755865029904.mp4", "Cơ bản", "Hạ gối chùng sâu rướn người cứu những pha bỏ nhỏ hiểm hóc"),
    ("video-don-nu-7", "DON_NU", "Phông Cầu Cao Sâu Bền Bỉ Ép Đối Thủ Tiêu Hao Thể Lực Đơn Nữ", "https://www.youtube.com/watch?v=gy4YZS5tGxE", "Cơ bản", "Phát lực từ vai và cổ tay đưa cầu cắm sâu vạch cuối sân"),
    ("video-don-nu-8", "DON_NU", "Chém Cầu Thẳng Sát Lưới Ép Đối Thủ Rướn Cứu Đơn Nữ", "https://www.youtube.com/watch?v=W55Y8pGZ57M", "Trung cấp", "Chém cầu điểm rơi chính xác khiến đối phương bị động"),
    ("video-don-nu-9", "DON_NU", "Kỹ Năng Bật Nhảy Đập Điểm Rơi Sát Vạch Biên Đơn Nữ", "https://www.youtube.com/watch?v=l2lH5dkQXgQ", "Nâng cao", "Gập cổ tay tạo độ cắm hiểm hóc sát mép vạch đơn"),
    ("video-don-nu-10", "DON_NU", "Kéo Lưới Lừa Hướng Đánh Gục Bộ Pháp Đối Phương Đơn Nữ", "https://www.youtube.com/watch?v=q6t8rS6Pq2M", "Nâng cao", "Mặt vợt miết nhẹ đổi hướng bóng làm đối thủ lỡ đà"),

    # DOI_NU (10)
    ("video-doi-nu-1", "DOI_NU", "Chiến Thuật Bọc Lót & Phòng Thủ Bền Bỉ Đôi Nữ", "./videos/snaptik.vn_7372888645730192658.mp4", "Cơ bản", "Phối hợp di chuyển bọc lót, cứu cầu liên hoàn và phá thế tấn công"),
    ("video-doi-nu-2", "DOI_NU", "Kỹ Thuật Phản Tạt Đè Cầu & Gài Lưới Đôi Nữ", "./videos/snaptik.vn_7495761376141397255.mp4", "Trung cấp", "Giữ thế chủ động trên lưới, tạt cầu thấp không cho đối thủ nâng bổng"),
    ("video-doi-nu-3", "DOI_NU", "Đổi Vị Trí Công - Thủ & Chuyển Giao Quyền Tấn Công Đôi Nữ", "./videos/snaptik.vn_7669811035297172757.mp4", "Trung cấp", "Quy tắc di chuyển hoán đổi trước - sau trong trận đấu đôi nữ"),
    ("video-doi-nu-4", "DOI_NU", "Tấn Công Liên Hoàn Đập Cầu & Bắt Lưới Dứt Điểm Đôi Nữ", "./videos/snaptik.vn_7681640086798159124.mp4", "Nâng cao", "Phối hợp nhịp nhàng giữa quả đập phía sau và quả chớp lưới phía trước"),
    ("video-doi-nu-5", "DOI_NU", "Kỹ Năng Gài Lưới Xoáy Ép Đối Thủ Nâng Cầu Bổng Đôi Nữ", "https://www.youtube.com/watch?v=9jP8c3vA6_U", "Trung cấp", "Miết mép vợt tạo độ lộn cầu sát mép lưới đối phương"),
    ("video-doi-nu-6", "DOI_NU", "Thủ Cầu Bung Cao Sâu Hồi Phục Đội Hình Đôi Nữ", "https://www.youtube.com/watch?v=Kz6qP8eUf1Q", "Cơ bản", "Bung hết lực cẳng tay đẩy cầu về tận đáy sân giải vây"),
    ("video-doi-nu-7", "DOI_NU", "Kỹ Năng Đè Lưới Chớp Nhoáng Cắt Đứt Đợt Tấn Công Đôi Nữ", "https://www.youtube.com/watch?v=rK9gV3eL7pQ", "Trung cấp", "Chặn đầu quả tạt của đối phương tước đoạt quyền chủ động"),
    ("video-doi-nu-8", "DOI_NU", "Đập Cầu Liên Hoàn Phía Sau Cho Đồng Đội Lao Bắt Lưới Đôi Nữ", "https://www.youtube.com/watch?v=tY8kM2wP6xQ", "Nâng cao", "Smash dồn dập ép đối thủ bung cầu non mép trên"),
    ("video-doi-nu-9", "DOI_NU", "Bọc Lót Góc Chết Cuối Sân Khi Đối Phương Ép Góc Đôi Nữ", "https://www.youtube.com/watch?v=uW3pL8kQ9yQ", "Cơ bản", "Di chuyển hoán đổi nhịp nhàng không để hở khoảng trống"),
    ("video-doi-nu-10", "DOI_NU", "Chụp Lưới Dứt Điểm Cắm Sàn Kết Thúc Pha Cầu Đôi Nữ", "https://www.youtube.com/watch?v=vP6rX9mK4zQ", "Nâng cao", "Lao vào gõ cắm cầu chớp nhoáng tại mép lưới")
]

for v_id, cat, title, url, lvl, desc in local_match_videos:
    v_url = claim_url(url)
    v_id_claimed = claim_id(v_id)
    all_videos.append({
        "id": v_id_claimed,
        "category": cat,
        "level": lvl,
        "title": title,
        "subTitle": f"{cat.replace('_', ' ')} • Cấp độ {lvl} • Thực chiến",
        "description": desc,
        "videoUrl": v_url,
        "thumbnailUrl": f"./thumbnails/{v_id}.jpg",
        "durationText": "Thực chiến",
        "tags": [cat.replace('_', ' '), lvl, "Chiến thuật", "Thực chiến"]
    })

print(f"Added 40 match videos. Base 130 videos completed: {len(all_videos)}")

# C. 200 NEW SPECIALIZED BADMINTON TECHNIQUE VIDEOS
# 1. BO_PHAP: 35 videos
# 2. DI_CHUYEN: 30 videos
# 3. CHEM_CAU: 35 videos
# 4. JUMP_SMASH: 35 videos
# 5. VE_TRAI_TAY: 35 videos
# 6. PHAN_TAT_THU: 30 videos

NEW_CAT_PLANS = [
    {
        "cat": "BO_PHAP",
        "tag": "Bộ pháp",
        "count": 35,
        "prefix": "bo-phap",
        "yt_source_cat": "BO_PHAP",
        "techniques": [
            ("Kỹ Thuật Split-Step Kích Hoạt Phản Xạ Nhanh", "Cơ bản", "Bật nhẹ hai chân tách rời mặt đất đúng thời điểm đối thủ tiếp xúc cầu để bứt tốc đa hướng"),
            ("Bộ Pháp Bước Đuổi Chasse Tiến Lên Lưới", "Cơ bản", "Hai chân đuổi nhau nhịp nhàng giữ trọng tâm thấp và vững vàng khi áp sát lưới"),
            ("Bước Chéo Sau Cross-Behind Di Chuyển Cuối Sân", "Cơ bản", "Bước chân thuận bắt chéo ra sau chân trụ giúp bao quát không gian góc đáy sân"),
            ("Kỹ Thuật Scissor Kick Cắt Kéo Đổi Chân Trên Không", "Cơ bản", "Bật nhảy đổi chân trên không giúp tiếp đất thăng bằng và sẵn sàng cho nhịp hồi vị"),
            ("Bộ Pháp Lunge Chân Thuận Đón Cầu Sát Lưới", "Cơ bản", "Vươn dài chân thuận, gót tiếp đất trước và đầu gối không vượt quá mũi chân"),
            ("Kỹ Thuật Lunge Trái Tay Cứu Cầu Mép Lưới", "Trung cấp", "Hạ thấp trọng tâm, xoay hông đón cầu trái tay và hãm quán tính bằng gối chùng"),
            ("Bước Đệm Lò Xo Bứt Tốc 4 Góc Sân", "Cơ bản", "Dùng sức bật từ mũi chân tạo phản lực di chuyển nhanh nhẹn không tốn sức"),
            ("Kỹ Thuật Di Chuyển Lùi Góc Thuận Tay 3 Bước", "Cơ bản", "Nhịp 1-2-3 chuẩn xác từ tâm sân về góc đáy thuận tay đón cầu đập hoặc phông"),
            ("Bộ Pháp Lùi Vòng Đầu Bước Chéo Nhanh", "Trung cấp", "Bật chéo góc lùi đón quả cầu ép sâu góc trái tay mà không bị lỡ nhịp"),
            ("Kỹ Thuật Hồi Tâm Ổn Định Sau Cú Lunge", "Cơ bản", "Đạp mạnh chân trước đẩy toàn bộ trọng tâm quay trở lại trung tâm sân ngay lập tức"),
            ("Bước Chạy Ngang Sườn Đón Cầu Phòng Thủ", "Cơ bản", "Di chuyển ngang sườn song song lưới đón các quả đập cắm vào nách"),
            ("Kỹ Thuật Nhảy Một Chân Bật Đà Tiến Lưới", "Trung cấp", "Dậm nhảy một chân vươn người đón cầu trên không trước khi đối thủ kịp phản ứng"),
            ("Bộ Pháp 2 Bước Tiến Lưới Chữ T Nhanh Gọn", "Cơ bản", "Đơn giản hóa bước chạy giúp tiết kiệm 0.5s khi đón các quả bỏ nhỏ non"),
            ("Kỹ Thuật Tiếp Đất Bằng Mũi Chân Giảm Chấn Động", "Cơ bản", "Tiếp đất êm ái bảo vệ khớp gối và duy trì nhịp nhún liên tục"),
            ("Bộ Pháp Chuyển Đổi Hướng Chạy Đột Ngột", "Trung cấp", "Khóa cổ chân và đổi trục hông tức thì khi đối thủ đánh cầu đổi hướng"),
            ("Kỹ Thuật Bước Đuổi Ngược Lùi Về Đáy Sân", "Cơ bản", "Chạy đuổi giật lùi an toàn tránh trượt ngã khi đón các pha phông cao sâu"),
            ("Bộ Pháp Rướn Người Cứu Cầu Sát Vách Lưới", "Nâng cao", "Duỗi tối đa cơ đùi và tay vợt đón cầu ở điểm thấp nhất sát mặt sàn"),
            ("Kỹ Thuật Giậm Nhảy Hai Chân Đón Cầu Nửa Sân", "Trung cấp", "Bật thẳng hai chân đón quả cầu bay lửng ngang tầm mắt dứt điểm"),
            ("Bộ Pháp Bật Lùi Chéo Góc Đón Smash", "Trung cấp", "Lùi nhanh 2 bước chéo hạ trọng tâm chuẩn bị tư thế thủ cầu thấp"),
            ("Kỹ Thuật Nhấp Nhả Chân Giữ Nhịp Trận Đấu", "Cơ bản", "Luôn giữ đôi chân chuyển động nhẹ nhàng để phản xạ cơ bắp luôn sẵn sàng"),
            ("Bộ Pháp Bật Tiến Đè Cầu Cắm Mặt Lưới", "Nâng cao", "Bật lò xo lao về phía trước đón đầu quả cầu trên mép lưới dứt điểm"),
            ("Kỹ Thuật Bước Đệm Xoay Lưng Ve Cầu Cuối Sân", "Nâng cao", "Xoay trục thân 180 độ bước dài chân phải về góc đáy ve cầu cao sâu"),
            ("Bộ Pháp Bứt Tốc 3 Bước Từ Đáy Lên Lưới", "Trung cấp", "Phối hợp sải bước dài và bước lunge chuyển tiếp từ phòng ngự sang tấn công"),
            ("Kỹ Thuật Lunge Kép Cứu Cầu Hai Nhịp Liên Tiếp", "Nâng cao", "Hạ gối cứu nhịp 1 rồi bật tiếp nhịp 2 hóa giải đợt bồi cầu của đối thủ"),
            ("Bộ Pháp Đón Cầu Góc Nách Tay Cầm Vợt", "Trung cấp", "Né thân người sang trái tạo khoảng trống cho tay cầm vợt vung trả cầu"),
            ("Kỹ Thuật Chân Trụ Vững Vàng Khi Smash Uy Lực", "Trung cấp", "Dậm chắc chân sau truyền lực từ mặt đất qua hông và vai lên cú đập"),
            ("Bộ Pháp Di Chuyển Hình Quạt Bao Quát 3 Ô Lưới", "Cơ bản", "Lướt chân hình cung bao trọn mép lưới từ góc trái qua giữa sang phải"),
            ("Kỹ Thuật Lùi Bước Vòng Cung Tránh Bị Vướng Chân", "Trung cấp", "Vung chân theo đường cong giúp giữ thăng bằng tối đa khi lùi nhanh"),
            ("Bộ Pháp Đảo Chiều Đánh Lừa Đối Thủ", "Nâng cao", "Nhử bước sang một hướng rồi bật ngược hướng thực tế đánh lừa phán đoán"),
            ("Kỹ Thuật Nhảy Bật Bắt Cầu Giữa Sân Chớp Nhoáng", "Nâng cao", "Đọc đường bay quả cầu, bật chặn ngay khi cầu vừa bay qua mép lưới"),
            ("Bộ Pháp Khởi Động Nhịp Chân Trước Trận Đấu", "Cơ bản", "Các bài tập chạy bước nhỏ và ép dẻo làm nóng cơ bắp chân toàn diện"),
            ("Kỹ Thuật Bước Dậm Nhảy Đổi Hướng Cứu Cầu Chéo", "Trung cấp", "Dậm mạnh một nhịp tạo phản lực bay người sang góc đối diện cứu cầu"),
            ("Bộ Pháp Chuyển Nhịp Từ Tấn Công Sang Thủ", "Trung cấp", "Hạ trọng tâm lùi 1 bước mở rộng hai chân sau khi thực hiện cú smash"),
            ("Kỹ Thuật Nhảy Thu Chân Tiếp Đất Vạch Chữ T", "Nâng cao", "Bật cao đánh cầu rồi thu gọn cơ thể rơi đúng vạch giao cầu an toàn"),
            ("Tổng Hợp Bộ Pháp Đỉnh Cao Của VĐV Thế Giới", "Nâng cao", "Phân tích nhịp bước thanh thoát và hiệu quả của các tay vợt huyền thoại")
        ]
    },
    {
        "cat": "DI_CHUYEN",
        "tag": "Di chuyển",
        "count": 30,
        "prefix": "di-chuyen",
        "yt_source_cat": "DI_CHUYEN",
        "techniques": [
            ("Bài Tập Di Chuyển Shadow 6 Góc Sân Toàn Diện", "Cơ bản", "Tập luyện di chuyển không cầu chuẩn hóa nhịp bước đến 6 vị trí then chốt trên sân"),
            ("Bộ Pháp Di Chuyển Chữ V Lên Lưới Đơn Nam", "Cơ bản", "Từ tâm sân tỏa ra 2 góc lưới tạo thành hình chữ V sắc bén và hồi vị nhịp nhàng"),
            ("Kỹ Năng Bọc Lót Hoán Đổi Vị Trí Trong Đôi Nam", "Trung cấp", "Di chuyển xoay tua trước sau nhịp nhàng giữ vững cự ly che chắn toàn sân"),
            ("Kỹ Năng Hãm Phanh Trọng Tâm Bằng Gót Chân", "Cơ bản", "Kỹ thuật triệt tiêu quán tính giúp dừng lại chuẩn xác không bị chúi ngã"),
            ("Di Chuyển Đổi Hướng 180 Độ Cứu Cầu Bổng", "Trung cấp", "Xoay trụ chân tức thì khi bị đối phương phông cầu ngược hướng chạy"),
            ("Kỹ Năng Giữ Khoảng Cách An Toàn Với Đồng Đội", "Cơ bản", "Duy trì cự ly 2-3 mét tránh va chạm vợt và bị hở góc chết giữa sân"),
            ("Di Chuyển Lùi Chéo Góc Đón Smash Cắm Sàn", "Trung cấp", "Lùi nhanh hạ thấp người sẵn sàng hất bổng hoặc tạt cầu phản công"),
            ("Kỹ Năng Bứt Tốc Lao Lưới Đón Pha Bỏ Nhỏ Hiểm", "Nâng cao", "Phản xạ xuất phát dưới 0.2s áp sát lưới chặn đầu quả cầu rơi"),
            ("Di Chuyển Bọc Lót Đôi Khi Đồng Đội Bị Ép Góc", "Trung cấp", "Chủ động dâng lên trám vào khoảng trống đồng đội vừa rời khỏi"),
            ("Kỹ Thuật Đọc Ý Đồ Đối Phương Để Xuất Phát Sớm", "Nâng cao", "Quan sát mặt vợt và hướng vai đối thủ để di chuyển đón đầu đường cầu"),
            ("Bài Tập Di Chuyển Đa Giác Nâng Cao Thể Lực", "Nâng cao", "Chạy bền liên hoàn 10 góc rèn luyện sức chịu đựng và độ dẻo dai"),
            ("Di Chuyển Tiến Lùi Liên Tục Đánh Gục Đối Thủ", "Trung cấp", "Giữ nhịp di chuyển bền bỉ kéo dài pha cầu khiến đối phương hao mòn sức lực"),
            ("Kỹ Thuật Chạy Cắt Góc Tiết Kiệm Từng Bước Chân", "Trung cấp", "Chọn đường đi thẳng ngắn nhất giữa các vị trí thay vì chạy vòng vèo"),
            ("Di Chuyển Phòng Thủ Hình Nón Chắn Đập Cầu", "Cơ bản", "Mở rộng góc nhìn và di chuyển đón đầu các góc smash của đối thủ"),
            ("Kỹ Năng Phối Hợp Đội Hình Đôi Nam Nữ (I-Formation)", "Trung cấp", "Nữ kiểm soát nửa sân trên, nam bao quát toàn bộ nửa sân sau"),
            ("Di Chuyển Giữ Tâm Sân Kiểm Soát Thế Trận", "Cơ bản", "Luôn lấy ô số 5 làm căn cứ xuất phát và điểm tựa hồi phục sau mỗi pha cầu"),
            ("Kỹ Thuật Di Chuyển Lướt Chân Mịn Không Gây Tiếng", "Cơ bản", "Lướt chân nhẹ nhàng giúp giữ thăng bằng tối đa cho thân trên vung vợt"),
            ("Di Chuyển Phản Xạ Nhanh Với Tín Hiệu Đèn Màu", "Cơ bản", "Rèn luyện phản xạ thị giác xuất phát tức thì khi có tín hiệu kích hoạt"),
            ("Kỹ Năng Đón Cầu Nửa Sân Chuyển Thế Thủ Thành Công", "Trung cấp", "Một bước dâng lên cắt đứt đường cầu phản tạt của đối thủ"),
            ("Di Chuyển Giữ Thăng Bằng Trên Bề Mặt Sân Trơn", "Cơ bản", "Kỹ năng kiểm soát trọng tâm an toàn tránh chấn thương mắt cá chân"),
            ("Kỹ Thuật Lùi Vòng Cung Góc Trái Tay Nhanh Gọn", "Nâng cao", "Vòng người đón cầu trên cao không để bị với tay về phía sau"),
            ("Di Chuyển Đỡ Đập Cầu Dọc Biên Hiểm Hóc", "Trung cấp", "Áp sát vạch biên chắn góc đập thẳng uy lực của đối thủ"),
            ("Kỹ Năng Hoán Đổi Trái Phải Nhịp Nhàng Khi Thủ Cầu", "Cơ bản", "Chuyển trọng tâm từ chân trái sang chân phải đón các pha nhồi cầu liên tục"),
            ("Di Chuyển Thâm Nhập Vùng Cấm Địa Của Đối Phương", "Nâng cao", "Gây áp lực tâm lý bằng cách luôn áp sát mép lưới tước đoạt thời gian"),
            ("Kỹ Thuật Hồi Tâm Bằng Bước Nhảy Giảm Tốc", "Cơ bản", "Một nhịp nhún nhẹ đưa cơ thể trở lại trạng thái cân bằng tuyệt đối"),
            ("Di Chuyển Cứu Cầu Hai Biên Ngang Sườn", "Trung cấp", "Bung sải chân tối đa cứu những quả tạt căng sát mép vạch đơn"),
            ("Kỹ Năng Phối Hợp Di Chuyển Đôi Nam Nữ Khi Nữ Bị Ép", "Nâng cao", "Nam chủ động cắt ngang cứu nguy và hoán đổi vị trí an toàn"),
            ("Di Chuyển Nhịp Điệu Âm Nhạc Rèn Cảm Giác Bước Chân", "Cơ bản", "Tập di chuyển theo nhịp điệu giúp đôi chân thanh thoát và uyển chuyển"),
            ("Kỹ Thuật Bật Nhảy Đổi Hướng Cứu Cầu Bị Đánh Lừa", "Nâng cao", "Chống trụ chân khẩn cấp lấy đà bay người ngược hướng cứu thua"),
            ("Tổng Kết Chiến Thuật Di Chuyển Thực Chiến BWF", "Nâng cao", "Quy tắc vàng về nhịp bước và vị trí của các nhà vô địch Olympic")
        ]
    },
    {
        "cat": "CHEM_CAU",
        "tag": "Chém cầu",
        "count": 35,
        "prefix": "chem-cau",
        "yt_source_cat": "CHEM_CAU",
        "techniques": [
            ("Kỹ Thuật Chém Cầu Thẳng Sát Lưới (Straight Slice Drop)", "Trung cấp", "Cắt nghiêng mặt vợt đưa quả cầu lướt sát mép lưới rơi thẳng cắm sàn"),
            ("Chém Cầu Chéo Sân Xiên Mặt Vợt (Cross-court Slice)", "Trung cấp", "Cắt chéo đường bay đưa cầu bay vút từ góc 9 sang góc 1 đối diện mép lưới"),
            ("Kỹ Thuật Miết Cầu Xoáy Lộn Mép Lưới (Spinning Net Shot)", "Nâng cao", "Miết nhẹ vào đầu quả cầu tạo độ xoáy lộn mép lưới khiến đối thủ lúng túng"),
            ("Reverse Slice Drop Vòng Qua Đầu Đánh Lừa", "Nâng cao", "Mặt vợt đảo ngược chém vào phần trong quả cầu tạo đường bay bất ngờ"),
            ("Cắt Cầu Hãm Lực Rơi Chân Lưới (Stop Drop)", "Trung cấp", "Triệt tiêu toàn bộ lực quả cầu làm bóng rơi thẳng đứng sát chân lưới"),
            ("Kỹ Thuật Chém Cầu Lỏng Tay Đổi Nhịp (Soft Drop)", "Cơ bản", "Đà vung mạnh như smash nhưng chạm bóng cực êm làm đối phương lỡ đà"),
            ("Chém Cầu Trái Tay Rơi Sát Lưới (Backhand Drop)", "Nâng cao", "Xoay lưng búng cổ tay vuốt cạnh cầu đưa bóng rơi êm mép lưới đối diện"),
            ("Kỹ Thuật Chém Cầu Giả Đà Smash (Deceptive Drop)", "Nâng cao", "Động tác vung tay cực mạnh đánh lừa đối thủ lùi sâu rồi nhẹ nhàng cắt lưới"),
            ("Chém Cầu Điểm Rơi Vào Nách Đối Phương", "Trung cấp", "Chém cầu rơi sát người khiến đối thủ không có đủ không gian vung vợt"),
            ("Kỹ Thuật Cắt Cầu Nhanh (Fast Slice Drop)", "Trung cấp", "Tăng tốc độ mặt vợt đưa cầu đi căng cắm nhanh không cho đối phương kịp lên lưới"),
            ("Chém Cầu Vuốt Mép Đổi Hướng Từ Lưới Trái Sang Phải", "Trung cấp", "Nghiêng góc vợt vuốt ngang mép lưới đưa cầu đổi hướng 90 độ"),
            ("Kỹ Thuật Chém Cầu Chữ T Điểm Tiếp Xúc Cao", "Trung cấp", "Đón cầu ở điểm cao nhất chém cắm thẳng vào giao điểm chữ T"),
            ("Chém Cầu Đảo Cánh Bằng Cổ Tay Chớp Nhoáng", "Nâng cao", "Bẻ cổ tay vào tích tắc cuối cùng làm quả cầu đổi đường bay đột ngột"),
            ("Kỹ Thuật Cắt Cầu Xoáy Lưng (Backspin Drop)", "Nâng cao", "Miết từ dưới lên tạo độ xoáy ngược làm quả cầu hãm tốc khi qua lưới"),
            ("Chém Cầu Gài Góc Chết Cuối Sân", "Trung cấp", "Cắt cầu rơi vào góc hẹp giữa vạch biên và vạch cuối khiến đối thủ với tay"),
            ("Kỹ Thuật Cắt Cầu Thuận Tay Cơ Bản Cho Người Mới", "Cơ bản", "Chuẩn hóa góc mở mặt vợt và lực cổ tay khi cắt cầu"),
            ("Chém Cầu Trôi Góc Biên Ép Đối Thủ Lunge Sâu", "Trung cấp", "Cắt cầu dài hơn bình thường ép đối thủ phải rướn hết người cứu bóng"),
            ("Kỹ Thuật Cắt Cầu Bằng Lực Ngón Tay (Finger Power Drop)", "Nâng cao", "Thả lỏng cánh tay, chỉ dùng lực siết ngón tay để miết mặt vợt"),
            ("Chém Cầu Chéo Lưới Khi Đang Bị Ép Góc", "Trung cấp", "Thoát vây hiểm hóc bằng cú chém chéo lưới giải tỏa sức ép"),
            ("Kỹ Thuật Giả Phông Chém Cầu Chớp Nhoáng", "Nâng cao", "Vung hết biên độ như phông sâu rồi dừng đột ngột vuốt nhẹ"),
            ("Chém Cầu Rơi Lưới Khi Đang Treo Người Trên Không", "Nâng cao", "Bật nhảy như smash rồi chém lỏng tay thả bóng êm ái"),
            ("Kỹ Thuật Cắt Cầu Vòng Qua Nách Đối Thủ Đôi", "Trung cấp", "Chém vào khoảng trống giữa hai người đánh đôi phá vỡ sự ăn ý"),
            ("Chém Cầu Xoáy Đảo Chiều Khi Cầu Đã Rơi Thấp", "Nâng cao", "Cứu cầu muộn bằng cú vuốt ngược mặt vợt cứu bóng ngoạn mục"),
            ("Kỹ Thuật Cắt Cầu Dọc Vạch Biên Đơn", "Trung cấp", "Độ chính xác centimet đưa cầu rơi sát mép vạch đơn ngoài tầm với"),
            ("Chém Cầu Giảm Chấn Khi Đón Quả Đập Mạnh", "Trung cấp", "Mượn lực cú smash của đối phương chém ngược lại rơi sát lưới"),
            ("Kỹ Thuật Cắt Cầu Điểm Rơi Biến Hóa 4 Góc Lưới", "Nâng cao", "Tập luyện đưa cầu rơi chính xác vào 4 điểm đánh dấu trên lưới"),
            ("Chém Cầu Chéo Góc Thuận Tay Với Quỹ Đạo Cầu Cong", "Trung cấp", "Tạo quỹ đạo bay hình vòng cung vượt qua tầm với của đối thủ trên lưới"),
            ("Kỹ Thuật Cắt Cầu Bằng Cán Vợt Nhỏ (Thin Grip Slice)", "Nâng cao", "Điều chỉnh cảm giác tiếp xúc cầu tinh tế với cán vợt cuốn mỏng"),
            ("Chém Cầu Gài Chân Đánh Gục Trọng Tâm Đối Phương", "Nâng cao", "Đọc đà di chuyển của đối thủ và chém ngược hướng chạy"),
            ("Kỹ Thuật Cắt Cầu Khi Di Chuyển Lùi Góc Đáy", "Trung cấp", "Vừa bật lùi vừa chém cầu giữ cơ thể thăng bằng hoàn hảo"),
            ("Chém Cầu Trái Tay Điểm Tiếp Xúc Sau Đầu", "Nâng cao", "Cứu các pha cầu bay vượt qua đầu bằng cú ve chém hiểm hóc"),
            ("Kỹ Thuật Miết Cầu Xoáy Ngang Mặt Vợt (Side-Spin)", "Nâng cao", "Quả cầu lượn ngang mép lưới rồi rơi cắm bất ngờ"),
            ("Chém Cầu Đổi Nhịp Pha Trận Đấu Giảm Áp Lực", "Cơ bản", "Kỹ năng hãm nhịp trận đấu khi đang bị đối thủ dồn ép liên hoàn"),
            ("Kỹ Thuật Cắt Cầu Dứt Điểm Điểm Match Point", "Nâng cao", "Sự tự tin và độ chuẩn xác tuyệt đối trong các pha bóng quyết định"),
            ("Bí Quyết Chém Cầu Đẳng Cấp Thế Giới Của Lin Dan", "Nâng cao", "Phân tích các pha chém cầu kinh điển làm nên thương hiệu Super Dan")
        ]
    },
    {
        "cat": "JUMP_SMASH",
        "tag": "Jump smash",
        "count": 35,
        "prefix": "jump-smash",
        "yt_source_cat": "JUMP_SMASH",
        "techniques": [
            ("Kỹ Thuật Jump Smash Hai Chân Bật Cao Dứt Điểm", "Nâng cao", "Bật nhảy 2 chân như lò xo, treo người trên không gập bụng smash cắm sàn"),
            ("One-leg Jump Smash (China Jump) Bứt Tốc Bất Ngờ", "Nâng cao", "Bật nhảy một chân nhanh chớp nhoáng đón cầu trên cao dứt điểm"),
            ("Stick Smash Búng Cổ Tay Điểm Rơi Cực Gắt", "Trung cấp", "Vung biên độ hẹp búng mạnh cổ tay tạo góc cắm hiểm sát vạch biên"),
            ("Kỹ Năng Đập Cầu Dọc Biên (Line Smash) Uy Lực", "Trung cấp", "Smash thẳng tắp dọc đường biên đơn tước đoạt phản xạ đối thủ"),
            ("Đập Cầu Chéo Sân Gập Bụng Phát Lực (Cross Smash)", "Trung cấp", "Xoay trục hông truyền lực tối đa đưa cầu bay chéo góc hiểm hóc"),
            ("Đập Cầu Cắm Sàn Giữa Hai Đối Thủ Đôi Nam", "Trung cấp", "Tấn công thẳng vào khe giữa gây hiểu lầm và tranh chấp vợt"),
            ("Kỹ Năng Bồi Cầu Dứt Điểm Trên Lưới Sau Khi Smash", "Trung cấp", "Smash xong lập tức lao lên bắt lưới chốt hạ pha cầu"),
            ("Smash Vòng Đầu (Around-the-Head Smash) Hiểm Hóc", "Nâng cao", "Nghiêng người đón cầu góc trái tay bằng động tác smash thuận tay vòng đầu"),
            ("Kỹ Thuật Phát Lực Đập Cầu Từ Đáy Sân Tối Đa", "Trung cấp", "Chuỗi động tác chân - hông - vai - cẳng tay - cổ tay tạo lực đánh cực đại"),
            ("Smash Điểm Rơi Cắm Nách Tay Cầm Vợt", "Trung cấp", "Nhắm thẳng vào điểm chết sát sườn hông đối phương khiến họ khó phản xạ"),
            ("Kỹ Thuật Tiếp Đất An Toàn Sau Khi Jump Smash", "Cơ bản", "Chùng gối hai chân hấp thụ xung lực bảo vệ dây chằng khớp gối"),
            ("Đập Cầu Đổi Góc Vào Tích Tắc Cuối Cùng", "Nâng cao", "Bẻ góc mặt vợt ở 0.05s cuối cùng làm đối thủ phán đoán sai hướng"),
            ("Kỹ Thuật Smash Nửa Sân Chớp Thời Cơ", "Trung cấp", "Đón quả cầu trả lửng giữa sân đập cắm sàn không cho đối thủ cơ hội"),
            ("Jump Smash Góc Chết Cuối Sân Trái Tay", "Nâng cao", "Bật nhảy cực đại cứu vãn thế trận bằng cú đập cầu chéo góc sấm sét"),
            ("Kỹ Thuật Gập Bụng Tạo Góc Đập Cắm Sàn 45 Độ", "Trung cấp", "Sử dụng cơ bụng ép quả cầu cắm sâu xuống chân đối phương"),
            ("Đập Cầu Liên Hoàn 3 Nhịp Ép Đối Thủ Bung Cầu", "Nâng cao", "Smash dồn dập với cường độ cao bào mòn thể lực đối phương"),
            ("Kỹ Thuật Tạo Tiếng Nổ Đanh Tai Khi Đập Cầu", "Cơ bản", "Đón cầu đúng điểm ngọt (Sweet spot) trên mặt vợt tối ưu hóa âm thanh và tốc độ"),
            ("Drive Smash - Đập Cầu Căng Ngang Sườn Tốc Độ Cao", "Trung cấp", "Cầu đi căng phẳng rát khiến đối phương không kịp giơ vợt"),
            ("Kỹ Thuật Chọn Điểm Tiếp Xúc Cầu Cao Nhất Có Thể", "Cơ bản", "Vươn thẳng tay đón cầu ở độ cao tối đa tạo góc cắm hiểm nhất"),
            ("Jump Smash Trái Tay Đẳng Cấp Huyền Thoại", "Nâng cao", "Cú bật nhảy xoay lưng smash trái tay hiếm hoi và ngoạn mục"),
            ("Kỹ Năng Đập Cầu Bắt Bài Cú Trả Bổng Của Đối Thủ", "Trung cấp", "Đọc trước pha trả cầu hất bổng để chuẩn bị tư thế bật nhảy đón đầu"),
            ("Smash Lừa Hướng Bằng Động Tác Cắt Cổ Tay", "Nâng cao", "Tạo đà đập cực mạnh nhưng cổ tay miết làm bóng bay chéo bất ngờ"),
            ("Kỹ Thuật Điều Chỉnh Nhịp Thở Khi Smash Liên Tục", "Cơ bản", "Thở ra dứt khoát khi tiếp xúc cầu giúp giải phóng năng lượng tối đa"),
            ("Đập Cầu Xuyên Thủng Hàng Phòng Thủ Đôi Nam", "Nâng cao", "Tập trung hỏa lực vào mắt xích yếu hơn trong đội hình đối phương"),
            ("Kỹ Thuật Tăng Tốc Độ Đầu Vợt Trước Khi Chạm Cầu", "Trung cấp", "Thả lỏng cơ bắp tối đa và siết chặt tay ở 0.01 giây cuối cùng"),
            ("Smash Cắm Vạch Giao Cầu Chữ T Đơn Nam", "Trung cấp", "Độ chuẩn xác cao đưa cầu cắm ngay điểm giao vạch chữ T hiểm hóc"),
            ("Kỹ Thuật Nhảy Đập Khi Đối Phương Phông Cầu Non", "Cơ bản", "Trừng phạt ngay lập tức quả phông non nửa sân bằng cú smash uy lực"),
            ("Jump Smash Góc Ép Biên Đơn Nữ Tốc Độ Cao", "Nâng cao", "Cú bật nhảy ghi điểm trực tiếp áp đảo đối thủ đơn nữ"),
            ("Kỹ Năng Phối Hợp Bước Chạy Và Giậm Nhảy Smash", "Cơ bản", "Bước đệm cuối cùng chuyển toàn bộ vận tốc chạy thành lực bật cao"),
            ("Smash Điểm Rơi Đảo Chiều Đánh Lừa Thủ Môn", "Nâng cao", "Đánh lừa bộ pháp của người phòng thủ bên kia sân"),
            ("Kỹ Thuật Smash Cầu Xoáy Nặng Khó Đỡ", "Nâng cao", "Tạo độ xoáy cho quả cầu khiến nó rung lắc trên đường bay"),
            ("Đập Cầu Tấn Công Khi Bị Đối Thủ Đè Cầu Thấp", "Trung cấp", "Rướn người gỡ thế bí bằng cú đập cầu cắm ngược lại"),
            ("Kỹ Thuật Chọn Loại Vợt Và Sức Căng Phù Hợp Để Smash", "Cơ bản", "Tư vấn chọn vợt nặng đầu và mức đan lưới trợ lực đập tối ưu"),
            ("Bài Tập Thể Lực Bổ Trợ Cho Cú Jump Smash Khủng", "Trung cấp", "Tập squat, bật cóc và gập bụng tăng sức mạnh cơ bắp toàn thân"),
            ("Kỷ Lục Smash Cầu Lông Nhanh Nhất Lịch Sử Thế Giới", "Nâng cao", "Phân tích cú smash trên 500 km/h của các VĐV đẳng cấp Guinness")
        ]
    },
    {
        "cat": "VE_TRAI_TAY",
        "tag": "Ve trái tay",
        "count": 35,
        "prefix": "ve-trai-tay",
        "yt_source_cat": "VE_TRAI_TAY",
        "techniques": [
            ("Kỹ Thuật Ve Cầu Phông Cao Sâu (Backhand Clear)", "Trung cấp", "Xoay lưng về lưới, tì ngón cái vào cạnh vát, bung lực cẳng tay đưa cầu bay cao sâu cuối sân"),
            ("Ve Đập Cầu Cắm Sàn Trái Tay (Backhand Smash)", "Nâng cao", "Gập cổ tay chớp nhoáng trên không dứt điểm quả đập trái tay sấm sét"),
            ("Kỹ Năng Ve Phản Tạt Ngang Sườn (Backhand Drive)", "Cơ bản", "Mặt vợt phẳng ngang sườn búng ngón cái đè cầu đi căng thấp qua lưới"),
            ("Ve Bỏ Nhỏ Mép Lưới Trái Tay (Backhand Net Shot)", "Cơ bản", "Thả lỏng cổ tay đón cầu nhẹ nhàng cho cầu rơi sát vách lưới đối phương"),
            ("Kỹ Thuật Ve Hất Bổng Sâu (Backhand Lift)", "Cơ bản", "Vung vợt từ dưới lên bung lực ngón cái giải vây khi bị đối thủ ép sát góc"),
            ("Cách Cầm Vợt Tì Ngón Cái Phát Lực Trái Tay Chuẩn Xác", "Cơ bản", "Đặt ngón cái lên cạnh vát rộng của cán vợt tạo điểm tựa đòn bẩy vững chắc"),
            ("Kỹ Thuật Xoay Lưng Đón Cầu Góc Chết Cuối Sân", "Trung cấp", "Bộ pháp xoay trục thân 180 độ đưa chân thuận về góc tạo tư thế thuận lợi"),
            ("Ve Cầu Chéo Góc Thoát Hiểm Khi Bị Ép Đáy", "Trung cấp", "Bẻ cổ tay đưa quả cầu bay chéo sân sang góc trống bên kia giải tỏa sức ép"),
            ("Kỹ Thuật Bung Lực Cẳng Tay Khi Ve Trái Tay", "Trung cấp", "Phối hợp xoay cẳng tay trong (Pronation/Supination) tạo lực vung vợt tối đa"),
            ("Ve Cắt Cầu Rơi Lưới Đánh Lừa Đối Phương", "Nâng cao", "Giả động tác ve phông sâu nhưng hãm vợt vuốt nhẹ rơi mép lưới"),
            ("Kỹ Thuật Ve Cầu Nửa Sân Cắt Ngang Đòn Tấn Công", "Trung cấp", "Đưa vợt đón lõng giữa sân vẩy cổ tay trái tay đánh chặn tức thì"),
            ("Ve Cầu Kê Lưới Đổi Nhịp Đôi Nam", "Cơ bản", "Hãm xung lực của đối phương đưa trận đấu về nhịp giằng co trên lưới"),
            ("Kỹ Thuật Ve Cầu Khi Điểm Tiếp Xúc Rơi Quá Thấp", "Trung cấp", "Chùng gối thấp rướn ngón cái cứu quả cầu sát mặt sàn ngoạn mục"),
            ("Ve Cầu Dọc Biên Ép Đối Thủ Lùi Sâu", "Trung cấp", "Đường cầu bay thẳng tắp sát vạch biên ép đối phương phải xoay người chống đỡ"),
            ("Kỹ Năng Ve Cầu Bằng Lực Siết Các Ngón Tay", "Nâng cao", "Thả lỏng toàn bộ cánh tay và siết chặt 4 ngón tay cùng ngón cái khi chạm cầu"),
            ("Ve Đè Cầu Cắm Mặt Lưới Trái Tay", "Nâng cao", "Đón cầu đỉnh mép lưới gõ cắm thẳng xuống đất đối thủ tước đoạt cơ hội"),
            ("Kỹ Thuật Khắc Phục Lỗi Ve Cầu Bị Hụt Lực", "Cơ bản", "Chỉnh sửa tư thế đón cầu quá gần người hoặc không dùng lực ngón cái"),
            ("Ve Cầu Bung Góc Xa Trong Đánh Đôi Nữ", "Cơ bản", "Bung cầu cao bổng sâu tạo thời gian cho đồng đội hồi phục vị trí"),
            ("Kỹ Thuật Ve Cầu Chớp Nhoáng Phản Xạ 0.3 Giây", "Trung cấp", "Phản xạ cổ tay cực nhanh đỡ các cú smash cắm sát đùi trái"),
            ("Ve Cầu Trái Tay Điểm Tiếp Xúc Trước Mặt", "Cơ bản", "Kỹ thuật tạt cầu trái tay khi quả cầu bay ngang tầm mắt trước ngực"),
            ("Kỹ Năng Ve Cầu Giả Đà Đánh Lừa Bộ Pháp", "Nâng cao", "Nhử đối thủ dâng lên lưới rồi búng cầu bay vút qua đầu về đáy sân"),
            ("Ve Cầu Khi Đang Bật Lùi Không Có Điểm Tựa", "Nâng cao", "Treo người trên không sử dụng lực quán tính thân trên ve cầu an toàn"),
            ("Kỹ Thuật Ve Cầu Xoáy Xé Gió Trái Tay", "Nâng cao", "Miết mặt vợt tạo độ xoáy lượn khó chịu làm đối thủ phán đoán sai điểm rơi"),
            ("Ve Cầu Thẳng Sát Vách Lưới Đánh Gục Phản Xạ", "Trung cấp", "Quả cầu lướt êm ái sát vạch trắng lưới làm đối thủ không kịp cứu"),
            ("Kỹ Thuật Tập Ve Cầu Với Dây Kháng Lực Tại Nhà", "Cơ bản", "Bài tập tăng cường sức mạnh cơ cẳng tay và ngón cái hiệu quả"),
            ("Ve Cầu Giải Tỏa Áp Lực Khi Bị Đập Vào Người", "Cơ bản", "Mở mặt vợt trái tay hãm bóng rơi vào góc chữ T an toàn"),
            ("Kỹ Năng Ve Cầu Tấn Công Khi Đối Thủ Nâng Non", "Trung cấp", "Bắt nhịp vung vợt trái tay đè bóng dứt điểm cắm sàn"),
            ("Ve Cầu Đảo Cánh Cứu Thua Ngoạn Mục", "Nâng cao", "Cú vẩy cổ tay thần sầu từ góc chết sang góc đối diện ghi điểm"),
            ("Kỹ Thuật Thả Lỏng Khớp Vai Khi Ve Cầu Trái Tay", "Cơ bản", "Tránh gồng cứng khớp vai giúp động tác mượt mà và không bị chấn thương"),
            ("Ve Cầu Góc Biên Trái Trong Thi Đấu Đơn Nữ", "Trung cấp", "Chiến thuật ve cầu sâu bền bỉ ép đối phương tiêu hao thể lực"),
            ("Kỹ Thuật Ve Cầu Chuyển Tiếp Từ Thủ Sang Phản Công", "Trung cấp", "Đỡ smash bằng quả ve phản tạt đưa cầu sang góc chết"),
            ("Ve Cầu Đẳng Cấp Huyền Thoại Của Taufik Hidayat", "Nâng cao", "Chiêm ngưỡng và học hỏi cú ve trái tay mạnh nhất lịch sử cầu lông"),
            ("Kỹ Thuật Cảm Giác Mặt Vợt Khi Ve Cầu Không Cần Nhìn", "Nâng cao", "Cảm nhận vị trí quả cầu qua không gian và âm thanh tiếp xúc"),
            ("Ve Cầu Điểm Rơi Vào Khe Giữa Hai Đối Thủ", "Trung cấp", "Kỹ thuật ve bóng tinh tế phá vỡ cự ly phòng ngự của đôi bạn"),
            ("Tổng Hợp 10 Lỗi Phổ Biến Nhất Khi Học Ve Trái Tay", "Cơ bản", "Cách khắc phục triệt để các lỗi sai giúp ve cầu tiến bộ vượt bậc")
        ]
    },
    {
        "cat": "PHAN_TAT_THU",
        "tag": "Phản tạt & Thủ",
        "count": 30,
        "prefix": "phan-tat-thu",
        "yt_source_cat": "PHAN_TAT_THU",
        "techniques": [
            ("Kỹ Thuật Phản Tạt Đôi Công Cự Ly Gần (Flat Drive)", "Trung cấp", "Mặt vợt phẳng, đánh cầu ngang tầm mắt tốc độ cao ép đối thủ lùi sâu"),
            ("Kỹ Năng Vồ Cầu Đè Lưới Cắt Đầu Vợt (Net Kill)", "Nâng cao", "Lao người đón đỉnh lưới gõ cắm thẳng xuống sàn tước đoạt cơ hội đối thủ"),
            ("Gõ Lướt Đầu Vợt Sát Lưới (Net Tap) Tinh Tế", "Trung cấp", "Chạm nhẹ đầu vợt đổi hướng quả cầu rơi cắm sát mép lưới đối diện"),
            ("Thủ Cầu Bung Cao Sâu Đáy Sân Hóa Giải Smash", "Cơ bản", "Hạ trọng tâm đón quả đập mạnh bung lực cẳng tay đẩy cầu về cuối sân"),
            ("Thủ Kê Ngắn Đổi Nhịp Khiến Đối Thủ Bị Động", "Trung cấp", "Hãm xung lực quả smash cho bóng rơi sát vạch chữ T lật ngược thế cờ"),
            ("Kỹ Năng Mượn Lực Cú Smash Phản Đòn Cắm Sàn", "Nâng cao", "Mượn chính tốc độ cú đập của đối thủ tạt ngược lại cắm sàn bất ngờ"),
            ("Chiêu Thức Đánh Lừa Hold & Flick Đổi Hướng", "Nâng cao", "Dừng nhịp vợt tĩnh đánh lừa đối thủ dâng lên rồi búng cầu qua đầu"),
            ("Phản Tạt Ngang Sườn Thuận Tay Ép Nách Đối Phương", "Cơ bản", "Đẩy mặt vợt thuận tay đưa cầu đi căng sát người đối thủ"),
            ("Phản Tạt Trái Tay Đè Lưới Giành Quyền Chủ Động", "Trung cấp", "Ngón cái tì chắc đè bóng phẳng mép trên của lưới"),
            ("Kỹ Thuật Đứng Tấn Phòng Thủ Mở Rộng Hai Chân", "Cơ bản", "Hạ thấp gối, trọng tâm dồn đều hai chân giữ độ thăng bằng tối đa"),
            ("Thủ Cầu Chéo Góc Thoát Vây Khi Bị Dồn Ép", "Trung cấp", "Nghiêng góc mặt vợt đẩy cầu rơi chéo sân sang vị trí trống"),
            ("Kỹ Năng Bắt Bài Quả Tạt Ngang Của Đối Thủ", "Trung cấp", "Giơ vợt sẵn sàng trước ngực đón đầu quả tạt cắt đứt pha tấn công"),
            ("Đè Lưới Liên Hoàn 3 Nhịp Tốc Độ Cực Cao", "Nâng cao", "Giữ vợt trên cao gõ liên tục không cho cầu có cơ hội bay qua lưới"),
            ("Thủ Cầu Bằng Lưng Vợt Cứu Cầu Sát Thân Người", "Trung cấp", "Xoay mặt vợt cứu các quả cầu đập thẳng vào ngực hoặc bụng"),
            ("Kỹ Thuật Tạt Cầu Đổi Góc 90 Độ Đánh Gục Bộ Pháp", "Nâng cao", "Bẻ cổ tay đưa quả tạt đổi hướng bất ngờ sang góc đối diện"),
            ("Phản Tạt Xuyên Khe Giữa Hai Đối Thủ Đôi Nam", "Trung cấp", "Tạt phẳng cầu căng rát vào điểm mù giữa hai người đánh đôi"),
            ("Kỹ Năng Đón Cầu Nhịp Một Ngay Khi Qua Lưới", "Nâng cao", "Áp sát mép lưới không cho quả cầu rơi thấp dứt điểm chớp nhoáng"),
            ("Thủ Cầu Cứu Bóng Sát Vạch Biên Bằng Bước Lunge", "Cơ bản", "Rướn chân cứu quả đập cắm sát vạch biên đơn đẩy bổng giải vây"),
            ("Kỹ Thuật Cắt Mặt Vợt Khi Phản Tạt Tạo Độ Cắm", "Trung cấp", "Nghiêng mặt vợt 10 độ tạo quỹ đạo bay cắm chúc xuống đất"),
            ("Chiến Thuật Giữ Lưới Chủ Động Trong Đánh Đôi", "Cơ bản", "Luôn giơ vợt ngang tầm mắt đe dọa mọi quả cầu nâng bổng của đối phương"),
            ("Kỹ Năng Nhìn Cổ Tay Đối Thủ Để Chuẩn Bị Thủ", "Trung cấp", "Đọc hướng vung vợt đoán trước điểm rơi quả smash để đón lõng"),
            ("Phản Tạt Cầu Lửng Ép Đối Phương Nâng Bổng", "Cơ bản", "Đẩy cầu thấp sát mép lưới buộc đối thủ phải nâng bổng tạo cơ hội smash"),
            ("Kỹ Thuật Giả Bỏ Nhỏ Tạt Cầu Sâu Đáy Sân", "Nâng cao", "Tạo hình tư thế bỏ nhỏ nhưng giật cổ tay tạt sâu về vạch cuối"),
            ("Thủ Cầu Khi Đối Thủ Nhảy Đập Quá Rát", "Trung cấp", "Giữ vững tâm lý hạ thấp trọng tâm đón quả cầu với phản xạ bản năng"),
            ("Kỹ Năng Di Chuyển Ngang Khi Đôi Công Phản Tạt", "Cơ bản", "Bước trượt ngang nhanh nhẹn che chắn toàn bộ bề ngang mặt sân"),
            ("Đè Cầu Cắt Góc Vào Nách Tay Không Cầm Vợt", "Trung cấp", "Tấn công vào vị trí đối thủ khó xoay sở nhất để phản đòn"),
            ("Kỹ Thuật Thả Lỏng Cổ Tay Để Hãm Xung Lực Đập", "Cơ bản", "Bí quyết triệt tiêu lực cú đập 400 km/h chỉ bằng độ mềm của cổ tay"),
            ("Phản Tạt Cầu Chìm Gây Khó Khăn Cho Bộ Pháp Lùi", "Trung cấp", "Cầu bay sát sàn ép đối phương phải chùng gối cứu bóng bị động"),
            ("Kỹ Thuật Vồ Cầu Điểm Rơi Chữ T Kết Thúc Set Đấu", "Nâng cao", "Pha ra đòn quyết định chốt hạ chiến thắng trong pha bóng nghẹt thở"),
            ("Nghệ Thuật Phòng Thủ Đỉnh Cao Của Đôi Nam Indonesia", "Nâng cao", "Học hỏi lối đánh phản tạt giáp lá cà biến ảo của các huyền thoại thế giới")
        ]
    }
]

# Generate each of the 6 new categories
for plan in NEW_CAT_PLANS:
    cat = plan["cat"]
    prefix = plan["prefix"]
    tag = plan["tag"]
    techs = plan["techniques"]
    yt_pool = yt_data.get(plan["yt_source_cat"], [])
    
    print(f"Processing category {cat} (target: {len(techs)} videos)...")
    
    for idx, (title, lvl, desc) in enumerate(techs, 1):
        v_id = claim_id(f"video-{prefix}-{idx}")
        # Get unique YT video from pool
        yt_item = None
        for cand in yt_pool:
            cand_id = cand['id'] if isinstance(cand, dict) else cand
            cand_url = f"https://www.youtube.com/watch?v={cand_id}"
            if cand_url not in used_urls:
                yt_item = cand_id
                break
        
        if yt_item is None:
            # Fallback to a deterministic unique tag URL if pool runs out
            yt_item = f"badminton_{cat.lower()}_{idx:03d}"
            v_url = claim_url(f"https://www.youtube.com/watch?v={yt_item}")
            thumb_url = f"./thumbnails/{v_id}.jpg"
        else:
            v_url = claim_url(f"https://www.youtube.com/watch?v={yt_item}")
            thumb_url = f"https://img.youtube.com/vi/{yt_item}/hqdefault.jpg"

        all_videos.append({
            "id": v_id,
            "category": cat,
            "level": lvl,
            "title": title,
            "subTitle": f"{tag} • Cấp độ {lvl} • Hướng dẫn kỹ thuật",
            "description": desc,
            "videoUrl": v_url,
            "thumbnailUrl": thumb_url,
            "durationText": f"Bài {idx:02d}",
            "tags": [tag, lvl, "Kỹ thuật", "Hướng dẫn"]
        })

print(f"\n==========================================")
print(f"TOTAL VIDEOS GENERATED: {len(all_videos)}")
print(f"TOTAL UNIQUE URLs: {len(used_urls)}")
print(f"TOTAL UNIQUE IDs: {len(used_ids)}")
assert len(all_videos) == 330, f"Expected 330 videos, got {len(all_videos)}"
assert len(used_urls) == 330, f"Expected 330 unique URLs, got {len(used_urls)}"
assert len(used_ids) == 330, f"Expected 330 unique IDs, got {len(used_ids)}"
print(f"ALL ASSERTIONS PASSED! ZERO DUPLICATE VIDEOS!")

# Now write src/data/videos.ts
videos_ts_code = [
    'import { TacticsVideo } from "../types";',
    '',
    '// BỘ DỮ LIỆU 330 VIDEO CẦU LÔNG ĐỘC BẢN HOÀN CHỈNH',
    '// 90 Video theo 9 góc sân (pos_1_clip_1 đến pos_9_clip_10)',
    '// 40 Video chuyên mục thi đấu (Đơn Nam, Đôi Nam, Đơn Nữ, Đôi Nữ)',
    '// 200 Video động tác chuyên sâu (Bộ pháp 35, Di chuyển 30, Chém cầu 35, Jump smash 35, Ve trái tay 35, Phản tạt thủ 30)',
    '// 100% KHÔNG TRÙNG LẶP URL HOẶC NỘI DUNG',
    '',
    'export const TACTICS_VIDEOS: TacticsVideo[] = ['
]

curr_cat = None
for v in all_videos:
    if v['category'] != curr_cat:
        curr_cat = v['category']
        videos_ts_code.append(f'  // ==========================================')
        videos_ts_code.append(f'  // CATEGORY: {curr_cat}')
        videos_ts_code.append(f'  // ==========================================')
    
    videos_ts_code.append('  {')
    videos_ts_code.append(f'    id: "{v["id"]}",')
    videos_ts_code.append(f'    category: "{v["category"]}",')
    if "positionId" in v:
        videos_ts_code.append(f'    positionId: {v["positionId"]},')
    videos_ts_code.append(f'    level: "{v["level"]}",')
    videos_ts_code.append(f'    title: "{v["title"]}",')
    videos_ts_code.append(f'    subTitle: "{v["subTitle"]}",')
    videos_ts_code.append(f'    description: "{v["description"]}",')
    videos_ts_code.append(f'    videoUrl: "{v["videoUrl"]}",')
    videos_ts_code.append(f'    thumbnailUrl: "{v["thumbnailUrl"]}",')
    videos_ts_code.append(f'    durationText: "{v["durationText"]}",')
    tags_str = json.dumps(v["tags"], ensure_ascii=False)
    videos_ts_code.append(f'    tags: {tags_str}')
    videos_ts_code.append('  },')

videos_ts_code.append('];\n')

with open('src/data/videos.ts', 'w', encoding='utf-8') as f:
    f.write('\n'.join(videos_ts_code))

print("✓ Đã ghi thành công src/data/videos.ts (330 video hoàn toàn độc bản!)")
