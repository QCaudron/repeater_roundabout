---
title: Programming Files
subtitle: Program your radios with Repeater Roundabout repeaters.
---

In order to make the contesting life a little easier, we provide some files you can use to program your radios. These files are automatically generated each time a new repeater is added. Many thanks to [Mike K7MCK](https://www.qrz.com/db/k7mck) for contributing code to generate the AnyTone D878 files.

| Download | Type | FM | DMR | DSTAR | Fusion |
|:--------:|:-----|:--:|:---:|:-----:|:------:|
| <a href="assets/rr_frequencies.csv" download><img src="assets/download-solid.svg" height="30px" /></a> | [Chirp](https://chirp.danplanet.com/projects/chirp/wiki/Home) | <img src="assets/check-solid.svg" height="20px" /> | | | <img src="assets/check-solid.svg" height="20px" /> |
| <a href="assets/d878.csv" download><img src="assets/download-solid.svg" height="30px" /></a> | [AnyTone AT-D878](https://support.bridgecomsystems.com/anytone-878-v2-model-cps-firmware-downloads) | <img src="assets/check-solid.svg" height="20px" /> | <img src="assets/check-solid.svg" height="20px" /> | | |
| <a href="#" download><img src="assets/download-solid.svg" height="30px" /></a> | Icom IC-705 | <img src="assets/check-solid.svg" height="20px" /> | | <img src="assets/check-solid.svg" height="20px" /> | |

## Anytone D878 Instructions

You will actually need to download multiple files to program the AnyTone AT-D878 radio.

1. <a href="assets/d878-talk-groups.CSV" download>Talk Groups</a> - If you want to use the DMR repeaters on
  this list, you will need to have the defined list of talk groups in addition to the channel information in
  the main download (above).
2. <a href="assets/d878-scanlist.CSV" download>Scan List</a> - If you want to use the scanner in the radio
  to scan across all the repeaters in the Roundabout, you will also need to import this file.

  When you open the CPS software, tools/import menu and select each of the files you've downloaded
  in the appropriate category (Channel, Scan List, and/or Talk Groups).  Then use the 
  Program/Write to Radio menu to send the program to your D878.
