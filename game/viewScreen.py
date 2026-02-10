import numpy as np
import cv2
from mss import mss
from ultralytics import YOLO
import easyocr

model = YOLO('best.pt')
reader = easyocr.Reader(['en'])  # initialize EasyOCR once

def get_visuals():
    with mss() as sct:
        monitor = sct.monitors[1]  # your primary monitor
        screen_width = monitor["width"]
        screen_height = monitor["height"]


    # Define capture region: only the left half
        left_half = {
            "top": monitor["top"],
            "left": monitor["left"],
            "width": screen_width // 2,
            "height": screen_height
        }

        screenshot = sct.grab(left_half)
        frame = np.array(screenshot, dtype=np.uint8)[:, :, :3]
        results = model(frame, verbose=False)
        return_list  = []
        for box in results[0].boxes:
            coordinates = box.xyxy.tolist()[0]
            x1, y1, x2, y2 = coordinates[0], coordinates[1], coordinates[2], coordinates[3]
            confidence = box.conf.item()
            class_id = int(box.cls.item())
            class_name = results[0].names[class_id]
            #if confidence > 0.40:
            return_list.append({"class_name": class_name, "confidence":confidence, "coordinates":(x1,x2,y1,y2)})
        
        menu = [item for item in return_list if item['class_name'] == "menu"]
        if len(menu) > 0:
            h, w, _ = frame.shape
            x1 = max(0, int(menu[0]["coordinates"][0]))
            x2 = max(0, int(menu[0]["coordinates"][1]))
            y1 = min(w, int(menu[0]["coordinates"][2]))
            y2 = min(h, int(menu[0]["coordinates"][3]))
            text_results = []
            # print("x1: " + str(x1))
            # print("y1: " + str(y1))
            # print("x2: " + str(x2))
            # print("y2: " + str(y2))
            cropped = frame[y1:y2, x1:x2]
            #cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            #cv2.imwrite("menu_crop.png", cropped)
            ocr_results = reader.readtext(cropped)
            for (bbox, text, prob) in ocr_results:
                text_results.append(text)
            return {"text_results":text_results}
        
        no_player_list = [item for item in return_list if item['class_name'] != "player"]
        total_items =  [{k: v for k, v in item.items() if k != "confidence"} for item in no_player_list] 
        middle_point = (left_half["width"]/2, left_half["height"]/2)
        for item in total_items:
            x1, x2, y1, y2 = item["coordinates"]
            if x1 <= middle_point[0]:
                x1 = "left"
            else:
                x1 = "right"
            if y1 <= middle_point[1]:
                y1 = "up"
            else:
                y1 = "down"
            item["coordinates"] = (x1,y1)
        return total_items
        

