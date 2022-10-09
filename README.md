# Repeater Roundabout

This repo manages the website for the [Repeater Roundabout](https://repeaterroundabout.com). The `main` branch is automatically deployed to the production site; it is built using Jekyll to generate static HTML pages from the Markdown files in the root directory. These Markdown files are generated programmatically from the `assets/templates` directory, which contains the templates for the various pages on the site, and from information contained in `assets/repeaters.json`.


## Template files

The files in `assets/templates/` are used to generate the pages on the site. 

- `assets/templates/index.md` is the homepage; template elements include `{{ n_repeaters }}` and `{{ date_updated }}`.
- `assets/templates/repeaters.md` is the repeaters page; template elements include `{{ table }}` (a table of repeaters with frequencies and such) and `{{ associations }}` (a list naming and linking each group contributing their repeaters).
- `assets/templates/map.md` is the map page; template elements include `{{ repeater_pins }}` (a list of pins for each repeater on the map); this template is filled with Leaflet code to generate the map.
- `assets/templates/map.html` is for local development only; it generates `demo_map.html` which is not styled and is not used in production, but can be opened in a browser to see the map locally and ensure it is correctly centered and zoomed.


## Adding a repeater

To add a repeater, you should call `python scripts/update.py`. This script will prompt you for the repeater's information, and will add it to the `assets/repeaters.json` file containing all known repeaters, as well as regenerating the `assets/rr_frequencies.csv` file for CHIRP use. 

This script can be called directly, in which case it will prompt you for repeater information, or you can call it by passing the following arguments to the command-line for the same effect.

- Group name (`--name`): The short name of the group that runs one or more repeaters (for example, `PSRG` or `Shoreline ACS`)
- Location (`--loc`): The general location of the repeater (for example, `Seattle` or `Buck Mtn.`)
- Callsign (`--call`): The repeater's callsign (for example, `WW7PSR`)
- Frequency (`--freq`): The repeater's frequency (for example, `146.960`)
- Offset (`--offset`): The repeater's offset, in MHz (for example, `+0.6`)
- Tone (`--tone`): The repeater's tone, in Hz (for example, `103.5`); for DMR repeaters, use something like `CC2/TS1 BEARS1 TG/312488` for color code, time slot, and talk group name and number
- Mode (`--mode`): The repeater's mode (for example, `FM` or `DMR`); defaults to `FM` if not provided
- Latitude (`--lat`): The repeater's latitude, in decimal degrees (for example, `47.6062`)
- Longitude (`--lon`): The repeater's longitude, in decimal degrees (for example, `-122.3321`)
- Long name (`--long_name`): The full name of the group that runs the repeater (for example, `Puget Sound Repeater Group` or `Shoreline Amateur Communication Society`)
- Website (`--url`): The URL of the group's website (for example, `https://psrg.org` or `https://shorelineacs.org`); please include the `http://` prefix

For example, you may call `python scripts/update.py` to be prompted to enter all of this information, or call

```bash
python scripts/update --name PSRG --loc Seattle --freq 146.960 --offset -0.6 --tone 103.5 --lat 47.623963 --lon -122.315173 --long_name "Puget Sound Repeater Group" --url https://psrg.org
```

## Regenerating the site

If any changes are made to `repeaters.json` or to template files, you can regenerate the website's root `.md` files without adding a new repeater by calling `python scripts/update.py --regen`.


## Contributing

Contributions are welcome -- please open a pull request against a feature branch, or open an issue if you have any questions or suggestions.
