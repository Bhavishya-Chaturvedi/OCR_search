
import os
from typing import List
import easyocr
import argparse

reader = easyocr.Reader(['en'], gpu = True)

# for ocr over an image 
def ocr_scan(image_path: str ) -> str:
    result = reader.readtext(str(image_path))
    recognized_text = " ".join(elem[1] for elem in result)
    
    return recognized_text


# for looping ocr over a folder and search keyword
def search_images(directory: str, keyword: str) -> List[str]:
    
    matching_images = []
    for root, dir ,files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):
                image_path=os.path.join(root,file)
                detected_text = ocr_scan(image_path)
                if keyword.lower() in detected_text.lower():
                    matching_images.append(image_path)
    
    return matching_images


def main():
    #define cli tool that allows ocr search over images/ images in folder
    parser = argparse.ArgumentParser(description="OCR search tool for local images")
    parser.add_argument('-d', "--directory", type=str, help="Directory containing the images")
    parser.add_argument('-i', "--image", type=str, help="The single image to scan")
    parser.add_argument('-k', "--keyword", type=str, help="Keyword to search for") 

    args = parser.parse_args()

    if args.directory:
        matching_images =search_images(args.directory, args.keyword)
        print("Images that contain the Keyword")
        for image_path in matching_images:
            print(image_path)
    else:
        detected_text = ocr_scan(args.image)
        if args.keyword.lower() in detected_text.lower():
            print(f"Keyword detected in image")
            print(f"Detected Text: {detected_text}")
        else:
            print("Keyword not detected in the image")

    

if __name__ == "__main__":
    main()

