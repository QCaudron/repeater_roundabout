---
title: Programming Files
subtitle: Program your radios with Repeater Roundabout repeaters.
---

In order to make the contesting life a little easier, we provide some files you can use to program your radios. These files are automatically generated each time a new repeater is added. Many thanks to [Mike K7MCK](https://www.qrz.com/db/k7mck) for contributing code to generate the AnyTone D878 files.

| Download | Type | FM | DMR | DSTAR | Fusion |
|:--------:|:-----|:--:|:---:|:-----:|:------:|
| <a href="assets/rr_frequencies.csv" download><img src="assets/download-solid.svg" height="30px" /></a> | [Chirp](https://chirp.danplanet.com/projects/chirp/wiki/Home) | <img src="assets/check-solid.svg" height="20px" /> | | | <img src="assets/check-solid.svg" height="20px" /> |
| <a href="assets/d878.zip" download><img src="assets/download-solid.svg" height="30px" /></a> | [AnyTone AT-D878](https://support.bridgecomsystems.com/anytone-878-v2-model-cps-firmware-downloads) | <img src="assets/check-solid.svg" height="20px" /> | <img src="assets/check-solid.svg" height="20px" /> | | |
| <a href="#" download><img src="assets/download-solid.svg" height="30px" /></a> | Icom IC-705 | <img src="assets/check-solid.svg" height="20px" /> | | <img src="assets/check-solid.svg" height="20px" /> | |

<br />


## Chirp help

[Chirp](https://chirp.danplanet.com/projects/chirp/wiki/Home) is a free, open-source tool for programming a large number of radios.

1. You'll want to check that Chirp [supports your radio](https://chirp.danplanet.com/projects/chirp/wiki/Supported_Radios). 
2. You will need a programming cable that works with your radio. Chirp has [a guide on the subject](https://chirp.danplanet.com/projects/chirp/wiki/CableGuide), and Dave Casler KE0OG has [a video on the subject](https://www.youtube.com/watch?v=nzkFVtyttKM) for some of the common Chinese radios.
3. [Install Chirp](https://chirp.danplanet.com/projects/chirp/wiki/Download) on your computer.
4. You are now ready to test [cloning from your radio](https://chirp.danplanet.com/projects/chirp/wiki/Beginners_Guide). If this works, your radio and computer are correctly communicating, and you are ready to write our <a href="assets/rr_frequencies.csv" download>CSV file</a>. Dave Casler has [a good video to get you started](https://www.youtube.com/watch?v=Mrpqq-xi00g).

For more information, check out [Chirp's Wiki](https://chirp.danplanet.com/projects/chirp/wiki/Home).


## AnyTone D878 instructions

Our <a href="assets/d878.zip" download>download for the D878</a> is a zip file containing three files :
- `d878.csv` contains all of the repeater information (frequencies, offsets, tones)
- `d878-talk-groups.csv` contains a set of talk group definitions for the DMR repeaters
- `d878-scanlist.csv` contains information that allows you to scan across all repeaters in the Roundabout

When you open the CPS software, go to the `Tools > Import` menu and select each of the files you've downloaded in the appropriate category (Channel, Scan List, and/or Talk Groups). Then use the `Program > Write to Radio` menu to send the program to your D878.
