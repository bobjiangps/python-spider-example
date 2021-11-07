import img2pdf
import os


if __name__ == "__main__":
    comic_folder_path = "./海滩女神"
    chapter_list = os.listdir(comic_folder_path)
    chapter_list.sort(key=lambda x: int(x.split("_")[0][1:-1]))
    print(chapter_list)
    for chapter in chapter_list:
        chapter_path = os.path.join(comic_folder_path, chapter)
        chapter_pics = os.listdir(chapter_path)
        chapter_pics.sort(key=lambda x: int(x.split(".")[0]))
        images = [os.path.join(chapter_path, pic) for pic in chapter_pics]
        print(f"{chapter}-{len(images)}")
        with open(f"./{chapter}.pdf", "wb") as f:
            f.write(img2pdf.convert(images))
