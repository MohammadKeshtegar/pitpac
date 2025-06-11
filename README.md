# pitpac

## Description

Pitpac is a python base application built with qt. i built this app for my personal usecases like creating pdf from some image or combining some pdf with each other.

The application has the below features:

- Create pdf from some image
- Combine some pdf into one pdf
- Resing images
- Extracting text from images
- Reducing the video size

In the settings you can change:

1. Show a preview of the resied image
2. The location that app uses to open a dialog window
3. The font size and font family

## Installation

Just run

```
pip install -r requirements.txt
```

And this should install all the nessecary packages for you.

_Notes_:

1. For extracting text from image, i used pytesseract packges which is an OCR tool for recongnizing and reading text in images. Besides this package you need to install tesseract it self in your machine, so then you can use this package in your app.

2. If you ran it the via terminal and faced these errors

   ```
   QFont::fromString: Invalid description 'Fira Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
   QFont::fromString: Invalid description 'FiraCode Nerd Font Mono,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
   QFont::fromString: Invalid description 'Fira Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
   QFont::fromString: Invalid description 'Fira Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
   ```

   That's ok, you can use the app without any issue. That's because in the qt5 app the fonts are not applied correctly, unlike qt6 which this issue is fixed in it.

3. Some videos like with `.mkw` format, the video bitrate and audio bitrate might not be found, so i put an input too enter you own desier bitrate both for video bitrate and audio bitrate.

4. The application theme is only dark mode for now. In the future updates i'll add setting for creating you own custom theme.

If you faced any unexpected issue you can contact me in [@MohammadKeshtegar](https://t.me/Mohammadkeshtegar1401).
