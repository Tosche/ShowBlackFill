# ShowBlackFill.glyphsReporter

This is a plugin for the [Glyphs font editor](http://glyphsapp.com/) by Georg Seifert.

It fills closed paths with almost black even while you are still drawing (yes, not perfectly black). In Dark Mode, it will show in white. After installation, it will add the menu item *View > Show Black Fill* (de: *Schwarze Füllung anzeigen,* fr: *Afficher remplissage noir,* es: *Mostrar relleno negro*).

You can set a keyboard shortcut in System Preferences. I personally set it to Option+Command+B (I could make it as default, but don’t want to force it).
It is based on [Show Filled Preview](https://github.com/mekkablue/ShowFilledPreview) (thanks!), made for those who prefer a darker and sharper version.
Huge thanks to [mekkablue](https://github.com/mekkablue) for debugging!

![Paths are filled in almost black while editing.](ShowBlackFill.png "Show Black Fill Screenshot")

### Installation

You can use Glyphs' Plugin Manager and let it handle everything. If you want it the hard way...

1. Download the complete ZIP file and unpack it, or clone the repository.
2. Double click the .glyphsReporter file. Confirm the dialog that appears in Glyphs.
3. Restart Glyphs

The plugin will appear in the *View* menu.

### Usage Instructions

1. Open a glyph in Edit View.
2. Use *View > Show Black Fill* to toggle the the Black Fill Preview.

### License

Copyright 2014 Toshi Omagari (@tosche_e).
Based on sample codes by Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
