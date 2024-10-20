# pitpac

## Description

Pitpac is a python base application built with qt. i built this app for my personal usecases like creating pdf from some image or combining some pdf with each other.

the app has the below features:

- create pdf from some image
- combine some pdf into one pdf
- resing images
- extracting text from images

The app also have a settings page that for now has only one option and it's light/dark mode. I'll add more settings to it in future.

## Installation

Just run

```
pip install -r required.txt
```

And this should install all the nessecary packages for you.

_Notes_:
If you run the via terminal and faced to these errors

```
QFont::fromString: Invalid description 'Fira Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
QFont::fromString: Invalid description 'FiraCode Nerd Font Mono,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
QFont::fromString: Invalid description 'Fira Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
QFont::fromString: Invalid description 'Fira Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1'
```

That's ok you can use the app without any issue. That's because in the qt5 app the fonts are not applied correctly, unlike qt6 which this issue is fixed in it.

If you faced any unexpected issue you can contact me in [@MohammadKeshtegar](https://t.me/Mohammadkeshtegar1401)
