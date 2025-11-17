diff --git a/ascii_art.py b/ascii_art.py
index 25cc3ea449d77daf141035a33fbe79d4fdb70e14..df99006557ff61aff35b7dd6034776bb75388af2 100644
--- a/ascii_art.py
+++ b/ascii_art.py
@@ -1,44 +1,51 @@
 import argparse
 from PIL import Image
 
 ASCII_CHARS = "@%#*+=-:. "
 
 def resize_image(image, new_width=100):
     width, height = image.size
     ratio = height / width / 1.65
-    new_height = int(new_width * ratio)
+    new_height = max(1, int(new_width * ratio))
     return image.resize((new_width, new_height))
 
 def grayify(image):
     return image.convert("L")
 
 def pixels_to_ascii(image):
     pixels = image.getdata()
-    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
+    scale = len(ASCII_CHARS) - 1
+    characters = "".join(
+        [ASCII_CHARS[pixel * scale // 255] for pixel in pixels]
+    )
     return characters
 
 def convert_image_to_ascii(path, new_width=100):
     try:
         image = Image.open(path)
     except Exception as e:
         print("Unable to open image:", e)
         return
 
     image = resize_image(image, new_width)
     image = grayify(image)
 
     ascii_str = pixels_to_ascii(image)
     img_width = image.width
-    ascii_img = "
-".join([ascii_str[index:(index+img_width)] for index in range(0, len(ascii_str), img_width)])
+    ascii_img = "\n".join(
+        [
+            ascii_str[index : index + img_width]
+            for index in range(0, len(ascii_str), img_width)
+        ]
+    )
     return ascii_img
 
 if __name__ == "__main__":
     parser = argparse.ArgumentParser(description="Convert image to ASCII art.")
     parser.add_argument("image_path", help="Path to the image file")
     parser.add_argument("--width", type=int, default=100, help="Width of ASCII output")
     args = parser.parse_args()
 
     ascii_image = convert_image_to_ascii(args.image_path, args.width)
     if ascii_image:
         print(ascii_image)
