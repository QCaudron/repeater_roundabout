# Repeater Roundabout

This repo manages the website for the [Repeater Roundabout](https://repeaterroundabout.com). The `main` branch is automatically deployed to the production site; it is built using Jekyll to generate static HTML pages from the Markdown files in the root directory. These Markdown files are generated programmatically from the `assets/templates` directory, which contains the templates for the various pages on the site, and from information contained in `assets/repeaters.json`.


## Template files

The files in `assets/templates/` are used to generate the pages on the site.

- `assets/templates/index.md` is the homepage; template elements include `{{ date_updated }}` and `{{ index_content }}`, which is populated by either ongoing contest information or leaderboard data, depending on arguments passed to `scripts/update.py` (specifically, the `--score` argument, which triggers a leaderboard calculation).
- `assets/templates/repeaters.md` is the repeaters page; template elements include `{{ table }}` (a table of repeaters with frequencies and such) and `{{ associations }}` (a list naming and linking each group contributing their repeaters).
- `assets/templates/map.md` is the map page; template elements include `{{ repeater_pins }}` (a list of pins for each repeater on the map); this template is filled with Leaflet code to generate the map.
- `assets/templates/rules.md` contains the rules for the event; template elements include `{{ n_repeaters }}` and `{{ n_groups }}`.
- `assets/templates/map.html` is for local development only; it generates `demo_map.html` which is not styled and is not used in production, but can be opened in a browser to see the map locally and ensure it is correctly centered and zoomed.


## Adding a repeater

To add a repeater, you should call `python scripts/update.py`. This script will prompt you for the repeater's information, and will add it to the `assets/repeaters.json` file containing all known repeaters, as well as regenerating the `assets/rr_frequencies.csv` file for CHIRP use.

`update.py` has the ability to import repeaters from RepeaterBook, [WWARA data exports][wwara-data], prior Repeater Roundabout `repeaters.json` files, and manually via command line arguments.  If you call the `update.py` without any arguments, it will prompt you for repeater information.  `update.py` accepts the following command line arguments:

- Callsign (`--call`): The repeater's callsign (for example, `WW7PSR`)
- Frequency (`--freq`): The repeater's frequency (for example, `146.960`).  If specified when importing from WWARA or a prior `repeaters.json` file, only the repeater matching the call and frequency will be imported.
- Group name (`--name`): The short name of the group that runs one or more repeaters (for example, `PSRG` or `Shoreline ACS`)
- Location (`--loc`): The general location of the repeater (for example, `Seattle` or `Buck Mtn.`)
- Offset (`--offset`): The repeater's offset, in MHz (for example, `+0.6`)
- Tone (`--tone`): The repeater's tone, in Hz (for example, `103.5`); for DMR repeaters, use something like `CC2/TS1 BEARS1 TG/312488` for color code, time slot, and talk group name and number
- Mode (`--mode`): The repeater's mode (for example, `FM` or `DMR`); defaults to `FM` if not provided
- Latitude (`--lat`): The repeater's latitude, in decimal degrees (for example, `47.6062`)
- Longitude (`--lon`): The repeater's longitude, in decimal degrees (for example, `-122.3321`)
- Long name (`--long_name`): The full name of the group that runs the repeater (for example, `Puget Sound Repeater Group` or `Shoreline Amateur Communication Society`)
- Website (`--url`): The URL of the group's website (for example, `https://psrg.org` or `https://shorelineacs.org`); please include the `http://` prefix
- RepeaterBook ID (`--id`): The ID of the repeater on RepeaterBook (an integer you can find at the very end of the URL)
- RepeaterBook State ID (`--state_id`): The State ID of the repeater on RepeaterBook (an integer you can find after `state_id=` in the URL).  Defaults to Washington (53) if not specified.
- WWARA Data Export File (`--wwara_csv`): The path to a [WWARA's repeater CSV file][wwara-data]. All repeaters matching the `--call` and optional `--freq` flags will be imported.
- Prior Repeater Roundabout `repeaters.json` file (`--prior_json`): The path to prior year's repeater file (for example, `2024/repeaters.json`). All repeaters matching the `--call` and optional `--freq` flags will be imported.

### Examples

You can add a repeater using only command line arguments:

```bash
python scripts/update --name PSRG --loc Seattle \
    --freq 146.960 --offset -0.6 --tone 103.5 \
    --lat 47.623963 --lon -122.315173 \
    --long_name "Puget Sound Repeater Group" \
    --url https://psrg.org
```

To import a record from RepeaterBook, you need only specify a RepeaterBook ID, Group Name, Location, Long Name, Website, and, for states other than Washington, a State ID. The easiest way to add a repeater is to call `python scripts/update.py`, enter in both a group name and a general location, the RepeaterBook ID, and hit enter a bunch of times to accept the empty defaults, which will be overwritten by RepeaterBook data. Once you get to Long Name, you will need to provide that and the group's Website yourself.

To import a repeater from RepeaterBook, run:

```bash
python scripts/update.py --state_id=16 --id=21198 \
    --name=SWI-ARC --loc="Squaw Butte, ID" \
    --long_name="South West Idaho Amateur Radio Club" \
    --url="https://www.k7swi.org/"
```

To import all repeaters matching a given callsign from a WWARA CSV file by specifying the call, Group Name, Long Name, and URL, run:

```bash
python scripts/update.py --wwara_csv=/wwara/WWARA-rptrlist-20251021.csv \
    --call=NM7E --name=NMARESC \
    --long_name="North Mason Amateur Radio Emergency Service Club" \
    --url="https://nmaresc.wordpress.com/"
```

To import all repeaters matching a given callsign from a prior Repeater Roundabout file by specifying only the call and the file:

```python
python scripts/update.py --prior_json=2024/repeaters.json --call=PSRG
```

To limit import from `--wara_csv` and `--prior_json` to a single repeater by specifying both the call *and* the frequency:

```python
python scripts/update.py --prior_json=2024/repeaters.json --call=K7LWH --freq=145.490
```

### Combining Import Sources

If you provide flags for more than one import source (any combination of RepeaterBook, WWARA, and prior Repeater Roundabout), `update.py` will attempt to merge data in a useful way.  Flags specified on the command line always override values imported from another source.  Otherwise, the value from the highest priority source will be used.  The priority order, from highest to lowest, for most fields is:

- Command line arguments
- WWARA
- RepeaterBook
- Repeater Roundabout record from prior year

The rationale is that WWARA should have the most up-to-date information, followed by RepeaterBook, followed by past Repeater Roundabouts.

However, because we tend to customize Group Name, Long Name, Location, and Website fields, we give higher priority to prior Repeater Roundabout records.  For these fields, the order of priority is:

- Command line arguments
- Repeater Roundabout record from prior year
- WWARA
- RepeaterBook

So, for example, to import all K7LWH repeaters from WWARA, but take the Group Name, Long Name, Location, and Website fields from last year's Repeater Roundabout, run:

```bash
python scripts/update.py \
    --wwara_csv=/wwara/WWARA-rptrlist-20251021.csv \
    --prior_json=2024/repeaters.json \
    --call=K7LWH
```

## Regenerating the site

If any changes are made to `repeaters.json` or to template files, you can regenerate the website's root `.md` files without adding a new repeater by calling `python scripts/update.py --regen`.


## Populating the leaderboards

When the competition is over, call `python scripts/update.py --score` to have the index page populated with the leaderboards, rather than ongoing contest information.


## Contributing

Contributions are welcome -- please open a pull request against a feature branch, or open an issue if you have any questions or suggestions. Note that any changes to `.md` files should be made to the respective template files in `assets/templates/` and not to the root `.md` files, as the latter are generated programmatically.


## Python Environment

The scripts in this repo use Python3. In order to install the dependencies, it is recommended to create a python virtual environment with the appropriate dependencies installed.

Note that Python version 3.12 or higher is required. We recommend using `uv`. After cloning the repo, from the parent directory, call

```bash
uv sync
```


## Typescript Development Environment

To compile TypeScript to JavaScript the tool chain includes, node/npm. We install TypeScript locally in `node_packages` so we have a consistent version between contributors.

```
# Assumes you have nvm [installed](https://github.com/nvm-sh/nvm)
$ nvm use         # Looks in the .nvmrc file to select the current version of node

$ npm install     # Install the node packages we use (TypeScript)

$ npx tsc         # Compile the TypeScript files in src to assets/scripts.
```

## Communications

Communications with clubs are tracked in our [tracking spreadsheet][tracking-sheet].  There is a tab for each year.

For 2025, responses are recorded using a [Google Form](https://docs.google.com/forms/d/1B3YadjpYomSUBScpoGuWp7R2S82oEMRAlzQBvR_YE98/edit) that automatically updates the [2025 Responses tab](https://docs.google.com/spreadsheets/d/1x6b34Q5FImiCTkuKqAVbpptse_vyh7PCZ74o5EKImPU/edit?gid=437006012#gid=437006012).  You can see repeaters that need updating by applying the [Repeaters To Add filter view](https://docs.google.com/spreadsheets/d/1x6b34Q5FImiCTkuKqAVbpptse_vyh7PCZ74o5EKImPU/edit?gid=1429833766#gid=1429833766&fvid=156395386).

### Sending Emails

Mass emails are sent via the [tracking spreadsheet][tracking-sheet] and GMail using a [Mail Merge Apps Script](https://developers.google.com/apps-script/samples/automations/mail-merge).  The script will send your draft email to every recipient on the selected tab whose `Email Sent` column is blank.  Before sending the email, the script replace any template variables strings, denoted by curly braces, found in the draft with the value of the corresponding spreadsheet column.  E.g. `{{xyz}}` will be replaced with the value from spreadsheet column `xyz`.

Note: Do not rename spreadsheet columns without updating the mail merge script and email templates.

1. View [recipients of the next email campaign](https://docs.google.com/spreadsheets/d/1x6b34Q5FImiCTkuKqAVbpptse_vyh7PCZ74o5EKImPU/edit?gid=1429833766#gid=1429833766&fvid=1596602663) to ensure your desired recipients are included.  To include someone, clear their `Email Sent` field.  To exclude them, set the `Email Sent` field to a non-empty value.

    Tip: It's good practice to send a test email to yourself by excluding everyone else before blasting an email out to everyone.

1. Prepare a GMail draft of the email you want to send giving a unique Subject line.  See our [corpus of email templates](https://docs.google.com/document/d/1WqKj2xd6ETskQg0085Yo2bDo65MunMhi-FvP9cfqebA/edit?tab=t.0).  Use template variables like `{{Callsign}}` to insert the value of the `Callsign` column into the email.

1. Open `Mail Merge > Send Emails` and enter the subject of your email.  The script will retrieve that draft and send it to all rows with an empty `Email Sent` column.  On success, it will update the `Email Sent` column with the current date.  If an error occurs, it will be recorded in the `Email Sent` column.

    Note: If you have a plain GMail account (non-Google Workspace) the script is limited to sending only 100 emails per day.


[tracking-sheet]: https://docs.google.com/spreadsheets/d/1x6b34Q5FImiCTkuKqAVbpptse_vyh7PCZ74o5EKImPU/edit?gid=1429833766#gid=1429833766
[wwara-data]: https://www.wwara.org/coordinations/coordination-data-files/
